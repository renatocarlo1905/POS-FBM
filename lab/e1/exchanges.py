"""Online commercial exchanges. Original sales and closed sessions remain immutable."""
import copy,json,uuid,hashlib
from datetime import datetime,timedelta
from zoneinfo import ZoneInfo
from domain import require,now,pack,money,cleantext
from sales import calc_sale
from cash import cash_state
from extensions import transaction
TZ=ZoneInfo('America/Mexico_City')
def init(c):
 c.db.executescript('''CREATE TABLE IF NOT EXISTS merchandise_exchanges(id text PRIMARY KEY,digest text NOT NULL,body text NOT NULL);
 DROP TRIGGER IF EXISTS immutable_merchandise_exchanges ON merchandise_exchanges;
 CREATE TRIGGER immutable_merchandise_exchanges BEFORE UPDATE OR DELETE ON merchandise_exchanges FOR EACH ROW EXECUTE FUNCTION prevent_fact_change();''')
 roles=c.get('roles');changed=False
 for key,role in roles.items():
  if 'exchange' not in role['permissions']:role['permissions']['exchange']=key=='admin';changed=True
 if changed:c.put('roles',roles)
def documents(c):
 out=[]
 for row in c.db.execute('SELECT body FROM merchandise_exchanges'):
  d=json.loads(row[0]);d=__import__('folios').decorate(c,d)
  for key in ('out','return'):d[key]=__import__('folios').decorate(c,d[key])
  original=c.db.execute('SELECT body FROM events WHERE id=?',(d['target'],)).fetchone()
  target_event=json.loads(original[0]) if original else {'id':d['target'].removesuffix('-ENTREGA')}
  if d['target'].startswith('SIM-'):
   target_event=__import__('simulated').receipt(c,d['target']) or target_event
  d['target_code']=__import__('folios').code(__import__('folios').decorate(c,target_event))
  out.append(d)
 return out
def user(c,uid):
 u=next((u for u in c.get('users') if u['id']==uid),None);require(u and u['active'] and c.policy(u).get('exchange'),'Sin permiso para realizar cambios de mercancía.');return u

def source(c,target):
 import extensions
 found=next((e for d in documents(c) for e in [d['out']] if e['id']==target),None)
 if found:return copy.deepcopy(found)
 if isinstance(target,str) and target.startswith('SIM-') and c.db.execute("SELECT to_regclass('simulated_sales')").fetchone()[0]:
  fixture=__import__('simulated').receipt(c,target);require(fixture,'Venta inexistente.');return fixture
 v=extensions.sale_view(c,target);require(not v['adjusted'].get('cancelled'),'La venta fue anulada.');return {**v['original'],'payload':v['adjusted']}
def lookup(c,uid,q):
 user(c,uid);q=cleantext(q,100).lower();require(len(q)>=3,'Escribe al menos 3 caracteres del folio, fecha o vendedor.')
 rows=[json.loads(r['body']) for r in c.events() if r['status']=='accepted' and json.loads(r['body'])['kind']=='sale']
 rows += [d['out'] for d in documents(c)]
 if c.db.execute("SELECT to_regclass('simulated_sales')").fetchone()[0]:rows+=__import__('simulated').sales(c)
 for row in c.db.execute('SELECT document FROM corrections ORDER BY ordinal'):
  d=json.loads(row[0]);p=d['payload'];new=p.get('replacement')
  if new:rows.append({'id':new['id'],'at':p['original_at'],'branch':d['branch'],'actor_name':p['operator'],'payload':new})
 rows=[__import__('folios').decorate(c,e) for e in rows]
 exact=[e for e in rows if q==__import__('folios').code(e).lower()]
 if exact:rows=exact
 return [{'id':e['id'],'short_code':__import__('folios').code(e),'at':e['at'],'branch':e['branch'],'actor_name':e['actor_name'],'total':e['payload']['total']} for e in sorted(rows,key=lambda e:e['at'],reverse=True) if q in (__import__('folios').code(e)+' '+e['id']+' '+e['at']+' '+e['actor_name']).lower()][:40]
def view(c,uid,target):
 user(c,uid);e=source(c,target);used={}
 for d in documents(c):
  if d['target']==target:
   for x in d['returned']:used[x['id']]=used.get(x['id'],0)+x['qty']
 deadline=datetime.fromisoformat(e['at']).astimezone(TZ).date()+timedelta(days=15)
 return {'source':e,'remaining':{x['id']:x['qty']-used.get(x['id'],0) for x in e['payload']['items']},'used':used,'deadline':str(deadline)}
def split(amount,weights):
 total=sum(weights);out=[amount*w//total for w in weights] if total else [0]*len(weights)
 for i in sorted(range(len(weights)),key=lambda i:-(amount*weights[i]%total if total else 0))[:amount-sum(out)]:out[i]+=1
 return out

def preview(c,uid,branch,d):
 u=user(c,uid);require(branch in (1,2) and branch in u['branches'],'El cambio se registra desde una sucursal autorizada.')
 current=cash_state([json.loads(r['body']) for r in c.events(branch) if r['status']=='accepted']);require(current,'Abre una caja antes del cambio.');require(d.get('session')==current['id'],'La caja cambió; vuelve a abrir el formulario.')
 v=view(c,uid,d.get('target'));require(datetime.fromisoformat(now()).astimezone(TZ).date()<=datetime.fromisoformat(v['deadline']).date(),'El plazo de 15 días naturales terminó.')
 require(d.get('condition') is True,'Confirma el origen y buen estado de las piezas.');reason=cleantext(d.get('reason',''),500);require(reason,'Escribe el motivo del cambio.')
 returned=[];seen=set();orig=v['source']['payload'];parts={x['id']:x for x in orig['items']};alloc={}
 selections=d.get('returned',[]);require(isinstance(selections,list) and selections,'Selecciona las piezas que recibes.')
 for item in selections:
  pid=item.get('id');q=item.get('qty');x=parts.get(pid);require(x and pid not in seen and type(q)is int and 0<q<=v['remaining'][pid],'Cantidad devuelta inválida o ya cambiada.');seen.add(pid);used=v['used'].get(pid,0)
  portion=lambda n:n*(used+q)//x['qty']-n*used//x['qty']
  net=portion(x['net']);gross=x['price']*q
  returned.append({**x,'qty':q,'gross':gross,'net':net,'discount':gross-net})
  attributions=x.get('attributions') or [{'sellers':orig['sellers'],'amount':x['net']}]
  # Attribute disjoint cumulative cent ranges; repeated partial returns cannot duplicate cents.
  low=x['net']*used//x['qty'];high=low+net;offset=0
  for a in attributions:
   n=max(0,min(high,offset+a['amount'])-max(low,offset));offset+=a['amount']
   key=tuple(sorted(a['sellers']));alloc[key]=alloc.get(key,0)+n
 credit=sum(x['net'] for x in returned);require(credit>0,'El valor reconocido debe ser positivo.')
 catalog={x['id']:x for x in c.catalog(True)}
 for x in returned:
  if not x.get('non_inventory'):catalog[x['id']]['available']+=x['qty']
 raw=d.get('sale',{});cash=money(raw.get('cash',0));policy=c.policy(u)
 new=calc_sale({**raw,'cash':str((cash+credit)/100)},catalog,policy,c.get('categories',[]));require(new['total']>=credit,'La mercancía nueva debe valer igual o más que las piezas recibidas, después del descuento.')
 difference=new['total']-credit;require(new['card']+new['transfer']<=difference,'Los pagos electrónicos no pueden superar la diferencia.');require(cash+new['card']+new['transfer']==difference,'Error: ingresa el importe exacto de la diferencia.')
 require(all(x.get('non_inventory') or x['qty']<=catalog[x['id']]['available'] for x in new['items']),'Existencias insuficientes.')
 sellers=raw.get('sellers',[]);active={x['id'] for x in c.get('users') if x['active']};require(isinstance(sellers,list) and sellers and len(set(sellers))==len(sellers) and all(x in active for x in sellers),'Selecciona vendedores válidos.')
 attribution=[{'sellers':list(k),'amount':n} for k,n in alloc.items() if n]
 if difference:attribution.append({'sellers':sellers,'amount':difference})
 new.update(cash=difference-new['card']-new['transfer'],received_cash=cash,change=cash-(difference-new['card']-new['transfer']),sellers=sellers,attributions=attribution,session=current['id'])
 # Persist attribution per new unit group for a subsequent partial exchange.
 remaining=[a['amount'] for a in attribution]
 for i,x in enumerate(new['items']):
  values=remaining[:] if i==len(new['items'])-1 else split(x['net'],remaining)
  x['attributions']=[{'sellers':a['sellers'],'amount':n} for a,n in zip(attribution,values) if n]
  remaining=[r-n for r,n in zip(remaining,values)]
 return {'target':d['target'],'source_at':v['source']['at'],'branch':branch,'session':current['id'],'operator':uid,'actor_name':u['name'],'reason':reason,'returned':returned,'credit':credit,'difference':difference,'new':new,'return_attributions':[{'sellers':list(k),'amount':-n} for k,n in alloc.items() if n]}

@transaction
def confirm(c,uid,branch,d):
 user(c,uid);key=d.get('request_id')
 try:uuid.UUID(key)
 except (ValueError,TypeError,AttributeError):require(False,'Identificador de cambio inválido.')
 digest=hashlib.sha256(pack({'uid':uid,'branch':branch,'data':d}).encode()).hexdigest();old=c.db.execute('SELECT * FROM merchandise_exchanges WHERE id=?',(key,)).fetchone()
 if old:require(old['digest']==digest,'Identificador reutilizado con datos diferentes.');return next(x for x in documents(c) if x['id']=='CAM-'+key)
 p=preview(c,uid,branch,d);require(not d.get('preview_hash') or d['preview_hash']==hashlib.sha256(pack(p).encode()).hexdigest(),'El cambio se modificó; vuelve a consultar y comparar.');at=now();identifier='CAM-'+key
 import extensions
 for x in p['returned']:
  if not x.get('non_inventory'):extensions.add_stock(c,x['id'],'coyoacan',x['qty'],identifier,'Cambio: pieza recibida',at)
 for x in p['new']['items']:
  if not x.get('non_inventory'):extensions.add_stock(c,x['id'],'coyoacan',-x['qty'],identifier,'Cambio: pieza entregada',at)
 base={'kind':'sale','status':'accepted','at':at,'branch':branch,'actor':uid,'actor_name':p['actor_name'],'exchange_id':identifier,'template':c.get('templates')[str(branch)]}
 negative=[{**x,**{k:-x[k] for k in ('qty','gross','discount','net')}} for x in p['returned']]
 ret={'items':negative,'gross':sum(x['gross'] for x in negative),'discount':sum(x['discount'] for x in negative),'total':-p['credit'],'cash':0,'card':0,'transfer':0,'received_cash':0,'change':0,'sellers':source(c,d['target'])['payload']['sellers'],'attributions':p['return_attributions'],'session':p['session']}
 short_code=__import__('folios').allocate(c,identifier,branch,'C')
 doc={**p,'short_code':short_code,'id':identifier,'at':at,'out':{**base,'id':identifier+'-ENTREGA','payload':p['new']},'return':{**base,'id':identifier+'-RECEPCION','payload':ret},'template':base['template']}
 c.db.execute('INSERT INTO merchandise_exchanges VALUES(?,?,?)',(key,digest,pack(doc)));c.db.execute('INSERT INTO related_changes VALUES(?,?)',(d['target'],identifier));c.audit(uid,'merchandise_exchange',{'id':identifier,'target':d['target'],'difference':p['difference']});return next(x for x in documents(c) if x['id']==identifier)

def events(c):return [e for d in documents(c) for e in (d['return'],d['out'])]
def movements(c,branch):return [{'id':d['id'],'session':d['session'],'kind':'exchange','reason':'Cambio '+d.get('short_code',d['id']),'amount':d['new']['cash'],**{k:d['new'][k] for k in ('cash','card','transfer')},'at':d['at'],'actor':d['actor_name'],'difference':d['difference']} for d in documents(c) if d['branch']==branch]
def alerts(c):return [{'id':d['id'],'short_code':d.get('short_code',d['id']),'target_code':d['target_code'],'at':d['at'],'branch':d['branch'],'target':d['target'],'pieces':[x for x in d['returned'] if x.get('non_inventory')]} for d in documents(c) if any(x.get('non_inventory') for x in d['returned'])]
def receipt(c,key):
 d=next((d for d in documents(c) if key in (d['id'],d['out']['id'],d['return']['id'])),None);require(d,'Comprobante de cambio inexistente.')
 return {'id':d['id'],'short_code':d.get('short_code',d['id']),'kind':'exchange','at':d['at'],'branch':d['branch'],'actor_name':d['actor_name'],'payload':d,'template':d['template']}

def receipt_events(c,branch):
 return [{'id':d['id'],'short_code':d['short_code'],'kind':'exchange','status':'accepted','at':d['at'],'branch':d['branch'],'actor_name':d['actor_name'],'payload':{'total':d['difference'],'amount':d['difference'],'reason':'Diferencia cobrada · Origen '+d.get('target_code',d['target']),**{k:d['new'][k] for k in ('cash','card','transfer')}}} for d in documents(c) if d['branch']==branch]
