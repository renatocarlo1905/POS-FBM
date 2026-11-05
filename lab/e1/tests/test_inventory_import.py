import base64, csv, io, json, sys, unittest, zipfile
from pathlib import Path
from unittest.mock import patch
from concurrent.futures import ThreadPoolExecutor
import xml.etree.ElementTree as ET
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import test_e1
import inventory_import as imp
import extensions as ext
from domain import RuleError

class InventoryImport(unittest.TestCase):
 setUpClass=classmethod(test_e1.Lab.setUpClass.__func__)
 tearDownClass=classmethod(test_e1.Lab.tearDownClass.__func__)
 setUp=test_e1.Lab.setUp
 tearDown=test_e1.Lab.tearDown
 def row(self,name='A. IMPORTACIÓN NUEVA'):
  return [name,'ANILLO IMPORTACIÓN NUEVA','Plata','Anillos','Proveedor de prueba','480','180','2.500','3','Coyoacán','Sí','Fijo','','','']
 def file(self,rows,reference='RECEPCION-TEST-1'):
  out=io.StringIO();csv.writer(out).writerows([imp.HEADERS,*rows])
  return {'reference':reference,'filename':'productos.csv','content':base64.b64encode(out.getvalue().encode()).decode()}
 def ready(self,d):
  result=imp.preview(self.c,'carlo',d);self.assertEqual(result['errors'],[]);return {**d,'preview_hash':result['preview_hash']}
 def test_new_products_atomic_stock_and_retries(self):
  count=len(self.c.catalog());r1=self.row();r2=self.row('A. IMPORTACIÓN OFICINA');r2[9]='Oficina'
  data=self.ready(self.file([r1,r2]));self.assertEqual(len(self.c.catalog()),count)
  with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(lambda _:imp.confirm(self.c,'carlo',data),range(2)))
  result=results[0];self.assertEqual(result['count'],2);self.assertEqual(len(self.c.catalog()),count+2)
  self.assertTrue(any(r.get('duplicate') for r in results))
  for product in result['products']:
   self.assertEqual(next(p for p in self.c.catalog() if p['id']==product['id'])['warehouses'][product['warehouse']],3)
  self.assertTrue(imp.preview(self.c,'carlo',data)['already_imported'])
  changed=self.row();changed[8]='4'
  with self.assertRaises(RuleError):imp.preview(self.c,'carlo',self.file([changed]))
  duplicate=imp.preview(self.c,'carlo',self.file([r1],'DIFFERENT-REFERENCE'))
  self.assertIn('Ya existe',duplicate['errors'][0]['message'])
 def test_all_rows_validated_no_partial_write(self):
  first=self.row();bad=self.row('A. INVALIDO');bad[2]='Desconocido';count=len(self.c.catalog())
  d=self.file([first,bad]);p=imp.preview(self.c,'carlo',d);self.assertEqual(p['errors'][0]['row'],3)
  with self.assertRaises(RuleError):imp.confirm(self.c,'carlo',{**d,'preview_hash':p['preview_hash']})
  self.assertEqual(len(self.c.catalog()),count)
  repeated=self.file([first,first]);self.assertIn('repetido',imp.preview(self.c,'carlo',repeated)['errors'][0]['message'])
  for col,value in [(5,'-1'),(6,''),(7,'999.001'),(8,'2.5'),(8,'0'),(10,'Tal vez'),(0,''),(1,'')]:
   row=self.row();row[col]=value
   self.assertTrue(imp.preview(self.c,'carlo',self.file([row]))['errors'])
 def test_rollback_on_failure_and_stale_preview(self):
  count=len(self.c.catalog());data=self.ready(self.file([self.row(),self.row('A. SEGUNDO')]))
  original=ext.create_product.__wrapped__;counter=0
  def fails(c,actor,d):
   nonlocal counter
   counter+=1
   if counter==2:raise RuleError('Fallo forzado')
   return original(c,actor,d)
  with patch.object(ext.create_product,'__wrapped__',fails):
   with self.assertRaisesRegex(RuleError,'Fallo forzado'):imp.confirm(self.c,'carlo',data)
  self.assertEqual(len(self.c.catalog()),count)
  self.assertEqual(self.c.db.execute('SELECT count(*) FROM inventory_entries').fetchone()[0],0)
  self.c.put('materials',{**self.c.get('materials'),'1':'Plata modificada'})
  with self.assertRaises(RuleError):imp.confirm(self.c,'carlo',data)
  self.assertEqual(len(self.c.catalog()),count)
 def test_google_export_read_and_confirm(self):
  source=Path(__file__).parent/'fixtures/products-google-sheets.xlsx';raw=source.read_bytes()
  data={'filename':'google.xlsx','reference':'GOOGLE-TEST','content':base64.b64encode(raw).decode()}
  self.assertEqual(imp.read_rows(data)[0][1][0],'A. SOL SIMPLE')
  result=imp.confirm(self.c,'carlo',self.ready(data))
  self.assertEqual(result['count'],1);self.assertEqual(result['units'],1)
  product=next(p for p in self.c.catalog(True) if p['id']==result['products'][0]['id'])
  self.assertEqual(product['name'],'A. SOL SIMPLE');self.assertEqual(product['description'],'ANILLO SOL SIMPLE');self.assertEqual(product['price'],48000)
 def test_blank_rows_ignored_and_incomplete_rows_reported(self):
  data=self.file([[],self.row(),[''],['A. INCOMPLETO']])
  preview=imp.preview(self.c,'carlo',data)
  self.assertEqual(preview['count'],1)
  self.assertEqual(preview['errors'][0]['row'],5)
  with self.assertRaises(RuleError):imp.confirm(self.c,'carlo',{**data,'preview_hash':preview['preview_hash']})
 def test_formula_price_persisted_and_recomputed_on_edit(self):
  import uuid
  from product_pricing import calculate
  for ending,expected in [('50',85000),('90',89000)]:
   self.assertEqual(calculate({'price_mode':'formula','price_base':'cost','price_multiplier':'2.77','price_ending':ending},30000,None)[0],expected)
  self.assertEqual(calculate({'price_mode':'formula','price_base':'weight','price_multiplier':'1000','price_ending':'90'},0,'1.2')[0],129000)
  self.assertEqual(calculate({'price_mode':'formula','price_base':'cost','price_multiplier':'1','price_ending':'50'},85000,None)[0],85000)
  row=self.row();row[5]='';row[6]='300';row[10]='No';row[11:]=['Fórmula','Costo','2.77','90']
  d=self.file([row]);p=imp.preview(self.c,'carlo',d);self.assertEqual(p['rows'][0]['product']['price'],'890')
  result=imp.confirm(self.c,'carlo',{**d,'preview_hash':p['preview_hash']})
  product=next(x for x in self.c.catalog(True) if x['id']==result['products'][0]['id'])
  self.assertEqual(product['price_rule'],{'base':'cost','multiplier':'2.77','ending':'90'})
  self.assertFalse(product['print_price'])
  changed=ext.edit_product(self.c,'carlo',{'id':product['id'],'revision':0,'request_id':str(uuid.uuid4()),'name':product['name'],'description':product['description'],'material_id':product['material_id'],'category_id':product['category_id'],'cost':'400','price':'890','weight':product['weight'],'reason':'Actualizar costo','print_price':False})['product']
  self.assertEqual(changed['price'],119000);self.assertEqual(changed['price_rule'],product['price_rule'])
  for change in [(12,'Otra'),(13,'0'),(13,'NaN'),(14,'80'),(6,'0')]:
   invalid=row.copy();invalid[change[0]]=change[1];invalid[0]='A. OTRA'
   self.assertTrue(imp.preview(self.c,'carlo',self.file([invalid],'OTRA'))['errors'])
 def test_permissions_formats_and_limits(self):
  data=self.file([self.row()])
  with self.assertRaises(RuleError):imp.preview(self.c,'citlali',data)
  with self.assertRaises(RuleError):imp.confirm(self.c,'citlali',data)
  for override in [{'filename':'datos.xls'},{'content':'not base64'},{'reference':''},{'content':'a'*600010}]:
   with self.assertRaises(RuleError):imp.preview(self.c,'carlo',{**data,**override})
  with self.assertRaises(RuleError):imp.preview(self.c,'carlo',self.file([self.row()]*501))
 def test_http_admin_and_both_branches_preview_and_confirmation(self):
  import urllib.request,urllib.error
  from server import Application
  app=Application(self.path/'http-import',18880,self.config);app.start()
  def call(port,path,data,token=''):
   req=urllib.request.Request(f'http://127.0.0.1:{port}/api/{path}',data=json.dumps(data).encode(),headers={'Content-Type':'application/json','Authorization':'Bearer '+token})
   with urllib.request.urlopen(req) as response:return json.loads(response.read())
  try:
   admin=call(18880,'login',{'user':'carlo','password':'Carlo-E1-2026!'})['token'];pos=call(18881,'login',{'user':'carlo','password':'Carlo-E1-2026!'})['token'];data=self.file([self.row()])
   self.assertEqual(call(18881,'inventory-import-preview',data,pos)['count'],1)
   preview=call(18880,'inventory-import-preview',data,admin)
   self.assertEqual(preview['count'],1);self.assertEqual(preview['errors'],[])
   result=call(18880,'inventory-import-confirm',{**data,'preview_hash':preview['preview_hash']},admin)
   self.assertEqual(result['count'],1)
   for branch in (1,2):
    port=18880+branch
    token=call(port,'login',{'user':'carlo','password':'Carlo-E1-2026!'})['token']
    row=self.row('A. SUCURSAL '+str(branch));row[11:]=['Fórmula','Costo','2.77','90']
    data=self.file([row],'SUC-'+str(branch))
    preview=call(port,'inventory-import-preview',data,token)
    self.assertNotIn('price_multiplier',preview['rows'][0]['product'])
    self.assertNotIn('price_base',preview['rows'][0]['product'])
    self.assertIn('price_multiplier',call(18880,'inventory-import-preview',data,admin)['rows'][0]['product'])
    result=call(port,'inventory-import-confirm',{**data,'preview_hash':preview['preview_hash']},token)
    self.assertEqual(result['count'],1)
    self.assertTrue(call(18880,'inventory-import-preview',data,admin)['already_imported'])
    req=urllib.request.Request(f'http://127.0.0.1:{port}/api/state',headers={'Authorization':'Bearer '+token})
    with urllib.request.urlopen(req) as response:state=json.loads(response.read())
    imported=next(p for p in state['catalog'] if p['id']==result['products'][0]['id'])
    self.assertNotIn('price_rule',imported);self.assertGreater(imported['price'],0)
    self.assertEqual(next(p for p in app.central.catalog(True) if p['id']==imported['id'])['price_rule']['multiplier'],'2.77')
    call(port,'offline',{'offline':True},token)
    with self.assertRaises(urllib.error.HTTPError):call(port,'inventory-import-preview',data,token)
  finally:app.stop()

if __name__=='__main__':unittest.main()
