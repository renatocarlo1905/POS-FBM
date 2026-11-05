import unittest,uuid
import test_e1
import extensions as ext
from domain import RuleError
class RecurrentInventory(unittest.TestCase):
 setUpClass=classmethod(test_e1.Lab.setUpClass.__func__)
 tearDownClass=classmethod(test_e1.Lab.tearDownClass.__func__)
 setUp=test_e1.Lab.setUp
 tearDown=test_e1.Lab.tearDown
 def draft(self):return {'request_id':str(uuid.uuid4()),'warehouse':'coyoacan','reason':'Recepción recurrente','items':[{'product':'p1','quantity':2},{'product':'p2','quantity':3}]}
 def quantities(self):return {p['id']:p['warehouses']['coyoacan'] for p in self.c.catalog()}
 def test_atomic_retry_and_permissions(self):
  d=self.draft();before=self.quantities();r=ext.recurrent_ingress(self.c,'carlo',d)
  self.assertEqual(r['units'],5);self.assertEqual(self.quantities()['p1'],before['p1']+2)
  self.assertEqual(ext.recurrent_ingress(self.c,'carlo',d),r)
  self.assertEqual(self.quantities()['p2'],before['p2']+3)
  with self.assertRaises(RuleError):ext.recurrent_ingress(self.c,'citlali',self.draft())
  with self.assertRaises(RuleError):ext.recurrent_ingress(self.c,'carlo',{**d,'reason':'Otro motivo'})
 def test_invalid_row_rolls_back_all(self):
  before=self.quantities();d=self.draft();d['items'][1]['product']='missing'
  with self.assertRaises(RuleError):ext.recurrent_ingress(self.c,'carlo',d)
  self.assertEqual(self.quantities(),before)
  d=self.draft();d['items'][1]=d['items'][0]
  with self.assertRaises(RuleError):ext.recurrent_ingress(self.c,'carlo',d)
  d=self.draft();d['items'][1]['quantity']=0
  with self.assertRaises(RuleError):ext.recurrent_ingress(self.c,'carlo',d)
  self.assertEqual(self.quantities(),before)
