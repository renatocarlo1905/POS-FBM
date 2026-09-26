"""Create an isolated PostgreSQL 18 laboratory, bound only to loopback."""
import json, os, secrets, subprocess, time
from pathlib import Path
ROOT=Path(__file__).parent;DATA=ROOT/'data';DATA.mkdir(exist_ok=True);DATA.chmod(0o700)
config=DATA/'postgres.json';envfile=DATA/'postgres.env'
if not config.exists():
    config.write_text(json.dumps({'host':'127.0.0.1','port':55432,'dbname':'pos_e1','user':'pos_e1_app','password':secrets.token_urlsafe(32)}));config.chmod(0o600)
if not envfile.exists():
    envfile.write_text('POSTGRES_USER=pos_e1_admin\nPOSTGRES_PASSWORD='+secrets.token_urlsafe(32)+'\nPOSTGRES_DB=postgres\n');envfile.chmod(0o600)
name='pos-frida-e1-postgres'
exists=subprocess.run(['docker','container','inspect',name],capture_output=True).returncode==0
if exists:subprocess.run(['docker','start',name],check=True,stdout=subprocess.DEVNULL)
else:subprocess.run(['docker','run','-d','--name',name,'--memory','512m','--env-file',str(envfile),'--publish','127.0.0.1:55432:5432','--mount','type=volume,source=pos-frida-e1-pgdata,target=/var/lib/postgresql','postgres:18@sha256:4ef4dbc939d61acea57712655ddb4b4ab27419c913f94cca0cd57cb3ea3c2280'],check=True,stdout=subprocess.DEVNULL)
for _ in range(40):
    if subprocess.run(['docker','exec',name,'pg_isready','-U','pos_e1_admin'],capture_output=True).returncode==0:break
    time.sleep(.5)
else:raise SystemExit('PostgreSQL no disponible.')
def sql(query):return subprocess.run(['docker','exec','-i',name,'psql','-X','-v','ON_ERROR_STOP=1','-U','pos_e1_admin','-d','postgres','-At'],input=query,text=True,capture_output=True,check=True).stdout.strip()
c=json.loads(config.read_text())
if sql("SELECT 1 FROM pg_roles WHERE rolname='pos_e1_app'")!='1':sql("CREATE ROLE pos_e1_app LOGIN PASSWORD '"+c['password']+"' NOSUPERUSER NOCREATEDB NOCREATEROLE;")
if sql("SELECT 1 FROM pg_database WHERE datname='pos_e1'")!='1':sql('CREATE DATABASE pos_e1 OWNER pos_e1_app;')
print('PostgreSQL E1 listo en 127.0.0.1:55432. Base pos_e1; rol de aplicación sin superusuario. Credenciales guardadas localmente.')
