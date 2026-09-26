"""One-time, user-authorized removal of three E1 manual cash sessions and their sales."""
import sys,json,sqlite3,datetime,hashlib
from pathlib import Path
from collections import Counter
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'lab/e1'))
from core import Central,pack,now
from cash_reports import report
DATA=ROOT/'lab/e1/data'
TARGETS={'46ee0829-d6f7-4351-a640-ae857e54c8ab','e34d274d-8903-4af2-ac69-73d52f835d10','3ab9067c-72a2-41b1-8d02-d0b47a6b524e'}
c=Central(DATA/'postgres.json')
events=[json.loads(r['body']) for r in c.events()]
assert {e['id'] for e in events if e['kind']=='open'}==TARGETS,'Cash sessions changed; inspect before proceeding'
assert len(events)==8 and all(e['id'] in TARGETS or e['payload'].get('session') in TARGETS for e in events)
sales=[e for e in events if e['kind']=='sale'];assert len(sales)==4
corr=list(c.db.execute('SELECT * FROM corrections'));assert len(corr)==1 and corr[0]['target'] in {e['id'] for e in sales}
assert not list(c.db.execute('SELECT * FROM related_changes'))
ids={e['id'] for e in events};origins=ids|{r['id'] for r in corr}
restore=Counter()
for e in sales:
 for item in e['payload']['items']:restore[item['id']]+=item['qty']
for r in c.db.execute('SELECT * FROM stock_ledger'):
 if r['origin'] in {x['id'] for x in corr}:
  assert r['warehouse']=='coyoacan';restore[r['product']]-=r['delta']
def simulated_digest():
 return {t:hashlib.sha256(pack([r['body'] for r in c.db.execute('SELECT body FROM '+t+' ORDER BY id')]).encode()).hexdigest() for t in ('simulated_sales','simulated_shifts')}
digests=simulated_digest()
backup=DATA/'backups'/('eliminar-manuales-confirmado-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S'));backup.mkdir()
c.backup(backup/'central.dump')
locals=[]
for b in (1,2):
 db=sqlite3.connect(DATA/f'sucursal-{b}.sqlite3',isolation_level=None)
 rows=db.execute('SELECT id,status FROM operations').fetchall();assert all(id in ids and status=='accepted' for id,status in rows)
 out=sqlite3.connect(backup/f'sucursal-{b}.sqlite3');db.backup(out);out.close();locals.append((b,db))
stock_before={r['id']:r['available'] for r in c.db.execute('SELECT * FROM stock')}
c.db.execute('BEGIN IMMEDIATE')
try:
 for table in ('events','corrections','stock_ledger'):c.db.execute(f'ALTER TABLE {table} DISABLE TRIGGER immutable_{table}')
 for product,qty in restore.items():c.db.execute('UPDATE stock SET available=available+? WHERE id=?',(qty,product))
 for origin in origins:c.db.execute('DELETE FROM stock_ledger WHERE origin=?',(origin,))
 for row in corr:c.db.execute('DELETE FROM corrections WHERE id=?',(row['id'],))
 for id in ids:c.db.execute('DELETE FROM events WHERE id=?',(id,))
 for table in ('events','corrections','stock_ledger'):c.db.execute(f'ALTER TABLE {table} ENABLE TRIGGER immutable_{table}')
 c.audit('carlo','manual_cash_test_data_removed',{'cash_sessions':sorted(TARGETS),'sales':len(sales),'corrections':len(corr),'stock_restored':dict(restore),'backup':str(backup),'authorization':'Usuario confirmó eliminar cajas manuales, ventas y corrección y revertir existencias.'})
 assert simulated_digest()==digests
 c.db.execute('COMMIT')
except:c.db.execute('ROLLBACK');raise
for b,db in locals:
 db.execute('BEGIN IMMEDIATE')
 for id in ids:db.execute('DELETE FROM operations WHERE id=?',(id,));db.execute('DELETE FROM kv WHERE k=?',('pdf:'+id,))
 for k,v in {'corrections':[],'cash_adjustments':{},'catalog':c.catalog(True),'last_sync':now(),'sync_error':''}.items():db.execute('INSERT OR REPLACE INTO kv VALUES(?,?)',(k,pack(v)))
 db.execute('COMMIT')
 out=sqlite3.connect(DATA/f'second-copy/sucursal-{b}.sqlite3');db.backup(out);out.close()
 assert db.execute('SELECT count(*) FROM operations').fetchone()[0]==0;db.close()
assert all(r['simulated'] for r in report(c));assert len(report(c))==1070
assert simulated_digest()==digests
for r in c.db.execute('SELECT * FROM stock'):assert r['available']==stock_before[r['id']]+restore[r['id']]
assert all(r['tgenabled']=='O' for r in c.db.execute("SELECT tgenabled FROM pg_trigger WHERE tgname IN ('immutable_events','immutable_corrections','immutable_stock_ledger')"))
c.backup(DATA/'backups/central.dump')
result={'manual_cash_removed':3,'manual_sales_removed':4,'corrections_removed':1,'stock_restored':dict(restore),'simulated_cash_preserved':1070,'simulated_data_unchanged':True,'backup':str(backup)}
(backup/'resultado.json').write_text(json.dumps(result,ensure_ascii=False,indent=2));print(json.dumps(result,ensure_ascii=False));c.db.close()
