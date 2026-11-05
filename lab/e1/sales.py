"""Sale calculation and payment validation."""
from decimal import Decimal, ROUND_HALF_UP
from domain import require, money, percent, cleantext
def calc_sale(data,products,policy,categories=None):
    require(policy.get('sell'),'Sin permiso para vender.')
    rate=percent(data.get('discount',0))
    require(not rate or policy.get('discount') and rate<=policy['max_discount'],'Descuento superior a tu autorización.')
    raw=data.get('items',[]);require(isinstance(raw,list) and 0<len(raw)<=100,'Agrega entre 1 y 100 partidas.')
    seen=set();items=[]
    for x in raw:
        require(isinstance(x,dict),'Partida inválida.')
        pid=x.get('id');q=x.get('qty');special=x.get('special');extra={}
        if special is not None:
            require(isinstance(pid,str) and pid.startswith('99-') and len(pid)==39 and isinstance(special,dict),'Partida 99 inválida.')
            import uuid
            try:uuid.UUID(pid[3:])
            except (ValueError,TypeError):require(False,'Identificador de partida 99 inválido.')
            name=cleantext(special.get('description',''),200);price=money(special.get('price',0))
            rows={str(c['id']):c for c in (categories or [])};cid=str(special.get('category_id',''));category=rows.get(cid)
            require(name and price>0 and category,'Completa descripción, categoría y precio mayor a cero para el código 99.')
            parent=category;visited=set()
            while parent.get('parent'):
                require(parent['id'] not in visited,'Categoría inválida.');visited.add(parent['id']);parent=rows.get(str(parent['parent']))
                require(parent,'Categoría inválida.')
            p={'id':pid,'name':'99 · '+name,'code':'99','price':price}
            extra={'non_inventory':True,'category_id':cid,'category':parent['name'],'subcategory':category['name'],'special':{'description':name,'price':str(Decimal(price)/100),'category_id':cid}}
        else:p=products.get(pid)
        require(p and p['id'] not in seen and type(q) is int and 1<=q<=1000,'Producto/cantidad inválidos o repetidos.')
        seen.add(p['id']);items.append({'id':p['id'],'name':p['name'],'code':p['code'],'qty':q,'price':p['price'],'gross':p['price']*q,**extra})
    gross=sum(x['gross'] for x in items)
    if 'discount_amount' in data:
        discount=money(data['discount_amount'])
        require(not discount or policy.get('discount') and discount*10000<=gross*policy['max_discount'],'Descuento superior a tu autorización.')
        rate=int((Decimal(discount)*10000/gross).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    else:
        discount=int((Decimal(gross)*rate/10000).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
    # Allocate rounded total discount by largest remainder, deterministic original line order.
    shares=[discount*x['gross']//gross for x in items];rem=discount-sum(shares)
    order=sorted(range(len(items)),key=lambda i:-(discount*items[i]['gross']%gross))
    for i in order[:rem]: shares[i]+=1
    for x,d in zip(items,shares):x.update(discount=d,net=x['gross']-d)
    total=gross-discount;require(total>0,'En E1 el total debe ser mayor a cero.')
    cash=money(data.get('cash',0));card=money(data.get('card',0));transfer=money(data.get('transfer',0))
    require(card+transfer<=total and cash+card+transfer>=total,'Pago insuficiente o cambio originado en medios distintos al efectivo.')
    bank=cleantext(data.get('bank',''),80);last4=cleantext(data.get('last4',''),4);reference=cleantext(data.get('reference',''),100)
    require(not card or bank and len(last4)==4 and last4.isascii() and last4.isdigit(),'Completa banco y últimos cuatro dígitos.')
    require(not transfer or reference,'La transferencia requiere referencia.')
    return {'items':items,'gross':gross,'discount':discount,'rate':rate,'total':total,'cash':total-card-transfer,'received_cash':cash,'change':cash-(total-card-transfer),'card':card,'transfer':transfer,'bank':bank,'last4':last4,'reference':reference}
