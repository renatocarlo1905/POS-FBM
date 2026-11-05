"""POS authentication, operations and authorized state projection."""
import json, secrets, uuid
from pathlib import Path
from domain import require, RuleError, now, pack, money, cleantext
from identity import matches
from local_storage import DB
from sales import calc_sale
from cash import cash_state, cash_summary
from synchronization import SynchronizationService
class Store(SynchronizationService, DB):
    def __init__(self,path,branch,transport,copy_dir):
        super().__init__(path);self.branch=branch;self.transport=transport;self.copy_dir=Path(copy_dir);self.sessions={}
        self.db.executescript('CREATE TABLE IF NOT EXISTS operations(id TEXT PRIMARY KEY, seq INTEGER UNIQUE, body TEXT, status TEXT, issue TEXT);')
        if self.get('offline') is None:self.put('offline',False);self.put('credentials',{})

    def copy(self):
        try:self.backup(self.copy_dir/f'sucursal-{self.branch}.sqlite3');self.put('copy_status',{'ok':True,'at':now()})
        except Exception:self.put('copy_status',{'ok':False,'at':now(),'message':'No se pudo actualizar la segunda copia. La operación está guardada en este POS.'})

    def login(self,user,password):
        with self.lock:
            creds=self.get('credentials',{});uid=user.lower();cached=creds.get(uid)
            if not self.get('offline'):
                try:
                    result=self.transport('login',{'user':uid,'password':password,'branch':self.branch})
                    creds[uid]=result;self.put('credentials',creds)
                except ConnectionError:
                    require(cached and matches(password,cached['verifier']),'Central no disponible. Primero inicia sesión conectado en este POS.');result=cached
            else:
                require(cached and matches(password,cached['verifier']),'Sin autorización descargada o contraseña local incorrecta.');result=cached
            token=secrets.token_urlsafe(32);self.sessions[token]=uid
            try:self.sync(uid)
            except ConnectionError:pass
            return {'token':token}

    def auth(self,token):
        uid=self.sessions.get(token);require(uid,'Inicia sesión en este POS.');c=self.get('credentials',{}).get(uid);require(c,'Acceso local no disponible.');return uid,c

    def rows(self):return [dict(r) for r in self.db.execute('SELECT * FROM operations ORDER BY seq')]

    def operations(self):return [json.loads(r['body']) for r in self.rows() if r['status']!='rejected']

    def available(self):
        ps={p['id']:dict(p) for p in self.get('catalog',[])}
        for r in self.rows():
            e=json.loads(r['body'])
            if r['status']=='pending' and e['kind']=='sale':
                for x in e['payload']['items']:
                    if not x.get('non_inventory'):ps[x['id']]['available']-=x['qty']
        return ps

    def close_preview(self,token,data):
        with self.lock:
            uid,c=self.auth(token)
            require(c['snapshot']['policy'].get('cash_close'),'No tienes permiso para cerrar caja.')
            if not self.get('offline'):
                try:self.sync(uid)
                except ConnectionError:pass
            uid,c=self.auth(token)
            require(c['snapshot']['policy'].get('cash_close'),'No tienes permiso para cerrar caja.')
            current=cash_state(self.operations());require(current,'No hay caja abierta.')
            require(data.get('session')==current['id'],'La caja cambió. Vuelve a abrir el formulario.')
            counted=money(data.get('counted',''));fund=money(data.get('fund',''))
            require(fund<=counted,'El fondo siguiente no puede superar el efectivo real en caja.')
            expected=current['expected']+self.get('cash_adjustments',{}).get(current['id'],0)
            return {'expected':expected,'counted':counted,'fund':fund,'envelope':counted-fund,'difference':counted-expected,'local':bool(self.get('offline') or self.get('sync_error'))}

    def submit(self,token,kind,data,request_id):
        with self.lock:
            # Browser retains a UUID across uncertain HTTP replies.
            try:uuid.UUID(request_id)
            except (ValueError,TypeError,AttributeError):raise RuleError('Identificador de operación inválido.')
            uid,c=self.auth(token)
            prior=self.db.execute('SELECT body FROM operations WHERE id=?',(request_id,)).fetchone()
            if prior:
                prev=json.loads(prior[0]);require(prev['kind']==kind and prev['actor']==uid and prev['input']==data,'UUID reutilizado con contenido diferente.')
                return {'id':request_id,'repeated':True,**({'close_summary':prev['payload']} if kind=='close' else {})}
            online=not self.get('offline')
            if online:
                try:self.sync(uid)
                except ConnectionError:online=False
            uid,c=self.auth(token);policy=c['snapshot']['policy'];require(policy.get({'sale':'sell','open':'cash_open','close':'cash_close','move':'cash_move'}.get(kind,'')),'No tienes permiso para esta acción.')
            current=cash_state(self.operations());p={}
            if current:current['expected']+=self.get('cash_adjustments',{}).get(current['id'],0)
            if kind=='open':require(not current,'Ya hay una caja abierta en esta sucursal.');p={'opening':money(data.get('opening',0))}
            else:
                require(current,'Abre caja primero.');p={'session':current['id']}
                if kind=='sale':
                    products=self.available();p.update(calc_sale(data,products,policy,self.get('catalog_meta',{}).get('categories',[])))
                    require(p['received_cash']==p['cash'],'Ingresa el importe exacto: efectivo, tarjeta y transferencia deben sumar el total de la venta.')
                    require(all(x.get('non_inventory') or x['qty']<=products[x['id']]['available'] for x in p['items']),'Cantidad superior a la disponibilidad conocida.')
                    p['request']=data
                    sellers=data.get('sellers',[uid]);staff={s['id'] for s in self.get('staff',[])};require(isinstance(sellers,list) and sellers and len(set(sellers))==len(sellers) and all(s in staff for s in sellers),'Selecciona vendedores válidos.');p['sellers']=sellers
                elif kind=='move':
                    amount=money(data.get('amount',0));reason=cleantext(data.get('reason',''),300);typ=data.get('type');require(amount>0 and reason and typ in ('Entrada','Gasto','Retiro'),'Completa importe, tipo y motivo.')
                    p.update(amount=amount,reason=reason,type=typ)
                elif kind=='close':
                    counted=money(data.get('counted',0));fund=money(data.get('fund',0));require(fund<=counted,'El fondo siguiente no puede superar el efectivo real en caja.');envelope=counted-fund
                    if 'envelope' in data:require(money(data['envelope'])==envelope,'Fondo y sobre deben sumar el efectivo contado.')
                    p.update(counted=counted,fund=fund,envelope=envelope,expected=current['expected'],difference=counted-current['expected'])
            seq=self.db.execute('SELECT COALESCE(MAX(seq),0)+1 FROM operations').fetchone()[0]
            event={'id':request_id,'seq':seq,'branch':self.branch,'kind':kind,'actor':uid,'actor_name':c['snapshot']['name'],'at':now(),'offline':not online,'grant':c['grant'],'payload':p,'input':data,'template':self.get('template')}
            self.db.execute('INSERT INTO operations VALUES(?,?,?,?,?)',(request_id,seq,pack(event),'pending',''))
            self.copy()
            try:self.sync(uid)
            except (ConnectionError,RuleError) as ex:self.put('sync_error',str(ex))
            return {'id':request_id,**({'close_summary':p} if kind=='close' else {})}

    def state(self,token):
        with self.lock:
            uid,c=self.auth(token);error=''
            try:self.sync(uid)
            except (ConnectionError,RuleError) as e:error=str(e)
            uid,c=self.auth(token);policy=c['snapshot']['policy'];cash=cash_state(self.operations())
            summary=cash_summary(self.operations(),self.get('corrections',[]),self.get('order_cash_moves',[]),cash,self.get('cash_adjustments',{}).get(cash['id'],0)) if cash and policy.get('cash_summary') else None
            exchange_moves=[m for m in self.get('exchange_moves',[]) if cash and m['session']==cash['id']]
            if summary:
                summary['exchanges']={k:sum(m[k] for m in exchange_moves) for k in ('cash','card','transfer')}
            if cash:
                cash={k:v for k,v in cash.items() if k!='expected'}
                cash['moves']+=self.get('order_cash_moves',[])+exchange_moves
            ops=[]
            for r in reversed(self.rows()):
                e=json.loads(r['body']); e.pop('grant');e.pop('input');e['payload'].pop('request',None)
                if e['kind']=='sale':e['short_code']=__import__('folios').code(e)
                ops.append({**e,'status':r['status'],'issue':r['issue']})
            return {'user':c['snapshot']['name'],'policy':policy,'authorization_at':c['snapshot']['issued_at'],'offline':self.get('offline'),'branch':self.branch,'catalog':[{k:v for k,v in p.items() if k!='cost' or policy.get('cost')} for p in self.available().values()],'session':cash,**({'cash_summary':summary} if policy.get('cash_summary') else {}),'operations':ops if policy.get('receipts') else [],'pending':sum(r['status']=='pending' for r in self.rows()),'last_sync':self.get('last_sync'),'sync_error':error,'copy':self.get('copy_status'),'template':self.get('template'),'staff':self.get('staff',[]),'corrections':self.get('corrections',[]) if policy.get('receipts') else [],**self.get('catalog_meta',{})}
