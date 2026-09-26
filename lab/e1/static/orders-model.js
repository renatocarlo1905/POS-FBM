'use strict';
const orderPaid=o=>o.payments.reduce((sum,p)=>sum+p.amount,0)-(o.credit_issued||0);
const orderBalance=o=>Math.max(0,o.total-orderPaid(o));
const orderClosed=o=>['delivered','cancelled','released'].includes(o.status);
function orderFlag(o,asOf){
 if(orderClosed(o))return '';
 if(o.kind==='layaway'&&!orderBalance(o))return 'awaiting';
 if(!o.due||(o.kind==='repair'&&o.status!=='ready'))return '';
 if(asOf>o.due)return 'expired';
 const days=(new Date(o.due+'T12:00Z')-new Date(asOf+'T12:00Z'))/86400000;
 return o.kind==='layaway'&&days<=7?'soon':'';
}
function orderStatus(o){return (o.kind==='layaway'?{pending:'Pendiente de liquidación',settled:'Liquidado · pendiente de entrega',delivered:'Entregado',cancelled:'Cancelado',released:'Liberado'}:{received:'Recibida',in_repair:'En reparación',ready:'Lista para entregar',delivered:'Entregada',cancelled:'Cancelada'})[o.status];}
if(typeof module!=='undefined')module.exports={orderPaid,orderBalance,orderClosed,orderFlag,orderStatus};
