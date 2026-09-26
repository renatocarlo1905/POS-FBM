"""Isolated, read-only order fixtures and branded example receipt PDFs."""
import io,json
from datetime import datetime
from pathlib import Path
from core import require
ROOT=Path(__file__).parent

def receipts(order):
 copies=['Cliente','Local'] if order['kind']=='layaway' else ['Cliente','Negocio','Con las piezas']
 result=[{'id':p['id'],'label':p['kind'],'at':p['at'],'copies':['Cliente','Negocio'] if order['kind']=='repair' and i else copies,'payment':p} for i,p in enumerate(order['payments'])]
 if order['delivery']:result.append({'id':order['delivery']['receipt'],'label':'Entrega','at':order['delivery']['at'],'copies':['Cliente','Negocio']})
 if order['status'] in ('cancelled','released'):result.append({'id':order['id']+'-CIERRE','label':'Cancelación' if order['status']=='cancelled' else 'Liberación autorizada','at':order['history'][-1]['at'],'copies':['Cliente','Local'] if order['kind']=='layaway' else ['Registro interno']})
 return result

def document(order_id,index):
 data=json.loads((ROOT/'orders_demo.json').read_text());order=next((o for o in data['rows'] if o['id']==order_id),None);require(order,'Orden de ejemplo inexistente.')
 docs=receipts(order);require(type(index)is int and 0<=index<len(docs),'Comprobante de ejemplo inexistente.')
 return order,docs[index]

def receipt_pdf(order_id,index,source=None):
 from reportlab.pdfgen.canvas import Canvas
 from reportlab.pdfbase.pdfmetrics import registerFont,stringWidth
 from reportlab.pdfbase.ttfonts import TTFont
 from reportlab.lib.colors import HexColor
 order,doc=document(order_id,index) if source is None else (source,receipts(source)[index])
 registerFont(TTFont('OrderSans',str(ROOT/'static/Montserrat-Regular.ttf')));registerFont(TTFont('OrderBold',str(ROOT/'static/Montserrat-Bold.ttf')))
 buffer=io.BytesIO();canvas=Canvas(buffer);canvas.setTitle('SIMULADO - '+doc['id']);width=80*72/25.4;margin=14;usable=width-margin*2
 fmt=lambda v:f'${v/100:,.2f} MXN'
 paid=sum(p['amount'] for p in order['payments'] if p['at']<=doc['at'])-order.get('credit_issued',0);budget=order['total']
 if order['kind']=='repair':budget=[b['after'] for b in order['budget_history'] if b['at']<=doc['at']][-1]
 for copy in doc['copies']:
  lines=[]
  def add(text,bold=False):
   font='OrderBold' if bold else 'OrderSans';size=8
   for paragraph in str(text).split('\n'):
    current=''
    for word in paragraph.split():
     candidate=(current+' '+word).strip()
     if current and stringWidth(candidate,font,size)>usable:
      lines.append((current,font,size));current=''
     while stringWidth(word,font,size)>usable:
      split=1
      while split<len(word) and stringWidth(word[:split+1],font,size)<=usable:split+=1
      lines.append((word[:split],font,size));word=word[split:]
     current=(current+' '+word).strip()
    lines.append((current,font,size))
  add('FRIDA BLANCAS MÉXICO',True);add('Joyería Artesanal');add('SIMULADO - SIN VALIDEZ OPERATIVA' if order.get('simulated',True) else 'LABORATORIO - OPERACIÓN DE PRUEBA',True);add('Copia: '+copy,True)
  add(('APARTADO' if order['kind']=='layaway' else 'REPARACIÓN')+' - '+doc['label'].upper(),True)
  add('Folio: '+doc['id']);add('Orden: '+order['id']);add(datetime.fromisoformat(doc['at']).strftime('%d/%m/%Y %H:%M')+' · Ciudad de México')
  event=doc.get('payment') or order['delivery'] or {'branch':order['branch'],'actor':order['history'][-1]['actor']}
  add('Sucursal del movimiento: '+str(event['branch']));add('Atendió: '+event['actor']);add('Sucursal de registro: '+str(order['branch']))
  add('');add('Cliente: '+order['customer']['name']);add('Teléfono: '+order['customer']['phone']);add('PIEZAS',True)
  for item in order['items']:
   add(str(item['qty'])+' × '+item['name'])
   if 'price' in item:add('Precio al registro: '+fmt(item['price']))
  if order['kind']=='repair':add('Piezas propiedad del cliente, fuera del inventario de venta.');add('Trabajo: '+order['work']);add('Entrega prevista: '+order['expected_delivery'])
  add('');add(('Presupuesto a esta fecha: ' if order['kind']=='repair' else 'Total acordado: ')+fmt(budget),True)
  if 'payment' in doc:add(doc['label']+': '+fmt(doc['payment']['amount']),True);add('Medio: '+doc['payment']['method'])
  if 'payment' in doc:
   p=doc['payment']
   if p.get('card'):add('Banco: '+p.get('bank','')+' · Últimos dígitos: '+p.get('last4',''))
   if p.get('transfer'):add('Referencia: '+p.get('reference',''))
   if 'received_cash' in p:add('Efectivo recibido: '+fmt(p['received_cash']));add('Cambio: '+fmt(p['change']))
  add('Pagado a esta fecha: '+fmt(paid));add(('Saldo al cierre, no cobrable: ' if doc['label'] in ('Cancelación','Liberación autorizada') else 'Saldo pendiente: ')+fmt(max(0,budget-paid)),True)
  if order['kind']=='layaway':add('Plazo de pago: '+order['due']+' al final del día.');add('Vendedores originales: '+', '.join(order['sellers']))
  else:
   add('Matanga - sin asignación. Sin comisión comercial.')
   if order['ready'] and order['ready']<=doc['at']:add('Recogida hasta: '+order['due']+' al final del día.')
  if order.get('conversion'):
   add('Mercancía por cancelación',True)
   for item in order['conversion']['items']:add(str(item['qty'])+' × '+item['name'])
   add('Valor aplicado: '+fmt(order['conversion']['applied']));add('Diferencia: '+fmt(order['conversion']['difference']))
   if order.get('conversion_payment'):add('Medios de la diferencia: '+order['conversion_payment']['method'])
  if doc['label']=='Entrega':add('Entrega del conjunto completo; no registra otro cobro.')
  if doc['label'] in ('Cancelación','Liberación autorizada'):add(order['history'][-1]['note'])
  if order['kind']=='repair' and ((doc['label']=='Entrega' and copy=='Negocio') or doc['label']=='Cancelación'):
   add('');add('Firma de conformidad / recepción:');add('');add('____________________________');add('Nombre: ____________________')
  add('');add('DOCUMENTO FICTICIO DE CONSULTA' if order.get('simulated',True) else 'COMPROBANTE DE PRUEBA',True);add('No registra pagos, reservas ni entregas.' if order.get('simulated',True) else 'Movimiento registrado en el laboratorio local.');add('Descargar de nuevo no duplica operaciones.');add('Gracias por tu visita.')
  height=155+sum(size+4 for _,_,size in lines)+25;canvas.setPageSize((width,height))
  from branding import draw_brand
  draw_brand(canvas,width,height-14)
  y=height-150
  for text,font,size in lines:
   canvas.setFillColor(HexColor('#434345'));canvas.setFont(font,size);canvas.drawString(margin,y,text);y-=size+4
  canvas.setStrokeColor(HexColor('#b87923'));canvas.line(margin,14,width-margin,14);canvas.showPage()
 canvas.save();return buffer.getvalue(),doc['id']+'.pdf'
