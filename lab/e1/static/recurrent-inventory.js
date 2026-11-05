'use strict';
let recurrentDraft=null,recurrentQuery='',recurrentType='name';
function recurrentKey(){if(!state.user_id)throw Error('Actualiza la página antes de continuar.');return `e1-recurrent:${branch}:${state.user_id}`;}
function recurrentSave(){localStorage.setItem(recurrentKey(),JSON.stringify(recurrentDraft));const status=$('#recurrent-status');if(status)status.textContent='Borrador guardado en este navegador.';}
function recurrentOpen(){
 if(!allowedInventory()||(branch&&!state.policy.inventory_view))throw Error('No tienes permiso para ingresar mercancía.');
 const raw=localStorage.getItem(recurrentKey());recurrentDraft=raw?JSON.parse(raw):{request_id:crypto.randomUUID(),warehouse:'coyoacan',reason:'',items:[],pending:false};
 recurrentQuery='';recurrentRender();
}
function recurrentRender(){
 const d=recurrentDraft;
 modal('Mercancía recurrente',`<p id="recurrent-status" role="status">Borrador guardado en este navegador. Puedes cerrar y retomarlo con el mismo usuario.</p>${d.pending?notice('Hay un ingreso pendiente de confirmar. Reintenta para consultar el resultado sin duplicar unidades.'):''}<fieldset ${d.pending?'disabled':''} style="border:0;padding:0;margin:0"><div class="grid2">${selection('recurrent-warehouse','Almacén de ingreso',state.warehouses,d.warehouse)}${field('recurrent-reason','Referencia o motivo',d.reason,'text','maxlength="300"')}</div><div class="grid2"><label>Buscar por<select id="recurrent-type">${descriptionSearchOptions(recurrentType)}</select></label><label>Descripción o código<input id="recurrent-search" autocomplete="off" value="${esc(recurrentQuery)}" placeholder="Buscar producto…"></label></div><div id="recurrent-results"></div><h3>Productos por ingresar</h3><div id="recurrent-items"></div></fieldset><div class="actions">${button('close','Guardar y cerrar')}${button('recurrent-review',d.pending?'Reintentar confirmación':'Revisar ingreso','','primary')}</div>`);
 recurrentResults();recurrentItems();
}
function recurrentResults(){
 const q=recurrentQuery.trim().toLowerCase(),matches=q?state.catalog.filter(p=>p.active!==false&&productMatches(p,q,recurrentType)):[];
 $('#recurrent-results').innerHTML=!q?'<p class="muted">Escribe para buscar productos.</p>':!matches.length?'<p>Sin coincidencias.</p>':`<div class="table-wrap" style="max-height:260px;overflow:auto"><table><tbody>${matches.slice(0,20).map(p=>`<tr><td><strong>${esc(p.name)}</strong><small>${esc(p.description)}</small><small>${esc(p.code)}</small></td><td>${button('recurrent-add','Añadir',`data-id="${esc(p.id)}"`)}</td></tr>`).join('')}</tbody></table></div>${matches.length>20?'<p class="muted">Primeras 20 coincidencias. Precisa la búsqueda.</p>':''}`;
}
function recurrentItems(){
 $('#recurrent-items').innerHTML=recurrentDraft.items.length?`<div class="table-wrap"><table><thead><tr><th>Producto</th><th>Unidades a ingresar</th><th></th></tr></thead><tbody>${recurrentDraft.items.map(x=>{const p=state.catalog.find(p=>p.id===x.product);return `<tr><td><strong>${esc(p?.name||x.name)}</strong><small>${esc(p?.description||'')}</small><small>${esc(p?.code||x.code)}</small></td><td><input aria-label="Unidades de ${esc(x.name)}" data-recurrent-qty="${esc(x.product)}" type="number" min="1" max="100000" step="1" value="${esc(x.quantity)}" style="width:110px"></td><td>${button('recurrent-remove','Quitar',`data-id="${esc(x.product)}"`)}</td></tr>`;}).join('')}</tbody></table></div>`:'<p class="muted">Todavía no agregas productos.</p>';
}
actions['recurrent-open']=recurrentOpen;
actions['recurrent-add']=b=>{if(recurrentDraft.pending)return;const p=state.catalog.find(p=>p.id===b.dataset.id),x=recurrentDraft.items.find(x=>x.product===p.id);if(x)x.quantity=Number(x.quantity||0)+1;else {if(recurrentDraft.items.length>=500)throw Error('Máximo 500 productos por ingreso.');recurrentDraft.items.push({product:p.id,name:p.name,code:p.code,quantity:1});}recurrentSave();recurrentItems();};
actions['recurrent-remove']=b=>{if(recurrentDraft.pending)return;recurrentDraft.items=recurrentDraft.items.filter(x=>x.product!==b.dataset.id);recurrentSave();recurrentItems();};
document.addEventListener('input',e=>{
 if(!recurrentDraft||recurrentDraft.pending)return;
 if(e.target.id==='recurrent-search'){recurrentQuery=e.target.value;recurrentResults();return;}
 if(e.target.dataset.recurrentQty){recurrentDraft.items.find(x=>x.product===e.target.dataset.recurrentQty).quantity=e.target.value;recurrentSave();}
 if(e.target.name==='recurrent-reason'){recurrentDraft.reason=e.target.value;recurrentSave();}
});
document.addEventListener('change',e=>{
 if(!recurrentDraft||recurrentDraft.pending)return;
 if(e.target.id==='recurrent-type'){recurrentType=e.target.value;recurrentResults();}
 if(e.target.name==='recurrent-warehouse'){recurrentDraft.warehouse=e.target.value;recurrentSave();}
});
actions['recurrent-review']=async()=>{
 if(recurrentDraft.pending)return actions['recurrent-confirm']();
 const d=recurrentDraft;
 if(!d.reason.trim())throw Error('Escribe una referencia o motivo.');
 if(!d.items.length||d.items.some(x=>!Number.isInteger(Number(x.quantity))||Number(x.quantity)<1||Number(x.quantity)>100000))throw Error('Agrega productos con cantidades enteras de 1 a 100000.');
 modal('Confirmar ingreso recurrente',`<p>${esc(state.warehouses[d.warehouse])} · ${esc(d.reason)}</p><div class="table-wrap"><table><thead><tr><th>Producto</th><th>Unidades</th></tr></thead><tbody>${d.items.map(x=>`<tr><td>${esc(x.name)}<small>${esc(x.code)}</small></td><td>${Number(x.quantity)}</td></tr>`).join('')}</tbody></table></div><p><strong>${d.items.reduce((n,x)=>n+Number(x.quantity),0)} unidades en ${d.items.length} productos.</strong></p><div class="actions">${button('recurrent-back','Volver a la lista')}${button('recurrent-confirm','Confirmar ingreso','','primary')}</div>`);
};
actions['recurrent-back']=recurrentRender;
actions['recurrent-confirm']=async()=>{
 if(branch&&state.offline)throw Error('Conecta la sucursal para confirmar. Tu borrador está guardado.');
 const d=recurrentDraft;d.pending=true;recurrentSave();
 try {
  const response=await fetch('/api/recurrent-ingress',{method:'POST',headers:{'Content-Type':'application/json','Authorization':'Bearer '+token},body:JSON.stringify({request_id:d.request_id,warehouse:d.warehouse,reason:d.reason,items:d.items.map(x=>({product:x.product,quantity:Number(x.quantity)}))})});
  const result=await response.json();
  if(!response.ok){if(response.status>=400&&response.status<500){d.pending=false;recurrentSave();}throw Error(result.error||'No se pudo confirmar el ingreso.');}
  localStorage.removeItem(recurrentKey());recurrentDraft=null;$('#modal').close();await refresh();toast(`Ingreso registrado: ${result.units} unidades en ${result.count} productos.`);
 }catch(e){if(recurrentDraft)recurrentRender();throw e;}
};
