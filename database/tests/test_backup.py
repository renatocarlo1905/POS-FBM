"""Restore the latest development backup into a disposable DB and compare catalogs."""
import sys,subprocess,uuid
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from manage import sql,NAME,ROOT

db='pos_restore_'+uuid.uuid4().hex[:12]
sql('CREATE DATABASE '+db)
try:
    dump=sorted((ROOT/'backups').glob('*.dump'))[-1]
    with dump.open('rb') as stream:
        subprocess.run(['docker','exec','-i',NAME,'pg_restore','-U','pos_owner','-d',db,
            '--exit-on-error','--no-owner'],stdin=stream,check=True,capture_output=True)
    for query in [
        "SELECT table_name,column_name,data_type,is_nullable FROM information_schema.columns WHERE table_schema='pos' ORDER BY table_name,ordinal_position",
        "SELECT * FROM pos.schema_migrations ORDER BY version",
        "SELECT * FROM pos.branches ORDER BY code",
        "SELECT * FROM pos.warehouses ORDER BY code",
        "SELECT * FROM pos.locations ORDER BY code",
        "SELECT count(*) FROM pos.sales",
        "SELECT proname,pg_get_functiondef(oid) FROM pg_proc WHERE pronamespace='pos'::regnamespace ORDER BY proname"
    ]:
        assert sql(query,db)==sql(query),'Restore mismatch: '+query
    print('PASS backup restored; columns, functions, migrations, branches, warehouses, locations and sale count match')
finally:
    sql('DROP DATABASE '+db+' WITH (FORCE)')
