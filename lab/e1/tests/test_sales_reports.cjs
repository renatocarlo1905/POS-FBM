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

const mixedCatalog=[{id:'silver',type:'Anillos',category_id:'ring',material_id:1,cost:10},{id:'gold',type:'Anillos',category_id:'ring',material_id:2,cost:20}];
const mixedSale={...sale,payload:{...sale.payload,items:[{id:'silver',name:'Plata',gross:200,discount:20,net:180,qty:2},{id:'gold',name:'Oro',gross:500,discount:50,net:450,qty:1}]}};
const silver=aggregateSales([mixedSale],mixedCatalog,users,'bycategory',{material:'1',category:'ring',categoryIds:['ring']});
assert.equal(silver.length,1);assert.equal(silver[0].net,180);assert.equal(silver[0].discount,20);assert.equal(silver[0].qty,2);assert.equal(silver[0].count,1);
assert.equal(aggregateSales([mixedSale],mixedCatalog,users,'bycategory',{material:'3'}).length,0);
assert.equal(aggregateSales([mixedSale],mixedCatalog,users,'bycategory',{material:'1',category:'other',categoryIds:['other']}).length,0);
assert.equal(aggregateSales([sale],catalog,users,'bycategory',{material:'unknown'})[0].net,99);
console.log('OK: filtros combinados por partida, material ausente y descuentos proporcionales conservados.');
const specialSale={...sale,payload:{...sale.payload,items:[{id:'99-test',code:'99',name:'99 · Dije especial',non_inventory:true,category_id:'dije',category:'Dijes',qty:2,gross:25100,discount:100,net:25000}]}};
const specialCategory=aggregateSales([specialSale],[],users,'bycategory',{category:'dije',categoryIds:['dije']});
assert.equal(specialCategory[0].name,'Dijes');assert.equal(specialCategory[0].net,25000);assert.equal(specialCategory[0].costUnknown,true);
assert.equal(aggregateSales([specialSale],[],users,'byitem')[0].name,'99 · Dije especial');
console.log('OK: partidas 99 conservan categoría, descripción e importe sin asumir costo cero.');
// A commercial exchange offsets the returned value and attributes only the new difference.
const originalExchangeSale={...sale,payload:{...sale.payload,total:101,gross:103,discount:2,sellers:['a','b'],cash:101,card:0,items:[{id:'old',name:'Anterior',qty:1,gross:103,discount:2,net:101}]}};
const receivedExchange={...sale,payload:{...originalExchangeSale.payload,total:-101,gross:-103,discount:-2,cash:0,items:[{id:'old',name:'Anterior',qty:-1,gross:-103,discount:-2,net:-101}],attributions:[{sellers:['a','b'],amount:-101}]}};
const deliveredExchange={...sale,payload:{...sale.payload,total:151,gross:154,discount:3,cash:50,card:0,sellers:['c'],items:[{id:'new',name:'Nueva',qty:1,gross:154,discount:3,net:151}],attributions:[{sellers:['a','b'],amount:101},{sellers:['c'],amount:50}]}};
const exchanged=[originalExchangeSale,receivedExchange,deliveredExchange];
assert.equal(aggregateSales(exchanged,[],[],'byitem').reduce((n,r)=>n+r.net,0),151);
assert.equal(aggregateSales(exchanged,[],[],'bypayment')[0].net,151);
const attributedExchange=aggregateSales(exchanged,[],[],'byemployee');assert.equal(attributedExchange.find(r=>r.id==='a').net,51);assert.equal(attributedExchange.find(r=>r.id==='b').net,50);assert.equal(attributedExchange.find(r=>r.id==='c').net,50);
assert.equal(attributedExchange.reduce((n,r)=>n+r.discount,0),3);
console.log('OK: cambios comerciales, importes negativos, atribución y centavos conciliados.');
