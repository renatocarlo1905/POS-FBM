"""Manual inventory and immutable corrections for the E1 local laboratory."""
import base64, copy, hashlib, json, uuid
from decimal import Decimal, InvalidOperation
from pathlib import Path
from core import RuleError, require, cleantext, money, now, pack, template, calc_sale, PERMS

WAREHOUSES={'coyoacan':'Coyoacán','oficina':'Oficina','santa_rosa':'Santa Rosa'}
EXTRA_PERMS={'product_create':'Crear productos e ingresar mercancía','cancel_sale':'Anular venta por error','correct_payment':'Corregir medio de pago','correct_sellers':'Corregir vendedores'}
PERMS.update(EXTRA_PERMS)

def transaction(fn):
 def wrapped(c,*args,**kwargs):
  with c.lock:
   c.db.execute('BEGIN IMMEDIATE')
   try:r=fn(c,*args,**kwargs);c.db.execute('COMMIT');return r
   except Exception:c.db.execute('ROLLBACK');raise
 return wrapped

def init(c):
 c.db.executescript('''
 CREATE TABLE IF NOT EXISTS products(id text PRIMARY KEY, code text UNIQUE NOT NULL, data text NOT NULL);
 CREATE TABLE IF NOT EXISTS warehouse_stock(product text REFERENCES products, warehouse text, quantity integer NOT NULL, PRIMARY KEY(product,warehouse));
 CREATE TABLE IF NOT EXISTS inventory_entries(id text PRIMARY KEY, request_hash text NOT NULL, at text NOT NULL, actor text NOT NULL, data text NOT NULL);
 CREATE TABLE IF NOT EXISTS corrections(id text PRIMARY KEY, target text NOT NULL, kind text NOT NULL, before_data text NOT NULL, after_data text NOT NULL, reason text NOT NULL, operator text NOT NULL, authorizer text NOT NULL, at text NOT NULL, origin integer NOT NULL, request_hash text NOT NULL, document text NOT NULL);
 ALTER TABLE corrections DROP CONSTRAINT IF EXISTS corrections_target_fkey;
 ALTER TABLE corrections ADD COLUMN IF NOT EXISTS ordinal bigint GENERATED ALWAYS AS IDENTITY;
 CREATE TABLE IF NOT EXISTS stock_ledger(id text PRIMARY KEY, product text NOT NULL, warehouse text NOT NULL, delta integer NOT NULL, at text NOT NULL, origin text NOT NULL, reason text NOT NULL);
 CREATE TABLE IF NOT EXISTS related_changes(sale text NOT NULL, related text NOT NULL, PRIMARY KEY(sale,related));
 CREATE OR REPLACE FUNCTION prevent_fact_change() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'Immutable fact: append a correction instead'; END $$;
 DROP TRIGGER IF EXISTS immutable_events ON events;
 CREATE TRIGGER immutable_events BEFORE UPDATE OR DELETE ON events FOR EACH ROW EXECUTE FUNCTION prevent_fact_change();
 DROP TRIGGER IF EXISTS immutable_corrections ON corrections;
 CREATE TRIGGER immutable_corrections BEFORE UPDATE OR DELETE ON corrections FOR EACH ROW EXECUTE FUNCTION prevent_fact_change();
 DROP TRIGGER IF EXISTS immutable_stock_ledger ON stock_ledger;
 CREATE TRIGGER immutable_stock_ledger BEFORE UPDATE OR DELETE ON stock_ledger FOR EACH ROW EXECUTE FUNCTION prevent_fact_change();
 ''')
 from core import PRODUCTS
 for p in PRODUCTS:
  data={'id':p[0],'code':p[2],'name':p[1],'description':p[1]+' · Pieza de laboratorio','material':'Plata' if p[0] not in ('p5','p6') else 'Tumbaga' if p[0]=='p5' else 'Oro','material_id':1 if p[0] not in ('p5','p6') else 3 if p[0]=='p5' else 2,'type':p[1].split()[0],'type_id':int(p[2][2:4]),'sub1':'','sub2':'','price':p[3],'cost':p[4],'provider':1,'weight':None,'image':'','active':True,'print_price':True}
  c.db.execute('INSERT INTO products VALUES(?,?,?) ON CONFLICT(id) DO NOTHING',(p[0],p[2],pack(data)))
 if not c.get('materials'):c.put('materials',{'1':'Plata','2':'Oro','3':'Tumbaga','4':'Alpaca'});c.put('types',{'1':'Anillos','2':'Aretes','3':'Dijes','4':'Pulseras','5':'Collares'});c.put('providers',[{'id':1,'name':'Proveedor de prueba','phone':'','contact':'','address':''}])
 if c.get('categories') is None:
  categories=[{'id':k,'name':v,'parent':None,'description':''} for k,v in c.get('types').items()]
  for row in c.db.execute('SELECT id,data FROM products'):
   product=json.loads(row['data']);parent=str(product['type_id'])
   for key in ('sub1','sub2'):
    name=product.get(key,'').strip()
    if not name:continue
    found=next((x for x in categories if x['parent']==parent and x['name'].casefold()==name.casefold()),None)
    if not found:
     found={'id':'cat-'+uuid.uuid4().hex,'name':name,'parent':parent,'description':''};categories.append(found)
    parent=found['id']
   product['category_id']=parent;c.db.execute('UPDATE products SET data=? WHERE id=?',(pack(product),row['id']))
  c.put('categories',categories)

 roles=c.get('roles')
 for rid,r in roles.items():
  for k in EXTRA_PERMS:r['permissions'].setdefault(k,rid=='admin')
 c.put('roles',roles)
 if not c.get('branding_v1'):
  logo='data:image/png;base64,'+base64.b64encode((Path(__file__).parent/'static/company-logo.png').read_bytes()).decode();ts=c.get('templates')
  for t in ts.values():
   if not t.get('logo'):t['logo']=logo
  c.put('templates',ts);c.put('branding_v1',True)


def catalog(c,cost=False):
 stock={r['id']:r['available'] for r in c.db.execute('SELECT * FROM stock')};other={}
 for r in c.db.execute('SELECT * FROM warehouse_stock'):other.setdefault(r['product'],{})[r['warehouse']]=r['quantity']
 result=[]
 for r in c.db.execute('SELECT data FROM products ORDER BY code'):
  p=json.loads(r['data']);p['available']=stock.get(p['id'],0);p['warehouses']={'coyoacan':p['available'],'oficina':0,'santa_rosa':0,**other.get(p['id'],{})}
  if not cost:p.pop('cost',None)
  result.append(p)
 return result

def add_stock(c,pid,warehouse,qty,origin,reason,at=None):
 require(warehouse in WAREHOUSES,'Almacén inválido.')
 if warehouse=='coyoacan':c.db.execute('INSERT INTO stock VALUES(?,?) ON CONFLICT(id) DO UPDATE SET available=stock.available+EXCLUDED.available',(pid,qty))
 else:c.db.execute('INSERT INTO warehouse_stock VALUES(?,?,?) ON CONFLICT(product,warehouse) DO UPDATE SET quantity=warehouse_stock.quantity+EXCLUDED.quantity',(pid,warehouse,qty))
 if qty:c.db.execute('INSERT INTO stock_ledger VALUES(?,?,?,?,?,?,?)',(str(uuid.uuid4()),pid,warehouse,qty,at or now(),origin,reason))

def category_path(c,id):
 rows={x['id']:x for x in c.get('categories',[])};path=[]
 while id:
  require(id in rows and len(path)<3,'Categoría inválida.');x=rows[id];path.insert(0,x);id=x['parent']
 return path

@transaction
def create_category(c,actor,d):
 require(c.policy(next(u for u in c.get('users') if u['id']==actor)).get('product_create'),'Sin permiso para administrar categorías.')
 name=cleantext(d.get('name',''),80);require(name,'Escribe el nombre de la categoría.')
 parent=d.get('parent') or None;rows=c.get('categories',[])
 require(not any(x['parent']==parent and x['name'].casefold()==name.casefold() for x in rows),'Ya existe una categoría con ese nombre en este nivel.')
 if parent:
  require(len(category_path(c,parent))<3,'Se admiten categoría principal y dos niveles de subcategorías.');id='cat-'+uuid.uuid4().hex
 else:
  types=c.get('types');id=str(max(max(map(int,types),default=0),c.get('category_last_id',0))+1);require(int(id)<=99,'Se alcanzó el límite de 99 categorías principales del código de artículos.');types[id]=name;c.put('types',types);c.put('category_last_id',int(id))
 row={'id':id,'name':name,'parent':parent,'description':cleantext(d.get('description',''),500)};rows.append(row);c.put('categories',rows);c.audit(actor,'category_created',row);return row

def refresh_product_category(c,product,id):
 path=category_path(c,id);product.update(category_id=id,type_id=int(path[0]['id']),type=path[0]['name'],sub1=path[1]['name'] if len(path)>1 else '',sub2=path[2]['name'] if len(path)>2 else '')
 c.db.execute('UPDATE products SET data=? WHERE id=?',(pack(product),product['id']))

@transaction
def edit_category(c,actor,d):
 require(c.policy(next(u for u in c.get('users') if u['id']==actor)).get('product_create'),'Sin permiso para administrar categorías.')
 rows=c.get('categories',[]);row=next((x for x in rows if x['id']==d.get('id')),None);require(row,'Categoría inexistente.')
 before=copy.deepcopy(row);name=cleantext(d.get('name',''),80);require(name,'Escribe el nombre de la categoría.')
 require(not any(x['id']!=row['id'] and x['parent']==row['parent'] and x['name'].casefold()==name.casefold() for x in rows),'Ya existe una categoría con ese nombre en este nivel.')
 row.update(name=name,description=cleantext(d.get('description',''),500));c.put('categories',rows)
 if not row['parent']:
  types=c.get('types');types[row['id']]=name;c.put('types',types)
 for item in c.db.execute('SELECT data FROM products'):
  product=json.loads(item[0]);id=str(product.get('category_id') or product['type_id'])
  if any(x['id']==row['id'] for x in category_path(c,id)):refresh_product_category(c,product,id)
 c.audit(actor,'category_updated',{'before':before,'after':row});return row

@transaction
def delete_category(c,actor,d):
 require(c.policy(next(u for u in c.get('users') if u['id']==actor)).get('product_create'),'Sin permiso para administrar categorías.')
 rows=c.get('categories',[]);row=next((x for x in rows if x['id']==d.get('id')),None);require(row,'Categoría inexistente.')
 require(not any(x['parent']==row['id'] for x in rows),'Elimina primero las subcategorías de esta categoría.')
 products=[json.loads(r[0]) for r in c.db.execute('SELECT data FROM products')];assigned=[p for p in products if str(p.get('category_id') or p['type_id'])==row['id']]
 replacement=d.get('replacement')
 if assigned:
  require(replacement and replacement!=row['id'],'Selecciona otra categoría para los artículos asignados.');category_path(c,replacement)
  for product in assigned:refresh_product_category(c,product,replacement)
 c.put('category_last_id',max(c.get('category_last_id',0),max(map(int,c.get('types')),default=0)))
 if not row['parent']:
  types=c.get('types');types.pop(row['id']);c.put('types',types)
 c.put('categories',[x for x in rows if x['id']!=row['id']]);c.audit(actor,'category_deleted',{'category':row,'replacement':replacement,'products':[p['id'] for p in assigned]});return {'deleted':row['id'],'reassigned':len(assigned)}

@transaction
def provider(c,actor,d):
 name=cleantext(d.get('name',''),100);require(name,'Nombre del proveedor obligatorio.');rows=c.get('providers');id=max(p['id'] for p in rows)+1
 rows.append({'id':id,'name':name,**{k:cleantext(d.get(k,''),200) for k in ('phone','contact','address')}});c.put('providers',rows);c.audit(actor,'provider_created',{'id':id,'name':name});return {'id':id}

@transaction
def create_product(c,actor,d):
 id=d.get('request_id');require(isinstance(id,str) and len(id)==36,'Identificador requerido.');digest=hashlib.sha256(pack(d).encode()).hexdigest();old=c.db.execute('SELECT * FROM inventory_entries WHERE id=?',(id,)).fetchone()
 if old:require(old['request_hash']==digest,'Identificador repetido con distintos datos.');return json.loads(old['data'])
 name=cleantext(d.get('name',''),100);description=cleantext(d.get('description',''),1000);require(name and description,'Las dos descripciones son obligatorias.')
 d=dict(d)
 if d.get('category_id'):
  path=category_path(c,d['category_id']);d.update(type_id=path[0]['id'],sub1=path[1]['name'] if len(path)>1 else '',sub2=path[2]['name'] if len(path)>2 else '')
 materials=c.get('materials');types=c.get('types');m=str(d.get('material_id'));t=str(d.get('type_id'));require(m in materials and t in types,'Selecciona material y tipo registrados.')
 provider_id=int(d.get('provider',0));require(any(x['id']==provider_id for x in c.get('providers')),'Selecciona proveedor registrado.')
 price=money(d.get('price'));cost=money(d.get('cost'));require(price>0,'Precio mayor a cero requerido.')
 weight=d.get('weight','').strip();w=None
 if weight:
  try:w=Decimal(weight.replace(',','.'))
  except InvalidOperation:raise RuleError('Peso inválido.')
  require(w.is_finite() and 0<=w<=999 and w*1000==(w*1000).to_integral_value(),'Peso máximo 999 g y tres decimales.')
 qty=d.get('quantity');require(type(qty)is int and 0<=qty<=100000,'Cantidad entera no negativa requerida.');warehouse=d.get('warehouse');require(warehouse in WAREHOUSES,'Almacén requerido.')
 prefix=f'{int(m):02}{int(t):02}';seq=max([int(r['code'][-5:]) for r in c.db.execute('SELECT code FROM products') if len(r['code'])==15 and r['code'].isdigit() and r['code'].startswith(prefix)]+[0])+1;require(seq<=99999,'Consecutivo agotado.')
 code=prefix+f'{int(w*1000) if w is not None else 0:06}{seq:05}';image=d.get('image','');require(not image or image.startswith('data:image/png;base64,'),'La imagen de producto debe ser PNG.');template({'logo':image})
 pid='p-'+uuid.uuid4().hex;product={'id':pid,'code':code,'name':name,'description':description,'material':materials[m],'material_id':int(m),'type':types[t],'type_id':int(t),'category_id':d.get('category_id',t),'sub1':cleantext(d.get('sub1',''),80),'sub2':cleantext(d.get('sub2',''),80),'price':price,'cost':cost,'provider':provider_id,'weight':str(w) if w is not None else None,'image':image,'active':True,'print_price':bool(d.get('print_price',True))}
 c.db.execute('INSERT INTO products VALUES(?,?,?)',(pid,code,pack(product)));c.db.execute('INSERT INTO stock VALUES(?,0)',(pid,))
 add_stock(c,pid,warehouse,qty,id,'Alta manual de producto');result={'product':product,'quantity':qty,'warehouse':warehouse,'at':now()}
 c.db.execute('INSERT INTO inventory_entries VALUES(?,?,?,?,?)',(id,digest,now(),actor,pack(result)));c.audit(actor,'product_created',{'id':pid,'code':code,'quantity':qty,'warehouse':warehouse});return result

@transaction
def ingress(c,actor,d):
 ident=d.get('request_id');require(isinstance(ident,str) and len(ident)==36,'Identificador requerido.');digest=hashlib.sha256(pack(d).encode()).hexdigest();old=c.db.execute('SELECT * FROM inventory_entries WHERE id=?',(ident,)).fetchone()
 if old:require(old['request_hash']==digest,'Identificador repetido con distintos datos.');return json.loads(old['data'])
 r=c.db.execute('SELECT data FROM products WHERE id=?',(d.get('product'),)).fetchone();require(r,'Producto inexistente.');p=json.loads(r[0]);require(p['active'],'Reactiva el producto antes de ingresar mercancía.')
 qty=d.get('quantity');require(type(qty)is int and 0<qty<=100000,'Cantidad entera positiva requerida.');reason=cleantext(d.get('reason',''),300);require(reason,'Motivo requerido.');w=d.get('warehouse');add_stock(c,p['id'],w,qty,ident,reason)
 result={'product':p,'quantity':qty,'warehouse':w,'at':now(),'reason':reason};c.db.execute('INSERT INTO inventory_entries VALUES(?,?,?,?,?)',(ident,digest,now(),actor,pack(result)));c.audit(actor,'stock_received',{'id':p['id'],'quantity':qty,'warehouse':w});return result

def sale_view(c,id):
 require(not isinstance(id,str) or not id.startswith('SIM-'),'Este folio pertenece al historial simulado para reportes y no admite correcciones. Selecciona una venta manual confirmada.')
 r=c.db.execute("SELECT * FROM events WHERE id=? AND status='accepted'",(id,)).fetchone()
 if r:e=json.loads(r['body'])
 else:
  doc=next((json.loads(x[0]) for x in c.db.execute('SELECT document FROM corrections') if (json.loads(x[0])['payload'].get('replacement') or {}).get('id')==id),None)
  require(doc,'Selecciona una operación confirmada.')
  e={'id':id,'branch':doc['branch'],'kind':'sale','at':doc['payload']['original_at'],'registered_at':doc['at'],'actor':doc['payload']['operator'],'actor_name':doc['payload']['operator'],'payload':doc['payload']['replacement'],'template':doc['template']}
 require(e['kind']=='sale','Esta operación no es una venta. Las correcciones de órdenes requieren su módulo y estado económico.')
 p=copy.deepcopy(e['payload']);p.setdefault('sellers',[e['actor']]);p['cancelled']=False;history=[]
 for x in c.db.execute('SELECT * FROM corrections WHERE target=? ORDER BY ordinal',(id,)):
  p=json.loads(x['after_data']);history.append({**dict(x),'before_data':json.loads(x['before_data']),'after_data':json.loads(x['after_data']),'document':json.loads(x['document'])})
 e.pop('grant',None);e.pop('input',None)
 close=next((json.loads(x['body']) for x in c.events(e['branch']) if json.loads(x['body'])['kind']=='close' and json.loads(x['body'])['payload']['session']==p['session']),None)
 delta=0
 if close:
  for row in c.db.execute('SELECT document FROM corrections ORDER BY ordinal'):
   doc=json.loads(row[0]);d=doc['payload']
   if d['session']==p['session'] and doc['at']>close['at']:
    a=d['after'];b=d['before'];delta+=(0 if a['cancelled'] else a['cash'])-b['cash']+(d['replacement']['cash'] if d['replacement'] else 0)
 return {'original':e,'adjusted':p,'history':history,'revision':len(history),'close':close,'close_adjustment':delta}

def correction_preview(c,uid,branch,d,authorize=True):
 u=next((u for u in c.get('users') if u['id']==uid),None);require(u and u['active'],'Usuario no activo.');action=d.get('action');permission={'payment':'correct_payment','sellers':'correct_sellers','cancel':'cancel_sale','replace':'cancel_sale'}.get(action);require(permission,'Acción no disponible.')
 authorizer=uid;policy=c.policy(u)
 if not policy.get(permission):
  auth=c.login(d.get('authorizer',''),d.get('authorization_password',''),branch);a=next(u for u in c.get('users') if u['id']==auth['snapshot']['user']);require(c.policy(a).get(permission),'El autorizador no tiene este permiso.');authorizer=a['id'];policy=c.policy(a)
 reason=cleantext(d.get('reason',''),500);require(reason,'Motivo escrito obligatorio.')
 v=sale_view(c,d.get('target'));before=v['adjusted'];require(not before['cancelled'],'La venta ya fue anulada.');require(branch==0 or v['original']['branch']==branch,'Selecciona una venta de esta sucursal.')
 require(d.get('revision')==v['revision'],'La operación cambió; vuelve a consultar y comparar.')
 if action in ('cancel','replace'):
  links=list(c.db.execute('SELECT related FROM related_changes WHERE sale=?',(d['target'],)));require(not links,'La venta tiene cambios de mercancía vinculados y no puede anularse.')
 after=copy.deepcopy(before);extra=None
 if action=='payment':
  cash=money(d.get('cash',0));card=money(d.get('card',0));transfer=money(d.get('transfer',0));require(cash+card+transfer==before['total'],'El reparto debe conservar exactamente el total.')
  bank=cleantext(d.get('bank',''),80);last4=cleantext(d.get('last4',''),4);ref=cleantext(d.get('reference',''),100);require(not card or bank and len(last4)==4 and last4.isascii() and last4.isdigit(),'Completa banco y últimos cuatro dígitos.');require(not transfer or ref,'Falta referencia de transferencia.')
  after.update(cash=cash,card=card,transfer=transfer,bank=bank,last4=last4,reference=ref,received_cash=cash,change=0)
 elif action=='sellers':
  sellers=d.get('sellers');active={u['id'] for u in c.get('users') if u['active']};require(isinstance(sellers,list) and len(sellers)>0 and len(set(sellers))==len(sellers) and all(s in active for s in sellers),'Selecciona al menos un vendedor válido, sin repetir.');after['sellers']=sellers
 else:
  after['cancelled']=True
  if action=='replace':
   # New record captures correct bookkeeping, never invokes an external collection.
   products={p['id']:p for p in catalog(c,True)}
   for item in before['items']:products[item['id']]['available']+=item['qty']
   data=d.get('replacement',{});extra=calc_sale(data,products,policy)
   require(all(x['qty']<=products[x['id']]['available'] for x in extra['items']),'Existencia insuficiente para el reemplazo.')
   sellers=data.get('sellers',before['sellers']);active={u['id'] for u in c.get('users') if u['active']};require(sellers and len(set(sellers))==len(sellers) and all(s in active for s in sellers),'Vendedores de reemplazo inválidos.');extra['sellers']=sellers
 return {'target':d['target'],'action':action,'before':before,'after':after,'replacement':extra,'reason':reason,'operator':uid,'authorizer':authorizer,'revision':v['revision'],'branch':v['original']['branch'],'original_at':v['original']['at'],'session':before['session']}

@transaction
def correct(c,uid,branch,d):
 id=d.get('request_id');require(isinstance(id,str) and len(id)==36,'Identificador requerido.')
 safe={k:v for k,v in d.items() if k!='authorization_password'};digest=hashlib.sha256(pack({'uid':uid,'branch':branch,'data':safe}).encode()).hexdigest();old=c.db.execute('SELECT * FROM corrections WHERE id=?',(id,)).fetchone()
 if old:require(old['request_hash']==digest,'Identificador repetido con distintos datos.');return json.loads(old['document'])
 v=correction_preview(c,uid,branch,d);at=now()
 if v['action'] in ('cancel','replace'):
  for x in v['before']['items']:add_stock(c,x['id'],'coyoacan',x['qty'],id,'Anulación por error',at)
 if v['replacement']:
  for x in v['replacement']['items']:add_stock(c,x['id'],'coyoacan',-x['qty'],id,'Venta correcta vinculada',at)
  v['replacement']['id']='R-'+id;v['replacement']['session']=v['session']
 doc={'id':id,'branch':v['branch'],'kind':'correction','at':at,'actor_name':uid,'template':c.get('templates')[str(v['branch'])],'payload':{**v,'at':at,'id':id,'origin':'Dashboard' if not branch else 'POS'}}
 c.db.execute('INSERT INTO corrections(id,target,kind,before_data,after_data,reason,operator,authorizer,at,origin,request_hash,document) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)',(id,v['target'],v['action'],pack(v['before']),pack(v['after']),v['reason'],uid,v['authorizer'],at,branch,digest,pack(doc)))
 c.audit(uid,'correction',{'id':id,'target':v['target'],'action':v['action'],'authorizer':v['authorizer']});return doc

def corrections(c,branch=None):
 rows=c.db.execute('SELECT document FROM corrections'+(' WHERE origin=?' if branch else '')+' ORDER BY ordinal',(branch,) if branch else ())
 return [json.loads(r[0]) for r in rows]

def cash_adjustments(c,branch):
 import order_service
 result=order_service.adjustments(c,branch)
 for r in c.db.execute('SELECT document FROM corrections'):
  d=json.loads(r[0]);v=d['payload']
  if v['branch']!=branch:continue
  delta=(0 if v['after']['cancelled'] else v['after']['cash'])-v['before']['cash']
  if v['replacement']:delta+=v['replacement']['cash']
  result[v['session']]=result.get(v['session'],0)+delta
 return result
