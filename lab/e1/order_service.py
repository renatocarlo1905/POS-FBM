"""Online orders: atomic PostgreSQL documents, reservations, receipts and cash allocations."""
import copy,json,uuid,hashlib
from datetime import datetime,timedelta
from pathlib import Path
from core import require,RuleError,now,pack,money,cleantext,cash_state

def init(c):
 c.db.executescript('''CREATE TABLE IF NOT EXISTS service_orders(id text PRIMARY KEY,body text NOT NULL);
 CREATE TABLE IF NOT EXISTS order_requests(id text PRIMARY KEY,digest text NOT NULL,result text NOT NULL);
 CREATE TABLE IF NOT EXISTS order_credit(phone text PRIMARY KEY,amount bigint NOT NULL CHECK(amount>=0));''')
 roles=c.get('roles',{});changed=False
 for role in roles.values():
  if 'orders' not in role['permissions']:role['permissions']['orders']=bool(role['permissions'].get('sell'));changed=True
 if changed:c.put('roles',roles)
 if not c.get('orders_seed_v1'):
  for o in json.loads((Path(__file__).parent/'orders_demo.json').read_text())['rows']:
   o.update(simulated=True,revision=1,documents=[],credit_issued=0)
   c.db.execute('INSERT INTO service_orders VALUES(?,?) ON CONFLICT DO NOTHING',(o['id'],pack(o)))
  c.put('orders_seed_v1',True)
def all_orders(c):return [json.loads(r[0]) for r in c.db.execute('SELECT body FROM service_orders')]
def get(c,key):
 r=c.db.execute('SELECT body FROM service_orders WHERE id=?',(key,)).fetchone();require(r,'Orden inexistente.');return json.loads(r[0])
def save(c,o):c.db.execute('INSERT INTO service_orders VALUES(?,?) ON CONFLICT(id) DO UPDATE SET body=EXCLUDED.body',(o['id'],pack(o)))
def paid(o):return sum(p['amount'] for p in o['payments'])-o.get('credit_issued',0)
def balance(o):return max(0,o['total']-paid(o))
def closed(o):return o['status'] in ('delivered','cancelled','released')
def text(d,k,limit=300,required=True):
 v=cleantext(d.get(k,''),limit);require(v or not required,'Completa '+k+'.');return v

def movements(c,branch=None):
 return [{**p,'order':o['id']} for o in all_orders(c) if not o.get('simulated') for p in o['payments']+([o['conversion_payment']] if o.get('conversion_payment') else []) if not branch or p['branch']==branch]
def adjustments(c,branch):
 result={}
 for p in movements(c,branch):result[p['session']]=result.get(p['session'],0)+p['cash']
 return result

def sale_events(c):
 result=[]
 for o in all_orders(c):
  if o.get('simulated'):continue
  for key in ('sale','replacement_sale'):
   if o.get(key):
    event=copy.deepcopy(o[key]);event['receipt_index']=max(0,len(o['documents'])-1) if key=='replacement_sale' else max(0,len(o['payments'])-1);result.append(event)
 return result
def recognize(o,u,branch,at):
 if o.get('sale') or balance(o):return
 o['settled']=at
 if o['kind']=='layaway':o['status']='settled'
 items=[{**x,'gross':x['qty']*x['price'],'net':x['qty']*x['price'],'discount':0} for x in o['items']] if o['kind']=='layaway' else [{'id':'repair-service','name':'Servicio de reparación','qty':1,'price':o['total'],'gross':o['total'],'net':o['total'],'discount':0,'cost':0,'category':'Reparaciones'}]
 o['sale']={'id':o['id']+'-VENTA','order_id':o['id'],'kind':'sale','status':'accepted','branch':branch or o['branch'],'at':at,'actor':u['id'],'actor_name':u['name'],'payload':{'session':o['payments'][-1].get('session') if o['payments'] and o['payments'][-1].get('at')==at else None,'items':items,'gross':o['total'],'total':o['total'],'discount':0,'rate':0,'cash':0,'card':0,'transfer':0,'received_cash':0,'change':0,'sellers':o.get('seller_ids',[]) or ['Matanga - sin asignación']}}

def document(o,label,at,payment=None):
 from orders_preview import receipts
 # Store an immutable snapshot for reprints, even after administrative corrections.
 index=len(receipts(o))-1
 o['documents'].append({'label':label,'at':at,'order':{k:copy.deepcopy(v) for k,v in o.items() if k!='documents'},'index':index})

def stock(c,items,direction,ref,reason):
 for x in items:
  if direction<0:
   r=c.db.execute('UPDATE stock SET available=available-? WHERE id=? AND available>=? RETURNING id',(x['qty'],x['id'],x['qty'])).fetchone();require(r,'Existencia insuficiente: '+x['name'])
  else:c.db.execute('UPDATE stock SET available=available+? WHERE id=?',(x['qty'],x['id']))
  c.db.execute('INSERT INTO stock_ledger VALUES(?,?,?,?,?,?,?)',(str(uuid.uuid4()),x['id'],'coyoacan',direction*x['qty'],now(),ref,reason))

def product_items(c,data):
 catalog={p['id']:p for p in c.catalog(True)};raw=data.get('items');require(isinstance(raw,list) and 0<len(raw)<=100,'Agrega entre 1 y 100 piezas.');out=[];seen=set()
 for row in raw:
  p=catalog.get(row.get('id'));q=row.get('qty');require(p and p['id'] not in seen and type(q)is int and 1<=q<=1000,'Producto o cantidad inválida.');seen.add(p['id']);out.append({k:p[k] for k in ('id','name','code','price','cost')}|{'qty':q,'category':p.get('type','Sin categoría')})
 return out

def payment(c,o,u,branch,d,at,minimum=1):
 require(branch in (1,2),'Los cobros se registran desde el POS.');require(not closed(o) and balance(o)>0,'Orden cerrada o liquidada.')
 if o['kind']=='layaway' and o['due']<at[:10]:require(u['role']=='admin' and text(d,'reason'),'Apartado vencido: requiere administrador y motivo.')
 events=[json.loads(r['body']) for r in c.events(branch) if r['status']=='accepted'];session=cash_state(events);require(session,'Abre caja antes de cobrar.')
 amount=money(d.get('amount'));require(minimum<=amount<=balance(o),'Importe fuera del anticipo mínimo o saldo pendiente.')
 if o['kind']=='repair' and o['payments']:require(o['status']=='ready','La reparación debe estar lista para liquidarla al recoger.');require(amount==balance(o),'Las reparaciones solo admiten anticipo y liquidación final.')
 cash=money(d.get('cash',0));card=money(d.get('card',0));transfer=money(d.get('transfer',0));credit=money(d.get('credit',0));require(card+transfer+credit<=amount and cash+card+transfer+credit>=amount,'Pago insuficiente o cambio no originado en efectivo.')
 bank=text(d,'bank',80,False);last4=text(d,'last4',4,False);reference=text(d,'reference',100,False)
 require(not card or bank and len(last4)==4 and last4.isascii() and last4.isdigit(),'Completa banco y últimos cuatro dígitos.');require(not transfer or reference,'Referencia de transferencia obligatoria.')
 if credit:
  r=c.db.execute('UPDATE order_credit SET amount=amount-? WHERE phone=? AND amount>=? RETURNING phone',(credit,o['customer']['phone'],credit)).fetchone();require(r,'Saldo a favor insuficiente para este teléfono de cliente.')
 p={'id':o['id']+'-P'+str(len(o['payments'])+1),'kind':'Anticipo' if not o['payments'] else 'Liquidación' if amount==balance(o) else 'Abono','at':at,'branch':branch,'actor':u['name'],'session':session['id'],'amount':amount,'cash':amount-card-transfer-credit,'received_cash':cash,'change':cash-(amount-card-transfer-credit),'card':card,'transfer':transfer,'credit':credit,'bank':bank,'last4':last4,'reference':reference,'reason':d.get('reason',''),'method':' · '.join(f'{label}: ${value/100:,.2f}' for label,value in [('Efectivo',amount-card-transfer-credit),('Tarjeta',card),('Transferencia',transfer),('Saldo a favor',credit)] if value)}
 o['payments'].append(p);recognize(o,u,branch,at)
 if 'history' in o:o['history'].append({'at':at,'actor':u['name'],'from':o['status'],'to':o['status'],'note':p['kind']+' en sucursal '+str(branch)+(' · '+text(d,'reason',500,False) if d.get('reason') else '')});
 if 'history' in o:document(o,p['kind'],at)

def execute(c,u,branch,d):
 require(u['role']=='admin' or c.policy(u).get('orders',c.policy(u).get('sell')),'Sin permiso para gestionar órdenes.')
 try:uuid.UUID(d.get('request_id',''))
 except (ValueError,TypeError):raise RuleError('Identificador de petición inválido.')
 digest=hashlib.sha256(pack({'user':u['id'],'branch':branch,'data':d}).encode()).hexdigest()
 c.db.execute('BEGIN IMMEDIATE')
 try:
  prev=c.db.execute('SELECT * FROM order_requests WHERE id=?',(d['request_id'],)).fetchone()
  if prev:
   require(prev['digest']==digest,'Petición reutilizada con datos distintos.');c.db.execute('COMMIT');return json.loads(prev['result'])
  action=d.get('action');at=now();before=None
  if action=='settings':
   require(u['role']=='admin','Configuración exclusiva del administrador.');settings={k:d.get(k) for k in ('layaway_days','repair_days')};require(all(type(v)is int and 1<=v<=3650 for v in settings.values()),'Usa plazos enteros entre 1 y 3650 días.');c.put('order_settings',settings);c.audit(u['id'],'order_settings',settings);result={'settings':settings};c.db.execute('INSERT INTO order_requests VALUES(?,?,?)',(d['request_id'],digest,pack(result)));c.db.execute('COMMIT');return result
  if action=='create':
   require(branch in (1,2),'Crea las órdenes desde el POS.');kind=d.get('kind');require(kind in ('layaway','repair'),'Tipo inválido.')
   name=text(d,'name',100);phone=text(d,'phone',30);require(len(phone)>=7,'Teléfono incompleto.')
   o={'id':('APA-' if kind=='layaway' else 'REP-')+uuid.uuid4().hex[:12].upper(),'kind':kind,'branch':branch,'created':at,'customer':{'name':name,'phone':phone},'payments':[],'history':[],'budget_history':[],'delivery':None,'settled':None,'ready':None,'term':c.get('order_settings',{'layaway_days':45,'repair_days':45})['layaway_days' if kind=='layaway' else 'repair_days'],'due':None,'work':'','expected_delivery':None,'notes':text(d,'notes',1000,False),'sellers':[],'seller_ids':[],'ever_in_repair':False,'credit_issued':0,'revision':0,'simulated':False,'documents':[]}
   if kind=='layaway':
    o['items']=product_items(c,d);o['total']=sum(x['price']*x['qty'] for x in o['items']);o['due']=(datetime.fromisoformat(at)+timedelta(days=o['term'])).date().isoformat();o['status']='pending'
    staff={s['id']:s['name'] for s in c.users() if s['active']};ids=d.get('sellers',[]);require(isinstance(ids,list) and ids and all(i in staff for i in ids),'Selecciona vendedores válidos.');o['seller_ids']=list(dict.fromkeys(ids));o['sellers']=[staff[i] for i in o['seller_ids']];stock(c,o['items'],-1,o['id'],'Reserva de apartado')
   else:
    raw=d.get('pieces',[]);require(isinstance(raw,list) and 0<len(raw)<=100,'Describe las piezas del cliente.');o['items']=[{'name':cleantext(x,300),'qty':1} for x in raw];require(all(x['name'] for x in o['items']),'Pieza sin descripción.')
    o['total']=money(d.get('total'));require(o['total']>0,'Presupuesto positivo obligatorio.');o['work']=text(d,'work',1000);o['expected_delivery']=text(d,'expected_delivery',10);datetime.fromisoformat(o['expected_delivery']);require(o['expected_delivery']>=at[:10],'La entrega prevista no puede ser anterior a hoy.');o['status']='received';o['budget_history']=[{'at':at,'before':None,'after':o['total'],'actor':u['name'],'reason':'Presupuesto inicial','agreement':text(d,'agreement',500)}]
   o['history'].append({'at':at,'actor':u['name'],'from':'—','to':o['status'],'note':'Alta desde sucursal '+str(branch)})
   payment(c,o,u,branch,d,at,(o['total']*(40 if kind=='layaway' else 50)+99)//100)
  else:
   o=get(c,d.get('id'));before=copy.deepcopy(o);require(type(d.get('revision'))is int and d['revision']==o['revision'],'Otra sesión cambió la orden. Actualiza antes de guardar.')
   require(not o.get('simulated') or action=='edit','Los ejemplos históricos solo admiten edición de consulta. Crea una orden nueva para operar caja e inventario.')
   if action=='pay':payment(c,o,u,branch,d,at)
   elif action=='edit':
    require(u['role']=='admin','Solo el administrador puede editar órdenes.');reason=text(d,'reason',500)
    o['customer']={'name':text(d,'name',100),'phone':text(d,'phone',30)};require(len(o['customer']['phone'])>=7,'Teléfono incompleto.');o['notes']=text(d,'notes',1000,False)
    if o['kind']=='repair':
     work=text(d,'work',1000);expected=text(d,'expected_delivery',10);datetime.fromisoformat(expected)
     require(not o['settled'] or (work==o['work'] and expected==o['expected_delivery']),'Orden liquidada: trabajo y entrega prevista bloqueados.');o['work']=work;o['expected_delivery']=expected
     total=money(d.get('total'));require(total>0,'Presupuesto positivo obligatorio.')
     if total!=o['total']:
      require(not o['settled'] and not closed(o),'No se puede modificar el presupuesto de una orden liquidada o cerrada.');agreement=text(d,'agreement',500)
      o['budget_history'].append({'at':at,'before':o['total'],'after':total,'actor':u['name'],'reason':reason,'agreement':agreement});o['total']=total
      excess=max(0,paid(o)-total)
      if excess:
       o['credit_issued']+=excess
       if not o.get('simulated'):c.db.execute('INSERT INTO order_credit VALUES(?,?) ON CONFLICT(phone) DO UPDATE SET amount=order_credit.amount+EXCLUDED.amount',(o['customer']['phone'],excess))
      if not o.get('simulated'):recognize(o,u,branch or o['branch'],at)
    o['history'].append({'at':at,'actor':u['name'],'from':o['status'],'to':o['status'],'note':'Corrección administrativa: '+reason,'before':{k:before[k] for k in ('customer','notes','total','work','expected_delivery')}})
   elif action=='state':
    require(u['role']=='admin','Solo el administrador puede cambiar estados.');require(o['kind']=='repair' and not closed(o),'Reparación no disponible.');target=d.get('status');require(target in ('received','in_repair','ready'),'Estado inválido.');require(target!=o['status'],'La orden ya tiene ese estado.');reason=text(d,'reason',500)
    previous=o['status'];o['status']=target
    if target=='in_repair':o['ever_in_repair']=True
    if target=='ready':o['ever_in_repair']=True;o['ready']=at;o['due']=(datetime.fromisoformat(at)+timedelta(days=o['term'])).date().isoformat()
    else:o['ready']=None;o['due']=None
    o['history'].append({'at':at,'actor':u['name'],'from':previous,'to':target,'note':reason})
   elif action=='deliver':
    require(branch in (1,2),'La entrega se registra desde el POS.');require(not closed(o) and not balance(o),'Liquida el saldo antes de entregar.');require(o['kind']=='layaway' or o['status']=='ready','La reparación todavía no está lista.');require(d.get('confirmed')is True,'Confirma la entrega del conjunto completo.')
    previous=o['status'];o['status']='delivered';o['delivery']={'at':at,'branch':branch,'actor':u['name'],'receipt':o['id']+'-ENT','signature':o['kind']=='repair'};o['history'].append({'at':at,'actor':u['name'],'from':previous,'to':'delivered','note':'Conjunto completo entregado.'});document(o,'Entrega',at)
   elif action=='release':
    require(u['role']=='admin','Liberación exclusiva del administrador.');require(o['kind']=='layaway' and not closed(o) and balance(o)>0 and o['due']<at[:10],'Solo se liberan apartados vencidos sin liquidar.');reason=text(d,'reason',500);stock(c,o['items'],1,o['id'],'Liberación de apartado vencido');previous=o['status'];o['status']='released';o['history'].append({'at':at,'actor':u['name'],'from':previous,'to':'released','note':reason+' · Sin devolución de efectivo.'});document(o,'Liberación autorizada',at)
   elif action=='cancel':
    require(u['role']=='admin' and branch in (1,2),'Cancelación comercial exclusiva del administrador desde POS.');require(not closed(o) and not o['settled'],'Orden cerrada o liquidada.')
    require((o['kind']=='layaway' and at[:10]<=(datetime.fromisoformat(o['created'])+timedelta(days=7)).date().isoformat()) or (o['kind']=='repair' and o['status']=='received' and not o['ever_in_repair']),'La orden ya no admite cancelación comercial.')
    session=cash_state([json.loads(r['body']) for r in c.events(branch) if r['status']=='accepted']);require(session,'Abre caja antes de cancelar por mercancía.');reason=text(d,'reason',500);items=product_items(c,d);total=sum(x['qty']*x['price'] for x in items);value=paid(o);require(total>=value,'La mercancía debe cubrir como mínimo lo pagado.')
    replacement={'id':o['id']+'-CAMBIO','kind':'layaway','branch':branch,'customer':o['customer'],'items':items,'total':total,'credit_issued':0,'payments':[{'amount':value}],'due':at[:10],'settled':None,'status':'pending','documents':[]}
    staff={s['id']:s['name'] for s in c.users() if s['active']};ids=d.get('sellers',[]);require(isinstance(ids,list) and ids and all(i in staff for i in ids),'Selecciona vendedores para la diferencia.');replacement['seller_ids']=list(dict.fromkeys(ids))
    if total>value:
     require(money(d.get('amount'))==total-value,'Cobra exactamente la diferencia.');payment(c,replacement,u,branch,d,at)
     p=replacement['payments'][-1];p['kind']='Diferencia de cancelación';o['conversion_payment']=p
    else:recognize(replacement,u,branch,at)
    if o['kind']=='layaway':stock(c,o['items'],1,o['id'],'Liberación por cancelación')
    stock(c,items,-1,o['id'],'Mercancía por cancelación')
    replacement['sale']['payload']['session']=session['id']
    o['replacement_sale']=replacement['sale'];o['replacement_sale']['order_id']=o['id'];o['replacement_sale']['payload']['sellers']=list(dict.fromkeys((o.get('seller_ids') or ['Matanga - sin asignación'])+ids));o['replacement_sale']['payload']['attributions']=[{'sellers':o.get('seller_ids') or ['Matanga - sin asignación'],'amount':value},{'sellers':ids,'amount':total-value}]
    previous=o['status'];o['status']='cancelled';o['conversion']={'items':items,'total':total,'applied':value,'difference':total-value,'sellers':ids};o['history'].append({'at':at,'actor':u['name'],'from':previous,'to':'cancelled','note':reason+' · Piezas devueltas/liberadas; importe pagado aplicado a mercancía, sin devolución de efectivo.'});document(o,'Cancelación',at)
   else:raise RuleError('Acción de orden desconocida.')
  o['revision']+=1;save(c,o);c.audit(u['id'],'order_'+action,{'order':o['id'],'branch':branch,'before':before,'after':o});result={'id':o['id'],'revision':o['revision']};c.db.execute('INSERT INTO order_requests VALUES(?,?,?)',(d['request_id'],digest,pack(result)));c.db.execute('COMMIT');return result
 except Exception:c.db.execute('ROLLBACK');raise


def collection_events(c):
 result=[]
 for p in movements(c):
  o=get(c,p['order']);index=next((i for i,d in enumerate(o['documents']) if any(x['id']==p['id'] for x in d['order']['payments'])),len(o['documents'])-1)
  result.append({'id':p['id'],'order_id':p['order'],'receipt_index':max(0,index),'kind':'order_payment','status':'accepted','branch':p['branch'],'at':p['at'],'actor_name':p['actor'],'actor':'','payload':{**p,'gross':0,'discount':0,'total':0,'items':[],'sellers':o.get('seller_ids',[])}})
 return result
