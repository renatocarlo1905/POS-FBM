'use strict';
let exchangeView=null,exchangeDraft=null;
const correctionPage=pages.corrections;
pages.corrections=()=>`${branch?`<section class="panel"><h2>Cambio de mercancía</h2><p>Recibe piezas de una compra anterior y entrega otras de igual o mayor valor. Solo la diferencia se cobra en la caja actual. Puedes usar ventas del historial de prueba o ventas registradas desde el POS.</p>${button('exchange-start','Buscar venta para cambio',!state.policy.exchange||state.offline||!state.session?'disabled':'','primary')}${!state.policy.exchange?'<p>Tu rol necesita el derecho «Realizar cambios comerciales de mercancía».</p>':''}</section>`:''}${correctionPage()}`;
actions['exchange-start']=()=>{
 exchangeView=null;
 modal('Buscar venta para cambio',form('exchange-search',`${field('query','Código del ticket, fecha o vendedor','','search','id="exchange-ticket-query" autocomplete="off" required minlength="3" placeholder="Ejemplo: V1- o parte del folio"')}<p>Consulta ventas de ambas sucursales. También puedes buscar el código C de un cambio anterior. En este laboratorio también puedes realizar cambios de ventas con código SV.</p>`,'Buscar')+'<div id="exchange-search-results"></div>');
};
let exchangeSearchTimer=null,exchangeSearchVersion=0;
$('#modal').addEventListener('close',()=>{clearTimeout(exchangeSearchTimer);exchangeSearchVersion++;});
async function searchExchangeTickets(query){
 clearTimeout(exchangeSearchTimer);const version=++exchangeSearchVersion,target=$('#exchange-search-results'),owner=token;
 if(!target)return;
 query=query.trim();
 if(query.length<3){target.innerHTML='<p class="muted">Escribe al menos 3 caracteres para ver coincidencias.</p>';return;}
 target.innerHTML='<div class="orders-loading" role="status"><span class="loading-spinner" aria-hidden="true"></span><strong>Buscando coincidencias…</strong></div>';
 const current=()=>version===exchangeSearchVersion&&token===owner&&$('#modal').open&&$('#exchange-search-results')===target;
 try{
  const rows=await api('exchange-search',{query});if(!current())return;
  target.innerHTML=rows.map(e=>`<div class="replacement-result"><div><strong>${esc(e.short_code||e.id)}</strong><small>${date(e.at)} · Sucursal ${e.branch} · ${esc(e.actor_name)} · ${money(e.total)}</small></div>${e.eligible===false?`<p role="status">${esc(e.blocking_reason)}</p>`:button('exchange-select','Seleccionar venta',`data-id="${esc(e.id)}"`)}</div>`).join('')||'<p>No se encontraron coincidencias. Prueba con otra parte del folio, fecha o vendedor.</p>';
  if(rows.length===40)target.innerHTML+='<p class="muted">Se muestran hasta 40 coincidencias. Escribe más caracteres para precisar la búsqueda.</p>';
 }catch(e){if(current())target.innerHTML=`<p role="alert">${esc(e.message)}. Pulsa Buscar para reintentar.</p>`;}
}
extraForms['exchange-search']=(f,d)=>{searchExchangeTickets(d.query);};
document.addEventListener('input',e=>{
 if(e.target.id!=='exchange-ticket-query')return;
 clearTimeout(exchangeSearchTimer);exchangeSearchVersion++;
 const query=e.target.value;
 if(query.trim().length<3){searchExchangeTickets(query);return;}
 $('#exchange-search-results').innerHTML='<p role="status">Buscando coincidencias…</p>';
 exchangeSearchTimer=setTimeout(()=>searchExchangeTickets(query),300);
});
actions['exchange-select']=async b=>{
 exchangeView=await api('exchange-view',{target:b.dataset.id});const v=exchangeView,p=v.source.payload;
 modal('Cambio de mercancía',form('exchange-draft',`<p>Origen: ${esc(receiptCode(v.source))} · Sucursal ${v.source.branch}<br>Fecha: ${date(v.source.at)} · Plazo hasta ${esc(v.deadline)}</p><h3>Piezas que recibes del cliente</h3>${p.items.map((x,i)=>`<section class="replacement-row"><strong>${esc(x.name)}</strong><p>${x.qty} compradas · ${v.remaining[x.id]} disponibles para cambio · Importe neto pagado ${money(x.net)}</p>${field('return_'+i,'Cantidad a recibir de '+esc(x.name),'0','number',`min="0" max="${v.remaining[x.id]}" step="1" required data-return-index="${i}"`)}${x.non_inventory?notice('Código 99: no regresará a inventario. Se avisará al administrador.') :''}</section>`).join('')}${check('condition','Verifiqué el origen y buen estado de las piezas, sin rayaduras ni defectos',false)}${replacementEditor({items:[]}).replace('Piezas de la venta','Piezas que entregas').replace('Elige Cambiar pieza y busca por nombre o código. Las piezas que no cambies se conservan.','Agrega las piezas nuevas buscando por nombre o código.')}<div id="exchange-totals" aria-live="polite"></div>${field('discount_amount','Descuento de mercancía nueva ($)','0','number','min="0" step="0.01"') }<p id="exchange-discount-reference" aria-live="polite"></p><h3>Cobrar únicamente la diferencia</h3><div class="grid2">${field('cash','Efectivo recibido','0','text','inputmode="decimal"')}${field('card','Tarjeta aplicada','0','text','inputmode="decimal"')}${field('transfer','Transferencia aplicada','0','text','inputmode="decimal"')}</div><div id="exchange-card" hidden>${field('bank','Banco')}${field('last4','Últimos cuatro dígitos','','text','maxlength="4"')}</div><div id="exchange-transfer" hidden>${field('reference','Referencia de transferencia')}</div>${sellerPicker([])}${field('reason','Motivo del cambio','','text','required maxlength="500"')}<p>La caja y venta originales se conservan. Requiere conexión y caja abierta.</p>`,'Comparar cambio'));
 updateExchangeTotals();
};
function exchangeReturns(){return exchangeView.source.payload.items.map((x,i)=>({id:x.id,qty:Number($(`[name="return_${i}"]`)?.value||0)})).filter(x=>x.qty>0);}
function updateExchangeTotals(){
 if(!$('#exchange-totals')||!exchangeView)return;
 const v=exchangeView;let credit=0;
 for(const x of exchangeReturns()){const original=v.source.payload.items.find(i=>i.id===x.id),used=v.used[x.id]||0;credit+=Math.floor(original.net*(used+x.qty)/original.qty)-Math.floor(original.net*used/original.qty);}
 const gross=replacementRows.filter(r=>!r.removed).reduce((n,r)=>n+(state.catalog.find(p=>p.id===r.id)?.price||0)*r.qty,0),discount=Math.round(Number($('[name="discount_amount"]')?.value||0)*100),net=gross-discount;
 const limit=state.policy.discount?Number(state.policy.max_discount||0):0,max=Math.floor(gross*limit/10000);
 const input=$('[name="discount_amount"]');input.max=(max/100).toFixed(2);
 $('#exchange-discount-reference').textContent=`Equivale a ${gross?(discount/gross*100).toFixed(2):'0.00'} % · Máximo autorizado ${money(max)} (${limit/100} %)`;
 $('#exchange-totals').innerHTML=`<div class="sum"><span>Valor reconocido</span><strong>${money(credit)}</strong></div><div class="sum"><span>Mercancía nueva después de descuento</span><strong>${money(net)}</strong></div><div class="sum total"><span>Diferencia por cobrar</span><strong>${money(net-credit)}</strong></div>${net<credit?notice('Agrega mercancía: el importe nuevo no puede ser menor al valor reconocido.'):''}`;
}
const exchangeRenderRows=renderReplacementRows;
renderReplacementRows=function(){exchangeRenderRows();updateExchangeTotals();};
document.addEventListener('input',e=>{
 if(!e.target.closest('form[data-form="exchange-draft"]'))return;
 updateExchangeTotals();$('#exchange-card').hidden=!(Number($('[name="card"]').value)>0);$('#exchange-transfer').hidden=!(Number($('[name="transfer"]').value)>0);
});
extraForms['exchange-draft']=async(f,d)=>{
 exchangeDraft={request_id:crypto.randomUUID(),target:exchangeView.source.id,session:state.session.id,returned:exchangeReturns(),condition:!!d.condition,reason:d.reason,sale:{...d,items:replacementItems(),sellers:[...checkoutSellers]}};
 const p=await api('exchange-preview',exchangeDraft);exchangeDraft.preview_hash=p.preview_hash;
 modal('Confirmar cambio de mercancía',`<p>Venta original ${esc(receiptCode(exchangeView.source))}</p><div class="grid2"><div><h3>Recibes</h3>${p.returned.map(x=>`<p>${x.qty} × ${esc(x.name)} · ${money(x.net)}${x.non_inventory?'<br><strong>99: aviso al administrador; sin ingreso a inventario.</strong>':''}</p>`).join('')}</div><div><h3>Entregas</h3>${p.new.items.map(x=>`<p>${x.qty} × ${esc(x.name)} · ${money(x.net)}</p>`).join('')}</div></div><p>Valor reconocido: ${money(p.credit)}<br>Total mercancía nueva: ${money(p.new.total)}</p><div class="sum total"><span>Diferencia cobrada hoy</span><strong>${money(p.difference)}</strong></div><p>Efectivo aplicado ${money(p.new.cash)} · Tarjeta ${money(p.new.card)} · Transferencia ${money(p.new.transfer)}<br>Cambio en efectivo ${money(p.new.change)}</p><p>Motivo: ${esc(p.reason)}<br>Atendió: ${esc(p.actor_name)}</p>${notice('Se conserva la venta original. Recibe y entrega las piezas indicadas antes de confirmar.')}<div class="actions">${button('close','Cancelar')}${button('exchange-confirm','Confirmar cambio','','primary')}</div>`);
};
actions['exchange-confirm']=async()=>{
 const p=await api('exchange-confirm',exchangeDraft);exchangeDraft=null;exchangeView=null;await refresh();modal('Cambio registrado',`<p>Código ${esc(p.short_code||p.id)}<br>Diferencia cobrada ${money(p.difference)}</p>${button('pdf','Ver e imprimir comprobante',`data-id="${esc(p.id)}"`,'primary')}<p>Imprime una copia para el cliente y otra para el local.</p>`);
};
if(!branch){const summaryBeforeExchanges=pages.summary;pages.summary=()=>`${state.exchange_alerts?.length?`<section class="panel"><h2>Pendientes: piezas 99 recibidas en cambios</h2><p>Estas piezas se recibieron físicamente y no ingresaron al inventario.</p>${state.exchange_alerts.map(a=>`<div class="replacement-result"><div><strong>${esc(a.short_code||a.id)}</strong><small>${date(a.at)} · Sucursal ${a.branch} · Origen ${esc(a.target_code||a.target)}</small>${a.pieces.map(x=>`<p>${x.qty} × ${esc(x.name)}</p>`).join('')}</div>${button('pdf','Ver comprobante',`data-id="${esc(a.id)}"`)}</div>`).join('')}</section>`:''}${summaryBeforeExchanges()}`;}
