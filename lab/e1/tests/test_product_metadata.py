import sys,unittest,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import test_e1
import extensions as ext
from domain import RuleError

class ProductMetadata(unittest.TestCase):
 setUpClass=classmethod(test_e1.Lab.setUpClass.__func__)
 tearDownClass=classmethod(test_e1.Lab.tearDownClass.__func__)
 setUp=test_e1.Lab.setUp
 tearDown=test_e1.Lab.tearDown
 op=test_e1.Lab.op
 correction=test_e1.Lab.correction
 def create(self,provider=1):
  return ext.create_product(self.c,'carlo',{'request_id':str(uuid.uuid4()),'name':'A. FECHAS','description':'ANILLO FECHAS','material_id':'1','category_id':'1','provider':provider,'price':'100','cost':'40','weight':'','quantity':3,'warehouse':'coyoacan'})['product']
 def product(self,pid):return next(p for p in self.c.catalog(True) if p['id']==pid)
 def edit(self,p,**extra):
  return ext.edit_product(self.c,'carlo',{'id':p['id'],'revision':p.get('revision',0),'request_id':str(uuid.uuid4()),'name':p['name'],'description':p['description'],'material_id':p['material_id'],'category_id':p['category_id'],'provider':p['provider'],'price':'110','cost':'40','weight':'','reason':'Actualizar ficha',**extra})['product']
 def test_dates_creation_sale_edit_cancel_and_retry(self):
  self.assertIsNone(self.product('p1')['created_at'])
  p=self.create();pid=p['id'];p=self.product(pid);created=p['created_at'];self.assertTrue(created);self.assertIsNone(p['edited_at'])
  self.a.sync('carlo');self.op(self.a,self.ta,'open',{'opening':'500'})
  sale=self.op(self.a,self.ta,'sale',{'items':[{'id':pid,'qty':1}],'cash':'100'})
  p=self.product(pid);self.assertEqual(p['last_activity_type'],'Venta');self.assertEqual(p['created_at'],created);self.assertIsNone(p['edited_at']);sold=p['last_movement_at']
  self.edit(p);p=self.product(pid);self.assertEqual(p['last_activity_type'],'Edición de datos');self.assertEqual(p['last_movement_at'],sold);self.assertEqual(p['created_at'],created)
  req=self.correction('cancel',sale['id']);ext.correct(self.c,'carlo',0,req)
  p=self.product(pid);self.assertEqual(p['last_activity_type'],'Anulación por error');last=p['updated_at'];self.assertEqual(p['created_at'],created)
  ext.correct(self.c,'carlo',0,req);self.assertEqual(self.product(pid)['updated_at'],last)
  ext.ingress(self.c,'carlo',{'request_id':str(uuid.uuid4()),'product':pid,'quantity':1,'warehouse':'oficina','reason':'Recepción nueva'})
  self.assertEqual(self.product(pid)['last_activity_type'],'Recepción nueva')
 def test_approved_providers_and_product_reassignment(self):
  with self.assertRaises(RuleError):ext.provider(self.c,'melissa',{'name':'No autorizado'})
  provider=ext.provider(self.c,'carlo',{'name':'Taller Sol','approved':True})
  with self.assertRaises(RuleError):ext.provider(self.c,'carlo',{'name':'taller sol'})
  p=self.create();p=self.edit(p,provider=provider['id']);self.assertEqual(p['provider'],provider['id'])
  ext.provider(self.c,'carlo',{'id':provider['id'],'name':'Taller Sol','approved':False})
  with self.assertRaises(RuleError):self.create(provider['id'])
  import inventory_import
  self.assertNotIn(str(provider['id']),inventory_import.catalogs(self.c)['providers'])
  self.edit(p) # Existing association remains valid for unrelated edits.
  p2=self.create()
  with self.assertRaises(RuleError):self.edit(p2,provider=provider['id'])

if __name__=='__main__':unittest.main()
