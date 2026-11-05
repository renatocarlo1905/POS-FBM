"""Receipt templates and PDF rendering."""
import base64, io
from pathlib import Path
from datetime import datetime
from domain import require, RuleError, cleantext
def template(value):
    out={k:cleantext(value.get(k,''),500) for k in ('header','footer')}
    out['width']=int(value.get('width',80));require(out['width'] in (58,80),'Elige 58 u 80 mm.')
    out['logo']=value.get('logo','')
    if out['logo']:
        require(isinstance(out['logo'],str) and len(out['logo'])<400000,'Logotipo demasiado grande (máximo 250 KB).')
        require(out['logo'].startswith(('data:image/png;base64,','data:image/jpeg;base64,')),'Usa PNG o JPEG.')
        from PIL import Image
        try:
            raw=base64.b64decode(out['logo'].split(',')[1],validate=True)
            with Image.open(io.BytesIO(raw)) as im:
                require(im.width<=2000 and im.height<=2000,'Logo máximo 2000 × 2000 píxeles.'); im.verify()
        except RuleError: raise
        except Exception: raise RuleError('Imagen no válida.')
    return out

def receipt_pdf(event,reprint=False):
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import ImageReader
    from reportlab.lib.colors import HexColor
    from reportlab.pdfbase.pdfmetrics import stringWidth, registerFont
    from reportlab.pdfbase.ttfonts import TTFont
    registerFont(TTFont('E1Sans',str(Path(__file__).parent/'static/Montserrat-Regular.ttf')))
    registerFont(TTFont('E1Bold',str(Path(__file__).parent/'static/Montserrat-Bold.ttf')))
    t=event.get('template') or template({});width=t['width']*72/25.4;usable=width-24
    lines=[]
    def add(text,bold=False,size=9):
        for paragraph in str(text).splitlines() or ['']:
            words=paragraph.split();line=''
            for word in words:
                # Hard-wrap long tokens as well as ordinary prose.
                for part in [word[i:i+28] for i in range(0,len(word),28)]:
                    candidate=(line+' '+part).strip()
                    if line and stringWidth(candidate,'E1Bold' if bold else 'E1Sans',size)>usable:lines.append((line,bold,size));line=part
                    else:line=candidate
            lines.append((line,bold,size))
    p=event['payload'];fmt=lambda n:f'${n/100:,.2f}'
    cancellation=event['kind']=='correction' and p['action']=='cancel'
    compact=cancellation or event['kind'] in ('move','open','close')
    if compact:
        add(t['header'].splitlines()[0] if t['header'] else 'Frida Blancas México',True,10)
        title='TICKET DE CANCELACIÓN' if cancellation else {'move':str(p.get('type','Movimiento')).upper()+' DE CAJA','open':'APERTURA DE CAJA','close':'CIERRE DE CAJA'}[event['kind']]
        add(title,True,10)
        add(f"Sucursal {event['branch']} · "+datetime.fromisoformat(event['at']).strftime('%d/%m/%Y %H:%M'))
        if not cancellation:
            if reprint:add('COPIA',True,8)
            add('Ref. '+__import__('folios').code(event),size=8)
            add('Responsable: '+event['actor_name'])
    else:
        add(t['header'],True,11);add('COMPROBANTE DE VENTA' if event.get('simulation_batch')=='history-through-20261103-v1' else 'COMPROBANTE DE PRUEBA',True,9)
        if reprint:add('COPIA / REIMPRESIÓN',True)
        add(f"Sucursal {event['branch']} · { {'sale':'VENTA','open':'APERTURA','move':'MOVIMIENTO','close':'CIERRE','exchange':'CAMBIO DE MERCANCÍA','correction':'CORRECCIÓN INTERNA'}[event['kind']] }");add(datetime.fromisoformat(event['at']).strftime('%d/%m/%Y %H:%M:%S'));add('Código '+__import__('folios').code(event));add('Atendió: '+event['actor_name']);add('-'*24)
    if event['kind']=='sale':
        for x in p['items']:add(f"{x['qty']} x {x['name']}");add(f"{fmt(x['price'])} c/u · Neto {fmt(x['net'])}")
        add('-'*24)
        for label,k in [('Subtotal','gross'),('Descuento','discount'),('TOTAL','total'),('Efectivo','cash'),('Tarjeta','card'),('Transferencia','transfer')]:add(label+': '+fmt(p[k]),k=='total',11 if k=='total' else 9)
        if p.get('card',0)>0:
            add('Banco: '+(p.get('bank') or 'No registrado'))
            last4=str(p.get('last4') or '')
            add('Tarjeta terminación: '+(last4 if len(last4)==4 and last4.isascii() and last4.isdigit() else 'No registrada'))
    elif event['kind']=='exchange':
        add('Venta de origen: '+p.get('target_code',p['target']));add('Fecha de origen: '+p['source_at']);add('Motivo: '+p['reason']);add('PIEZAS RECIBIDAS',True)
        for x in p['returned']:add(f"{x['qty']} x {x['name']} · {fmt(x['net'])}")
        add('Valor reconocido: '+fmt(p['credit']));add('PIEZAS ENTREGADAS',True)
        for x in p['new']['items']:add(f"{x['qty']} x {x['name']} · {fmt(x['net'])}")
        add('Descuento mercancía nueva: '+fmt(p['new']['discount']));add('Total mercancía nueva: '+fmt(p['new']['total']));add('DIFERENCIA: '+fmt(p['difference']),True)
        for label,k in [('Efectivo recibido','received_cash'),('Efectivo aplicado','cash'),('Tarjeta','card'),('Transferencia','transfer'),('Cambio','change')]:add(label+': '+fmt(p['new'][k]))
        add('Vendedores de la diferencia: '+', '.join(p['new']['sellers']));add('Sin devolución de dinero. Se conserva la venta y cierre original.');add('Conservar comprobante para cliente y local.')
        if any(x.get('non_inventory') for x in p['returned']):add('Código 99 recibido: sin ingreso a inventario; aviso al administrador.')
    elif event['kind']=='correction':
        if cancellation:
            add('Venta anulada: '+p.get('target_code',p['target']))
            add('Importe cancelado: '+fmt(p['before']['total'])+' MXN',True)
            add('Motivo: '+p['reason'])
            add('Canceló: '+p['operator'])
            if p['authorizer']!=p['operator']:add('Autorizó: '+p['authorizer'])
        else:
            add('Operación original: '+p.get('target_code',p['target']));add('Fecha original: '+datetime.fromisoformat(p['original_at']).strftime('%d/%m/%Y %H:%M:%S'));add('Acción: '+{'payment':'Corregir pago','sellers':'Corregir vendedores','cancel':'Anular venta','replace':'Anular y reemplazar'}[p['action']]);add('Motivo: '+p['reason']);add('Operador: '+p['operator']);add('Autorizador: '+p['authorizer']);add('Importe original: '+fmt(p['before']['total']));add('No representa entrega ni devolución de dinero.');
            for label,key in [('Efectivo','cash'),('Tarjeta','card'),('Transferencia','transfer')]:add(label+': '+fmt(p['before'][key])+' -> '+fmt(0 if p['after']['cancelled'] else p['after'][key]))
            add('Vendedores: '+', '.join(p['before']['sellers'])+' -> '+('Sin atribución' if p['after']['cancelled'] else ', '.join(p['after']['sellers'])))
            if p['replacement']:add('Reemplazo vinculado: '+p['replacement']['id']);add('Importe correcto: '+fmt(p['replacement']['total']))
    elif event['kind']=='open':add('Fondo inicial: '+fmt(p['opening'])+' MXN',True)
    elif event['kind']=='move':add('Importe: '+fmt(p['amount'])+' MXN',True);add('Concepto: '+p['reason'])
    else:
        add(('Dinero no anotado: ' if p['difference']>0 else 'Dinero faltante: ' if p['difference']<0 else 'Caja cuadrada: ')+fmt(abs(p['difference'])),True)
        for k,label in [('expected','Esperado'),('counted','Contado'),('difference','Diferencia'),('fund','Fondo siguiente'),('envelope','Sobre')]:add(label+': '+fmt(p[k]))
    if not compact:
        add('-'*24);add(t['footer']);add('MXN · Laboratorio E1')
    logo=None if compact else t.get('logo');brand_logo=bool(logo and logo=='data:image/png;base64,'+base64.b64encode((Path(__file__).parent/'static/company-logo.png').read_bytes()).decode());height=36+sum(s+5 for _,_,s in lines)+(min(usable,150)+8 if logo else 0)
    stream=io.BytesIO();c=canvas.Canvas(stream,pagesize=(width,height));c.setTitle('Comprobante E1 '+__import__('folios').code(event));y=height-18
    if brand_logo:
        from branding import draw_brand
        y-=draw_brand(c,width,y)+8
    elif logo:
        size=min(usable,150);c.drawImage(ImageReader(io.BytesIO(base64.b64decode(logo.split(',')[1]))),(width-size)/2,y-size,size,size,preserveAspectRatio=True,anchor='c',mask='auto');y-=size+8
    c.setFillColor(HexColor('#434345'))
    for text,bold,size in lines:c.setFont('E1Bold' if bold else 'E1Sans',size);c.drawString(12,y-size,text);y-=size+5
    c.save();return stream.getvalue()
