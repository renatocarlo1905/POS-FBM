import unittest,uuid
from test_order_operations import Orders
import order_training,order_service as orders
class Training(Orders):
 def test_training_operations(self):
  rows=order_training.prepare(self.c);self.assertEqual(len(rows),8);self.assertEqual(order_training.prepare(self.c),rows)
  self.assertEqual(orders.adjustments(self.c,1).get(self.a.operations()[0]['id'],0),0)
  self.assertNotIn(None,orders.adjustments(self.c,1))
  self.a.sync('carlo')
  from domain import pack
  pack(self.c.pull(self.c.login('carlo','Carlo-E1-2026!',1)['grant']))
  first=orders.get(self.c,rows[0]['id']);self.runorder({'action':'pay','id':first['id'],'revision':first['revision'],'amount':'10','cash':'10'},self.staff)
  repair=orders.get(self.c,rows[6]['id']);self.runorder({'action':'pay','id':repair['id'],'revision':repair['revision'],'amount':'400','cash':'400'},self.staff)
  repair=orders.get(self.c,repair['id']);self.runorder({'action':'deliver','id':repair['id'],'revision':repair['revision'],'confirmed':True},self.staff)
  self.assertEqual(orders.get(self.c,repair['id'])['status'],'delivered')
