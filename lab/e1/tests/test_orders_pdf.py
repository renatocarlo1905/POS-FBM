import io,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import orders_preview as orders
from pypdf import PdfReader
class Receipts(unittest.TestCase):
 def test_all_receipts(self):
  fixture=json.loads((orders.ROOT/'orders_demo.json').read_text())
  js=(orders.ROOT/'static/orders-demo.js').read_text()
  self.assertEqual(json.loads(js.split('const ORDER_DEMO=',1)[1].split(';\n',1)[0]),fixture)
  for order in fixture['rows']:
   for i,doc in enumerate(orders.receipts(order)):
    with self.subTest(id=order['id'],index=i):
     body,name=orders.receipt_pdf(order['id'],i);pdf=PdfReader(io.BytesIO(body))
     self.assertEqual(len(pdf.pages),len(doc['copies']))
     for page,copy in zip(pdf.pages,doc['copies']):
      text=page.extract_text();self.assertIn('SIMULADO',text);self.assertIn(copy,text);self.assertIn(doc['id'],text)
 def test_bad_document(self):
  for key,index in [('missing',0),('SIM-APA-001',-1),('SIM-APA-001',True),('SIM-APA-001',999)]:
   with self.assertRaises(Exception):orders.document(key,index)
if __name__=='__main__':unittest.main()
