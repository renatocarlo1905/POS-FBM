/* E0: pure rules for an in-memory demonstrator, not production authorization. */
(function(root){
'use strict';
function cents(value){
 const s=String(value).trim().replace(',','.');
 if(!/^\d+(\.\d{1,2})?$/.test(s)) throw Error('Introduce un importe positivo con hasta dos decimales.');
 const [a,b='']=s.split('.'); const n=Number(a)*100+Number(b.padEnd(2,'0'));
 if(!Number.isSafeInteger(n)) throw Error('Importe fuera de rango.'); return n;
}
function payment(total,cash,card=0,transfer=0){
 if(![total,cash,card,transfer].every(Number.isSafeInteger)||total<=0||Math.min(cash,card,transfer)<0) throw Error('Importes inválidos.');
 if(card+transfer>total) throw Error('Tarjeta y transferencia no pueden producir cambio.');
 const applied=total-card-transfer;
 if(cash<applied) throw Error('Los medios de pago no cubren el total.');
 return {cash:applied,received:cash,change:cash-applied,card,transfer,total};
}
function requireOnline(online){if(!online)throw Error('Esta operación requiere conexión.');}
function orderPayment(order,amount,online){
 requireOnline(online);
 if(order.paid>=order.total)throw Error('COR-17: la orden liquidada no admite cambios económicos.');
 if(!Number.isSafeInteger(amount)||amount<=0||amount>order.total-order.paid)throw Error('Abono fuera del saldo pendiente.');
 if(order.kind==='repair'&&amount!==order.total-order.paid)throw Error('La reparación solo admite liquidación final, sin abonos intermedios.');
 return {...order,paid:order.paid+amount};
}
function deliver(order,online,mode){
 requireOnline(online);
 if(mode!=='pos')throw Error('La entrega se registra únicamente desde el POS.');
 if(order.delivered)throw Error('La orden ya fue entregada.');
 if(order.paid!==order.total)throw Error('Debe liquidarse antes de entregar.');
 if(order.kind==='repair'&&order.status!=='Lista para entregar')throw Error('El trabajo debe estar listo para entregar.');
 return {...order,delivered:true,status:'Entregada'};
}
function stock(cart,products){
 if(!cart.length)throw Error('Agrega una pieza.');
 for(const item of cart){const p=products.find(x=>x.id===item.id);if(!p||!Number.isInteger(item.qty)||item.qty<=0||item.qty>p.available)throw Error('Cantidad superior a la disponibilidad conocida.');}
 return cart.reduce((s,x)=>s+products.find(p=>p.id===x.id).price*x.qty,0);
}
function closeCash(expected,counted,fund,envelope){
 if(![expected,counted,fund,envelope].every(Number.isSafeInteger)||Math.min(counted,fund,envelope)<0)throw Error('Importes inválidos.');
 if(fund+envelope!==counted)throw Error('Fondo siguiente y sobre deben sumar el efectivo contado.');
 return {expected,counted,fund,envelope,difference:counted-expected};
}
const api={cents,payment,orderPayment,deliver,stock,closeCash,requireOnline};root.E0Domain=api;
if(typeof module!=='undefined')module.exports=api;
})(globalThis);
