const fs=require('fs'),vm=require('vm'),assert=require('assert/strict'),path=require('path');
const source=fs.readFileSync(path.join(__dirname,'../static/extra.js'),'utf8');
async function run(action,printFails=false,saveFails=false){
 let saved=0,printed=0,title='',message='',requests=0;
 const ctx=vm.createContext({actions:{},correctionDraft:{action},branch:1,
 api:async()=>{requests++;if(saveFails)throw Error('Error guardado');saved++;return {id:'cancel-id',payload:{reason:'Error',operator:'carlo',authorizer:'carlo'}}},
 $:()=>({close(){}}),refresh:async()=>{},modal:t=>title=t,esc:x=>x,button:()=>'',notice:x=>x,toast:x=>message=x,
 previewReceipt:async(route,result,automatic)=>{assert.equal(automatic,true);if(printFails)throw Error('Popup bloqueado');const doc=await result;assert.equal(doc.id,'cancel-id');printed++;}});
 vm.runInContext(source.slice(source.indexOf("actions['confirm-correction']="),source.indexOf("\ndocument.addEventListener",source.indexOf("actions['confirm-correction']="))),ctx);
 if(saveFails)await assert.rejects(ctx.actions['confirm-correction'](),/Error guardado/);else await ctx.actions['confirm-correction']();
 return {saved,printed,title,message,requests};
}
(async()=>{
 let r=await run('cancel');assert.equal(r.printed,1);assert.equal(r.title,'Venta anulada');
 r=await run('cancel',true);assert.equal(r.saved,1);assert.equal(r.requests,1);assert.match(r.message,/quedó anulada/);
 r=await run('payment');assert.equal(r.printed,0);
 r=await run('cancel',false,true);assert.equal(r.printed,0);
 assert(!source.includes('<option value="replace">'));
 console.log('OK: cancelación, impresión automática, fallo de impresión sin repetir y fallo de guardado.');
})().catch(e=>{console.error(e);process.exitCode=1});
