const assert=require('node:assert/strict');
const D=require('./domain.js');
let count=0;function test(name,fn){fn();count++;console.log('PASS '+name);}
test('Dinero exacto, coma y rechazo de precisión ambigua',()=>{assert.equal(D.cents('1000.25'),100025);assert.equal(D.cents('0,10'),10);for(const v of ['-1','NaN','1.001','1e3',''])assert.throws(()=>D.cents(v));});
test('Pago mixto separa cambio y efectivo aplicado',()=>assert.deepEqual(D.payment(100000,50000,60000),{cash:40000,received:50000,change:10000,card:60000,transfer:0,total:100000}));
test('No producir cambio con tarjeta ni aceptar pago insuficiente',()=>{assert.throws(()=>D.payment(10000,0,11000));assert.throws(()=>D.payment(10000,9000));});
test('Disponibilidad conocida bloquea faltante y vacío',()=>{assert.equal(D.stock([{id:'a',qty:1}],[{id:'a',available:1,price:100}]),100);assert.throws(()=>D.stock([{id:'a',qty:2}],[{id:'a',available:1,price:100}]));assert.throws(()=>D.stock([],[]));});
test('Apartado permite abono positivo hasta saldo, solo online',()=>{const o={kind:'layaway',total:100000,paid:40000};assert.equal(D.orderPayment(o,20000,true).paid,60000);assert.equal(o.paid,40000);assert.throws(()=>D.orderPayment(o,70000,true));assert.throws(()=>D.orderPayment(o,100,false));});
test('Reparación no permite abonos intermedios',()=>{const o={kind:'repair',total:100000,paid:50000};assert.throws(()=>D.orderPayment(o,20000,true));assert.equal(D.orderPayment(o,50000,true).paid,100000);});
test('COR-17 bloquea economía liquidada',()=>assert.throws(()=>D.orderPayment({kind:'layaway',total:1000,paid:1000},1,true),/COR-17/));
test('Entrega exige POS, conexión, liquidación y trabajo listo',()=>{const o={kind:'repair',total:1000,paid:1000,status:'Lista para entregar',delivered:false};assert.throws(()=>D.deliver(o,true,'admin'));assert.throws(()=>D.deliver(o,false,'pos'));assert.throws(()=>D.deliver({...o,status:'Recibida'},true,'pos'));assert.throws(()=>D.deliver({...o,paid:500},true,'pos'));assert.equal(D.deliver(o,true,'pos').delivered,true);assert.throws(()=>D.deliver({...o,delivered:true},true,'pos'));});
test('Cierre acepta faltante pero valida distribución',()=>{assert.equal(D.closeCash(75000,73000,30000,43000).difference,-2000);assert.throws(()=>D.closeCash(75000,73000,30000,45000));});
console.log(`${count} grupos de reglas del prototipo verificados. No valida backend, persistencia ni dispositivos.`);
