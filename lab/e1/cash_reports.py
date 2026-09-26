"""Read-only cash reports; synthetic shifts never enter POS event sequences."""
import json, datetime as dt, random
from collections import defaultdict
from zoneinfo import ZoneInfo
from core import pack, now
TZ=ZoneInfo('America/Mexico_City')
TOTALS=('gross','discount','total','cash','card','transfer')
def init(c):
 c.db.executescript('CREATE TABLE IF NOT EXISTS simulated_shifts(id text PRIMARY KEY,body text NOT NULL);')
def summarize(sales):
 return {**{k:sum(s.get(k,0) for s in sales if not s.get('cancelled')) for k in TOTALS},'count':sum(not s.get('cancelled',False) for s in sales)}
def manual(events,corrections):
 result=[]
 for opening in [e for e in events if e['kind']=='open']:
  sid=opening['id'];related=[e for e in events if e['payload'].get('session')==sid];closing=next((e for e in related if e['kind']=='close'),None)
  sales={e['id']:dict(e['payload']) for e in related if e['kind']=='sale'};post_delta=0
  for c in corrections:
   p=c['payload']
   if p.get('session')!=sid:continue
   if p['target'] in sales:sales[p['target']]=p['after']
   if p.get('replacement'):sales[p['replacement']['id']]=p['replacement']
   if closing and c['at']>closing['at']:post_delta+=(0 if p['after'].get('cancelled') else p['after']['cash'])-p['before']['cash']+(p.get('replacement') or {}).get('cash',0)
  moves=[{'at':e['at'],'actor':e['actor_name'],'reason':e['payload']['reason'],'amount':e['payload']['amount']*(1 if e['payload']['type']=='Entrada' else -1)} for e in related if e['kind']=='move']
  totals=summarize(list(sales.values()));fund=opening['payload']['opening'];computed=fund+totals['cash']+sum(m['amount'] for m in moves)
  p=closing['payload'] if closing else {};expected=p.get('expected',computed);counted=p.get('counted')
  result.append({'id':sid,'branch':opening['branch'],'opened_at':opening['at'],'closed_at':closing['at'] if closing else None,'opened_by':opening['actor_name'],'closed_by':closing['actor_name'] if closing else None,'opening':fund,'expected':expected,'counted':counted,'difference':None if counted is None else counted-expected,'fund':p.get('fund'),'envelope':p.get('envelope'),'post_close_adjustment':post_delta,'adjusted_expected':expected+post_delta,'totals':totals,'moves':moves,'simulated':False})
 return result
def report(c):
 events=[json.loads(r['body']) for r in c.events() if r['status']=='accepted'];corrections=[json.loads(r[0]) for r in c.db.execute('SELECT document FROM corrections ORDER BY ordinal')]
 rows=manual(events,corrections)
 from order_service import movements,sale_events
 for row in rows:
  payments=[p for p in movements(c,row['branch']) if p['session']==row['id']]
  added=sum(p['cash'] for p in payments)
  recognized=[e['payload'] for e in sale_events(c) if e['payload'].get('session')==row['id']]
  for key in ('gross','discount','total'):row['totals'][key]+=sum(p.get(key,0) for p in recognized)
  row['totals']['count']+=len(recognized)
  row['moves'] += [{'at':p['at'],'actor':p['actor'],'reason':p['kind']+' · '+p['order'],'amount':p['cash']} for p in payments]
  row['order_collections']={k:sum(p.get(k,0) for p in payments) for k in ('cash','card','transfer','credit')}
  if not row['closed_at']:row['expected']+=added;row['adjusted_expected']+=added
 rows+=[json.loads(r[0]) for r in c.db.execute('SELECT body FROM simulated_shifts')]
 return sorted(rows,key=lambda x:x['opened_at'],reverse=True)
def seed(c):
 init(c)
 if c.db.execute('SELECT count(*) FROM simulated_shifts').fetchone()[0]:return {'already_loaded':True}
 rng=random.Random(260925);cutoff=dt.datetime.now(TZ);users=c.users();grouped=defaultdict(list)
 for row in c.db.execute('SELECT body FROM simulated_sales'):
  e=json.loads(row[0]);at=dt.datetime.fromisoformat(e['at']).astimezone(TZ);grouped[(at.date(),e['branch'],0 if at.hour<15 else 1)].append(e['payload'])
 rows=[];day=dt.date(2026,1,1)
 while day<=cutoff.date():
  for branch in (1,2):
   for shift in (0,1):
    opened=dt.datetime.combine(day,dt.time(10 if shift==0 else 15),TZ);closed=dt.datetime.combine(day,dt.time(15 if shift==0 else 20),TZ)
    if opened>cutoff:continue
    closed=min(closed,cutoff);isclosed=True;actor=users[(day.toordinal()+branch+shift)%len(users)]['name'];totals=summarize(grouped[(day,branch,shift)]);opening=50000
    moves=[]
    if rng.random()<.18:moves.append({'at':(opened+dt.timedelta(minutes=20)).isoformat(),'actor':actor,'reason':'Cambio para caja · Ficticio','amount':rng.choice([10000,20000,30000])})
    if rng.random()<.3:moves.append({'at':(opened+dt.timedelta(minutes=45)).isoformat(),'actor':actor,'reason':'Material de empaque · Ficticio','amount':-rng.choice([3500,5000,8500,12000])})
    moves=[m for m in moves if dt.datetime.fromisoformat(m['at'])<=cutoff]
    expected=opening+totals['cash']+sum(m['amount'] for m in moves);difference=rng.choices([0,-1000,-500,500,1000,2000],[80,4,4,4,4,4])[0] if isclosed else None;counted=expected+difference if isclosed else None
    rows.append({'id':f'SIM-CAJA-{day}-S{branch}-{shift+1}','branch':branch,'shift':'Mañana' if shift==0 else 'Tarde','opened_at':opened.isoformat(),'closed_at':closed.isoformat() if isclosed else None,'opened_by':actor,'closed_by':actor if isclosed else None,'opening':opening,'expected':expected,'counted':counted,'difference':difference,'fund':min(opening,counted) if isclosed else None,'envelope':max(0,counted-opening) if isclosed else None,'post_close_adjustment':0,'adjusted_expected':expected,'totals':totals,'moves':moves,'simulated':True})
  day+=dt.timedelta(days=1)
 c.db.execute('BEGIN IMMEDIATE')
 try:
  for row in rows:c.db.execute('INSERT INTO simulated_shifts VALUES(?,?)',(row['id'],pack(row)))
  info={'count':len(rows),'closed':sum(bool(r['closed_at']) for r in rows),'open':sum(not r['closed_at'] for r in rows),'at':now(),'sales_count':sum(r['totals']['count'] for r in rows),'net':sum(r['totals']['total'] for r in rows)}
  c.put('simulated-shifts-v1',info);c.audit('carlo','simulated_shifts_created',info);c.db.execute('COMMIT');return info
 except Exception:c.db.execute('ROLLBACK');raise
