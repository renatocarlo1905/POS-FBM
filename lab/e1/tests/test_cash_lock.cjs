const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
const source=fs.readFileSync(require('node:path').join(__dirname,'../static/app.js'),'utf8');
function setup(branch){
 const elements=new Map();const listeners={};
 function element(id){if(!elements.has(id))elements.set(id,{innerHTML:'',textContent:'',open:false,close(){this.open=false;},showModal(){this.open=true;}});return elements.get(id);}
 const context=vm.createContext({Intl,console,setTimeout(){},clearTimeout(){},setInterval(){},sessionStorage:{getItem(){return '';},removeItem(){},setItem(){}},document:{body:{dataset:{branch:String(branch)}},activeElement:{tagName:'BODY'},querySelector:element,addEventListener(k,fn){(listeners[k]??=[]).push(fn);}},location:{port:String(8870+branch)}});
 vm.runInContext(source,context);
 return {context,elements,run:code=>vm.runInContext(code,context),listeners};
}
(async()=>{
 for(const branch of [1,2]){
 const t=setup(branch);
 t.run("state={session:null,user:'Melissa',policy:{cash_open:true,receipts:true},catalog:[{name:'SECRET PRODUCT'}],operations:[]};view='inventory';cart=[{id:'p1'}];render();");
 let html=t.elements.get('#app').innerHTML;
 assert.match(html,/Caja cerrada/);assert.match(html,/data-action="open-cash"/);
 assert.doesNotMatch(html,/SECRET PRODUCT|data-action="nav"|id="search"|Cierres guardados/);
 assert.equal(t.run('cart.length'),0);
 // Every operational click is rejected before its handler can run.
 t.run("actions.nav=()=>{throw Error('HANDLER MUST NOT RUN');};");
 await t.listeners.click[0]({target:{closest(){return {dataset:{action:'nav',view:'inventory'}};}}});
 assert.match(t.elements.get('#toast').textContent,/Abre caja/);
 t.run("state.session={id:'opened'};pages.sale=()=>'<div id=active-sale>Venta habilitada</div>';render();");
 assert.match(t.elements.get('#app').innerHTML,/Venta habilitada/);
 assert.match(t.elements.get('#app').innerHTML,/data-action="nav"/);
 assert.doesNotMatch(t.elements.get('#app').innerHTML,/data-view="inventory"/);
 t.run("view='inventory';render();");
 assert.equal(t.run('view'),'sale');
 t.run("state.policy.inventory_view=true;render();");
 assert.match(t.elements.get('#app').innerHTML,/data-view="inventory"/);
 t.run("state.policy.inventory_view=false;view='inventory';render();");
 assert.equal(t.run('view'),'sale');

 t.run("state.session=null;document.querySelector('#modal').open=true;render();");
 assert.equal(t.elements.get('#modal').open,false);
 assert.doesNotMatch(t.elements.get('#app').innerHTML,/Venta habilitada/);
 t.run("state.policy.cash_open=false;render();");
 assert.match(t.elements.get('#app').innerHTML,/data-action="open-cash" disabled/);
 t.run("completedCloseId='close-1';document.querySelector('#modal').open=true;");
 assert.equal(t.run("lockedActionAllowed('pdf',{dataset:{id:'close-1'}})"),true);
 assert.equal(t.run("lockedActionAllowed('pdf',{dataset:{id:'sale-1'}})"),false);
 t.run("document.querySelector('#modal').close();");
 assert.equal(t.run("lockedActionAllowed('pdf',{dataset:{id:'close-1'}})"),false);
 }
 const admin=setup(0);admin.run("state={session:null};");assert.equal(admin.run('cashLocked()'),false);
 console.log('OK: bloqueo en ambas sucursales, navegación, reapertura, cierre, permisos y excepción del comprobante de cierre; administración independiente.');
})().catch(e=>{console.error(e);process.exitCode=1;});
