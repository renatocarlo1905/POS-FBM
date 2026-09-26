"""Historial sintético para reportes; separado de la cola y el efectivo operativo."""
import json
from core import pack

def init(c):
    c.db.executescript('CREATE TABLE IF NOT EXISTS simulated_sales(id text PRIMARY KEY,batch text NOT NULL,body text NOT NULL);')

def sales(c):
    return [json.loads(r[0]) for r in c.db.execute('SELECT body FROM simulated_sales ORDER BY id')]

def receipt(c, ident):
    r=c.db.execute('SELECT body FROM simulated_sales WHERE id=?',(ident,)).fetchone()
    if not r:return None
    e=json.loads(r[0]);e['template']=c.get('simulation-template:'+e['simulation_batch'])
    return e
