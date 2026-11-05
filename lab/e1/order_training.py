"""Explicit, one-time operational scenarios for the local laboratory."""
import copy,uuid
from datetime import datetime,timedelta
import order_service as orders
from domain import now,require
from extensions import transaction
KEY='operational-order-scenarios-v1'

@transaction
def prepare(c):
 previous=c.get(KEY)
 if previous:return previous
 admin=next(u for u in c.get('users') if u['id']=='carlo')
 products=[p for p in c.catalog(True) if p.get('active') and p['available']>=4 and p['price']>0]
 require(products,'Se necesita un producto con al menos cuatro unidades disponibles.')
 product=products[0];at=now();dt=datetime.fromisoformat(at)
 originals=[];result=[]
 cases=[('layaway','pending',.4,'Mariana Torres',1,'Anticipo'),('layaway','pending',.7,'Paola Aguilar',2,'Abonos'),('layaway','settled',1,'Lorena Campos',1,'Liquidado por entregar'),('layaway','pending',.4,'Verónica Duarte',2,'Vencido'),('repair','received',.5,'Elena Salazar',1,'Recibida'),('repair','in_repair',.5,'Alicia Robles',2,'En reparación'),('repair','ready',.5,'Diana Méndez',1,'Lista por liquidar'),('repair','ready',1,'Teresa Vidal',2,'Liquidada por entregar')]
 for i,(kind,status,ratio,name,branch,case) in enumerate(cases):
  source=next((o for o in orders.all_orders(c) if o.get('simulated') and o['customer']['name']==name),None) if i in (0,4) else None
  if source:originals.append(copy.deepcopy(source));branch=source['branch']
  ident=source['id'] if source else ('APA-' if kind=='layaway' else 'REP-')+uuid.uuid4().hex[:12].upper()
  created=(dt-timedelta(days=50 if case=='Vencido' else 2)).isoformat()
  total=product['price'] if kind=='layaway' else 80000
  o={'id':ident,'kind':kind,'status':status,'branch':branch,'created':created,'customer':{'name':name,'phone':f'55 0000 {301+i:04d}'},'payments':[],'history':[],'budget_history':[],'delivery':None,'settled':None,'ready':None,'term':45,'due':(datetime.fromisoformat(created)+timedelta(days=45)).date().isoformat() if kind=='layaway' else None,'work':'Ajuste de medida y revisión de engaste' if kind=='repair' else '', 'expected_delivery':(dt+timedelta(days=3)).date().isoformat() if kind=='repair' else None,'notes':'','sellers':[admin['name']] if kind=='layaway' else [],'seller_ids':[admin['id']] if kind=='layaway' else [],'ever_in_repair':status in ('in_repair','ready'),'credit_issued':0,'revision':(source.get('revision',0) if source else 0)+1,'simulated':False,'documents':[],'total':total,'training_scenario':case}
  if source and source.get('short_code'):o['short_code']=source['short_code']
  if kind=='layaway':
   o['items']=[{k:product[k] for k in ('id','name','code','price','cost')}|{'qty':1,'category':product.get('type','')}]
   orders.stock(c,o['items'],-1,ident,'Reserva de apartado')
  else:
   o['items']=[{'name':'Anillo con engaste flojo','qty':1}]
   o['budget_history']=[{'at':created,'before':None,'after':total,'actor':admin['name'],'reason':'Presupuesto inicial','agreement':'Presupuesto aceptado'}]
  if status=='ready':o['ready']=(dt-timedelta(days=1)).isoformat();o['due']=(dt+timedelta(days=45)).date().isoformat()
  o['history']=[{'at':created,'actor':admin['name'],'from':'—','to':status,'note':'Registro de la orden.'}]
  initial=round(total*(.4 if kind=='layaway' else .5));amounts=[initial]+([round(total*ratio)-initial] if ratio>(.4 if kind=='layaway' else .5) else [])
  for j,amount in enumerate(amounts):
   paid_at=created if j==0 else (dt-timedelta(days=1)).isoformat()
   p={'id':ident+'-P'+str(j+1),'kind':'Anticipo' if j==0 else 'Liquidación' if ratio==1 else 'Abono','at':paid_at,'branch':branch,'actor':admin['name'],'session':None,'amount':amount,'cash':amount,'received_cash':amount,'change':0,'card':0,'transfer':0,'credit':0,'bank':'','last4':'','reference':'','reason':'','method':'Efectivo'}
   o['payments'].append(p)
   orders.recognize(o,admin,branch,paid_at);orders.document(o,p['kind'],paid_at)
  orders.save(c,o);result.append({'id':ident,'name':name,'kind':kind,'case':case,'branch':branch,'balance':orders.balance(o)})
 c.put(KEY+'-originals',originals);c.put(KEY,result);c.audit('carlo','training_orders_prepared',{'orders':result,'source_backup':KEY+'-originals'})
 return result
