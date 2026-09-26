const assert=require('node:assert/strict');
const demo=require('../static/orders-demo.js');
const {orderFlag,orderPaid,orderBalance,orderClosed}=require('../static/orders-model.js');
const find=id=>demo.rows.find(o=>o.id===id);
assert.equal(demo.rows.length,14);assert.equal(new Set(demo.rows.map(o=>o.id)).size,14);
assert.equal(orderFlag(find('SIM-APA-003'),demo.asOf),'expired');
assert.equal(orderFlag(find('SIM-APA-004'),demo.asOf),'awaiting');
assert.equal(orderFlag(find('SIM-APA-002'),demo.asOf),'soon');
assert.equal(orderFlag(find('SIM-REP-014'),demo.asOf),'expired');
const o=find('SIM-APA-001');assert.equal(orderFlag(o,o.due),'soon');
assert.equal(orderFlag(o,'2026-11-09'),'expired');
for(const row of demo.rows){
 assert.ok(orderPaid(row)<=row.total);assert.equal(orderPaid(row)+orderBalance(row),row.total);
 assert.ok(row.payments.every(p=>p.amount>0&&p.at>=row.created&&p.at.slice(0,10)<=demo.asOf));
 assert.ok(row.history.every(h=>h.at>=row.created&&h.at.slice(0,10)<=demo.asOf));
 if(orderClosed(row))assert.equal(orderFlag(row,demo.asOf),'');
 if(row.delivery)assert.equal(orderBalance(row),0);
 if(row.kind==='repair'){assert.ok(row.payments.length<=2);assert.equal(row.sellers.length,0);if(row.status!=='ready'&&row.status!=='delivered')assert.equal(row.due,null);}
 else assert.ok(row.payments[0].amount>=row.total*.4);
}
assert.equal(find('SIM-REP-017').ever_in_repair,true);
assert.equal(find('SIM-REP-017').status,'received');
console.log('OK: 14 casos, plazos inclusivos, liquidado sin vencer, cobros y entregas coherentes, reparaciones sin abonos intermedios.');
