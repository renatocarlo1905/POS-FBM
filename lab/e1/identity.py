"""Password verification, grants, employees and role policies."""
import base64, hashlib, hmac, json, secrets, uuid
from domain import RuleError, require, now, pack, cleantext, percent
from defaults import PERMS
def hashed(password,salt=None):
    salt=salt or secrets.token_hex(16)
    return salt+':'+hashlib.pbkdf2_hmac('sha256',password.encode(),bytes.fromhex(salt),210000).hex()

def matches(password,value): return hmac.compare_digest(hashed(password,value.split(':')[0]),value)


class IdentityService:
    def policy(self,u):
        r=self.get('roles')[u['role']];return {**r['permissions'],'inventory_view':bool(r['permissions'].get('inventory_view',u['role']=='admin')),'max_discount':r['max_discount'],'admin':u['role']=='admin'}

    def sign(self,payload):
        body=base64.urlsafe_b64encode(pack(payload).encode()).decode()
        return body+'.'+hmac.new(bytes.fromhex(self.get('secret')),body.encode(),hashlib.sha256).hexdigest()

    def verify(self,token):
        try:
            body,sig=token.split('.');expected=hmac.new(bytes.fromhex(self.get('secret')),body.encode(),hashlib.sha256).hexdigest()
            require(hmac.compare_digest(sig,expected),'Autorización inválida.');return json.loads(base64.urlsafe_b64decode(body))
        except (ValueError,TypeError,AttributeError):raise RuleError('Autorización inválida.')

    def login(self,username,password,branch):
        with self.lock:
            u=next((u for u in self.get('users') if u['id']==username.lower()),None)
            require(u and u['active'] and matches(password,u['password']),'Usuario o contraseña incorrectos.')
            require(branch==0 and u['role']=='admin' or branch in u['branches'],'Sin acceso a esta aplicación o sucursal.')
            snapshot={'user':u['id'],'name':u['name'],'branch':branch,'revision':u['revision'],'policy':self.policy(u),'issued_at':now(),'nonce':secrets.token_hex(12)}
            grant=self.sign(snapshot); sessions=self.get('sessions');token=secrets.token_urlsafe(32);sessions[token]={'user':u['id'],'revision':u['revision'],'branch':branch};self.put('sessions',sessions)
            return {'token':token,'grant':grant,'snapshot':snapshot,'verifier':u['password']}

    def auth(self,token,admin=False):
        s=self.get('sessions',{}).get(token);require(s,'Inicia sesión de nuevo.')
        u=next((u for u in self.get('users') if u['id']==s['user']),None)
        require(u and u['active'] and u['revision']==s['revision'],'Tu acceso cambió; inicia sesión de nuevo.')
        require(not admin or u['role']=='admin','Acceso exclusivo de administrador.');return u

    def users(self):return [{**{k:v for k,v in u.items() if k!='password'},'seller_code':'FBV-'+u['id'].upper()} for u in self.get('users')]

    def edit_user(self,actor,data):
        with self.lock:
            users=self.get('users');uid=cleantext(data.get('id',''),50).lower();u=next((u for u in users if u['id']==uid),None)
            require(u,'Empleado inexistente.');role=data.get('role');require(role in self.get('roles'),'Rol inexistente.')
            require(uid!='carlo' or role=='admin' and data.get('active',True),'Carlo debe conservar acceso de administrador.')
            bs=data.get('branches',[1,2]);require(isinstance(bs,list) and bs and all(type(b)is int and b in (1,2) for b in bs),'Selecciona sucursales válidas.')
            password=data.get('password','');require(not password or 8<=len(password)<=128,'La nueva contraseña debe tener 8 a 128 caracteres.')
            u.update(name=cleantext(data.get('name',''),80),email=cleantext(data.get('email',''),120),phone=cleantext(data.get('phone',''),30),role=role,active=bool(data.get('active')),branches=sorted(set(bs)),revision=u['revision']+1)
            require(u['name'],'El nombre es obligatorio.')
            if password:u['password']=hashed(password)
            self.put('users',users);self.audit(actor,'employee_updated',{'id':uid,'role':role,'password_changed':bool(password)})

    def edit_role(self,actor,data):
        with self.lock:
            roles=self.get('roles');rid=data.get('id') or 'role-'+uuid.uuid4().hex[:8];require(rid!='admin','El rol administrador conserva todos los derechos.')
            name=cleantext(data.get('name',''),80);require(name,'Nombre obligatorio.')
            roles[rid]={'name':name,'permissions':{k:bool(data.get('permissions',{}).get(k,False)) for k in PERMS},'max_discount':percent(data.get('max_discount',0))}
            self.put('roles',roles);users=self.get('users')
            for u in users:
                if u['role']==rid:u['revision']+=1
            self.put('users',users);self.audit(actor,'role_updated',{'id':rid,'role':roles[rid]})
