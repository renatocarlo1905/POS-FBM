"""Historial sintético para reportes; separado de la cola y el efectivo operativo."""
import json
from domain import pack

def init_codes(c):
    c.db.executescript("""CREATE TABLE IF NOT EXISTS simulated_receipt_codes(
      identifier text PRIMARY KEY, prefix text NOT NULL, branch integer NOT NULL,
      number bigint GENERATED ALWAYS AS IDENTITY UNIQUE);
      """)
    c.db.executescript("""DROP TRIGGER IF EXISTS immutable_simulated_receipt_codes ON simulated_receipt_codes;
    CREATE TRIGGER immutable_simulated_receipt_codes BEFORE UPDATE OR DELETE ON simulated_receipt_codes
    FOR EACH ROW EXECUTE FUNCTION prevent_fact_change();""")

def assign_codes(c,rows,prefix):
    """Persistent aliases only; never rewrite historical payloads or internal IDs."""
    codes={r['identifier']:f"{r['prefix']}{r['branch']}-{r['number']:06d}" for r in c.db.execute('SELECT * FROM simulated_receipt_codes')}
    result=[]
    for e in sorted(rows,key=lambda e:(e.get('at') or e.get('opened_at') or e.get('created',''),e['id'])):
        if e['id'] not in codes:
            c.db.execute('INSERT INTO simulated_receipt_codes(identifier,prefix,branch) VALUES(?,?,?) ON CONFLICT(identifier) DO NOTHING',(e['id'],prefix,e['branch']))
            row=c.db.execute('SELECT * FROM simulated_receipt_codes WHERE identifier=?',(e['id'],)).fetchone()
            codes[e['id']]=f"{row['prefix']}{row['branch']}-{row['number']:06d}"
        result.append({**e,'short_code':codes[e['id']]})
    return result

def order_code(c,o):
    if not o.get('simulated'):return o
    return assign_codes(c,[o],'SA' if o['kind']=='layaway' else 'SR')[0]

def init(c):
    init_codes(c)
    c.db.executescript('CREATE TABLE IF NOT EXISTS simulated_sales(id text PRIMARY KEY,batch text NOT NULL,body text NOT NULL);')

def sales(c):
    return assign_codes(c,[json.loads(r[0]) for r in c.db.execute('SELECT body FROM simulated_sales ORDER BY id')],'SV')

def receipt(c, ident):
    r=c.db.execute('SELECT body FROM simulated_sales WHERE id=?',(ident,)).fetchone()
    if not r:return None
    e=json.loads(r[0]);e['template']=c.get('simulation-template:'+e['simulation_batch'])
    return assign_codes(c,[e],'SV')[0]
