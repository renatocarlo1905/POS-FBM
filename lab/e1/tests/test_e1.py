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
  self.c.db.execute('TRUNCATE simulated_receipt_codes,receipt_codes,merchandise_exchanges,corrections,related_changes,stock_ledger,inventory_entries,warehouse_stock,products,events,stock,audit,kv RESTART IDENTITY');self.c.db.close();self.c=Central(self.config)
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
 def test_27_code99_mixed_offline_receipt_and_corrections(self):
  import extensions as ext
  self.opening();stock={p['id']:p['available'] for p in self.c.catalog()};count=len(self.c.catalog())
  item={'id':'99-'+str(uuid.uuid4()),'qty':2,'special':{'description':'Dije especial fuera de inventario','category_id':'1','price':'125.50'}}
  self.a.put('offline',True)
  sale=self.op(self.a,self.ta,'sale',{'items':[{'id':'p1','qty':1},item],'cash':'1251','sellers':['carlo']})
  self.assertEqual(self.a.available()['p1']['available'],stock['p1']-1)
  self.a.put('offline',False);self.a.sync('carlo')
  view=ext.sale_view(self.c,sale['id']);p=view['adjusted'];self.assertEqual(p['total'],125100)
  self.assertTrue(p['items'][1]['non_inventory']);self.assertEqual(p['items'][1]['code'],'99');self.assertEqual(len(self.c.catalog()),count)
  self.assertEqual({p['id']:p['available'] for p in self.c.catalog()},{**stock,'p1':stock['p1']-1})
  text=' '.join(page.extract_text() for page in PdfReader(io.BytesIO(receipt_pdf(view['original']))).pages)
  self.assertIn('Dije especial',text)
  ext.correct(self.c,'carlo',0,self.correction('cancel',sale['id']))
  self.assertEqual({p['id']:p['available'] for p in self.c.catalog()},stock)
  for bad in [{'description':'','price':'1','category_id':'1'},{'description':'Prueba','price':'0','category_id':'1'},{'description':'Prueba','price':'1','category_id':'missing'}]:
   with self.assertRaises(RuleError):self.op(self.a,self.ta,'sale',{'items':[{**item,'special':bad}],'cash':'100','sellers':['carlo']})
 def test_28_exchange_cross_branch_preserves_closed_sale(self):
  import exchanges as ex,extensions as ext,cash_reports
  from unittest.mock import patch
  from datetime import datetime,timedelta
  self.opening();sale=self.sale(self.a,self.ta)['id'];original=self.c.db.execute('SELECT body FROM events WHERE id=?',(sale,)).fetchone()[0]
  closed=self.op(self.a,self.ta,'close',{'counted':'1500','fund':'500','envelope':'1000'})['id'];close_body=self.c.db.execute('SELECT body FROM events WHERE id=?',(closed,)).fetchone()[0]
  session=self.b.state(self.tb)['session']['id'];d={'target':sale,'session':session,'request_id':str(uuid.uuid4()),'returned':[{'id':'p1','qty':1}],'condition':True,'reason':'Prefiere otra pieza','sale':{'items':[{'id':'p4','qty':1}],'cash':'200','card':'300','bank':'Prueba','last4':'1234','sellers':['melissa']}}
  for cash in ('199','201'):
   with self.assertRaises(RuleError):ex.preview(self.c,'carlo',2,{**d,'sale':{**d['sale'],'cash':cash}})
  later=(datetime.fromisoformat(json.loads(original)['at'])+timedelta(days=2)).isoformat()
  with patch('exchanges.now',return_value=later):
   r=ex.confirm(self.c,'carlo',2,d);self.assertEqual(ex.confirm(self.c,'carlo',2,d)['id'],r['id'])
   with self.assertRaises(RuleError):ex.confirm(self.c,'carlo',2,{**d,'request_id':str(uuid.uuid4())})
  self.assertEqual((r['credit'],r['difference'],r['new']['cash'],r['new']['card']),(100000,50000,20000,30000))
  self.assertEqual(r['new']['attributions'],[{'sellers':['carlo'],'amount':100000},{'sellers':['melissa'],'amount':50000}])
  self.assertEqual(self.c.db.execute('SELECT body FROM events WHERE id=?',(sale,)).fetchone()[0],original);self.assertEqual(self.c.db.execute('SELECT body FROM events WHERE id=?',(closed,)).fetchone()[0],close_body)
  self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p1')['available'],8)
  with self.assertRaises(RuleError):ext.correct(self.c,'carlo',0,self.correction('cancel',sale))
  self.b.sync('melissa');self.assertEqual(ext.cash_adjustments(self.c,2)[session],20000)
  for _ in range(2):
   receipts=[e for e in self.b.state(self.tb)['operations'] if e['kind']=='exchange'];self.assertEqual(len(receipts),1);self.assertEqual(receipts[0]['id'],r['id']);self.assertEqual(receipts[0]['payload']['total'],50000)
  self.assertFalse(any(e['kind']=='exchange' for e in self.a.state(self.ta)['operations']))
  self.b.put('offline',True);self.assertTrue(any(e['id']==r['id'] for e in self.b.state(self.tb)['operations']));self.b.put('offline',False)
  cash_reports.init(self.c);row=next(r for r in cash_reports.report(self.c) if r['id']==session);self.assertEqual(row['expected'],70000)
  self.op(self.b,self.tb,'close',{'counted':'700','fund':'500','envelope':'200'});self.assertEqual(self.b.operations()[-1]['payload']['difference'],0)
  text=' '.join(p.extract_text() for p in PdfReader(io.BytesIO(receipt_pdf(ex.receipt(self.c,r['id'])))).pages);self.assertIn('CAMBIO DE MERCANC',text);self.assertNotIn('Cambio:',text);self.assertNotIn('Efectivo recibido:',text)
 def test_29_exchange_99_notification_and_guards(self):
  import exchanges as ex
  from unittest.mock import patch
  from datetime import datetime,timedelta
  self.opening();item={'id':'99-'+str(uuid.uuid4()),'qty':2,'special':{'description':'Pieza sin inventario','category_id':'1','price':'500'}}
  sale=self.op(self.a,self.ta,'sale',{'items':[item],'cash':'1000','sellers':['carlo']})['id'];session=self.a.state(self.ta)['session']['id']
  d={'target':sale,'session':session,'request_id':str(uuid.uuid4()),'returned':[{'id':item['id'],'qty':1}],'condition':True,'reason':'Cambio de pieza 99','sale':{'items':[{'id':'p1','qty':1}],'cash':'500','sellers':['carlo']}}
  with self.assertRaises(RuleError):ex.preview(self.c,'melissa',1,d)
  with self.assertRaises(RuleError):ex.preview(self.c,'carlo',1,{**d,'condition':False})
  with self.assertRaises(RuleError):ex.preview(self.c,'carlo',1,{**d,'session':'otra'})
  with patch('exchanges.now',return_value=(datetime.now().astimezone()+timedelta(days=16)).isoformat()):
   with self.assertRaises(RuleError):ex.preview(self.c,'carlo',1,d)
  r=ex.confirm(self.c,'carlo',1,d);self.assertEqual(ex.alerts(self.c)[0]['pieces'][0]['qty'],1)
  self.assertEqual(list(self.c.db.execute('SELECT * FROM stock_ledger WHERE product=?',(item['id'],))),[])
  self.assertEqual(ex.view(self.c,'carlo',sale)['remaining'][item['id']],1)
  self.assertEqual(ex.view(self.c,'carlo',r['out']['id'])['remaining']['p1'],1)
  # An equal-value subsequent exchange retains attribution, with zero cash collected.
  next_data={**d,'target':r['out']['id'],'request_id':str(uuid.uuid4()),'returned':[{'id':'p1','qty':1}],'sale':{'items':[{'id':'p1','qty':1}],'cash':'0','sellers':['melissa']}}
  follow=ex.confirm(self.c,'carlo',1,next_data);self.assertEqual(follow['difference'],0);self.assertEqual(follow['new']['cash'],0)
  bad={**d,'request_id':str(uuid.uuid4()),'sale':{'items':[{'id':'p1','qty':1}],'discount':'60','cash':'0','sellers':['carlo']}}
  with self.assertRaises(RuleError):ex.preview(self.c,'carlo',1,bad)
 def test_30_exchange_concurrent_requests_and_stale_preview(self):
  import exchanges as ex,hashlib
  self.opening();sale=self.sale(self.a,self.ta)['id'];session=self.a.state(self.ta)['session']['id']
  d={'target':sale,'session':session,'returned':[{'id':'p1','qty':1}],'condition':True,'reason':'Prueba concurrente','sale':{'items':[{'id':'p4','qty':1}],'cash':'500','sellers':['carlo']}}
  preview=ex.preview(self.c,'carlo',1,d);bad={**d,'request_id':str(uuid.uuid4()),'preview_hash':'no-coincide'}
  with self.assertRaises(RuleError):ex.confirm(self.c,'carlo',1,bad)
  self.assertEqual(len(ex.documents(self.c)),0)
  def attempt(_):
   try:return ex.confirm(self.c,'carlo',1,{**d,'request_id':str(uuid.uuid4()),'preview_hash':hashlib.sha256(pack(preview).encode()).hexdigest()})['id']
   except RuleError:return None
  with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(attempt,range(2)))
  self.assertEqual(sum(r is not None for r in results),1);self.assertEqual(len(ex.documents(self.c)),1)
 def test_31_public_sale_codes_offline_and_legacy(self):
  import folios,exchanges as ex,extensions as ext
  self.opening();self.a.put('offline',True)
  ident=self.sale(self.a,self.ta)['id'];raw=json.loads(self.a.rows()[-1]['body'])
  before=folios.code(raw);self.assertRegex(before,r'^V1-[0-9]{6}$')
  self.assertNotIn('short_code',raw)  # legacy immutable bodies also work
  self.assertEqual(self.a.state(self.ta)['operations'][0]['short_code'],before)
  text=PdfReader(io.BytesIO(receipt_pdf(raw))).pages[0].extract_text()
  self.assertIn(before,text);self.assertNotIn(ident,text)
  self.a.put('offline',False);self.a.sync('carlo')
  self.assertEqual(ex.lookup(self.c,'carlo',before.lower())[0]['id'],ident)
  self.assertEqual(folios.code(ext.sale_view(self.c,ident)['original']),before)
  other=self.sale(self.b,self.tb)['id'];other_code=folios.code(ext.sale_view(self.c,other)['original'])
  self.assertTrue(other_code.startswith('V2-'));self.assertNotEqual(before,other_code)
  self.assertEqual(ex.lookup(self.c,'carlo',ident[:8])[0]['id'],ident)
  # Decoration and backfill do not modify immutable events / hash.
  persisted=self.c.db.execute('SELECT body,hash FROM events WHERE id=?',(ident,)).fetchone()
  folios.init(self.c)
  self.assertEqual(dict(persisted),dict(self.c.db.execute('SELECT body,hash FROM events WHERE id=?',(ident,)).fetchone()))
 def test_32_public_exchange_codes(self):
  import folios,exchanges as ex
  self.opening();ident=self.sale(self.a,self.ta)['id']
  code=folios.code(folios.decorate(self.c,self.a.operations()[-1]))
  self.assertRegex(code,r'^V1-[0-9]{6}$')
  d={'target':ident,'session':self.a.state(self.ta)['session']['id'],'returned':[{'id':'p1','qty':1}],'condition':True,'reason':'Cambio','sale':{'items':[{'id':'p4','qty':1}],'cash':'500','sellers':['carlo']},'request_id':str(uuid.uuid4())}
  changed=ex.confirm(self.c,'carlo',1,d);short=changed['short_code']
  self.assertRegex(short,r'^C1-[0-9]{6}$');self.assertEqual(changed,ex.confirm(self.c,'carlo',1,d))
  self.assertEqual(ex.lookup(self.c,'carlo',short)[0]['id'],changed['out']['id'])
  text=PdfReader(io.BytesIO(receipt_pdf(ex.receipt(self.c,changed['id'])))).pages[0].extract_text()
  self.assertIn(short,text);self.assertIn(code,text);self.assertNotIn(changed['id'],text)
  folios.init(self.c);self.assertEqual(ex.documents(self.c)[0]['short_code'],short)
 def test_33_simulated_codes_stable_unique_and_nonfinancial(self):
  import simulated,cash_reports,order_service as orders
  simulated.init(self.c);cash_reports.init(self.c)
  self.opening();real=self.sale(self.a,self.ta)['id'];event=json.loads(self.a.rows()[-1]['body'])
  fixtures=[{**event,'id':'SIM-alpha','simulated':True,'simulation_batch':'test'},{**event,'id':'SIM-beta','branch':2,'simulated':True,'simulation_batch':'test'}]
  for e in fixtures:
   e.pop('seq',None);self.c.db.execute('INSERT INTO simulated_sales VALUES(?,?,?)',(e['id'],'test',pack(e)))
  self.c.put('simulation-template:test',event['template'])
  before=[dict(r) for r in self.c.db.execute('SELECT * FROM simulated_sales ORDER BY id')]
  rows=simulated.sales(self.c);codes={e['id']:e['short_code'] for e in rows}
  self.assertRegex(codes['SIM-alpha'],r'^SV1-[0-9]{6}$');self.assertRegex(codes['SIM-beta'],r'^SV2-[0-9]{6}$')
  self.assertEqual(len(set(codes.values())),2)
  self.assertEqual(simulated.receipt(self.c,'SIM-alpha')['short_code'],codes['SIM-alpha'])
  import exchanges
  result=exchanges.lookup(self.c,'carlo',codes['SIM-alpha'].lower())
  self.assertEqual(result[0]['id'],'SIM-alpha');self.assertNotEqual(result[0].get('eligible'),False)
  self.assertEqual(exchanges.view(self.c,'carlo','SIM-alpha')['source']['short_code'],codes['SIM-alpha'])
  self.assertEqual(exchanges.lookup(self.c,'carlo','SV1-999999'),[])

  text=PdfReader(io.BytesIO(receipt_pdf(simulated.receipt(self.c,'SIM-alpha')))).pages[0].extract_text();self.assertIn(codes['SIM-alpha'],text);self.assertNotIn('SIM-alpha',text)
  simulated.init(self.c);self.assertEqual(codes,{e['id']:e['short_code'] for e in simulated.sales(self.c)})
  self.assertEqual(before,[dict(r) for r in self.c.db.execute('SELECT * FROM simulated_sales ORDER BY id')])
  for order in orders.all_orders(self.c):
   if order.get('simulated'):
    self.assertRegex(order['short_code'],r'^S[AR][12]-[0-9]{6}$');self.assertEqual(orders.get(self.c,order['id'])['short_code'],order['short_code'])
  rows=simulated.assign_codes(self.c,[{'id':'SIM-CAJA-example','branch':1}],'SC');self.assertRegex(rows[0]['short_code'],r'^SC1-[0-9]{6}$')
  with self.assertRaises(Exception):self.c.db.execute("UPDATE simulated_receipt_codes SET branch=2 WHERE identifier='SIM-alpha'")
 def test_34_simulated_sale_operational_exchange(self):
  import simulated,exchanges as ex,extensions as ext
  simulated.init(self.c);self.opening();self.sale(self.a,self.ta)
  event=json.loads(self.a.rows()[-1]['body']);event.pop('seq');event.update(id='SIM-operational-exchange',simulated=True,simulation_batch='test')
  self.c.db.execute('INSERT INTO simulated_sales VALUES(?,?,?)',(event['id'],'test',pack(event)))
  original=pack(event);code=next(e['short_code'] for e in simulated.sales(self.c) if e['id']==event['id'])
  self.assertEqual(ex.lookup(self.c,'carlo',code)[0]['id'],event['id'])
  stock={p['id']:p['available'] for p in self.c.catalog()};session=self.a.state(self.ta)['session']['id']
  before_expected=self.a.state(self.ta)['cash_summary']['expected']
  d={'target':event['id'],'session':session,'returned':[{'id':'p1','qty':1}],'condition':True,'reason':'Cambio sobre historial ficticio','sale':{'items':[{'id':'p4','qty':1}],'cash':'446.50','discount_amount':'53.50','sellers':['carlo']},'request_id':str(uuid.uuid4())}
  changed=ex.confirm(self.c,'carlo',1,d)
  self.assertEqual(changed['difference'],44650);self.assertEqual(changed['target_code'],code)
  self.assertEqual(changed['new']['discount'],5350)
  after={p['id']:p['available'] for p in self.c.catalog()};self.assertEqual(after['p1'],stock['p1']+1);self.assertEqual(after['p4'],stock['p4']-1)
  self.assertEqual(self.a.state(self.ta)['cash_summary']['expected'],before_expected+44650)
  self.assertEqual(original,self.c.db.execute('SELECT body FROM simulated_sales WHERE id=?',(event['id'],)).fetchone()[0])
  with self.assertRaises(RuleError):ex.confirm(self.c,'carlo',1,{**d,'request_id':str(uuid.uuid4())})
  self.assertIn(code,PdfReader(io.BytesIO(receipt_pdf(ex.receipt(self.c,changed['id'])))).pages[0].extract_text())
 def test_35_close_automatic_envelope_and_discrepancy(self):
  self.opening()
  for counted,fund,expected_envelope,expected_difference,label in [('7030','530',650000,653000,'Dinero no anotado'),('450','100',35000,-5000,'Dinero faltante'),('500','500',0,0,'Caja cuadrada')]:
   result=self.op(self.a,self.ta,'close',{'counted':counted,'fund':fund})
   e=next(e for e in self.a.operations() if e['id']==result['id'])
   self.assertEqual(e['payload']['envelope'],expected_envelope);self.assertEqual(e['payload']['difference'],expected_difference)
   self.assertIn(label,PdfReader(io.BytesIO(receipt_pdf(e))).pages[0].extract_text())
   self.op(self.a,self.ta,'open',{'opening':'500'})
  count=len(self.a.rows())
  with self.assertRaises(RuleError):self.op(self.a,self.ta,'close',{'counted':'100','fund':'101'})
  self.assertEqual(len(self.a.rows()),count)
 def test_36_close_summary_without_reporting_permissions(self):
  self.opening();roles=self.c.get('roles');roles['sales']['permissions'].update(cash_summary=False,receipts=False,reprint=False,cash_close=True);self.c.put('roles',roles)
  state=self.b.state(self.tb);self.assertNotIn('cash_summary',state);self.assertEqual(state['operations'],[])
  data={'counted':'470','fund':'100','session':state['session']['id']};count=len(self.b.rows())
  preview=self.b.close_preview(self.tb,data);self.assertEqual(preview['difference'],-3000);self.assertEqual(preview['envelope'],37000)
  self.assertEqual(len(self.b.rows()),count);self.assertIsNotNone(self.b.state(self.tb)['session'])
  with self.assertRaises(RuleError):self.b.close_preview(self.tb,{**data,'session':'wrong'})
  ident=str(uuid.uuid4());result=self.b.submit(self.tb,'close',data,ident)
  self.assertEqual(result['close_summary']['difference'],-3000)
  self.assertEqual(self.b.submit(self.tb,'close',data,ident)['close_summary'],result['close_summary'])
  self.assertEqual(self.b.state(self.tb)['operations'],[])
  roles['sales']['permissions']['cash_close']=False;self.c.put('roles',roles)
  with self.assertRaises(RuleError):self.b.close_preview(self.tb,data)
 def test_01_postgres_shared_stock_and_money(self):
  self.assertIn('PostgreSQL',self.c.db.execute('SELECT version()').fetchone()[0]);self.opening()
  self.sale(self.a,self.ta,cash='400',card='600',bank='Prueba',last4='1234')
  self.sale(self.b,self.tb)
  self.assertEqual(self.c.catalog()[0]['available'],6)
  e=json.loads(self.a.rows()[-1]['body']);self.assertEqual((e['payload']['cash'],e['payload']['change']),(40000,0))
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
  self.opening();self.sale(self.a,self.ta,cash='400',card='600',bank='Demo',last4='1234')
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
  self.opening();self.a.put('offline',True);self.sale(self.a,self.ta,discount='12.34',cash='876.60')
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
 def test_19_cancel_ticket_then_independent_sale(self):
  import extensions as x
  self.opening();ident=self.sale(self.a,self.ta)['id']
  original=self.c.db.execute('SELECT body FROM events WHERE id=?',(ident,)).fetchone()[0]
  with self.assertRaisesRegex(RuleError,'Acción no disponible'):
   x.correct(self.c,'carlo',1,self.correction('replace',ident,replacement={'items':[{'id':'p2','qty':1}],'cash':'780'}))
  self.assertFalse(x.sale_view(self.c,ident)['adjusted']['cancelled'])
  d=self.correction('cancel',ident);doc=x.correct(self.c,'carlo',1,d)
  self.assertEqual(x.correct(self.c,'carlo',1,d)['id'],doc['id'])
  self.assertEqual(self.c.catalog()[0]['available'],8)
  self.assertEqual(self.c.db.execute('SELECT body FROM events WHERE id=?',(ident,)).fetchone()[0],original)
  for width in (58,80):
   printable=copy.deepcopy(doc);printable['template']['width']=width
   text=' '.join(' '.join(p.extract_text() for p in PdfReader(io.BytesIO(receipt_pdf(printable))).pages).split())
   self.assertIn('TICKET DE CANCELACIÓN',text);self.assertIn('Venta anulada:',text)
   self.assertIn('Error de captura',text);self.assertIn('Importe cancelado:',text)
   self.assertNotIn(' -> ',text);self.assertNotIn('Vendedores:',text);self.assertNotIn('Gracias por su visita',text)
   self.assertLess(float(PdfReader(io.BytesIO(receipt_pdf(printable))).pages[0].mediabox.height),340)
  self.a.sync('carlo')
  new=self.sale(self.a,self.ta,'p2')
  self.assertNotEqual(new['id'],ident)
  self.assertEqual(next(p for p in self.c.catalog() if p['id']=='p2')['available'],11)
  self.assertEqual(x.cash_adjustments(self.c,1)[doc['payload']['session']],-100000)
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
 def test_26_cash_summary_permission_and_payment_correction(self):
  import extensions as x
  self.opening()
  ident=self.sale(self.a,self.ta,cash='400',card='600',bank='Demo',last4='1234')['id']
  summary=self.a.state(self.ta)['cash_summary']
  self.assertEqual(summary['expected'],90000)
  self.assertEqual(summary['payments']['cash'],{'amount':40000,'count':1})
  self.assertEqual(summary['payments']['card'],{'amount':60000,'count':1})
  self.assertNotIn('cash_summary',self.b.state(self.tb))
  x.correct(self.c,'carlo',0,self.correction('payment',ident,cash='0',card='1000',bank='Demo',last4='1234',transfer='0'))
  corrected=self.a.state(self.ta)['cash_summary']
  self.assertEqual(corrected['expected'],50000)
  self.assertEqual(corrected['payments']['cash']['count'],0)
  self.assertEqual(corrected['payments']['card']['amount'],100000)
  roles=self.c.get('roles');permissions={**roles['sales']['permissions'],'cash_summary':True}
  self.c.edit_role('carlo',{'id':'sales','name':'Personal','permissions':permissions,'max_discount':0})
  self.tb=self.b.login('melissa','Melissa-E1-2026!')['token']
  self.assertEqual(self.b.state(self.tb)['cash_summary']['expected'],50000)
  self.b.put('offline',True)
  permissions['cash_summary']=False
  self.c.edit_role('carlo',{'id':'sales','name':'Personal','permissions':permissions,'max_discount':0})
  self.assertIn('cash_summary',self.b.state(self.tb))
  self.b.put('offline',False)
  self.tb=self.b.login('melissa','Melissa-E1-2026!')['token']
  self.assertNotIn('cash_summary',self.b.state(self.tb))

 def test_product_edit_admin_revision_aliases_and_stock(self):
  import extensions as ext
  p=next(p for p in self.c.catalog(True) if p['id']=='p1')
  stock=[dict(r) for r in self.c.db.execute('SELECT * FROM stock ORDER BY id')]
  events=self.c.events()
  d={'id':p['id'],'revision':0,'request_id':str(uuid.uuid4()),'name':'A. SOL SIMPLE','description':'ANILLO SOL SIMPLE','material_id':p['material_id'],'category_id':str(p.get('category_id',p['type_id'])),'provider':p['provider'],'price':'1100.00','cost':'510.00','weight':'','image':'','print_price':True,'reason':'Corregir ficha'}
  with self.assertRaises(RuleError):ext.edit_product(self.c,'melissa',d)
  result=ext.edit_product(self.c,'carlo',d);self.assertFalse(result['code_changed']);self.assertEqual(result['product']['name'],'A. SOL SIMPLE')
  self.assertEqual(ext.edit_product(self.c,'carlo',d),result)
  with self.assertRaises(RuleError):ext.edit_product(self.c,'carlo',{**d,'request_id':str(uuid.uuid4())})
  d.update(revision=1,request_id=str(uuid.uuid4()),weight='2.345')
  with self.assertRaises(RuleError):ext.edit_product(self.c,'carlo',d)
  d['acknowledge_label']=True
  result=ext.edit_product(self.c,'carlo',d);self.assertTrue(result['code_changed']);self.assertIn(p['code'],result['product']['aliases'])
  self.assertEqual(result['product']['code'][4:10],'002345')
  self.assertEqual([dict(r) for r in self.c.db.execute('SELECT * FROM stock ORDER BY id')],stock);self.assertEqual(self.c.events(),events)
  for change in ({'weight':'0'},{'name':''},{'description':''},{'provider':999},{'quantity':10},{'price':'0'},{'image':'bad'}):
   with self.assertRaises(RuleError):ext.edit_product(self.c,'carlo',{**d,'revision':2,'request_id':str(uuid.uuid4()),**change})
  codes=[result['product']['code'],p['code']]
  generated=ext.next_product_code(self.c,1,1,None)
  self.assertGreater(int(generated[-5:]),max(int(code[-5:]) for code in codes))

 def test_exact_payment_required_for_new_sales(self):
  self.opening()
  count=len(self.a.rows())
  for cash in ('1000.01','999.99','1500'):
   with self.assertRaises(RuleError):self.sale(self.a,self.ta,cash=cash)
  self.assertEqual(len(self.a.rows()),count)
  r=self.sale(self.a,self.ta,cash='350',card='400',transfer='250',bank='Banco',last4='1234',reference='REF-1')
  event=next(e for e in self.a.operations() if e['id']==r['id'])
  self.assertEqual(event['payload']['change'],0);self.assertEqual(event['payload']['cash'],35000)
  text=''.join(page.extract_text() for page in PdfReader(io.BytesIO(receipt_pdf(event))).pages)
  self.assertNotIn('Cambio:',text);self.assertNotIn('Efectivo recibido:',text);self.assertIn('Efectivo:',text)
  self.b.put('offline',True)
  with self.assertRaises(RuleError):self.sale(self.b,self.tb,cash='1001')
  self.sale(self.b,self.tb,cash='1000')

if __name__=='__main__':unittest.main(verbosity=2)
