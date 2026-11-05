"""POS queue delivery and atomic acknowledgement persistence."""
from domain import RuleError
import json
class SynchronizationService:
    def sync(self,uid):
        if self.get('offline'):return
        acknowledgements=[]
        for row in self.rows():
            if row['status']=='pending':
                reply=self.transport('receive',json.loads(row['body']))
                acknowledgements.append((reply['status'],reply['issue'],row['id']))
        creds=self.get('credentials');c=creds[uid]
        try:pull=self.transport('pull',{'grant':c['grant']})
        except RuleError:
            # Accepted queued facts remain accepted; new work requires fresh access.
            del creds[uid];self.put('credentials',creds);raise
        self.db.execute('BEGIN IMMEDIATE')
        try:
            self.db.executemany('UPDATE operations SET status=?,issue=? WHERE id=?',acknowledgements)
            self.put('catalog',pull['catalog']);self.put('template',pull['template']);self.put('last_sync',pull['at']);self.put('cash_adjustments',pull['cash_adjustments']);self.put('corrections',pull['corrections']);self.put('staff',pull['staff']);self.put('catalog_meta',pull['meta']);self.put('order_cash_moves',pull.get('order_cash_moves',[]));self.put('exchange_moves',pull.get('exchange_moves',[]));self.put('exchange_receipts',pull.get('exchange_receipts',[]))
            self.db.execute('COMMIT')
        except Exception:self.db.execute('ROLLBACK');raise
        if pull['relogin']:
            # Role/password changes refresh permissions but require password authentication again.
            del creds[uid];self.put('credentials',creds);raise RuleError('Tu acceso cambió. Inicia sesión otra vez conectado.')
        c.update(grant=pull['grant'],snapshot=pull['snapshot']);self.put('credentials',creds)
        self.put('catalog',pull['catalog']);self.put('template',pull['template']);self.put('last_sync',pull['at']);self.put('cash_adjustments',pull['cash_adjustments']);self.put('corrections',pull['corrections']);self.put('staff',pull['staff']);self.put('catalog_meta',pull['meta']);self.put('order_cash_moves',pull.get('order_cash_moves',[]));self.put('exchange_moves',pull.get('exchange_moves',[]));self.put('exchange_receipts',pull.get('exchange_receipts',[]));self.copy()
