"""Explicitly authorized E1 history replacement; --apply requires prior full backup.
Dry-run validates generation. --database targets a disposable clone for rehearsal.
Keeps source flags and persistent folios; does not disguise provenance internally.
"""
import argparse, collections, datetime as dt, hashlib, json, random, sqlite3, sys, threading
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'lab/e1'))
from central import Central
from pg import Connection
from domain import pack
from cash_reports import summarize, report
import seed_simulation as generator
import simulated
DATA=ROOT/'lab/e1/data';BATCH='history-through-20261103-v1'
CUT=dt.datetime(2026,11,3,23,59,59,tzinfo=generator.TZ)

def connect(database=None):
 c=Central.__new__(Central);c.config=json.loads((DATA/'postgres.json').read_text())
 if database:c.config['dbname']=database
 c.db=Connection(c.config);c.lock=threading.RLock();return c

def prepare(c):
 manifests=[json.loads(r['v']) for r in c.db.execute('SELECT v FROM kv WHERE k LIKE ?',('simulation-manifest:%',))]
 ids=next(m['product_ids'] for m in manifests if m.get('products_added')==24)
 products=[p for p in c.catalog(True) if p['id'] in ids]
 assert len(products)==24
 for p in products:p['name']=p['name'].replace(' · Ficticio','')
 generator.BATCH=BATCH
 sales=generator.generate(products,[u for u in c.users() if u['active']],CUT)
 grouped=collections.defaultdict(list)
 for e in sales:
  at=dt.datetime.fromisoformat(e['at']);shift=1 if at.hour<15 else 2
  e['issue']='';e['payload']['session']=f'SIM-CAJA-{BATCH}-{at.date()}-S{e["branch"]}-{shift}'
  e['payload']['bank']='BBVA' if e['payload']['card'] else ''
  if e['payload']['transfer']:e['payload']['reference']='TR-'+e['id'][-12:].upper()
  for item in e['payload']['items']:
   p=next(p for p in products if p['id']==item['id'])
   for k in ('cost','material','material_id','category','category_id','type_id'):
    if k in p:item[k]=p[k]
  grouped[e['payload']['session']].append(e)
 rng=random.Random(20261103);shifts=[];day=dt.date(2026,1,1);users=c.users()
 while day<=CUT.date():
  for b in (1,2):
   for shift in (1,2):
    sid=f'SIM-CAJA-{BATCH}-{day}-S{b}-{shift}';start=dt.datetime.combine(day,dt.time(10 if shift==1 else 15),generator.TZ);end=start+dt.timedelta(hours=5)
    actor=users[(day.toordinal()+b+shift)%len(users)]['name'];totals=summarize([e['payload'] for e in grouped[sid]])
    moves=[]
    if rng.random()<.22:moves=[{'at':(start+dt.timedelta(minutes=40)).isoformat(),'actor':actor,'reason':'Material de empaque','amount':-rng.choice([3500,5000,8500])}]
    expected=50000+totals['cash']+sum(m['amount'] for m in moves);diff=rng.choices([0,-500,500,-1000,1000],[90,3,3,2,2])[0];counted=expected+diff
    shifts.append(dict(id=sid,branch=b,shift='Mañana' if shift==1 else 'Tarde',opened_at=start.isoformat(),closed_at=end.isoformat(),opened_by=actor,closed_by=actor,opening=50000,expected=expected,counted=counted,difference=diff,fund=50000,envelope=counted-50000,post_close_adjustment=0,adjusted_expected=expected,totals=totals,moves=moves,simulated=True))
  day+=dt.timedelta(days=1)
 assert len(shifts)==307*4
 assert len({e['id'] for e in sales})==len(sales)
 for s in shifts:
  assert all(s['opened_at']<=e['at']<s['closed_at'] for e in grouped[s['id']])
  assert s['counted']==s['fund']+s['envelope']==s['expected']+s['difference']
 for e in sales:
  p=e['payload'];assert p['total']==p['cash']+p['card']+p['transfer']==p['gross']-p['discount'];assert sum(x['net'] for x in p['items'])==p['total']
 assert sum(s['totals']['count'] for s in shifts)==len(sales)
 return sales,shifts

def apply(c,sales,shifts):
 assert not c.get('history-refresh:'+BATCH),'Already applied'
 events=[json.loads(r['body']) for r in c.events()]
 assert len(events)==12,'Operations changed; inspect again'
 assert all(json.loads(r['body']).get('simulated') for r in c.db.execute('SELECT body FROM service_orders')),'Operational orders need review'
 origins={e['id'] for e in events}|{r['id'] for r in c.db.execute('SELECT id FROM corrections')}|{json.loads(r['body'])['id'] for r in c.db.execute('SELECT body FROM merchandise_exchanges')}
 ledger=[dict(r) for r in c.db.execute('SELECT * FROM stock_ledger') if r['origin'] in origins]
 assert len(ledger)==14
 restore=collections.Counter()
 for r in ledger:
  assert r['warehouse']=='coyoacan';restore[r['product']]-=r['delta']
 protected={t:hashlib.sha256(pack([dict(r) for r in c.db.execute('SELECT * FROM '+t+' ORDER BY 1')]).encode()).hexdigest() for t in ('products','inventory_entries','service_orders','warehouse_stock')}
 stock={r['id']:r['available'] for r in c.db.execute('SELECT * FROM stock')}
 c.db.execute('BEGIN IMMEDIATE')
 try:
  for t in ('events','corrections','stock_ledger','merchandise_exchanges'):c.db.execute(f'ALTER TABLE {t} DISABLE TRIGGER immutable_{t}')
  for pid,n in restore.items():c.db.execute('UPDATE stock SET available=available+? WHERE id=?',(n,pid))
  for r in ledger:c.db.execute('DELETE FROM stock_ledger WHERE id=?',(r['id'],))
  for t in ('related_changes','merchandise_exchanges','corrections','events','simulated_sales','simulated_shifts'):c.db.execute('DELETE FROM '+t)
  for t in ('events','corrections','stock_ledger','merchandise_exchanges'):c.db.execute(f'ALTER TABLE {t} ENABLE TRIGGER immutable_{t}')
  for e in sales:c.db.execute('INSERT INTO simulated_sales VALUES(?,?,?)',(e['id'],BATCH,pack(e)))
  for s in shifts:c.db.execute('INSERT INTO simulated_shifts VALUES(?,?)',(s['id'],pack(s)))
  template=c.get('templates')['1'].copy();template.update(header='FRIDA BLANCAS MÉXICO',footer='Gracias por tu visita.')
  c.put('simulation-template:'+BATCH,template)
  info={'through':CUT.isoformat(),'sales':len(sales),'shifts':len(shifts),'open':0,'restored_stock':dict(restore)}
  c.put('history-refresh:'+BATCH,info);c.audit('carlo','history_replaced_user_authorized',info)
  for t,digest in protected.items():assert hashlib.sha256(pack([dict(r) for r in c.db.execute('SELECT * FROM '+t+' ORDER BY 1')]).encode()).hexdigest()==digest
  for r in c.db.execute('SELECT * FROM stock'):assert r['available']==stock[r['id']]+restore[r['id']]
  assert all(r['tgenabled']=='O' for r in c.db.execute("SELECT tgenabled FROM pg_trigger WHERE tgname LIKE ?",('immutable_%',)))
  simulated.assign_codes(c,sales,'SV');simulated.assign_codes(c,shifts,'SC')
  rows=report(c);assert len(rows)==len(shifts) and all(r['closed_at'] for r in rows)
  c.db.execute('COMMIT')
 except BaseException:c.db.execute('ROLLBACK');raise
 return info

def clear_local(c,directory):
 for b in (1,2):
  db=sqlite3.connect(directory/f'sucursal-{b}.sqlite3');assert not db.execute("SELECT 1 FROM operations WHERE status='pending'").fetchone()
  db.execute('DELETE FROM operations')
  for key,value in {'corrections':[],'cash_adjustments':{},'order_cash_moves':[],'exchange_moves':[],'catalog':c.catalog(True),'sync_error':'','offline':False}.items():db.execute('INSERT OR REPLACE INTO kv VALUES(?,?)',(key,pack(value)))
  db.execute("DELETE FROM kv WHERE k LIKE 'pdf:%'");db.commit()
  assert db.execute('SELECT count(*) FROM operations').fetchone()[0]==0
  copy=directory/'second-copy';copy.mkdir(exist_ok=True);out=sqlite3.connect(copy/f'sucursal-{b}.sqlite3');db.backup(out);out.close();db.close()

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--database');parser.add_argument('--apply',action='store_true');parser.add_argument('--local-dir',type=Path);args=parser.parse_args()
 c=connect(args.database)
 try:
  sales,shifts=prepare(c);print(json.dumps({'sales':len(sales),'shifts':len(shifts),'last_sale':max(e['at'] for e in sales),'last_close':max(s['closed_at'] for s in shifts)}))
  if args.apply:
   info=apply(c,sales,shifts)
   if args.local_dir:clear_local(c,args.local_dir)
   print(json.dumps(info))
 finally:c.db.close()
