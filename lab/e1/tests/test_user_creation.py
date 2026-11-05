import unittest
import test_e1
from domain import RuleError

class UserCreation(unittest.TestCase):
 setUpClass=classmethod(test_e1.Lab.setUpClass.__func__)
 tearDownClass=classmethod(test_e1.Lab.tearDownClass.__func__)
 setUp=test_e1.Lab.setUp
 tearDown=test_e1.Lab.tearDown
 def data(self,**changes):
  role=next(k for k in self.c.get('roles') if k!='admin')
  return {'id':'nueva.persona','name':'Nueva persona','role':role,'branches':[1],'password':'ClavePrueba123!',**changes}
 def test_create_login_scope_and_duplicate(self):
  self.c.create_user('carlo',self.data())
  self.c.login('NUEVA.PERSONA','ClavePrueba123!',1)
  with self.assertRaises(RuleError):self.c.login('nueva.persona','ClavePrueba123!',2)
  with self.assertRaises(RuleError):self.c.login('nueva.persona','ClavePrueba123!',0)
  with self.assertRaises(RuleError):self.c.create_user('carlo',self.data(id='NUEVA.PERSONA'))
  user=next(u for u in self.c.users() if u['id']=='nueva.persona')
  self.assertNotIn('password',user);self.assertEqual(user['seller_code'],'FBV-NUEVA.PERSONA')
 def test_permission_and_invalid_inputs(self):
  count=len(self.c.users())
  with self.assertRaises(RuleError):self.c.create_user('melissa',self.data())
  for changes in [{'id':'a b'},{'name':''},{'branches':[]},{'branches':[3]},{'role':'unknown'},{'password':'short'}]:
   with self.assertRaises(RuleError):self.c.create_user('carlo',self.data(**changes))
  self.assertEqual(len(self.c.users()),count)
