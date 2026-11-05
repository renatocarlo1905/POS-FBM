"""Public receipt identifiers; UUIDs remain the immutable internal keys.

One durable POS queue per branch owns the existing unique (branch, seq).
V codes use that sequence offline as well as online. R/C codes are allocated
centrally for replacement sales and commercial exchanges respectively.
"""
import json

def code(event):
    if event.get('kind')=='sale' and type(event.get('seq')) is int:
        return f"V{event['branch']}-{event['seq']:06d}"
    return event.get('short_code') or event.get('payload',{}).get('short_code') or event['id']

def allocate(c,identifier,branch,prefix):
    c.db.execute('INSERT INTO receipt_codes(identifier,branch,prefix) VALUES(?,?,?) ON CONFLICT(identifier) DO NOTHING',(identifier,branch,prefix))
    row=c.db.execute('SELECT branch,prefix,number FROM receipt_codes WHERE identifier=?',(identifier,)).fetchone()
    return f"{row['prefix']}{row['branch']}-{row['number']:06d}"

def decorate(c,event):
    event=dict(event)
    if event.get('kind')=='sale' and event.get('seq') is not None:event['short_code']=code(event)
    else:
        identifier=event.get('exchange_id') or event['id']
        if not identifier.startswith(('R-','CAM-')):return event
        row=c.db.execute('SELECT branch,prefix,number FROM receipt_codes WHERE identifier=?',(identifier,)).fetchone()
        if row:event['short_code']=f"{row['prefix']}{row['branch']}-{row['number']:06d}"
    return event

def corrections(c,doc):
    doc=json.loads(json.dumps(doc));p=doc['payload']
    original=c.db.execute('SELECT body FROM events WHERE id=?',(p['target'],)).fetchone()
    p['target_code']=code(decorate(c,json.loads(original[0]) if original else {'id':p['target']}))
    if p.get('replacement'):p['replacement']=decorate(c,p['replacement'])
    return doc

def init(c):
    c.db.executescript("""CREATE TABLE IF NOT EXISTS receipt_codes(
      identifier text PRIMARY KEY, branch integer NOT NULL CHECK(branch IN (1,2)),
      prefix text NOT NULL CHECK(prefix IN ('R','C')),
      number bigint GENERATED ALWAYS AS IDENTITY UNIQUE);
      DROP TRIGGER IF EXISTS immutable_receipt_codes ON receipt_codes;
      CREATE TRIGGER immutable_receipt_codes BEFORE UPDATE OR DELETE ON receipt_codes
      FOR EACH ROW EXECUTE FUNCTION prevent_fact_change();""")
    for row in c.db.execute('SELECT document FROM corrections ORDER BY ordinal'):
        d=json.loads(row[0]);replacement=d['payload'].get('replacement')
        if replacement:allocate(c,replacement['id'],d['branch'],'R')
    for row in c.db.execute('SELECT body FROM merchandise_exchanges ORDER BY id'):
        d=json.loads(row[0]);allocate(c,d['id'],d['branch'],'C')
