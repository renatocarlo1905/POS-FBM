const assert=require('node:assert/strict');
const {aggregateSales}=require('../static/sales-model.js');
const sale={kind:'sale',status:'accepted',at:'2026-01-02T11:00:00-06:00',actor:'a',payload:{gross:101,discount:2,total:99,cash:49,card:50,transfer:0,sellers:['b','a'],items:[{id:'p',name:'Anillo',gross:101,discount:2,net:99,qty:1}]}};
const catalog=[{id:'p',type:'Anillos',cost:20}],users=[{id:'a',name:'A'},{id:'b',name:'B'}];
for(const kind of ['byitem','bycategory','byemployee','bypayment'])assert.equal(aggregateSales([sale],catalog,users,kind).reduce((s,r)=>s+r.net,0),99);
const employees=aggregateSales([sale],catalog,users,'byemployee');for(const r of employees)assert.equal(r.gross-r.discount,r.net);assert.equal(employees.reduce((s,r)=>s+r.gross,0),101);
assert.equal(aggregateSales([{...sale,adjusted:{...sale.payload,cancelled:true}}],catalog,users,'byitem').length,0);
const payments=aggregateSales([sale],catalog,users,'bypayment');assert.equal(payments.reduce((s,r)=>s+r.count,0),2);
const changed={...sale,adjusted:{...sale.payload,cash:0,card:99}};assert.equal(aggregateSales([changed],catalog,users,'bypayment')[0].net,99);
if(process.argv[2]){const f=require(process.argv[2]);for(const k of ['byitem','bycategory','byemployee','bypayment'])assert.equal(aggregateSales(f.events,f.catalog,f.users,k).reduce((s,r)=>s+r.net,0),568462900);}
console.log('OK: cuatro informes conciliados, centavos compartidos, anulaciones, pagos mixtos y correcciones.');
