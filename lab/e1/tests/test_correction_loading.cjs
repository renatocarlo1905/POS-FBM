const fs=require('fs'),vm=require('vm'),assert=require('assert/strict');
const source=fs.readFileSync(require('path').join(__dirname,'../static/extra.js'),'utf8');
const requests=[],dialog={open:false,addEventListener(k,fn){this[k]=fn;}};let html='',shown=[];
const ctx=vm.createContext({actions:{},state:{operations:[]},token:'session',correctionView:null,$:()=>dialog,api:()=>new Promise((resolve,reject)=>requests.push({resolve,reject})),modal:(title,body)=>{dialog.open=true;html=body},button:(a,text)=>text,notice:s=>s,esc:s=>s});
vm.runInContext(source.slice(source.indexOf('let correctionLoadVersion='),source.indexOf('function showCorrectionView')),ctx);ctx.showCorrectionView=v=>shown.push(v);
const open=id=>ctx.actions['correction-open']({dataset:{id}}),tick=()=>new Promise(r=>setImmediate(r));
(async()=>{
 assert.equal(open('sale1'),undefined);assert.match(html,/Cargando venta/);
 dialog.open=false;dialog.close();requests[0].resolve({id:'sale1'});await tick();assert.equal(shown.length,0);assert(!dialog.open);
 open('sale2');requests[1].reject(Error('Sin conexión'));await tick();assert.match(html,/Reintentar/);assert.match(html,/Sin conexión/);
 open('sale2');requests[2].resolve({id:'sale2'});await tick();assert.equal(shown[0].id,'sale2');
 open('sale3');open('sale4');requests[3].resolve({id:'sale3'});requests[4].resolve({id:'sale4'});await tick();assert.deepEqual(shown.map(x=>x.id),['sale2','sale4']);
 console.log('OK: ventana inmediata, cancelación, fallo/reintento y descarte de respuestas anteriores.');
})().catch(e=>{console.error(e);process.exitCode=1;});
