"""PostgreSQL persistence; positional parameter adapter shared with SQLite store code."""
import json, subprocess, threading
from pathlib import Path
import psycopg
from psycopg.rows import dict_row
class Row(dict):
    def __getitem__(self,key):return list(self.values())[key] if isinstance(key,int) else super().__getitem__(key)
class Result:
    def __init__(self,cursor):self.cursor=cursor
    def fetchone(self):
        r=self.cursor.fetchone();return Row(r) if r is not None else None
    def __iter__(self):return (Row(r) for r in self.cursor)
class Connection:
    def __init__(self,config):self.conn=psycopg.connect(**config,autocommit=True,row_factory=dict_row)
    def execute(self,query,args=()):
        if query=='BEGIN IMMEDIATE':
            self.conn.execute('BEGIN');return Result(self.conn.execute('SELECT pg_advisory_xact_lock(19092501)'))
        return Result(self.conn.execute(query.replace('?','%s'),args))
    def executescript(self,script):self.conn.execute(script)
    def close(self):self.conn.close()
class PGDB:
    def __init__(self,path):
        config=json.loads(Path(path).read_text());self.config=config;self.path=Path(path);self.lock=threading.RLock();self.db=Connection(config)
        self.db.executescript('CREATE TABLE IF NOT EXISTS kv(k text PRIMARY KEY,v text NOT NULL);')
    def get(self,k,default=None):
        r=self.db.execute('SELECT v FROM kv WHERE k=?',(k,)).fetchone();return json.loads(r['v']) if r else default
    def put(self,k,v):self.db.execute('INSERT INTO kv VALUES(?,?) ON CONFLICT(k) DO UPDATE SET v=EXCLUDED.v',(k,json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))))
    def backup(self,dest):
        dest=Path(dest).with_suffix('.dump');dest.parent.mkdir(parents=True,exist_ok=True);tmp=dest.with_suffix('.tmp')
        with tmp.open('wb') as stream:subprocess.run(['docker','exec','pos-frida-e1-postgres','pg_dump','-U','pos_e1_admin','-d',self.config['dbname'],'-Fc'],stdout=stream,stderr=subprocess.PIPE,check=True)
        tmp.replace(dest)
