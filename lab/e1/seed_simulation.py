#!/usr/bin/env python3
"""Genera datos ficticios reproducibles. Reejecutar no duplica el lote existente."""
import collections, datetime as dt, hashlib, json, random, uuid
from pathlib import Path
from zoneinfo import ZoneInfo
from core import Central, calc_sale, pack
import extensions as ext
import simulated

ROOT=Path(__file__).resolve().parent
BATCH='demo-2026-enero-septiembre-v1'
TZ=ZoneInfo('America/Mexico_City')
PRODUCTS=[
 ('Anillo luna creciente',1,1,480,180,'2.100'),('Anillo trenzado',1,1,650,250,'3.200'),
 ('Anillo flor de loto',1,1,890,360,'4.500'),('Anillo sol dorado',3,1,390,130,'3.800'),
 ('Aretes hoja pequeña',1,2,520,195,'2.900'),('Aretes colibrí',1,2,780,310,'4.200'),
 ('Aretes geometría',4,2,290,95,'3.000'),('Aretes cascada',1,2,1150,480,'6.700'),
 ('Dije corazón artesanal',1,3,430,160,'2.400'),('Dije mariposa',1,3,610,240,'3.600'),
 ('Dije obsidiana',3,3,740,280,'7.300'),('Dije estrella de oro',2,3,3900,2350,'1.600'),
 ('Pulsera eslabón fino',1,4,980,410,'8.200'),('Pulsera espiral',3,4,460,155,'9.100'),
 ('Pulsera flores',1,4,1450,620,'11.300'),('Pulsera ajustable',4,4,320,110,'6.600'),
 ('Collar luna y estrellas',1,5,1680,740,'12.500'),('Collar piedra turquesa',1,5,2100,930,'16.200'),
 ('Collar ramas',3,5,860,310,'14.700'),('Collar oro delicado',2,5,6800,4250,'2.800'),
 ('Anillo amatista',1,1,1250,530,'5.100'),('Aretes perla cultivada',1,2,1320,570,'5.800'),
 ('Dije árbol de la vida',1,3,690,270,'4.100'),('Pulsera nudo infinito',1,4,1180,490,'9.600')]

def ident(key):return str(uuid.uuid5(uuid.NAMESPACE_URL,BATCH+':'+key))

def generate(products, users, cutoff):
    rng=random.Random(20260925);result=[];date=dt.date(2026,1,1)
    policy={'sell':True,'discount':True,'max_discount':3000}
    while date<=cutoff.date():
        for branch in (1,2):
            # Variación semanal, crecimiento gradual y campañas estacionales ficticias.
            base=rng.randint(2,6)+(2 if date.weekday()>=4 else 0)+(date.month//3)
            if (date.month==2 and 10<=date.day<=14) or (date.month==5 and 5<=date.day<=10):base+=5
            if branch==2:base=max(1,base-1)
            if date.weekday()==0 and date.day%3==0:base=0
            seconds=sorted(rng.sample(range(10*3600,20*3600),base))
            for index,sec in enumerate(seconds):
                at=dt.datetime.combine(date,dt.time(),TZ)+dt.timedelta(seconds=sec)
                if at>cutoff:continue
                actor=users[(date.toordinal()+branch+index)%len(users)]
                chosen=rng.sample(products,rng.choices([1,2,3],[70,25,5])[0])
                items=[{'id':p['id'],'qty':rng.choices([1,2,3],[88,10,2])[0]} for p in chosen]
                gross=sum(next(p['price'] for p in products if p['id']==x['id'])*x['qty'] for x in items)
                discount=rng.choices([0,5,10,15,20],[65,12,15,6,2])[0]
                total=gross-(gross*discount+50)//100
                method=rng.choices(['cash','card','transfer','mixed'],[40,35,15,10])[0]
                card=total if method=='card' else (total//2 if method=='mixed' else 0)
                transfer=total if method=='transfer' else 0
                cash=total-card-transfer
                received=((cash+9999)//10000)*10000 if cash else 0
                request={'items':items,'discount':str(discount),'cash':str(received/100),'card':str(card/100),'transfer':str(transfer/100),'bank':'Banco ficticio' if card else '', 'last4':str(rng.randrange(10000)).zfill(4) if card else '', 'reference':'SIM-'+ident(f'{date}:{branch}:{index}')[:12] if transfer else ''}
                payload=calc_sale(request,{p['id']:p for p in products},policy)
                sellers=[actor['id']]
                if rng.random()<.13:sellers.append(rng.choice([u['id'] for u in users if u['id']!=actor['id']]))
                payload.update(sellers=sellers,session='SIM-SESION-'+str(date)+'-'+str(branch))
                result.append({'id':'SIM-'+ident(f'{date}:{branch}:{index}'),'kind':'sale','branch':branch,'actor':actor['id'],'actor_name':actor['name'],'at':at.isoformat(),'payload':payload,'status':'accepted','issue':'Historial simulado · Sin efecto en caja o existencias actuales','simulated':True,'simulation_batch':BATCH})
        date+=dt.timedelta(days=1)
    return result

def main():
    c=Central(ROOT/'data/postgres.json');simulated.init(c)
    existing=c.get('simulation-manifest:'+BATCH)
    if existing:
        print(json.dumps({'already_loaded':True,**existing},ensure_ascii=False,indent=2));return
    cutoff=dt.datetime.now(TZ)
    assert cutoff.year==2026,'Este generador es específico para el escenario de 2026.'
    c.backup(ROOT/'data/backups/pre-simulation-2026.dump')
    before=[(r['id'],r['hash']) for r in c.events()]
    products=[]
    for i,(name,m,t,price,cost,weight) in enumerate(PRODUCTS):
        r=ext.create_product(c,'carlo',{'request_id':ident('product:'+str(i)),'name':name+' · Ficticio','description':'Producto ficticio para pruebas del POS. '+name+'. No corresponde a mercancía real.','material_id':m,'type_id':t,'provider':1,'price':str(price),'cost':str(cost),'weight':weight,'quantity':80,'warehouse':'coyoacan','sub1':'Colección simulada 2026','sub2':'Pruebas','print_price':True})
        products.append(r['product'])
    users=c.users();events=generate(products,users,cutoff)
    assert len({e['id'] for e in events})==len(events)
    assert all(dt.datetime(2026,1,1,tzinfo=TZ)<=dt.datetime.fromisoformat(e['at'])<=cutoff for e in events)
    for e in events:
        p=e['payload'];assert p['total']==p['cash']+p['card']+p['transfer']==p['gross']-p['discount']
        assert sum(x['net'] for x in p['items'])==p['total']
    monthly=collections.Counter();by_user=collections.Counter();by_branch=collections.Counter()
    for e in events:monthly[e['at'][:7]]+=1;by_user[e['actor_name']]+=1;by_branch[e['branch']]+=1
    manifest={'batch':BATCH,'from':'2026-01-01','through':cutoff.isoformat(),'sales':len(events),'products_added':len(products),'units_per_product':80,'gross_cents':sum(e['payload']['gross'] for e in events),'discount_cents':sum(e['payload']['discount'] for e in events),'net_cents':sum(e['payload']['total'] for e in events),'by_month':dict(sorted(monthly.items())),'by_user':dict(by_user),'by_branch':dict(by_branch),'product_ids':[p['id'] for p in products]}
    c.db.execute('BEGIN IMMEDIATE')
    try:
        for e in events:c.db.execute('INSERT INTO simulated_sales VALUES(?,?,?)',(e['id'],BATCH,pack(e)))
        template=c.get('templates')['1'].copy();template['header']='FRIDA BLANCAS MÉXICO\nHISTORIAL SIMULADO 2026';template['footer']='DATOS FICTICIOS · SIN VALIDEZ FISCAL\nNo representa cobro ni movimiento de inventario.'
        c.put('simulation-template:'+BATCH,template);c.put('simulation-manifest:'+BATCH,manifest)
        c.audit('carlo','simulation_loaded',manifest);c.db.execute('COMMIT')
    except Exception:c.db.execute('ROLLBACK');raise
    assert before==[(r['id'],r['hash']) for r in c.events()],'Las operaciones previas deben permanecer intactas.'
    assert len(simulated.sales(c))==len(events)
    c.backup(ROOT/'data/backups/post-simulation-2026.dump')
    dest=ROOT.parents[1]/'docs/e1/datos-simulados-2026.json';dest.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(manifest,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
