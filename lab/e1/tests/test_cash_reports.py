import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from cash_reports import manual

def event(id,kind,p,at):return {'id':id,'kind':kind,'payload':p,'at':'2026-09-24T'+at+':00-06:00','actor_name':'Prueba','branch':1}
class CashReports(unittest.TestCase):
 def setUp(self):
  self.sale={'session':'o','gross':10000,'discount':0,'total':10000,'cash':10000,'card':0,'transfer':0}
  self.events=[event('o','open',{'opening':50000},'10:00'),event('s','sale',self.sale,'11:00'),event('m','move',{'session':'o','amount':1000,'reason':'Gasto','type':'Gasto'},'12:00')]
 def test_open_no_fabricated_count(self):
  r=manual(self.events,[])[0];self.assertEqual(r['expected'],59000);self.assertIsNone(r['counted']);self.assertIsNone(r['difference'])
 def test_closed_and_post_close_correction(self):
  self.events.append(event('c','close',{'session':'o','expected':59000,'counted':58500,'fund':50000,'envelope':8500},'15:00'))
  correction={'at':'2026-09-24T16:00:00-06:00','payload':{'session':'o','target':'s','before':self.sale,'after':{**self.sale,'cash':0,'card':10000},'replacement':None}}
  r=manual(self.events,[correction])[0];self.assertEqual(r['expected'],59000);self.assertEqual(r['difference'],-500);self.assertEqual(r['adjusted_expected'],49000);self.assertEqual(r['totals']['cash'],0)
 def test_cancellation_replacement_not_double_counted(self):
  replacement={**self.sale,'id':'R','total':8000,'gross':8000,'cash':8000}
  correction={'at':'2026-09-24T14:00:00-06:00','payload':{'session':'o','target':'s','before':self.sale,'after':{**self.sale,'cancelled':True},'replacement':replacement}}
  r=manual(self.events,[correction])[0];self.assertEqual(r['totals']['count'],1);self.assertEqual(r['totals']['total'],8000);self.assertEqual(r['expected'],57000)
if __name__=='__main__':unittest.main()
