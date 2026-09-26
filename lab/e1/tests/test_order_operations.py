import copy,json,sys,unittest,uuid,io
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import test_e1
Lab=test_e1.Lab
from core import RuleError,cash_state
import order_service as orders
import extensions,cash_reports,orders_preview
from pypdf import PdfReader
class Orders(unittest.TestCase):
 setUpClass=classmethod(Lab.setUpClass.__func__);tearDownClass=classmethod(Lab.tearDownClass.__func__)
 op=Lab.op;opening=Lab.opening;tearDown=Lab.tearDown
 def setUp(self):
  test_e1.Lab.setUp(self);cash_reports.init(self.c);self.c.db.execute('TRUNCATE service_orders,order_requests,order_credit');self.opening();self.admin=next(u for u in self.c.get('users') if u['id']=='carlo');self.staff=next(u for u in self.c.get('users') if u['id']=='melissa')
 def runorder(self,data,user=None,branch=1):
  with self.c.lock:return orders.execute(self.c,user or self.admin,branch,{'request_id':str(uuid.uuid4()),**data})
 def create(self,kind='layaway',**kw):
  d={'action':'create','kind':kind,'name':'Cliente de prueba','phone':'5551234567','items':[{'id':'p1','qty':1}],'sellers':['melissa'],'amount':'400','cash':'400','pieces':['Anillo del cliente'],'total':'800','work':'Soldar','expected_delivery':'2026-12-31','agreement':'Aceptado','notes':''};d.update(kw);r=self.runorder(d);return orders.get(self.c,r['id'])
 def test_layaway_cross_branch_cash_and_immutable_receipts(self):
  o=self.create();self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p1')['available'],7);self.assertEqual(orders.adjustments(self.c,1)[self.a.operations()[0]['id']],40000)
  self.runorder({'action':'pay','id':o['id'],'revision':1,'amount':'600','cash':'600'},self.staff,2);o=orders.get(self.c,o['id']);self.assertEqual(o['status'],'settled');self.assertEqual(o['sale']['branch'],2);self.assertEqual(len(orders.sale_events(self.c)),1)
  self.runorder({'action':'deliver','id':o['id'],'revision':2,'confirmed':True},self.staff,1);o=orders.get(self.c,o['id']);self.assertEqual(o['status'],'delivered');self.assertEqual(len(o['documents']),3)
  old=o['documents'][0]['order']['customer']['name'];self.runorder({'action':'edit','id':o['id'],'revision':3,'name':'Nombre corregido','phone':'5551234567','notes':'','reason':'Ortografía'},branch=0);self.assertEqual(orders.get(self.c,o['id'])['documents'][0]['order']['customer']['name'],old)
  self.a.sync('carlo');self.op(self.a,self.ta,'close',{'counted':'900','fund':'500','envelope':'400'});self.assertEqual(self.a.rows()[-1]['status'],'accepted')
  rows=cash_reports.report(self.c);closed=next(r for r in rows if r['branch']==1);self.assertEqual(closed['expected'],90000)
 def test_repair_budget_credit_and_delivery(self):
  o=self.create('repair',amount='400',cash='400');self.assertEqual(len(PdfReader(io.BytesIO(orders_preview.receipt_pdf(o['id'],0,o['documents'][0]['order'])[0])).pages),3)
  with self.assertRaises(RuleError):self.runorder({'action':'pay','id':o['id'],'revision':1,'amount':'100','cash':'100'},self.staff)
  self.runorder({'action':'edit','id':o['id'],'revision':1,'name':'Cliente de prueba','phone':'5551234567','notes':'','reason':'Trabajo más sencillo','agreement':'Aceptado','work':'Soldar','expected_delivery':'2026-12-31','total':'300'},branch=0)
  o=orders.get(self.c,o['id']);self.assertEqual(orders.balance(o),0);self.assertEqual(o['credit_issued'],10000);self.assertEqual(self.c.db.execute('SELECT amount FROM order_credit').fetchone()[0],10000)
  self.runorder({'action':'state','id':o['id'],'revision':2,'status':'ready','reason':'Trabajo terminado'},branch=0)
  self.runorder({'action':'deliver','id':o['id'],'revision':3,'confirmed':True},self.staff,2)
 def test_atomic_rollback_permissions_and_conflict(self):
  with self.assertRaises(RuleError):self.create(amount='399',cash='399')
  self.assertEqual(len(orders.all_orders(self.c)),0);self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p1')['available'],8)
  o=self.create()
  d={'action':'edit','id':o['id'],'revision':1,'name':'Cambio','phone':'5551234567','reason':'x','notes':''}
  with self.assertRaises(RuleError):self.runorder(d,self.staff)
  self.runorder(d)
  with self.assertRaises(RuleError):self.runorder(d)
 def test_idempotency_and_cancel_conversion(self):
  o=self.create();req={'request_id':str(uuid.uuid4()),'action':'pay','id':o['id'],'revision':1,'amount':'100','cash':'100'}
  self.runorder(req);self.runorder(req);self.assertEqual(len(orders.get(self.c,o['id'])['payments']),2)
  self.runorder({'action':'cancel','id':o['id'],'revision':2,'items':[{'id':'p3','qty':1}],'amount':'150','cash':'150','sellers':['ximena'],'reason':'Cliente cambia de pieza'})
  o=orders.get(self.c,o['id']);self.assertEqual(o['status'],'cancelled');self.assertEqual(sum(p['cash'] for p in orders.movements(self.c)),65000);self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p1')['available'],8);self.assertEqual(o['replacement_sale']['payload']['total'],65000)
 def test_repair_cannot_cancel_after_reversal(self):
  o=self.create('repair');self.runorder({'action':'state','id':o['id'],'revision':1,'status':'in_repair','reason':'Iniciar'})
  self.runorder({'action':'state','id':o['id'],'revision':2,'status':'received','reason':'Corregir'})
  with self.assertRaises(RuleError):self.runorder({'action':'cancel','id':o['id'],'revision':3,'items':[{'id':'p3','qty':1}],'amount':'250','cash':'250','sellers':['carlo'],'reason':'Cancelar'})
 def test_http_permissions_offline_and_pdf(self):
  import urllib.request,urllib.error,server
  self.c.db.execute('TRUNCATE events')
  app=server.Application(self.root/'http',8980,self.config);app.start()
  def call(branch,path,data=None,token=''):
   req=urllib.request.Request(f'http://127.0.0.1:{8980+branch}/api/'+path,data=json.dumps(data).encode() if data is not None else None,headers={'Content-Type':'application/json','Authorization':'Bearer '+token})
   with urllib.request.urlopen(req) as r:return json.load(r)
  try:
   t=call(1,'login',{'user':'melissa','password':'Melissa-E1-2026!'})['token'];admin=call(0,'login',{'user':'carlo','password':'Carlo-E1-2026!'})['token']
   call(1,'operation',{'kind':'open','data':{'opening':'500'},'request_id':str(uuid.uuid4())},t)
   d={'action':'create','kind':'repair','name':'Cliente HTTP','phone':'5551231234','pieces':['Cadena de prueba'],'total':'800','work':'Soldar','expected_delivery':'2026-12-31','agreement':'Aceptado','amount':'400','cash':'400','request_id':str(uuid.uuid4())}
   result=call(1,'order-write',d,t);self.assertEqual(call(1,'order-write',d,t),result)
   data=call(0,'orders',token=admin);o=next(o for o in data['rows'] if o['id']==result['id']);self.assertEqual(o['total'],80000)
   edit={'action':'edit','id':o['id'],'revision':1,'name':'Corregido','phone':'5551231234','notes':'','reason':'Prueba','work':'Soldar','expected_delivery':'2026-12-31','total':'800','request_id':str(uuid.uuid4())}
   with self.assertRaises(urllib.error.HTTPError):call(1,'order-write',edit,t)
   call(0,'order-write',edit,admin)
   self.assertEqual(next(o for o in call(1,'orders',token=t)['rows'] if o['id']==result['id'])['customer']['name'],'Corregido')
   preview=call(0,'order-pdf',{'id':o['id'],'index':0,'preview_window':True},admin)
   self.assertEqual(len(preview['pages']),3)
   self.assertTrue(all(p['src'].startswith('data:image/png;base64,') for p in preview['pages']))
   self.assertAlmostEqual(preview['pages'][0]['width'],80,delta=.1)
   with self.assertRaises(urllib.error.HTTPError):call(0,'order-pdf',{'id':o['id'],'index':0,'preview_window':True})
   url=call(0,'order-pdf',{'id':o['id'],'index':0,'download':True},admin)['url']
   with urllib.request.urlopen('http://127.0.0.1:8980'+url) as r:
    body=r.read();self.assertIn('attachment',r.headers['Content-Disposition']);self.assertEqual(len(PdfReader(io.BytesIO(body)).pages),3)
   (self.root/'receipt.pdf').write_bytes(body)
   call(1,'offline',{'offline':True},t)
   with self.assertRaises(urllib.error.HTTPError):call(1,'order-write',{**d,'request_id':str(uuid.uuid4())},t)
   self.assertEqual(len(orders.all_orders(self.c)),1)
  finally:app.stop()
 def test_settings_and_expired_release(self):
  o=self.create();self.runorder({'action':'settings','layaway_days':30,'repair_days':20},branch=0);new=self.create('repair')
  self.assertEqual(orders.get(self.c,o['id'])['term'],45);self.assertEqual(new['term'],20)
  o['due']='2026-01-01';orders.save(self.c,o)
  with self.assertRaises(RuleError):self.runorder({'action':'pay','id':o['id'],'revision':1,'amount':'100','cash':'100'},self.staff)
  self.runorder({'action':'release','id':o['id'],'revision':1,'reason':'Plazo agotado'},branch=0)
  self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p1')['available'],8)
 def test_cancel_reuses_last_reserved_piece(self):
  self.c.db.execute("UPDATE stock SET available=1 WHERE id='p1'");o=self.create()
  with self.assertRaises(RuleError):self.create()
  self.runorder({'action':'cancel','id':o['id'],'revision':1,'items':[{'id':'p1','qty':1}],'amount':'600','cash':'600','sellers':['carlo'],'reason':'Compra inmediata por conversión'})
  self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p1')['available'],0)
  self.assertEqual(len(orders.all_orders(self.c)),1)
del Lab
if __name__=='__main__':unittest.main()
