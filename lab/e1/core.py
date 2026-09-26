"""Local E1 laboratory. Each store owns a durable SQLite queue; central owns shared stock."""
import base64, hashlib, hmac, io, json, secrets, sqlite3, threading, uuid
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo

PERMS = {'orders':'Gestionar apartados y reparaciones','sell':'Registrar ventas','discount':'Aplicar descuentos','cash_open':'Abrir caja','cash_close':'Cerrar caja','cash_move':'Entradas, gastos y retiros','receipts':'Consultar comprobantes','reprint':'Descargar copias PDF','cost':'Consultar costos'}
PRODUCTS = [('p1','Anillo espiral','010100240000015',100000,50000,8),('p2','Aretes luna','010200320000016',78000,34000,12),('p3','Dije corazón','010300210000017',65000,28000,3),('p4','Pulsera eslabón','010400640000018',150000,72000,5),('p5','Collar nudo','030500000000019',90000,42000,1),('p6','Anillo sol','020100280000020',275000,160000,4)]
NAMES=['Carlo','Melissa','Ximena','Citlali','Jessica','Himelda','Zicaru']
class RuleError(Exception): pass

def require(ok, message):
    if not ok: raise RuleError(message)
def now(): return datetime.now(ZoneInfo('America/Mexico_City')).isoformat(timespec='microseconds')
def pack(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def money(v):
    try: n=Decimal(str(v).replace(',','.'))
    except InvalidOperation: raise RuleError('Importe inválido.')
    require(n.is_finite() and 0<=n<=Decimal('99999999.99') and n*100==(n*100).to_integral_value(),'Usa un importe positivo con hasta dos decimales.')
    return int(n*100)
def percent(v):
    n=money(v); require(n<=10000,'El porcentaje debe estar entre 0 y 100.'); return n

def hashed(password,salt=None):
    salt=salt or secrets.token_hex(16)
    return salt+':'+hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),210000).hex()
def matches(password,value): return hmac.compare_digest(hashed(password,value.split(':')[0]),value)
def cleantext(v,limit):
    require(isinstance(v,str) and len(v)<=limit,'Texto demasiado largo o inválido.');return v.strip()
def template(value):
    out={k:cleantext(value.get(k,''),500) for k in ('header','footer')}
    out['width']=int(value.get('width',80));require(out['width'] in (58,80),'Elige 58 u 80 mm.')
    out['logo']=value.get('logo','')
    if out['logo']:
        require(isinstance(out['logo'],str) and len(out['logo'])<400000,'Logotipo demasiado grande (máximo 250 KB).')
        require(out['logo'].startswith(('data:image/png;base64,','data:image/jpeg;base64,')),'Usa PNG o JPEG.')
        from PIL import Image
        try:
            raw=base64.b64decode(out['logo'].split(',')[1],validate=True)
            with Image.open(io.BytesIO(raw)) as im:
                require(im.width<=2000 and im.height<=2000,'Logo máximo 2000 × 2000 píxeles.'); im.verify()
        except RuleError: raise
        except Exception: raise RuleError('Imagen no válida.')
    return out

def calc_sale(data,products,policy):
    require(policy.get('sell'),'Sin permiso para vender.')
    rate=percent(data.get('discount',0))
    require(not rate or policy.get('discount') and rate<=policy['max_discount'],'Descuento superior a tu autorización.')
    raw=data.get('items',[]);require(isinstance(raw,list) and 0<len(raw)<=100,'Agrega entre 1 y 100 partidas.')
    seen=set();items=[]
    for x in raw:
        p=products.get(x.get('id'));q=x.get('qty')
        require(p and p['id'] not in seen and type(q) is int and 1<=q<=1000,'Producto/cantidad inválidos o repetidos.')
        seen.add(p['id']);items.append({'id':p['id'],'name':p['name'],'code':p['code'],'qty':q,'price':p['price'],'gross':p['price']*q})
    gross=sum(x['gross'] for x in items)
    if 'discount_amount' in data:
        discount=money(data['discount_amount'])
        require(not discount or policy.get('discount') and discount*10000<=gross*policy['max_discount'],'Descuento superior a tu autorización.')
        rate=int((Decimal(discount)*10000/gross).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    else:
        discount=int((Decimal(gross)*rate/10000).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    # Allocate rounded total discount by largest remainder, deterministic original line order.
    shares=[discount*x['gross']//gross for x in items];rem=discount-sum(shares)
    order=sorted(range(len(items)),key=lambda i:-(discount*items[i]['gross']%gross))
    for i in order[:rem]: shares[i]+=1
    for x,d in zip(items,shares):x.update(discount=d,net=x['gross']-d)
    total=gross-discount;require(total>0,'En E1 el total debe ser mayor a cero.')
    cash=money(data.get('cash',0));card=money(data.get('card',0));transfer=money(data.get('transfer',0))
    require(card+transfer<=total and cash+card+transfer>=total,'Pago insuficiente o cambio originado en medios distintos al efectivo.')
    bank=cleantext(data.get('bank',''),80);last4=cleantext(data.get('last4',''),4);reference=cleantext(data.get('reference',''),100)
    require(not card or bank and len(last4)==4 and last4.isascii() and last4.isdigit(),'Completa banco y últimos cuatro dígitos.')
    require(not transfer or reference,'La transferencia requiere referencia.')
    return {'items':items,'gross':gross,'discount':discount,'rate':rate,'total':total,'cash':total-card-transfer,'received_cash':cash,'change':cash-(total-card-transfer),'card':card,'transfer':transfer,'bank':bank,'last4':last4,'reference':reference}

class DB:
    def __init__(self,path):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        self.lock=threading.RLock();self.db=sqlite3.connect(self.path,check_same_thread=False,isolation_level=None)
        self.db.row_factory=sqlite3.Row;self.db.execute('PRAGMA journal_mode=WAL');self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY,v TEXT NOT NULL);')
    def get(self,k,default=None):
        r=self.db.execute('SELECT v FROM kv WHERE k=?',(k,)).fetchone();return json.loads(r[0]) if r else default
    def put(self,k,v):self.db.execute('INSERT OR REPLACE INTO kv VALUES(?,?)',(k,pack(v)))
    def backup(self,dest):
        with self.lock:
            dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
            tmp=dest.with_suffix('.tmp');out=sqlite3.connect(tmp)
            try:self.db.backup(out)
            finally:out.close()
            tmp.replace(dest)

from pg import PGDB

class Central(PGDB):
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
        from extensions import init
        init(self)
        __import__('order_service').init(self)
    def audit(self,actor,action,detail):self.db.execute('INSERT INTO audit(at,actor,action,detail) VALUES(?,?,?,?)',(now(),actor,action,pack(detail)))
    def policy(self,u):
        r=self.get('roles')[u['role']];return {**r['permissions'],'max_discount':r['max_discount'],'admin':u['role']=='admin'}
    def sign(self,payload):
        body=base64.urlsafe_b64encode(pack(payload).encode()).decode()
        return body+'.'+hmac.new(bytes.fromhex(self.get('secret')),body.encode(),hashlib.sha256).hexdigest()
    def verify(self,token):
        try:
            body,sig=token.split('.');expected=hmac.new(bytes.fromhex(self.get('secret')),body.encode(),hashlib.sha256).hexdigest()
            require(hmac.compare_digest(sig,expected),'Autorización inválida.');return json.loads(base64.urlsafe_b64decode(body))
        except (ValueError,TypeError,AttributeError):raise RuleError('Autorización inválida.')
    def login(self,username,password,branch):
        with self.lock:
            u=next((u for u in self.get('users') if u['id']==username.lower()),None)
            require(u and u['active'] and matches(password,u['password']),'Usuario o contraseña incorrectos.')
            require(branch==0 and u['role']=='admin' or branch in u['branches'],'Sin acceso a esta aplicación o sucursal.')
            snapshot={'user':u['id'],'name':u['name'],'branch':branch,'revision':u['revision'],'policy':self.policy(u),'issued_at':now(),'nonce':secrets.token_hex(12)}
            grant=self.sign(snapshot); sessions=self.get('sessions');token=secrets.token_urlsafe(32);sessions[token]={'user':u['id'],'revision':u['revision'],'branch':branch};self.put('sessions',sessions)
            return {'token':token,'grant':grant,'snapshot':snapshot,'verifier':u['password']}
    def auth(self,token,admin=False):
        s=self.get('sessions',{}).get(token);require(s,'Inicia sesión de nuevo.')
        u=next((u for u in self.get('users') if u['id']==s['user']),None)
        require(u and u['active'] and u['revision']==s['revision'],'Tu acceso cambió; inicia sesión de nuevo.')
        require(not admin or u['role']=='admin','Acceso exclusivo de administrador.');return u
    def users(self):return [{**{k:v for k,v in u.items() if k!='password'},'seller_code':'FBV-'+u['id'].upper()} for u in self.get('users')]
    def edit_user(self,actor,data):
        with self.lock:
            users=self.get('users');uid=cleantext(data.get('id',''),50).lower();u=next((u for u in users if u['id']==uid),None)
            require(u,'Empleado inexistente.');role=data.get('role');require(role in self.get('roles'),'Rol inexistente.')
            require(uid!='carlo' or role=='admin' and data.get('active',True),'Carlo debe conservar acceso de administrador.')
            bs=data.get('branches',[1,2]);require(isinstance(bs,list) and bs and all(type(b)is int and b in (1,2) for b in bs),'Selecciona sucursales válidas.')
            password=data.get('password','');require(not password or 8<=len(password)<=128,'La nueva contraseña debe tener 8 a 128 caracteres.')
            u.update(name=cleantext(data.get('name',''),80),email=cleantext(data.get('email',''),120),phone=cleantext(data.get('phone',''),30),role=role,active=bool(data.get('active')),branches=sorted(set(bs)),revision=u['revision']+1)
            require(u['name'],'El nombre es obligatorio.')
            if password:u['password']=hashed(password)
            self.put('users',users);self.audit(actor,'employee_updated',{'id':uid,'role':role,'password_changed':bool(password)})
    def edit_role(self,actor,data):
        with self.lock:
            roles=self.get('roles');rid=data.get('id') or 'role-'+uuid.uuid4().hex[:8];require(rid!='admin','El rol administrador conserva todos los derechos.')
            name=cleantext(data.get('name',''),80);require(name,'Nombre obligatorio.')
            roles[rid]={'name':name,'permissions':{k:bool(data.get('permissions',{}).get(k,False)) for k in PERMS},'max_discount':percent(data.get('max_discount',0))}
            self.put('roles',roles);users=self.get('users')
            for u in users:
                if u['role']==rid:u['revision']+=1
            self.put('users',users);self.audit(actor,'role_updated',{'id':rid,'role':roles[rid]})
    def catalog(self,cost=False):
        from extensions import catalog
        return catalog(self,cost)
    def pull(self,grant):
        with self.lock:
            old=self.verify(grant);u=next((u for u in self.get('users') if u['id']==old['user']),None)
            require(u and u['active'] and old['branch'] in u['branches'],'Acceso desactivado para esta sucursal.')
            snap={**old,'name':u['name'],'revision':u['revision'],'policy':self.policy(u),'issued_at':now()}
            return {'catalog':self.catalog(self.policy(u).get('cost',False)),'template':self.get('templates')[str(old['branch'])],'grant':self.sign(snap),'snapshot':snap,'at':now(),'relogin':u['revision']!=old['revision'],'cash_adjustments':__import__('extensions').cash_adjustments(self,old['branch']),'corrections':[json.loads(r[0]) for r in self.db.execute('SELECT document FROM corrections') if json.loads(r[0])['branch']==old['branch']],'staff':[{'id':x['id'],'name':x['name'],'seller_code':'FBV-'+x['id'].upper()} for x in self.get('users') if x['active']],'order_cash_moves':[{'id':p['id'],'kind':'order','amount':p['cash'],'reason':p['kind']+' · '+p['order']} for p in __import__('order_service').movements(self,old['branch']) if p['session']==(cash_state([json.loads(r['body']) for r in self.events(old['branch']) if r['status']=='accepted']) or {}).get('id')],'meta':{'materials':self.get('materials'),'types':self.get('types'),'categories':self.get('categories',[]),'providers':self.get('providers'),'warehouses':__import__('extensions').WAREHOUSES}}
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
                    catalog={x['id']:x for x in self.catalog()};expected=calc_sale(p['request'],catalog,policy)
                    require(all(p[k]==v for k,v in expected.items()),'Importes o partidas no válidos.')
                    shortages=[x for x in p['items'] if x['qty']>catalog[x['id']]['available']]
                    if shortages and not event['offline']:status='rejected';issue='Existencia central insuficiente. No registrar el cobro; revisa el comprobante rechazado.'
                    else:
                        for x in p['items']:
                            self.db.execute('UPDATE stock SET available=available-? WHERE id=?',(x['qty'],x['id']))
                            self.db.execute('INSERT INTO stock_ledger VALUES(?,?,?,?,?,?,?)',(opid+':'+x['id'],x['id'],'coyoacan',-x['qty'],event['at'],opid,'Venta'))
                        if shortages:issue='Existencia negativa por ventas desconectadas: revisar inventario.'
                if event['kind']=='move':require(p['amount']>0 and p['reason'] and p['type'] in ('Entrada','Gasto','Retiro'),'Movimiento inválido.')
                if event['kind']=='close':require(p['counted']==p['fund']+p['envelope'] and p['expected']==current['expected'],'Cierre inconsistente.')
                if event['offline'] and (not u or u['revision']!=g['revision']):issue+=' Operación con autorización descargada anteriormente.'
                self.db.execute('INSERT INTO events(id,branch,seq,body,hash,status,issue,received) VALUES(?,?,?,?,?,?,?,?)',(opid,branch,event['seq'],pack(event),digest,status,issue.strip(),now()))
                self.db.execute('COMMIT');return {'status':status,'issue':issue.strip(),'id':opid,'duplicate':False}
            except Exception:self.db.execute('ROLLBACK');raise

def cash_state(events):
    current=None
    for e in events:
        p=e['payload']
        if e['kind']=='open':current={'id':e['id'],'opening':p['opening'],'expected':p['opening'],'moves':[]}
        elif e['kind']=='close':current=None
        elif current:
            amount=p['cash'] if e['kind']=='sale' else p['amount']*(1 if p['type']=='Entrada' else -1)
            current['expected']+=amount;current['moves'].append({'id':e['id'],'kind':e['kind'],'amount':amount,'reason':p.get('reason','Venta')})
    return current

class Store(DB):
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
    def sync(self,uid):
        if self.get('offline'):return
        acknowledgements=[]
        for row in self.rows():
            if row['status']=='pending':
                reply=self.transport('receive',json.loads(row['body']))
                acknowledgements.append((reply['status'],reply['issue'],row['id']))
        creds=self.get('credentials');c=creds[uid]
        try:pull=self.transport('pull',{'grant':c['grant']})
        except RuleError:
            # Accepted queued facts remain accepted; new work requires fresh access.
            del creds[uid];self.put('credentials',creds);raise
        self.db.execute('BEGIN IMMEDIATE')
        try:
            self.db.executemany('UPDATE operations SET status=?,issue=? WHERE id=?',acknowledgements)
            self.put('catalog',pull['catalog']);self.put('template',pull['template']);self.put('last_sync',pull['at']);self.put('cash_adjustments',pull['cash_adjustments']);self.put('corrections',pull['corrections']);self.put('staff',pull['staff']);self.put('catalog_meta',pull['meta']);self.put('order_cash_moves',pull.get('order_cash_moves',[]))
            self.db.execute('COMMIT')
        except Exception:self.db.execute('ROLLBACK');raise
        if pull['relogin']:
            # Role/password changes refresh permissions but require password authentication again.
            del creds[uid];self.put('credentials',creds);raise RuleError('Tu acceso cambió. Inicia sesión otra vez conectado.')
        c.update(grant=pull['grant'],snapshot=pull['snapshot']);self.put('credentials',creds)
        self.put('catalog',pull['catalog']);self.put('template',pull['template']);self.put('last_sync',pull['at']);self.put('cash_adjustments',pull['cash_adjustments']);self.put('corrections',pull['corrections']);self.put('staff',pull['staff']);self.put('catalog_meta',pull['meta']);self.put('order_cash_moves',pull.get('order_cash_moves',[]));self.copy()
    def available(self):
        ps={p['id']:dict(p) for p in self.get('catalog',[])}
        for r in self.rows():
            e=json.loads(r['body'])
            if r['status']=='pending' and e['kind']=='sale':
                for x in e['payload']['items']:ps[x['id']]['available']-=x['qty']
        return ps
    def submit(self,token,kind,data,request_id):
        with self.lock:
            # Browser retains a UUID across uncertain HTTP replies.
            try:uuid.UUID(request_id)
            except (ValueError,TypeError,AttributeError):raise RuleError('Identificador de operación inválido.')
            uid,c=self.auth(token)
            prior=self.db.execute('SELECT body FROM operations WHERE id=?',(request_id,)).fetchone()
            if prior:
                prev=json.loads(prior[0]);require(prev['kind']==kind and prev['actor']==uid and prev['input']==data,'UUID reutilizado con contenido diferente.')
                return {'id':request_id,'repeated':True}
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
                    products=self.available();p.update(calc_sale(data,products,policy))
                    require(all(x['qty']<=products[x['id']]['available'] for x in p['items']),'Cantidad superior a la disponibilidad conocida.')
                    p['request']=data
                    sellers=data.get('sellers',[uid]);staff={s['id'] for s in self.get('staff',[])};require(isinstance(sellers,list) and sellers and len(set(sellers))==len(sellers) and all(s in staff for s in sellers),'Selecciona vendedores válidos.');p['sellers']=sellers
                elif kind=='move':
                    amount=money(data.get('amount',0));reason=cleantext(data.get('reason',''),300);typ=data.get('type');require(amount>0 and reason and typ in ('Entrada','Gasto','Retiro'),'Completa importe, tipo y motivo.')
                    p.update(amount=amount,reason=reason,type=typ)
                elif kind=='close':
                    counted=money(data.get('counted',0));fund=money(data.get('fund',0));envelope=money(data.get('envelope',0));require(counted==fund+envelope,'Fondo y sobre deben sumar el efectivo contado.')
                    p.update(counted=counted,fund=fund,envelope=envelope,expected=current['expected'],difference=counted-current['expected'])
            seq=self.db.execute('SELECT COALESCE(MAX(seq),0)+1 FROM operations').fetchone()[0]
            event={'id':request_id,'seq':seq,'branch':self.branch,'kind':kind,'actor':uid,'actor_name':c['snapshot']['name'],'at':now(),'offline':not online,'grant':c['grant'],'payload':p,'input':data,'template':self.get('template')}
            self.db.execute('INSERT INTO operations VALUES(?,?,?,?,?)',(request_id,seq,pack(event),'pending',''))
            self.copy()
            try:self.sync(uid)
            except (ConnectionError,RuleError) as ex:self.put('sync_error',str(ex))
            return {'id':request_id}
    def state(self,token):
        with self.lock:
            uid,c=self.auth(token);error=''
            try:self.sync(uid)
            except (ConnectionError,RuleError) as e:error=str(e)
            uid,c=self.auth(token);policy=c['snapshot']['policy'];cash=cash_state(self.operations())
            if cash:
                cash={k:v for k,v in cash.items() if k!='expected'}
                cash['moves']+=self.get('order_cash_moves',[])
            ops=[]
            for r in reversed(self.rows()):
                e=json.loads(r['body']); e.pop('grant');e.pop('input');e['payload'].pop('request',None)
                ops.append({**e,'status':r['status'],'issue':r['issue']})
            return {'user':c['snapshot']['name'],'policy':policy,'authorization_at':c['snapshot']['issued_at'],'offline':self.get('offline'),'branch':self.branch,'catalog':[{k:v for k,v in p.items() if k!='cost' or policy.get('cost')} for p in self.available().values()],'session':cash,'operations':ops if policy.get('receipts') else [],'pending':sum(r['status']=='pending' for r in self.rows()),'last_sync':self.get('last_sync'),'sync_error':error,'copy':self.get('copy_status'),'template':self.get('template'),'staff':self.get('staff',[]),'corrections':self.get('corrections',[]) if policy.get('receipts') else [],**self.get('catalog_meta',{})}

def receipt_pdf(event,reprint=False):
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase.pdfmetrics import stringWidth, registerFont
    from reportlab.pdfbase.ttfonts import TTFont
    registerFont(TTFont('E1Sans',str(Path(__file__).parent/'static/Montserrat-Regular.ttf')))
    registerFont(TTFont('E1Bold',str(Path(__file__).parent/'static/Montserrat-Bold.ttf')))
    t=event.get('template') or template({});width=t['width']*72/25.4;usable=width-24
    lines=[]
    def add(text,bold=False,size=9):
        for paragraph in str(text).splitlines() or ['']:
            words=paragraph.split();line=''
            for word in words:
                # Hard-wrap long tokens as well as ordinary prose.
                for part in [word[i:i+28] for i in range(0,len(word),28)]:
                    candidate=(line+' '+part).strip()
                    if line and stringWidth(candidate,'E1Bold' if bold else 'E1Sans',size)>usable:lines.append((line,bold,size));line=part
                    else:line=candidate
            lines.append((line,bold,size))
    add(t['header'],True,11);add('COMPROBANTE DE PRUEBA',True,9)
    if reprint:add('COPIA / REIMPRESIÓN',True)
    add(f"Sucursal {event['branch']} · { {'sale':'VENTA','open':'APERTURA','move':'MOVIMIENTO','close':'CIERRE','correction':'CORRECCIÓN INTERNA'}[event['kind']] }");add(datetime.fromisoformat(event['at']).strftime('%d/%m/%Y %H:%M:%S'));add('Folio '+event['id']);add('Atendió: '+event['actor_name']);add('-'*24)
    p=event['payload'];fmt=lambda n:f'${n/100:,.2f}'
    if event['kind']=='sale':
        for x in p['items']:add(f"{x['qty']} x {x['name']}");add(f"{fmt(x['price'])} c/u · Neto {fmt(x['net'])}")
        add('-'*24)
        for label,k in [('Subtotal','gross'),('Descuento','discount'),('TOTAL','total'),('Efectivo recibido','received_cash'),('Efectivo aplicado','cash'),('Tarjeta','card'),('Transferencia','transfer'),('Cambio','change')]:add(label+': '+fmt(p[k]),k=='total',11 if k=='total' else 9)
    elif event['kind']=='correction':
        add('Operación original: '+p['target']);add('Fecha original: '+datetime.fromisoformat(p['original_at']).strftime('%d/%m/%Y %H:%M:%S'));add('Acción: '+{'payment':'Corregir pago','sellers':'Corregir vendedores','cancel':'Anular venta','replace':'Anular y reemplazar'}[p['action']]);add('Motivo: '+p['reason']);add('Operador: '+p['operator']);add('Autorizador: '+p['authorizer']);add('Importe original: '+fmt(p['before']['total']));add('No representa entrega ni devolución de dinero.');
        for label,key in [('Efectivo','cash'),('Tarjeta','card'),('Transferencia','transfer')]:add(label+': '+fmt(p['before'][key])+' -> '+fmt(0 if p['after']['cancelled'] else p['after'][key]))
        add('Vendedores: '+', '.join(p['before']['sellers'])+' -> '+', '.join(p['after']['sellers']))
        if p['replacement']:add('Reemplazo vinculado: '+p['replacement']['id']);add('Importe correcto: '+fmt(p['replacement']['total']))
    elif event['kind']=='open':add('Fondo inicial: '+fmt(p['opening']))
    elif event['kind']=='move':add(p['type']+': '+fmt(p['amount']));add(p['reason'])
    else:
        for k,label in [('expected','Esperado'),('counted','Contado'),('difference','Diferencia'),('fund','Fondo siguiente'),('envelope','Sobre')]:add(label+': '+fmt(p[k]))
    add('-'*24);add(t['footer']);add('MXN · Laboratorio E1')
    logo=t.get('logo');brand_logo=bool(logo and logo=='data:image/png;base64,'+base64.b64encode((Path(__file__).parent/'static/company-logo.png').read_bytes()).decode());height=36+sum(s+5 for _,_,s in lines)+(min(usable,150)+8 if logo else 0)
    stream=io.BytesIO();c=canvas.Canvas(stream,pagesize=(width,height));c.setTitle('Comprobante E1 '+event['id']);y=height-18
    if brand_logo:
        from branding import draw_brand
        y-=draw_brand(c,width,y)+8
    elif logo:
        size=min(usable,150);c.drawImage(ImageReader(io.BytesIO(base64.b64decode(logo.split(',')[1]))),(width-size)/2,y-size,size,size,preserveAspectRatio=True,anchor='c',mask='auto');y-=size+8
    c.setFillColor(HexColor('#434345'))
    for text,bold,size in lines:c.setFont('E1Bold' if bold else 'E1Sans',size);c.drawString(12,y-size,text);y-=size+5
    c.save();return stream.getvalue()
