"""Central coordination, snapshots and idempotent event reception."""
import json, hashlib, secrets
from pg import PGDB
from domain import require, now, pack
from defaults import PERMS, PRODUCTS, NAMES
from identity import IdentityService, hashed
from receipts import template
from sales import calc_sale
from cash import cash_state
class Central(IdentityService, PGDB):
    def __init__(self,path):
        super().__init__(path)
        self.db.executescript('''CREATE TABLE IF NOT EXISTS events(id TEXT PRIMARY KEY, branch INTEGER CHECK(branch IN (1,2)),seq BIGINT CHECK(seq>0), body TEXT NOT NULL,hash TEXT NOT NULL,status TEXT CHECK(status IN ('accepted','rejected')),issue TEXT,received TEXT, ordinal BIGINT GENERATED ALWAYS AS IDENTITY, UNIQUE(branch,seq));
        CREATE TABLE IF NOT EXISTS stock(id TEXT PRIMARY KEY,available INTEGER);
        CREATE TABLE IF NOT EXISTS audit(id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,at TEXT,actor TEXT,action TEXT,detail TEXT);''')
        if not self.get('users'):
            roles={'admin':{'name':'Administrador','permissions':{k:True for k in PERMS},'max_discount':10000},'sales':{'name':'Personal de venta','permissions':{k:k in ('orders','sell','cash_open','cash_close','receipts','reprint') for k in PERMS},'max_discount':0}}
            users=[]
            for name in NAMES:
                users.append({'id':name.lower(),'name':name,'email':'','phone':'','role':'admin' if name=='Carlo' else 'sales','active':True,'branches':[1,2],'revision':1,'password':hashed(name+'-E1-2026!')})
            self.put('users',users);self.put('roles',roles);self.put('secret',secrets.token_hex(32));self.put('sessions',{})
            self.put('templates',{str(b):template({'header':f'FRIDA BLANCAS MÉXICO\nSucursal {b} · Coyoacán','footer':'Gracias por tu visita.\nCOMPROBANTE DE PRUEBA · SIN VALIDEZ FISCAL','width':80}) for b in (1,2)})
            for p in PRODUCTS:self.db.execute('INSERT INTO stock VALUES(?,?)',(p[0],p[5]))
        roles=self.get('roles');changed=False
        for rid,role in roles.items():
            if 'cash_summary' not in role['permissions']:
                role['permissions']['cash_summary']=rid=='admin';changed=True
        if changed:self.put('roles',roles)
        from extensions import init
        init(self)
        __import__('exchanges').init(self)
        __import__('folios').init(self)
        __import__('simulated').init_codes(self)
        __import__('order_service').init(self)

    def audit(self,actor,action,detail):self.db.execute('INSERT INTO audit(at,actor,action,detail) VALUES(?,?,?,?)',(now(),actor,action,pack(detail)))

    def catalog(self,cost=False):
        from extensions import catalog
        return catalog(self,cost)

    def pull(self,grant):
        with self.lock:
            old=self.verify(grant);u=next((u for u in self.get('users') if u['id']==old['user']),None)
            require(u and u['active'] and old['branch'] in u['branches'],'Acceso desactivado para esta sucursal.')
            snap={**old,'name':u['name'],'revision':u['revision'],'policy':self.policy(u),'issued_at':now()}
            return {'catalog':self.catalog(self.policy(u).get('cost',False)),'template':self.get('templates')[str(old['branch'])],'grant':self.sign(snap),'snapshot':snap,'at':now(),'relogin':u['revision']!=old['revision'],'cash_adjustments':__import__('extensions').cash_adjustments(self,old['branch']),'corrections':[__import__('folios').corrections(self,json.loads(r[0])) for r in self.db.execute('SELECT document FROM corrections ORDER BY ordinal') if json.loads(r[0])['branch']==old['branch']],'staff':[{'id':x['id'],'name':x['name'],'seller_code':'FBV-'+x['id'].upper()} for x in self.get('users') if x['active']],'order_cash_moves':[{'id':p['id'],'kind':'order','cash':p['cash'],'card':p.get('card',0),'transfer':p.get('transfer',0),'amount':p['cash'],'reason':p['kind']+' · '+p['order']} for p in __import__('order_service').movements(self,old['branch']) if p.get('session') and p['session']==(cash_state([json.loads(r['body']) for r in self.events(old['branch']) if r['status']=='accepted']) or {}).get('id')],'exchange_moves':__import__('exchanges').movements(self,old['branch']),'exchange_receipts':__import__('exchanges').receipt_events(self,old['branch']) if self.policy(u).get('receipts') else [],'meta':{'materials':self.get('materials'),'types':self.get('types'),'categories':self.get('categories',[]),'providers':self.get('providers'),'warehouses':__import__('extensions').WAREHOUSES}}

    def events(self,branch=None):
        query='SELECT * FROM events';args=()
        if branch:query+=' WHERE branch=?';args=(branch,)
        return [dict(r) for r in self.db.execute(query+' ORDER BY ordinal',args)]

    def receive(self,event):
        with self.lock:
            # Transaction includes stock, immutable event, sequence and acknowledgement.
            self.db.execute('BEGIN IMMEDIATE')
            try:
                opid=event['id'];digest=hashlib.sha256(pack(event).encode()).hexdigest();old=self.db.execute('SELECT * FROM events WHERE id=?',(opid,)).fetchone()
                if old:
                    require(old['hash']==digest,'Mismo UUID con contenido distinto: revisar, no volver a cobrar.')
                    self.db.execute('COMMIT');return {'status':old['status'],'issue':old['issue'],'id':opid,'duplicate':True}
                g=self.verify(event['grant']);branch=event['branch'];require(branch in (1,2) and g['branch']==branch,'Sucursal no autorizada.')
                last=self.db.execute('SELECT COALESCE(MAX(seq),0) FROM events WHERE branch=?',(branch,)).fetchone()[0]
                require(type(event['seq'])is int and event['seq']==last+1,'Falta una operación anterior; se conserva en la cola.')
                require(event['kind'] in ('open','sale','move','close'),'Tipo desconocido.')
                p=event['payload'];perm={'open':'cash_open','sale':'sell','move':'cash_move','close':'cash_close'}[event['kind']]
                policy=g['policy'];status='accepted';issue=''
                u=next((u for u in self.get('users') if u['id']==g['user']),None)
                if not event['offline']:
                    require(u and u['active'] and branch in u['branches'],'Acceso revocado.')
                    policy=self.policy(u)
                require(policy.get(perm),'Operación fuera de la autorización.')
                rows=[json.loads(r['body']) for r in self.events(branch) if r['status']=='accepted']
                current=cash_state(rows)
                if current:current['expected']+=__import__('extensions').cash_adjustments(self,branch).get(current['id'],0)
                if event['kind']=='open':require(not current and p['opening']>=0,'Ya hay una caja abierta.')
                else:require(current and p['session']==current['id'],'Sesión de caja no válida.')
                if event['kind']=='sale':
                    # Recompute all financial values centrally from immutable catalog and request.
                    catalog={x['id']:x for x in self.catalog()};expected=calc_sale(p['request'],catalog,policy,self.get('categories',[]))
                    require(all(p[k]==v for k,v in expected.items()),'Importes o partidas no válidos.')
                    shortages=[x for x in p['items'] if not x.get('non_inventory') and x['qty']>catalog[x['id']]['available']]
                    if shortages and not event['offline']:status='rejected';issue='Existencia central insuficiente. No registrar el cobro; revisa el comprobante rechazado.'
                    else:
                        for x in p['items']:
                            if x.get('non_inventory'):continue
                            self.db.execute('UPDATE stock SET available=available-? WHERE id=?',(x['qty'],x['id']))
                            self.db.execute('INSERT INTO stock_ledger VALUES(?,?,?,?,?,?,?)',(opid+':'+x['id'],x['id'],'coyoacan',-x['qty'],event['at'],opid,'Venta'))
                        if shortages:issue='Existencia negativa por ventas desconectadas: revisar inventario.'
                if event['kind']=='move':require(p['amount']>0 and p['reason'] and p['type'] in ('Entrada','Gasto','Retiro'),'Movimiento inválido.')
                if event['kind']=='close':require(all(type(p[k]) is int and p[k]>=0 for k in ('counted','fund','envelope')) and p['counted']==p['fund']+p['envelope'] and p['expected']==current['expected'] and p['difference']==p['counted']-p['expected'],'Cierre inconsistente.')
                if event['offline'] and (not u or u['revision']!=g['revision']):issue+=' Operación con autorización descargada anteriormente.'
                self.db.execute('INSERT INTO events(id,branch,seq,body,hash,status,issue,received) VALUES(?,?,?,?,?,?,?,?)',(opid,branch,event['seq'],pack(event),digest,status,issue.strip(),now()))
                self.db.execute('COMMIT');return {'status':status,'issue':issue.strip(),'id':opid,'duplicate':False}
            except Exception:self.db.execute('ROLLBACK');raise
