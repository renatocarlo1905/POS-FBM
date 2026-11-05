'use strict';
function aggregateSales(events,catalog,users,kind,filters={}){
 const map=new Map(),products=new Map(catalog.map(p=>[p.id,p])),names=new Map(users.map(u=>[u.id,u.name]));
 const get=(id,name,category='')=>{if(!map.has(id))map.set(id,{id,name,category,qty:0,gross:0,discount:0,net:0,cost:0,count:0,days:{}});return map.get(id);};
 const df=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Mexico_City',year:'numeric',month:'2-digit',day:'2-digit'});
 const add=(r,g,d,n,q,day,cost=0)=>{r.gross+=g;r.discount+=d;r.net+=n;r.qty+=q;r.cost+=cost;r.days[day]=(r.days[day]||0)+n;};
 const split=(v,n,i)=>Math.sign(v)*(Math.floor(Math.abs(v)/n)+(i<Math.abs(v)%n?1:0));
 for(const e of events){const p=e.adjusted||e.payload;if(!(e.kind==='sale'||kind==='bypayment'&&e.kind==='order_payment')||e.status!=='accepted'||p.cancelled)continue;const day=df.format(new Date(e.at));
  if(kind==='bypayment'){for(const [k,label] of [['cash','Efectivo'],['card','Tarjeta'],['transfer','Transferencia'],['credit','Saldo a favor']])if(p[k]>0){const r=get(k,label);add(r,p[k],0,p[k],0,day);r.count++;}continue;}
  if(kind==='byemployee'){const counted=new Set(),allocations=p.attributions||[{sellers:p.sellers?.length?p.sellers:[e.actor],amount:p.total}];const weights=allocations.map(a=>Math.abs(a.amount)),weightTotal=weights.reduce((a,b)=>a+b,0),ds=weights.map(w=>weightTotal?Math.floor(Math.abs(p.discount)*w/weightTotal):0);for(const j of weights.map((_,i)=>i).sort((a,b)=>(Math.abs(p.discount)*weights[b]%weightTotal)-(Math.abs(p.discount)*weights[a]%weightTotal)).slice(0,Math.abs(p.discount)-ds.reduce((a,b)=>a+b,0)))ds[j]++;for(const [ai,allocation] of allocations.entries()){const ids=[...new Set(allocation.sellers)].sort();ids.forEach((id,i)=>{const r=get(id,names.get(id)||id||'Sin empleado'),n=split(allocation.amount,ids.length,i),d=split(ds[ai]*Math.sign(p.discount),ids.length,i);add(r,n+d,d,n,0,day);if(!counted.has(id)){r.count++;counted.add(id);}});}continue;}
  const seen=new Set();for(const x of p.items){const product=products.get(x.id);if(filters.material&&filters.material!=='all'&&String(x.material_id??product?.material_id??'unknown')!==filters.material)continue;if(filters.category&&filters.category!=='all'&&!filters.categoryIds?.includes(String(x.category_id??product?.category_id??product?.type_id??'')))continue;const category=x.category||product?.type||'Sin categoría',id=kind==='bycategory'?category:x.id,r=get(id,kind==='bycategory'?category:x.name,category);add(r,x.gross,x.discount,x.net,x.qty,day,(x.cost??product?.cost??0)*x.qty);if(x.cost===undefined&&(!product||product.cost===undefined))r.costUnknown=true;seen.add(id);}for(const id of seen)map.get(id).count++;
 }
 return [...map.values()].sort((a,b)=>b.net-a.net||a.name.localeCompare(b.name));
}
if(typeof module!=='undefined')module.exports={aggregateSales};
