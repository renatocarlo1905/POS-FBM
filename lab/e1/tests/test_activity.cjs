const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const source=fs.readFileSync(require('path').join(__dirname,'../static/app.js'),'utf8');
function setup(){
 let timer,removed=0,appended=0;
 const control={innerHTML:'Confirmar corrección',disabled:false,classList:{add(){},remove(){}}};
 const close={disabled:false},dialog={open:true,contains:()=>true,append(){appended++;}};
 const c=vm.createContext({$:s=>s==='#modal'?dialog:close,esc:s=>s,setTimeout:fn=>(timer=fn,1),clearTimeout:()=>{timer=null;},document:{addEventListener(){},createElement:()=>({setAttribute(){},remove(){removed++;}})}});
 vm.runInContext(source.slice(source.indexOf('let activityModalLocks='),source.indexOf("document.addEventListener('click',async")),c);
 return {c,control,close,dialog,fire:()=>timer?.(),appended:()=>appended,removed:()=>removed};
}
for(const kind of ['confirm-correction','exchange-confirm','confirm-product','backup','pdf','refresh']){
 const t=setup(),done=t.c.beginActivity(t.control,kind);assert(t.control.disabled&&t.close.disabled);t.fire();assert.match(t.control.innerHTML,/loading-spinner/);assert.equal(t.appended(),1);done();assert.equal(t.control.innerHTML,'Confirmar corrección');assert(!t.control.disabled&&!t.close.disabled);assert.equal(t.removed(),1);assert.equal(vm.runInContext('activityModalLocks',t.c),0);
}
let t=setup(),done=t.c.beginActivity(t.control,'confirm-correction');done();t.fire();assert.equal(t.appended(),0);
t=setup();done=t.c.beginActivity(t.control,'nav');assert(!t.control.disabled);done();
t=setup();const f={querySelector:()=>t.control};done=t.c.beginActivity(f,'correction-draft',true);t.fire();assert.match(t.control.innerHTML,/Comparando corrección/);done();
console.log('OK: indicadores por acción/formulario, bloqueo/restauración, acciones rápidas sin parpadeo y navegación independiente.');
