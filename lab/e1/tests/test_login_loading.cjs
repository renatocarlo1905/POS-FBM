const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync(require('node:path').join(__dirname,'../static/app.js'),'utf8');
const tick=()=>new Promise(resolve=>setImmediate(resolve));
function setup(){
 const nodes={};const handlers={};const requests=[];let renders=0;
 const user={disabled:false},password={disabled:false},submit={disabled:false,innerHTML:''},progress={hidden:true,textContent:''},error={textContent:''};
 const form={dataset:{form:'login'},attrs:{},setAttribute(k,v){this.attrs[k]=v;},querySelectorAll(){return [user,password,submit];},querySelector(s){return ({'[type="submit"]':submit,'.login-progress':progress,'.error':error})[s];}};
 const c=vm.createContext({console,Intl,setTimeout(){},clearTimeout(){},setInterval(){},sessionStorage:{getItem(){return '';},setItem(){},removeItem(){}},document:{body:{dataset:{branch:'1'}},querySelector:s=>nodes[s]??=( {innerHTML:'',open:false,close(){}}),addEventListener(k,h){handlers[k]=h;}},FormData:class{*[Symbol.iterator](){yield ['user','example'];yield ['password','not-a-real-password'];}},location:{port:'8871'}});
 vm.runInContext(source,c);
 c.fakeApi=path=>new Promise((resolve,reject)=>requests.push({path,resolve,reject}));c.draw=()=>renders++;
 vm.runInContext('api=fakeApi;decorateState=()=>{};render=draw;',c);
 return {c,form,submit,progress,error,requests,run:()=>handlers.submit({target:form,preventDefault(){}}),renders:()=>renders};
}
(async()=>{
 let t=setup();const run=t.run();assert(t.submit.disabled);assert.match(t.progress.textContent,/Validando/);await t.run();assert.equal(t.requests.length,1);
 t.requests[0].resolve({token:'test'});await tick();assert.match(t.progress.textContent,/Cargando sistema/);assert(t.submit.disabled);assert.equal(t.requests[1].path,'state');t.requests[1].resolve({});await run;assert.equal(t.renders(),1);assert(!t.submit.disabled);assert(t.progress.hidden);
 for(const phase of ['login','state']){
  t=setup();const pending=t.run();if(phase==='state'){t.requests[0].resolve({token:'test'});await tick();}
  t.requests.at(-1).reject(Error('Fallo de prueba'));await pending;assert(!t.submit.disabled);assert(t.progress.hidden);assert.equal(t.error.textContent,'Fallo de prueba');assert.equal(t.form.attrs['aria-busy'],'false');
 }
 console.log('OK: indicador durante autenticación y carga inicial, doble envío bloqueado, recuperación tras ambos tipos de error.');
})().catch(e=>{console.error(e);process.exitCode=1;});
