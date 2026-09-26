'use strict';
function aggregateSales(events,catalog,users,kind){
 const map=new Map(),products=new Map(catalog.map(p=>[p.id,p])),names=new Map(users.map(u=>[u.id,u.name]));
 const get=(id,name,category='')=>{if(!map.has(id))map.set(id,{id,name,category,qty:0,gross:0,discount:0,net:0,cost:0,count:0,days:{}});return map.get(id);};
 const df=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Mexico_City',year:'numeric',month:'2-digit',day:'2-digit'});
 const add=(r,g,d,n,q,day,cost=0)=>{r.gross+=g;r.discount+=d;r.net+=n;r.qty+=q;r.cost+=cost;r.days[day]=(r.days[day]||0)+n;};
 const split=(v,n,i)=>Math.floor(v/n)+(i<v%n?1:0);
 for(const e of events){const p=e.adjusted||e.payload;if(!(e.kind==='sale'||kind==='bypayment'&&e.kind==='order_payment')||e.status!=='accepted'||p.cancelled)continue;const day=df.format(new Date(e.at));
  if(kind==='bypayment'){for(const [k,label] of [['cash','Efectivo'],['card','Tarjeta'],['transfer','Transferencia'],['credit','Saldo a favor']])if(p[k]>0){const r=get(k,label);add(r,p[k],0,p[k],0,day);r.count++;}continue;}
  if(kind==='byemployee'){const counted=new Set(),allocations=p.attributions||[{sellers:p.sellers?.length?p.sellers:[e.actor],amount:p.total}];for(const allocation of allocations){const ids=[...new Set(allocation.sellers)].sort();ids.forEach((id,i)=>{const r=get(id,names.get(id)||id||'Sin empleado'),n=split(allocation.amount,ids.length,i),d=split(p.discount,ids.length,i);add(r,n+d,d,n,0,day);if(!counted.has(id)){r.count++;counted.add(id);}});}continue;}
  const seen=new Set();for(const x of p.items){const product=products.get(x.id),category=x.category||product?.type||'Sin categoría',id=kind==='bycategory'?category:x.id,r=get(id,kind==='bycategory'?category:x.name,category);add(r,x.gross,x.discount,x.net,x.qty,day,(x.cost??product?.cost??0)*x.qty);if(x.cost===undefined&&(!product||product.cost===undefined))r.costUnknown=true;seen.add(id);}for(const id of seen)map.get(id).count++;
 }
 return [...map.values()].sort((a,b)=>b.net-a.net||a.name.localeCompare(b.name));
}
if(typeof module!=='undefined')module.exports={aggregateSales};
