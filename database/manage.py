"""Local development database lifecycle, migrations and backup (stdlib only)."""
from pathlib import Path
import subprocess, sys, time

ROOT = Path(__file__).resolve().parent.parent
NAME = 'pos-postgres-desarrollo'
IMAGE = 'postgres:18@sha256:4ef4dbc939d61acea57712655ddb4b4ab27419c913f94cca0cd57cb3ea3c2280'

def sql(text, database='pos_desarrollo'):
    return subprocess.run(['docker','exec','-i',NAME,'psql','-X','-v','ON_ERROR_STOP=1',
        '-U','pos_owner','-d',database,'-At'],input=text,text=True,capture_output=True,check=True).stdout.strip()

def migrate(database='pos_desarrollo'):
    exists = sql("SELECT to_regclass('pos.schema_migrations') IS NOT NULL",database)=='t'
    applied = set(sql('SELECT version FROM pos.schema_migrations',database).splitlines()) if exists else set()
    for f in sorted((ROOT/'database/migrations').glob('*.sql')):
        version=str(int(f.name.split('_')[0]))
        if version not in applied:
            sql(f.read_text(),database)
            print('Applied',f.name)

if __name__=='__main__':
    action=sys.argv[1] if len(sys.argv)>1 else 'status'
    if action=='start':
        known=subprocess.run(['docker','container','inspect',NAME],capture_output=True).returncode==0
        if known:
            subprocess.run(['docker','start',NAME],check=True)
        else:
            subprocess.run(['docker','run','-d','--name',NAME,'--memory','768m',
                '--env-file',str(ROOT/'.postgres.env'),'--mount',
                'type=volume,source=pos-postgres-desarrollo-data,target=/var/lib/postgresql',IMAGE],check=True)
        for _ in range(30):
            try:
                sql('SELECT 1'); break
            except subprocess.CalledProcessError: time.sleep(1)
        else: raise RuntimeError('PostgreSQL not ready')
        migrate()
    elif action=='migrate': migrate()
    elif action=='stop': subprocess.run(['docker','stop',NAME],check=True)
    elif action=='backup':
        from datetime import datetime
        folder=ROOT/'backups'; folder.mkdir(exist_ok=True)
        path=folder/('pos_desarrollo_'+datetime.now().strftime('%Y%m%d_%H%M%S')+'.dump')
        with path.open('xb') as stream:
            subprocess.run(['docker','exec',NAME,'pg_dump','-U','pos_owner','-d','pos_desarrollo','-Fc'],stdout=stream,check=True)
        path.chmod(0o600); print(path)
    elif action=='status': print(sql("SELECT current_database(),version(); SELECT * FROM pos.schema_migrations;"))
    else: raise SystemExit('Use start, stop, migrate, status or backup')
