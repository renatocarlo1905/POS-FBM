'use strict';
const statusText=document.querySelector('#status'),pages=document.querySelector('#pages'),printButton=document.querySelector('#print');
document.querySelector('#close').onclick=()=>window.close();
printButton.onclick=()=>window.print();
window.addEventListener('message',async function receive(e){
 if(e.origin!==location.origin||e.source!==window.opener||e.data?.type!=='receipt-data')return;
 window.removeEventListener('message',receive);
 const receipt=e.data.receipt;document.title=receipt.title+' · Frida';
 try{
  const sheet=document.styleSheets[0];
  await Promise.all(receipt.pages.map(async(p,i)=>{
   const image=new Image();image.alt=`Comprobante ${receipt.title}, copia ${i+1}`;image.src=p.src;image.className='receipt-page page-'+i;
   sheet.insertRule(`.page-${i}{width:${p.width}mm;page:receipt${i}}`,sheet.cssRules.length);
   sheet.insertRule(`@page receipt${i}{size:${p.width}mm ${p.height}mm;margin:0}`,sheet.cssRules.length);
   pages.append(image);await image.decode();
  }));
  statusText.textContent=`${receipt.pages.length} copia(s) · Listo para imprimir`;printButton.disabled=false;
 }catch{statusText.textContent='No se pudo mostrar el comprobante. Cierra esta ventana y vuelve a intentarlo.';}
});
if(window.opener)window.opener.postMessage({type:'receipt-ready'},location.origin);
else statusText.textContent='Abre un comprobante desde el dashboard o el punto de venta.';
