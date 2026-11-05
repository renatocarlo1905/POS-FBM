'use strict';
// Apply to initial controls and dynamically rendered screens and dialogs.
(() => {
 const selector='form,input,textarea,select';
 function disable(root){
  if(root.nodeType!==1&&root.nodeType!==9)return;
  if(root.matches?.(selector))root.setAttribute('autocomplete','off');
  root.querySelectorAll(selector).forEach(control=>control.setAttribute('autocomplete','off'));
 }
 disable(document);
 new MutationObserver(records=>{
  for(const record of records)for(const node of record.addedNodes)disable(node);
 }).observe(document.documentElement,{childList:true,subtree:true});
 document.addEventListener('focus',event=>{
  if(event.target.matches?.(selector))event.target.setAttribute('autocomplete','off');
 },true);
})();
