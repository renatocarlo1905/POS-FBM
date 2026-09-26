import copy, json, shutil, sqlite3, subprocess, sys, tempfile, unittest, uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from core import Central, Store, RuleError, calc_sale, template, receipt_pdf, cash_state, pack
from pypdf import PdfReader
import io
ROOT=Path(__file__).resolve().parents[1]

def admin_sql(sql):
 return subprocess.run(['docker','exec','-i','pos-frida-e1-postgres','psql','-X','-v','ON_ERROR_STOP=1','-U','pos_e1_admin','-d','postgres','-At'],input=sql,text=True,capture_output=True,check=True).stdout.strip()
class Lab(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.temp=tempfile.TemporaryDirectory();cls.root=Path(cls.temp.name);cls.name='e1_test_'+uuid.uuid4().hex[:10]
  admin_sql(f'CREATE DATABASE {cls.name} OWNER pos_e1_app;')
  cfg=json.loads((ROOT/'data/postgres.json').read_text());cfg['dbname']=cls.name
  cls.config=cls.root/'postgres.json';cls.config.write_text(json.dumps(cfg))
 @classmethod
 def tearDownClass(cls):
  admin_sql(f'DROP DATABASE {cls.name} WITH (FORCE);');cls.temp.cleanup()
 def setUp(self):
  self.c=Central(self.config)
  self.c.db.execute('TRUNCATE corrections,related_changes,stock_ledger,inventory_entries,warehouse_stock,products,events,stock,audit,kv RESTART IDENTITY');self.c.db.close();self.c=Central(self.config)
  self.path=self.root/uuid.uuid4().hex;self.stores=[]
  def transport(action,d):
   if action=='login':return self.c.login(d['user'],d['password'],d['branch'])
   if action=='pull':return self.c.pull(d['grant'])
   return self.c.receive(d)
  self.transport=transport
  self.a=Store(self.path/'s1.sqlite3',1,transport,self.path/'copy');self.b=Store(self.path/'s2.sqlite3',2,transport,self.path/'copy');self.stores=[self.a,self.b]
  self.ta=self.a.login('carlo','Carlo-E1-2026!')['token'];self.tb=self.b.login('melissa','Melissa-E1-2026!')['token']
 def tearDown(self):
  for s in self.stores:s.db.close()
  self.c.db.close()
 def op(self,s,t,k,d):return s.submit(t,k,d,str(uuid.uuid4()))
 def sale(self,s,t,id='p1',qty=1,**extra):
  price={p[0]:p[3] for p in __import__('core').PRODUCTS}[id]
  return self.op(s,t,'sale',{'items':[{'id':id,'qty':qty}],'cash':str(price*qty/100),**extra})
 def opening(self):
  self.op(self.a,self.ta,'open',{'opening':'500'});self.op(self.b,self.tb,'open',{'opening':'500'})
 def test_01_postgres_shared_stock_and_money(self):
  self.assertIn('PostgreSQL',self.c.db.execute('SELECT version()').fetchone()[0]);self.opening()
  self.sale(self.a,self.ta,cash='500',card='600',bank='Prueba',last4='1234')
  self.sale(self.b,self.tb)
  self.assertEqual(self.c.catalog()[0]['available'],6)
  e=json.loads(self.a.rows()[-1]['body']);self.assertEqual((e['payload']['cash'],e['payload']['change']),(40000,10000))
  self.assertEqual(cash_state(self.a.operations())['expected'],90000)
 def test_02_offline_last_unit_keeps_two_sales(self):
  self.opening();self.a.put('offline',True);self.b.put('offline',True)
  self.sale(self.a,self.ta,'p5');self.sale(self.b,self.tb,'p5')
  with self.assertRaises(RuleError):self.sale(self.a,self.ta,'p5')
  for s,u in [(self.a,'carlo'),(self.b,'melissa')]:s.put('offline',False);s.sync(u)
  self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p5')['available'],-1)
  self.assertIn('negativa',self.b.rows()[-1]['issue'])
 def test_03_lost_ack_restart_and_uuid_conflict(self):
  self.opening();original=self.a.transport;first=True
  def lost(action,d):
   nonlocal first
   result=original(action,d)
   if action=='receive' and first:first=False;raise ConnectionError('Acuse perdido')
   return result
  self.a.transport=lost;self.sale(self.a,self.ta);row=self.a.rows()[-1];self.assertEqual(row['status'],'pending')
  self.assertEqual(self.a.available()['p1']['available'],7)
  self.a.db.close();self.stores.remove(self.a);self.a=Store(self.path/'s1.sqlite3',1,original,self.path/'copy');self.stores.append(self.a)
  t=self.a.login('carlo','Carlo-E1-2026!')['token'];self.assertEqual(self.a.rows()[-1]['status'],'accepted');self.assertEqual(self.c.catalog()[0]['available'],7)
  event=json.loads(row['body']);self.assertTrue(self.c.receive(event)['duplicate']);event['payload']['total']+=1
  with self.assertRaises(RuleError):self.c.receive(event)
 def test_04_ack_and_snapshot_are_atomic(self):
  self.opening();self.a.put('offline',True);self.sale(self.a,self.ta);self.a.put('offline',False);old=self.a.transport
  def failed_pull(action,d):
   if action=='pull':raise ConnectionError('Sin snapshot')
   return old(action,d)
  self.a.transport=failed_pull
  with self.assertRaises(ConnectionError):self.a.sync('carlo')
  self.assertEqual(self.a.rows()[-1]['status'],'pending');self.assertEqual(self.a.available()['p1']['available'],7)
  self.a.transport=old;self.a.sync('carlo');self.assertEqual(self.a.available()['p1']['available'],7)
 def test_05_permissions_discount_and_last_downloaded(self):
  self.opening()
  with self.assertRaises(RuleError):self.sale(self.b,self.tb,discount='10')
  self.c.edit_role('carlo',{'id':'sales','name':'Personal de venta','permissions':{'sell':True,'discount':True,'cash_open':True,'cash_close':True,'receipts':True,'reprint':True},'max_discount':'10'})
  with self.assertRaises(RuleError):self.b.state(self.tb)
  self.tb=self.b.login('melissa','Melissa-E1-2026!')['token'];self.b.put('offline',True)
  self.c.edit_role('carlo',{'id':'sales','name':'Personal de venta','permissions':{'sell':True},'max_discount':'0'})
  with self.assertRaises(RuleError):self.sale(self.b,self.tb,discount='10.01')
  self.sale(self.b,self.tb,discount='10',cash='900')
  self.b.put('offline',False)
  with self.assertRaises(RuleError):self.b.sync('melissa')
  self.assertEqual(self.b.rows()[-1]['status'],'accepted');self.assertIn('anteriormente',self.b.rows()[-1]['issue'])
  self.tb=self.b.login('melissa','Melissa-E1-2026!')['token']
  with self.assertRaises(RuleError):self.sale(self.b,self.tb,discount='1')
 def test_06_edit_password_and_admin_protection(self):
  u=next(x for x in self.c.users() if x['id']=='ximena');u['password']='Nueva-clave-E1!';u['role']='admin';self.c.edit_user('carlo',u)
  with self.assertRaises(RuleError):self.c.login('ximena','Ximena-E1-2026!',0)
  result=self.c.login('ximena','Nueva-clave-E1!',0);self.assertTrue(self.c.auth(result['token'],True))
  self.assertNotIn('password',self.c.users()[0]);u=next(x for x in self.c.users() if x['id']=='carlo');u['role']='sales'
  with self.assertRaises(RuleError):self.c.edit_user('carlo',u)
  with self.assertRaises(RuleError):self.c.login('melissa','Melissa-E1-2026!',0)
 def test_07_cash_blind_close_and_distribution(self):
  self.opening();self.sale(self.a,self.ta,cash='500',card='600',bank='Demo',last4='1234')
  self.assertNotIn('expected',self.a.state(self.ta)['session'])
  with self.assertRaises(RuleError):self.op(self.a,self.ta,'close',{'counted':'880','fund':'500','envelope':'300'})
  self.op(self.a,self.ta,'close',{'counted':'880','fund':'500','envelope':'380'})
  p=self.a.operations()[-1]['payload'];self.assertEqual(p['difference'],-2000)
  with self.assertRaises(RuleError):self.sale(self.a,self.ta)
 def test_08_copy_failure_does_not_block(self):
  self.opening();self.a.copy_dir=self.path/'not-directory';self.a.copy_dir.write_text('failure')
  self.a.put('offline',True);self.sale(self.a,self.ta);self.assertFalse(self.a.get('copy_status')['ok']);self.assertEqual(self.a.rows()[-1]['status'],'pending')
 def test_09_independent_copy_restores_pending(self):
  self.opening();self.a.put('offline',True);self.sale(self.a,self.ta)
  restored=self.path/'recovered.sqlite3';shutil.copy2(self.path/'copy/sucursal-1.sqlite3',restored)
  recovered=Store(restored,1,self.transport,self.path/'recovered-copy');self.stores.append(recovered)
  recovered.put('offline',False);recovered.login('carlo','Carlo-E1-2026!');self.assertEqual(recovered.rows()[-1]['status'],'accepted');self.assertEqual(self.c.catalog()[0]['available'],7)
 def test_10_postgres_backup_restore(self):
  self.opening();self.sale(self.a,self.ta);path=self.path/'central.dump';self.c.backup(path)
  name='e1_restore_'+uuid.uuid4().hex[:8];admin_sql(f'CREATE DATABASE {name} OWNER pos_e1_app;')
  try:
   with path.open('rb') as stream:subprocess.run(['docker','exec','-i','pos-frida-e1-postgres','pg_restore','-U','pos_e1_admin','-d',name,'--exit-on-error'],stdin=stream,check=True,capture_output=True)
   result=subprocess.run(['docker','exec','pos-frida-e1-postgres','psql','-U','pos_e1_admin','-d',name,'-At','-c',"SELECT available FROM stock WHERE id='p1'"],capture_output=True,text=True,check=True)
   self.assertEqual(result.stdout.strip(),'7')
  finally:admin_sql(f'DROP DATABASE {name} WITH (FORCE);')
 def test_11_pdf_snapshot_and_wrapping(self):
  self.opening();self.sale(self.a,self.ta,discount='10',cash='900');e=self.a.operations()[-1]
  old=receipt_pdf(e,True);self.c.put('templates',{'1':template({'header':'CAMBIO NUEVO'}),'2':template({})})
  self.assertIn('FRIDA',PdfReader(io.BytesIO(old)).pages[0].extract_text());self.assertNotIn('CAMBIO NUEVO',PdfReader(io.BytesIO(receipt_pdf(e))).pages[0].extract_text())
  e['template']=template({'header':'FRIDA BLANCAS MÉXICO\nSucursal 1 · Coyoacán','footer':'Gracias por tu visita.\nComprobante de prueba.','width':58})
  target=ROOT.parents[1]/'output/pdf/Ticket_prueba_E1.pdf';target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(receipt_pdf(e,True))
  self.assertIn('$900.00',PdfReader(target).pages[0].extract_text())
 def test_12_concurrent_online_last_unit(self):
  self.opening();self.a.put('offline',True);self.b.put('offline',True);self.sale(self.a,self.ta,'p5');self.sale(self.b,self.tb,'p5')
  ea=self.a.operations()[-1];eb=self.b.operations()[-1];ea['offline']=False;eb['offline']=False
  # Two connections contend on PostgreSQL's transaction advisory lock.
  c2=Central(self.config)
  try:
   with ThreadPoolExecutor(2) as pool:results=list(pool.map(lambda v:v[0].receive(v[1]),[(self.c,ea),(c2,eb)]))
   self.assertEqual(sorted(r['status'] for r in results),['accepted','rejected']);self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p5')['available'],0)
  finally:c2.db.close()
 def test_13_http_boundaries_and_pdf(self):
  import urllib.request, urllib.error
  from server import Application
  app=Application(self.path/'http',18870,self.config);app.start()
  def call(port,path,data=None,token=''):
   req=urllib.request.Request(f'http://127.0.0.1:{port}/api/{path}',headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'},data=json.dumps(data).encode() if data is not None else None)
   with urllib.request.urlopen(req) as r:return r.read(),r.headers.get('Content-Type')
  try:
   with self.assertRaises(urllib.error.HTTPError):call(18870,'state')
   t=json.loads(call(18871,'login',{'user':'melissa','password':'Melissa-E1-2026!'})[0])['token']
   with self.assertRaises(urllib.error.HTTPError):call(18870,'employee',{'id':'melissa','role':'admin'},t)
   state=json.loads(call(18871,'state',token=t)[0]);self.assertNotIn('cost',state['catalog'][0]);self.assertNotIn('verifier',state)
   with self.assertRaises(urllib.error.HTTPError):call(18871,'operation',{'kind':'move','data':{'amount':'1','type':'Entrada','reason':'denegado'},'request_id':str(uuid.uuid4())},t)
   call(18871,'operation',{'kind':'open','data':{'opening':'500'},'request_id':str(uuid.uuid4())},t)
   id=str(uuid.uuid4());d={'kind':'sale','data':{'items':[{'id':'p1','qty':1}],'cash':'1000'},'request_id':id}
   call(18871,'operation',d,t);call(18871,'operation',d,t)
   pdf,mime=call(18871,'pdf',{'id':id},t);self.assertEqual(mime,'application/pdf');self.assertTrue(pdf.startswith(b'%PDF'))
   self.assertNotIn('COPIA / REIMPRESIÓN',PdfReader(io.BytesIO(pdf)).pages[0].extract_text())
   url=json.loads(call(18871,'pdf',{'id':id,'download':True},t)[0])['url']
   with urllib.request.urlopen('http://127.0.0.1:18871'+url) as response:self.assertTrue(response.read().startswith(b'%PDF'))
   with self.assertRaises(urllib.error.HTTPError):urllib.request.urlopen('http://127.0.0.1:18871'+url)
   pdf,_=call(18871,'pdf',{'id':id},t);self.assertIn('COPIA / REIMPRESIÓN',PdfReader(io.BytesIO(pdf)).pages[0].extract_text())
   self.assertEqual(len([e for e in self.c.events() if json.loads(e['body'])['kind']=='sale']),1)
   app.central.edit_role('carlo',{'id':'sales','name':'Sin comprobantes','permissions':{'sell':True,'reprint':True},'max_discount':'0'})
   t=json.loads(call(18871,'login',{'user':'melissa','password':'Melissa-E1-2026!'})[0])['token']
   state=json.loads(call(18871,'state',token=t)[0]);self.assertEqual(state['operations'],[]);self.assertEqual(state['corrections'],[])
   with self.assertRaises(urllib.error.HTTPError):call(18871,'pdf',{'id':id},t)
  finally:app.stop()
 def test_14_rounding_forgery_and_order(self):
  self.opening();self.a.put('offline',True);self.sale(self.a,self.ta,discount='12.34')
  e=self.a.operations()[-1];e['seq']+=1
  with self.assertRaises(RuleError):self.c.receive(e)
  e['seq']-=1;e['payload']['total']+=1
  with self.assertRaises(RuleError):self.c.receive(e)
  e['grant']=e['grant'][:-2]+'xx'
  with self.assertRaises(RuleError):self.c.receive(e)
  result=calc_sale({'items':[{'id':'p1','qty':1},{'id':'p2','qty':1}],'discount':'33.33','cash':'10000'},{p['id']:p for p in self.c.catalog()},{'sell':True,'discount':True,'max_discount':10000})
  self.assertEqual(sum(x['discount'] for x in result['items']),result['discount'])
  self.assertEqual(sum(x['net'] for x in result['items']),result['total'])
 def correction(self,action,target,**values):
  from extensions import sale_view
  return {'request_id':str(uuid.uuid4()),'target':target,'action':action,'reason':'Error de captura de prueba','revision':sale_view(self.c,target)['revision'],**values}
 def test_15_manual_product_and_ingress(self):
  import extensions as x
  p=x.provider(self.c,'carlo',{'name':'Artesano de prueba'})
  d={'request_id':str(uuid.uuid4()),'name':'Anillo nuevo','description':'Anillo artesanal nuevo','material_id':'1','type_id':'1','provider':p['id'],'price':'1234.56','cost':'500','weight':'2.400','quantity':3,'warehouse':'coyoacan'}
  r=x.create_product(self.c,'carlo',d);code=r['product']['code'];self.assertEqual(len(code),15);self.assertEqual(code[4:10],'002400');self.assertEqual(x.create_product(self.c,'carlo',d)['product']['id'],r['product']['id'])
  self.assertEqual(next(v for v in self.c.catalog() if v['code']==code)['available'],3)
  self.a.sync('carlo');self.op(self.a,self.ta,'open',{'opening':'500'});self.op(self.a,self.ta,'sale',{'items':[{'id':r['product']['id'],'qty':1}],'cash':'1234.56'})
  x.ingress(self.c,'carlo',{'request_id':str(uuid.uuid4()),'product':r['product']['id'],'quantity':2,'warehouse':'oficina','reason':'Recepción'})
  v=next(v for v in self.c.catalog(True) if v['code']==code);self.assertEqual((v['available'],v['warehouses']['oficina']),(2,2))
  bad={**d,'request_id':str(uuid.uuid4()),'weight':'999.001'}
  with self.assertRaises(RuleError):x.create_product(self.c,'carlo',bad)
 def test_16_payment_correction_preserves_close_and_original(self):
  import extensions as x
  self.opening();id=self.sale(self.a,self.ta)['id'];original=self.c.db.execute('SELECT body FROM events WHERE id=?',(id,)).fetchone()[0]
  self.op(self.a,self.ta,'close',{'counted':'1500','fund':'500','envelope':'1000'})
  d=self.correction('payment',id,cash='0',card='1000',bank='Demo',last4='1234',transfer='0');doc=x.correct(self.c,'carlo',0,d)
  v=x.sale_view(self.c,id);self.assertEqual(v['adjusted']['cash'],0);self.assertEqual(v['close']['payload']['expected'],150000);self.assertEqual(v['close_adjustment'],-100000);self.assertEqual(self.c.db.execute('SELECT body FROM events WHERE id=?',(id,)).fetchone()[0],original)
  self.assertEqual(x.correct(self.c,'carlo',0,d)['id'],doc['id']);self.assertEqual(len(v['history']),1)
  self.assertEqual(self.c.catalog()[0]['available'],7)
 def test_17_cancel_once_and_linked_exchange_block(self):
  import extensions as x
  self.opening();id=self.sale(self.a,self.ta)['id'];d=self.correction('cancel',id)
  self.c.db.execute('INSERT INTO related_changes VALUES(?,?)',(id,'CAM-TEST'))
  with self.assertRaises(RuleError):x.correct(self.c,'carlo',0,d)
  self.c.db.execute('DELETE FROM related_changes WHERE sale=?',(id,));x.correct(self.c,'carlo',0,d)
  self.assertEqual(self.c.catalog()[0]['available'],8)
  with self.assertRaises(RuleError):x.correct(self.c,'carlo',0,self.correction('cancel',id))
  self.assertTrue(x.sale_view(self.c,id)['adjusted']['cancelled'])
 def test_18_sellers_and_authorizer(self):
  import extensions as x
  self.opening();id=self.sale(self.b,self.tb)['id'];d=self.correction('sellers',id,sellers=['melissa','ximena'])
  with self.assertRaises(RuleError):x.correct(self.c,'melissa',2,d)
  d.update(authorizer='carlo',authorization_password='Carlo-E1-2026!');r=x.correct(self.c,'melissa',2,d)
  self.assertEqual((r['payload']['operator'],r['payload']['authorizer']),('melissa','carlo'));self.assertEqual(x.sale_view(self.c,id)['adjusted']['sellers'],['melissa','ximena'])
  self.assertNotIn('authorization_password',pack(r));self.assertEqual(x.cash_adjustments(self.c,2)[r['payload']['session']],0)
 def test_19_replacement_chain_atomic_and_stock(self):
  import extensions as x
  self.opening();id=self.sale(self.a,self.ta)['id'];d=self.correction('replace',id,replacement={'items':[{'id':'p2','qty':1}],'cash':'780','sellers':['carlo']})
  r=x.correct(self.c,'carlo',0,d);rid=r['payload']['replacement']['id'];self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p1')['available'],8);self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p2')['available'],11)
  self.assertEqual(x.sale_view(self.c,rid)['adjusted']['total'],78000)
  x.correct(self.c,'carlo',0,self.correction('cancel',rid));self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p2')['available'],12)
  self.assertEqual(x.cash_adjustments(self.c,1)[r['payload']['session']],-100000)
 def test_20_correction_race_permissions_immutability_and_brand(self):
  import extensions as x
  self.opening();id=self.sale(self.a,self.ta)['id'];d=self.correction('sellers',id,sellers=['carlo']);x.correct(self.c,'carlo',0,d)
  stale={**d,'request_id':str(uuid.uuid4())}
  with self.assertRaises(RuleError):x.correct(self.c,'carlo',0,stale)
  with self.assertRaises(Exception):self.c.db.execute('UPDATE events SET body=? WHERE id=?',('{}',id))
  self.assertTrue(self.c.get('templates')['1']['logo'].startswith('data:image/png;base64,'))
  e=self.a.operations()[-1];path=ROOT.parents[1]/'output/pdf/Ticket_prueba_E1.pdf';path.write_bytes(receipt_pdf(e));self.assertTrue(PdfReader(path).pages[0].images)
  cdoc=x.correct(self.c,'carlo',1,self.correction('payment',id,cash='0',card='1000',bank='Banco demo',last4='1234',transfer='0'))
  target=ROOT.parents[1]/'output/pdf/Correccion_prueba_E1.pdf';target.write_bytes(receipt_pdf(cdoc));text=PdfReader(target).pages[0].extract_text();self.assertIn('CORRECCIÓN',text);self.assertIn('Error de captura',text)
 def test_21_two_corrections_adjust_current_and_historical_cash(self):
  import extensions as x
  self.opening();a=self.sale(self.a,self.ta)['id'];b=self.sale(self.a,self.ta,'p2')['id']
  x.correct(self.c,'carlo',0,self.correction('payment',a,cash='0',card='1000',bank='Demo',last4='1234',transfer='0'))
  self.op(self.a,self.ta,'close',{'counted':'1280','fund':'500','envelope':'780'})
  x.correct(self.c,'carlo',0,self.correction('payment',b,cash='0',card='780',bank='Demo',last4='1234',transfer='0'))
  v=x.sale_view(self.c,a);self.assertEqual(v['close']['payload']['expected'],128000);self.assertEqual(v['close_adjustment'],-78000)
  self.op(self.a,self.ta,'open',{'opening':'500'});self.op(self.a,self.ta,'close',{'counted':'500','fund':'500','envelope':'0'});self.assertEqual(self.a.operations()[-1]['payload']['difference'],0)
 def test_23_only_one_cash_session_per_branch(self):
  self.opening()
  for store,token in [(self.a,self.ta),(self.b,self.tb)]:
   with self.assertRaises(RuleError):self.op(store,token,'open',{'opening':'100'})
   self.assertEqual(len([e for e in store.operations() if e['kind']=='open']),1)
 def test_22_exact_amount_discount_and_seller_codes(self):
  products={p['id']:p for p in self.c.catalog()};policy={'sell':True,'discount':True,'max_discount':4000}
  d={'items':[{'id':'p1','qty':1},{'id':'p2','qty':1}],'discount_amount':'259.16','cash':'2000'}
  result=calc_sale(d,products,policy);self.assertEqual(result['discount'],25916);self.assertEqual(result['total'],152084);self.assertEqual(sum(x['discount'] for x in result['items']),25916)
  for amount in ['712.01','-1','NaN','0.001']:
   with self.assertRaises(RuleError):calc_sale({**d,'discount_amount':amount},products,policy)
  with self.assertRaises(RuleError):calc_sale(d,products,{**policy,'discount':False})
  self.opening();self.sale(self.a,self.ta,discount_amount='259.16',cash='740.84');self.assertEqual(self.a.operations()[-1]['payload']['discount'],25916)
  codes=[s['seller_code'] for s in self.a.state(self.ta)['staff']];self.assertEqual(len(codes),len(set(codes)));self.assertIn('FBV-MELISSA',codes)
 def test_24_category_tree_product_and_permissions(self):
  import extensions as x
  root=x.create_category(self.c,'carlo',{'name':'Accesorios','description':'Complementos'})
  sub=x.create_category(self.c,'carlo',{'name':'Broches','parent':root['id']})
  leaf=x.create_category(self.c,'carlo',{'name':'Flores','parent':sub['id']})
  for d in [{'name':'accesorios'},{'name':'Inválida','parent':'no-existe'},{'name':'Cuarto nivel','parent':leaf['id']}]:
   with self.assertRaises(RuleError):x.create_category(self.c,'carlo',d)
  with self.assertRaises(RuleError):x.create_category(self.c,'melissa',{'name':'No autorizado'})
  d={'request_id':str(uuid.uuid4()),'name':'Broche de prueba','description':'Prueba de categoría','category_id':leaf['id'],'material_id':'1','provider':1,'price':'100','cost':'50','quantity':1,'warehouse':'coyoacan'}
  p=x.create_product(self.c,'carlo',d)['product'];self.assertEqual(p['type'],'Accesorios');self.assertEqual(p['sub1'],'Broches');self.assertEqual(p['sub2'],'Flores');self.assertEqual(len(p['code']),15)
  self.a.sync('carlo');self.assertIn(leaf,self.a.state(self.ta)['categories'])
 def test_25_category_edit_delete_reassignment(self):
  import extensions as x
  root=x.create_category(self.c,'carlo',{'name':'Accesorios'})
  leaf=x.create_category(self.c,'carlo',{'name':'Broches','parent':root['id']})
  d={'request_id':str(uuid.uuid4()),'name':'Broche','description':'Prueba','category_id':leaf['id'],'material_id':'1','provider':1,'price':'100','cost':'50','quantity':2,'warehouse':'coyoacan'}
  p=x.create_product(self.c,'carlo',d)['product']
  x.edit_category(self.c,'carlo',{'id':root['id'],'name':'Complementos','description':'Nueva descripción'})
  updated=next(v for v in self.c.catalog() if v['id']==p['id']);self.assertEqual(updated['type'],'Complementos');self.assertEqual(updated['code'],p['code'])
  with self.assertRaises(RuleError):x.delete_category(self.c,'carlo',{'id':root['id']})
  with self.assertRaises(RuleError):x.delete_category(self.c,'carlo',{'id':leaf['id']})
  with self.assertRaises(RuleError):x.edit_category(self.c,'carlo',{'id':root['id'],'name':'Anillos'})
  with self.assertRaises(RuleError):x.delete_category(self.c,'melissa',{'id':leaf['id'],'replacement':'1'})
  x.delete_category(self.c,'carlo',{'id':leaf['id'],'replacement':'1'})
  updated=next(v for v in self.c.catalog() if v['id']==p['id']);self.assertEqual(updated['category_id'],'1');self.assertEqual(updated['sub1'],'');self.assertEqual(updated['available'],2);self.assertEqual(updated['code'],p['code'])
  x.delete_category(self.c,'carlo',{'id':root['id']});self.assertNotIn(root['id'],self.c.get('types'))
  newer=x.create_category(self.c,'carlo',{'name':'Otra'});self.assertGreater(int(newer['id']),int(root['id']))
if __name__=='__main__':unittest.main(verbosity=2)
