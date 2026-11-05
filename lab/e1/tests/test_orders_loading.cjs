const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(require('node:path').join(__dirname,'../static/orders.js'),'utf8');
function setup(){
 const requests=[];let rendered=0;
 const c={titles:{},pages:{},extraForms:{},view:'sale',token:'user-1',branch:1,state:{session:{id:'cash'},policy:{},offline:false},busy:false,Date,console,
 $:()=>({open:false,addEventListener(){},classList:{remove(){}}}),document:{addEventListener(){}},setInterval(){},setTimeout(){},sessionStorage:{getItem(){return null;}},
 api:()=>new Promise((resolve,reject)=>requests.push({resolve,reject})),render:()=>{rendered++;},notice:s=>s,button:(a,s)=>`<button data-action="${a}">${s}</button>`,esc:s=>s,date:s=>s,
 selection:()=>'',field:()=>'',orderFlag:()=>'',money:n=>n,
 actions:{nav:b=>{c.view=b.dataset.view;c.render();},refresh:async()=>{}},
 };
 vm.createContext(c);vm.runInContext(source,c);
 return {c,requests,renders:()=>rendered};
}
const tick=()=>new Promise(resolve=>setImmediate(resolve));
const data={rows:[],settings:{},asOf:'2026-11-04',admin:false,can_pdf:false};
(async()=>{
 let {c,requests,renders}=setup();
 await c.actions.nav({dataset:{view:'layaways'}});
 assert.equal(c.view,'layaways');assert.equal(requests.length,1);
 assert.match(c.pages.layaways(),/Cargando órdenes/);assert.doesNotMatch(c.pages.layaways(),/No hay órdenes/);
 await c.actions.nav({dataset:{view:'repairs'}});assert.equal(c.view,'repairs');assert.equal(requests.length,1);
 await c.actions.nav({dataset:{view:'sale'}});const before=renders();requests[0].resolve(data);await tick();assert.equal(c.view,'sale');assert.equal(renders(),before);
 await c.actions.nav({dataset:{view:'layaways'}});assert.match(c.pages.layaways(),/Actualizando órdenes/);
 requests[1].reject(Error('Sin conexión'));await tick();assert.match(c.pages.layaways(),/Reintentar/);
 c.actions['orders-reload']();assert.equal(requests.length,3);requests[2].resolve(data);await tick();assert.doesNotMatch(c.pages.layaways(),/Reintentar|Cargando órdenes|Actualizando órdenes/);
 let t=setup();await t.c.actions.nav({dataset:{view:'layaways'}});t.requests[0].reject(Error('Error de consulta'));await tick();assert.match(t.c.pages.layaways(),/Error de consulta/);assert.doesNotMatch(t.c.pages.layaways(),/No hay órdenes/);
 t=setup();await t.c.actions.nav({dataset:{view:'layaways'}});t.c.token='user-2';t.requests[0].resolve(data);await tick();assert.match(t.c.pages.layaways(),/Cargando órdenes/);
 console.log('OK: navegación inmediata, carga compartida, salida durante consulta, actualización, error y reintento, respuesta de sesión anterior descartada.');
})().catch(e=>{console.error(e);process.exitCode=1;});
