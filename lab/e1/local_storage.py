"""Durable local SQLite persistence and backup."""
import json, sqlite3, threading
from pathlib import Path
from domain import pack
class DB:
    def __init__(self,path):
        self.path=Path(path); self.path.parent.mkdir(parents=True,exist_ok=True)
        self.lock=threading.RLock();self.db=sqlite3.connect(self.path,check_same_thread=False,isolation_level=None)
        self.db.row_factory=sqlite3.Row;self.db.execute('PRAGMA journal_mode=WAL');self.db.execute('PRAGMA synchronous=FULL')
        self.db.executescript('CREATE TABLE IF NOT EXISTS kv(k TEXT PRIMARY KEY,v TEXT NOT NULL);')
    def get(self,k,default=None):
        r=self.db.execute('SELECT v FROM kv WHERE k=?',(k,)).fetchone();return json.loads(r[0]) if r else default
    def put(self,k,v):self.db.execute('INSERT OR REPLACE INTO kv VALUES(?,?)',(k,pack(v)))
    def backup(self,dest):
        with self.lock:
            dest=Path(dest);dest.parent.mkdir(parents=True,exist_ok=True)
            tmp=dest.with_suffix('.tmp');out=sqlite3.connect(tmp)
            try:self.db.backup(out)
            finally:out.close()
            tmp.replace(dest)
