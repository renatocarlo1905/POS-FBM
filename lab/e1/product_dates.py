"""Product dates derived from committed inventory and audit history."""
import json
from datetime import datetime

def catalog_dates(c):
    result={}
    def entry(pid):
        return result.setdefault(pid,{'created_at':None,'edited_at':None,'last_movement_at':None,'last_movement_type':None,'updated_at':None,'last_activity_type':None})
    # One pass over relevant audit records, independent of the catalog size.
    for row in c.db.execute("SELECT at,action,detail FROM audit WHERE action IN ('product_created','product_edited','category_deleted') ORDER BY at::timestamptz,id"):
        d=json.loads(row['detail']);kind=row['action']
        ids=[d.get('id')] if kind=='product_created' else [d.get('after',{}).get('id')] if kind=='product_edited' else d.get('products',[])
        for pid in ids:
            if not pid:continue
            info=entry(pid)
            if kind=='product_created':
                if info['created_at'] is None:info['created_at']=row['at']
            else:info['edited_at']=row['at']
    for row in c.db.execute('SELECT DISTINCT ON (product) product,at,reason FROM stock_ledger ORDER BY product,at::timestamptz DESC,id DESC'):
        info=entry(row['product']);info['last_movement_at']=row['at'];info['last_movement_type']=row['reason']
    for info in result.values():
        candidates=[(info['created_at'],'Carga del artículo'),(info['edited_at'],'Edición de datos'),(info['last_movement_at'],info['last_movement_type'])]
        available=[x for x in candidates if x[0]]
        if available:info['updated_at'],info['last_activity_type']=max(available,key=lambda x:datetime.fromisoformat(x[0]))
    return result

EMPTY={'created_at':None,'edited_at':None,'last_movement_at':None,'last_movement_type':None,'updated_at':None,'last_activity_type':None}
