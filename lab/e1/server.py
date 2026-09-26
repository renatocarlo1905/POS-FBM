#!/usr/bin/env python3
"""Run three loopback HTTP services. No original project database is touched."""
import argparse, json, os, signal, threading, time, urllib.request, urllib.error, secrets
import extensions as ext
import simulated
import cash_reports
import order_service as orders
import csv, io
from contextlib import nullcontext
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from core import Central, Store, RuleError, require, pack, now, template, receipt_pdf, PERMS

STATIC=Path(__file__).parent/'static'
class Application:
    def __init__(self,data,port,pg_config=None):
        self.data=Path(data);self.data.mkdir(parents=True,exist_ok=True);os.chmod(self.data,0o700)
        self.port=port;self.central=Central(pg_config or Path(__file__).parent/'data/postgres.json');self.internal=os.urandom(32).hex();self.downloads={};self.login_attempts={};self.services=[]
        def transport(action,payload):
            req=urllib.request.Request(f'http://127.0.0.1:{port}/internal/{action}',data=pack(payload).encode(),headers={'Content-Type':'application/json','X-Lab-Service':self.internal},method='POST')
            try:
                with urllib.request.urlopen(req,timeout=4) as r:return json.load(r)
            except urllib.error.HTTPError as e:raise RuleError(json.load(e).get('error','Central rechazó la petición.'))
            except (urllib.error.URLError,TimeoutError,ConnectionError):raise ConnectionError('Central no disponible; operaciones locales conservadas.')
        simulated.init(self.central);cash_reports.init(self.central);orders.init(self.central)
        self.stores={b:Store(self.data/f'sucursal-{b}.sqlite3',b,transport,self.data/'second-copy') for b in (1,2)}
    def handler(self,branch):
        app=self
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args):pass
            def reply(self,value,status=200,ctype='application/json',filename=None):
                body=pack(value).encode() if ctype=='application/json' else value
                self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(body)));self.send_header('Cache-Control','no-store');self.send_header('X-Content-Type-Options','nosniff')
                self.send_header('Content-Security-Policy',"default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data:; object-src 'none'; frame-ancestors 'none'; base-uri 'none'")
                if filename:self.send_header('Content-Disposition',f'attachment; filename="{filename}"')
                self.end_headers();self.wfile.write(body)
            def pdf_reply(self,pdf,filename,data):
                if data.get('preview_window'):
                    from receipt_view import render_pages
                    return self.reply({'title':filename.removesuffix('.pdf'),'pages':render_pages(pdf)})
                if data.get('download'):
                    key=secrets.token_urlsafe(24);app.downloads[key]=(time.time()+60,branch,pdf,filename);return self.reply({'url':'/download/'+key})
                return self.reply(pdf,ctype='application/pdf',filename=filename)
            def do_GET(self):self.handle_request(False)
            def do_POST(self):self.handle_request(True)
            def handle_request(self,post):
                try:
                    expected=f'127.0.0.1:{app.port+branch}'
                    require(self.headers.get('Host') in (expected,f'localhost:{app.port+branch}'),'Host no permitido.')
                    origin=self.headers.get('Origin');require(not origin or origin in ('http://'+expected,f'http://localhost:{app.port+branch}'),'Origen no permitido.')
                    path=self.path.split('?')[0];data={};token=self.headers.get('Authorization','').removeprefix('Bearer ')
                    if post:
                        length=int(self.headers.get('Content-Length',0));require(0<length<700000,'Tamaño inválido.');data=json.loads(self.rfile.read(length));require(isinstance(data,dict),'Formato inválido.')
                    def manage(uid,origin,route,payload):
                        u=next(u for u in app.central.get('users') if u['id']==uid);policy=app.central.policy(u)
                        if route in ('product','ingress','provider','category','category-edit','category-delete'):
                            require(policy.get('product_create'),'Sin permiso para ingresar productos.');result={'product':ext.create_product,'ingress':ext.ingress,'provider':ext.provider,'category':ext.create_category,'category-edit':ext.edit_category,'category-delete':ext.delete_category}[route](app.central,uid,payload)
                        elif route=='correction-view':result=ext.sale_view(app.central,payload['target']);require(not origin or result['original']['branch']==origin,'Operación de otra sucursal.')
                        elif route=='correction-preview':result=ext.correction_preview(app.central,uid,origin,payload)
                        elif route=='correction':result=ext.correct(app.central,uid,origin,payload)
                        else:raise RuleError('Acción desconocida.')
                        app.central.backup(app.data/'backups/central.sqlite3');return result
                    if path.startswith('/download/') and not post:
                        item=app.downloads.pop(path.rsplit('/',1)[-1],None);require(item and item[0]>time.time() and item[1]==branch,'Descarga vencida. Genera el PDF de nuevo.');return self.reply(item[2],ctype=item[4] if len(item)>4 else 'application/pdf',filename=item[3])
                    if path.startswith('/internal/'):
                        require(branch==0 and post and self.headers.get('X-Lab-Service')==app.internal,'Servicio no autorizado.')
                        action=path.rsplit('/',1)[-1]
                        if action=='login':result=app.central.login(data['user'],data['password'],data['branch'])
                        elif action=='pull':result=app.central.pull(data['grant'])
                        elif action=='receive':result=app.central.receive(data);app.central.backup(app.data/'backups/central.sqlite3')
                        elif action=='manage':
                            with app.central.lock:
                                g=app.central.verify(data['grant']);u=next((u for u in app.central.get('users') if u['id']==g['user']),None);require(u and u['active'] and g['branch'] in u['branches'],'Acceso revocado.');result=manage(u['id'],g['branch'],data['route'],data['data'])
                        else:raise RuleError('Ruta inexistente.')
                        return self.reply(result)
                    if path=='/api/login' and post:
                        key=(branch,str(data.get('user','')).lower());attempts=[t for t in app.login_attempts.get(key,[]) if time.time()-t<60]
                        require(len(attempts)<10,'Demasiados intentos. Espera un minuto.')
                        try:
                            if branch:result=app.stores[branch].login(data.get('user',''),data.get('password',''))
                            else:result={'token':app.central.login(data.get('user',''),data.get('password',''),0)['token']}
                            app.login_attempts.pop(key,None)
                        except RuleError:app.login_attempts[key]=attempts+[time.time()];raise
                        return self.reply(result)
                    if path=='/api/logout' and post:
                        if branch:app.stores[branch].sessions.pop(token,None)
                        else:
                            with app.central.lock:
                                sessions=app.central.get('sessions');sessions.pop(token,None);app.central.put('sessions',sessions)
                        return self.reply({'ok':True})
                    if path in ('/api/orders','/api/order-write','/api/order-pdf'):
                        with (app.stores[branch].lock if branch else nullcontext()):
                            if branch:
                                store=app.stores[branch]
                                with store.lock:
                                    uid,credential=store.auth(token);require(not store.get('offline'),'Apartados y reparaciones requieren conexión.');store.sync(uid);uid,credential=store.auth(token)
                                    with app.central.lock:
                                        user=next((x for x in app.central.get('users') if x['id']==uid),None)
                                        require(user and user['active'] and branch in user['branches'] and user['revision']==credential['snapshot']['revision'],'Acceso revocado o modificado.')
                            else:user=app.central.auth(token,admin=True)
                            with app.central.lock:
                                if branch:
                                    user=next((x for x in app.central.get('users') if x['id']==uid),None);require(user and user['active'] and branch in user['branches'] and user['revision']==credential['snapshot']['revision'],'Acceso revocado o modificado.')
                                else:user=app.central.auth(token,admin=True)
                                policy=app.central.policy(user);require(policy.get('admin') or policy.get('orders',policy.get('sell')),'Sin permiso para gestionar órdenes.')
                                if path=='/api/orders' and not post:
                                    result=orders.all_orders(app.central)
                                    if not policy.get('admin') and not policy.get('cost'):
                                        for order in result:
                                            def hide_cost(value):
                                                if isinstance(value,dict):
                                                    value.pop('cost',None)
                                                    for child in value.values():hide_cost(child)
                                                elif isinstance(value,list):
                                                    for child in value:hide_cost(child)
                                            hide_cost(order)
                                    for order in result:
                                        credit=app.central.db.execute('SELECT amount FROM order_credit WHERE phone=?',(order['customer']['phone'],)).fetchone();order['customer_credit']=credit[0] if credit else 0
                                        order.pop('documents',None)
                                        if not policy.get('admin'):
                                            for history in order['history']:history.pop('before',None)
                                            order.pop('sale',None);order.pop('replacement_sale',None)
                                    return self.reply({'settings':app.central.get('order_settings',{'layaway_days':45,'repair_days':45}),'rows':result,'asOf':now()[:10],'admin':user['role']=='admin','can_pdf':bool(policy.get('admin') or policy.get('receipts') and policy.get('reprint'))})
                                if path=='/api/order-write' and post:
                                    result=orders.execute(app.central,user,branch,data);app.central.backup(app.data/'backups/central.sqlite3');return self.reply(result)
                                if path=='/api/order-pdf' and post:
                                    require(policy.get('admin') or policy.get('receipts') and policy.get('reprint'),'Sin permiso para descargar comprobantes.')
                                    import orders_preview
                                    order=orders.get(app.central,data.get('id'));index=data.get('index');require(type(index)is int and index>=0,'Comprobante inválido.')
                                    if order.get('documents'):
                                        require(index<len(order['documents']),'Comprobante inexistente.');doc=order['documents'][index];pdf,filename=orders_preview.receipt_pdf(order['id'],doc['index'],doc['order'])
                                    else:pdf,filename=orders_preview.receipt_pdf(order['id'],index,order)
                                    return self.pdf_reply(pdf,filename,data)
                                raise RuleError('Ruta de órdenes inválida.')
                    if path.startswith('/api/'):
                        if branch:
                            store=app.stores[branch]
                            with store.lock:
                                uid,c=store.auth(token)
                                if path=='/api/state' and not post:return self.reply(store.state(token))
                                if path=='/api/offline' and post:
                                    require(type(data.get('offline'))is bool,'Estado inválido.');store.put('offline',data['offline']);return self.reply({'ok':True})
                                if path=='/api/operation' and post:return self.reply(store.submit(token,data.get('kind'),data.get('data',{}),data.get('request_id')))
                                if path in ('/api/product','/api/ingress','/api/provider','/api/category','/api/category-edit','/api/category-delete','/api/correction-view','/api/correction-preview','/api/correction') and post:
                                    require(not store.get('offline'),'Esta operación requiere conexión.');store.sync(uid);uid,c=store.auth(token);result=store.transport('manage',{'grant':c['grant'],'route':path.rsplit('/',1)[-1],'data':data});store.sync(uid);return self.reply(result)
                                if path=='/api/pdf' and post:
                                    require(c['snapshot']['policy'].get('receipts') and c['snapshot']['policy'].get('reprint'),'Sin permiso para consultar o descargar comprobantes.')
                                    r=store.db.execute('SELECT * FROM operations WHERE id=?',(data.get('id'),)).fetchone()
                                    if not r:
                                        doc=next((d for d in store.get('corrections',[]) if d['id']==data.get('id') and d['payload']['origin']=='POS'),None)
                                        if not doc:
                                            source=next((d for d in store.get('corrections',[]) if (d['payload'].get('replacement') or {}).get('id')==data.get('id')),None);require(source,'Comprobante no disponible.')
                                            doc={'id':data['id'],'branch':branch,'kind':'sale','at':source['payload']['original_at'],'actor_name':source['payload']['operator'],'template':source['template'],'payload':source['payload']['replacement']}
                                        return self.pdf_reply(receipt_pdf(doc,True),'comprobante-'+doc['id'][:8]+'.pdf',data)
                                    require(r['status']!='rejected','Comprobante no disponible.')
                                    count=store.get('pdf:'+r['id'],0);pdf=receipt_pdf(json.loads(r['body']),count>0);store.put('pdf:'+r['id'],count+1)
                                    return self.pdf_reply(pdf,f'E1-S{branch}-{r["id"][:8]}.pdf',data)
                        else:
                            with app.central.lock:
                                u=app.central.auth(token,admin=True);actor=u['id']
                                if path=='/api/order-demo-pdf' and post:
                                    import orders_preview
                                    pdf,filename=orders_preview.receipt_pdf(data.get('id'),data.get('index'));return self.pdf_reply(pdf,filename,data)
                                if path=='/api/report-export' and post:
                                    lines=data.get('rows');require(isinstance(lines,list) and len(lines)<=10000 and all(isinstance(row,list) and len(row)<=20 for row in lines),'Reporte inválido.')
                                    output=io.StringIO();writer=csv.writer(output)
                                    for row in lines:
                                        clean=[]
                                        for cell in row:
                                            text=str(cell if cell is not None else '');clean.append("'"+text if isinstance(cell,str) and text.startswith(('=','+','-','@','\t','\r')) else text)
                                        writer.writerow(clean)
                                    key=secrets.token_urlsafe(24);app.downloads[key]=(time.time()+60,branch,('\ufeff'+output.getvalue()).encode('utf-8'),'reporte-ventas.csv','text/csv; charset=utf-8');return self.reply({'url':'/download/'+key})
                                if path=='/api/cash-reports' and not post:return self.reply(cash_reports.report(app.central))
                                if path=='/api/cash-export' and post:
                                    ids=data.get('ids',[]);require(isinstance(ids,list) and len(ids)<=10000 and all(isinstance(x,str) for x in ids),'Selección inválida.')
                                    selected=set(ids);output=io.StringIO();writer=csv.writer(output)
                                    writer.writerow(['Folio','Origen','Sucursal','Apertura','Cierre','Abierta por','Cerrada por','Esperado MXN','Contado MXN','Descuadre MXN'])
                                    def safe(v):
                                        v=str(v or '');return "'"+v if v.startswith(('=','+','-','@','\t','\r')) else v
                                    for r in cash_reports.report(app.central):
                                        if r['id'] in selected:writer.writerow([safe(r['id']),'Simulada' if r['simulated'] else 'Manual',r['branch'],r['opened_at'],r['closed_at'] or '',safe(r['opened_by']),safe(r['closed_by']),format(r['expected']/100,'.2f'),'' if r['counted'] is None else format(r['counted']/100,'.2f'),'' if r['difference'] is None else format(r['difference']/100,'.2f')])
                                    key=secrets.token_urlsafe(24);app.downloads[key]=(time.time()+60,branch,('\ufeff'+output.getvalue()).encode('utf-8'),'reporte-cajas.csv','text/csv; charset=utf-8');return self.reply({'url':'/download/'+key})
                                if path=='/api/state' and not post:
                                    events=[]
                                    for r in reversed(app.central.events()):
                                        e=json.loads(r['body']);e.pop('grant');e.pop('input');e['payload'].pop('request',None);events.append({**e,'status':r['status'],'issue':r['issue'],'received_at':r['received'],**({'adjusted':ext.sale_view(app.central,e['id'])['adjusted']} if e['kind']=='sale' and r['status']=='accepted' else {})})
                                    events.extend(simulated.sales(app.central));events.extend(orders.sale_events(app.central));events.extend(orders.collection_events(app.central));events.sort(key=lambda e:e['at'],reverse=True)
                                    return self.reply({'user':u['name'],'users':app.central.users(),'roles':app.central.get('roles'),'permissions':PERMS,'catalog':app.central.catalog(True),'templates':app.central.get('templates'),'operations':events,'audit':[dict(r) for r in app.central.db.execute('SELECT * FROM audit ORDER BY id DESC LIMIT 30')],'at':now(),'corrections':ext.corrections(app.central),'materials':app.central.get('materials'),'types':app.central.get('types'),'categories':app.central.get('categories',[]),'providers':app.central.get('providers'),'warehouses':ext.WAREHOUSES,'inventory_entries':[dict(r) for r in app.central.db.execute('SELECT * FROM inventory_entries ORDER BY at DESC LIMIT 50')]})
                                if path in ('/api/product','/api/ingress','/api/provider','/api/category','/api/category-edit','/api/category-delete','/api/correction-view','/api/correction-preview','/api/correction') and post:return self.reply(manage(actor,0,path.rsplit('/',1)[-1],data))
                                if path=='/api/employee' and post:app.central.edit_user(actor,data)
                                elif path=='/api/role' and post:app.central.edit_role(actor,data)
                                elif path=='/api/template' and post:
                                    b=str(data.get('branch'));require(b in ('1','2'),'Sucursal inválida.');templates=app.central.get('templates');templates[b]=template(data);app.central.put('templates',templates);app.central.audit(actor,'template_updated',{'branch':b})
                                elif path=='/api/backup' and post:app.central.backup(app.data/'backups/manual-central.sqlite3');app.central.audit(actor,'backup_created',{})
                                elif path=='/api/preview' and post:
                                    t=template(data);e={'id':'VISTA-PREVIA-SIN-OPERACION','branch':data.get('branch',1),'kind':'sale','at':now(),'actor_name':'Ejemplo','template':t,'payload':{'items':[{'qty':1,'name':'Anillo espiral','price':100000,'net':90000}],'gross':100000,'discount':10000,'total':90000,'received_cash':100000,'cash':90000,'change':10000,'card':0,'transfer':0}}
                                    return self.pdf_reply(receipt_pdf(e),'vista-previa-ticket.pdf',data)
                                elif path=='/api/pdf' and post:
                                    order_id='-'.join(str(data.get('id','')).split('-')[:2])
                                    if order_id.startswith(('APA-','REP-')):
                                        import orders_preview
                                        order=orders.get(app.central,order_id);doc=order['documents'][-1] if '-CAMBIO-' in str(data.get('id','')) else next((x for x in reversed(order['documents']) if x['label'] in ('Liquidación','Anticipo')),order['documents'][-1]);pdf,filename=orders_preview.receipt_pdf(order_id,doc['index'],doc['order']);return self.pdf_reply(pdf,filename,data)
                                    r=app.central.db.execute('SELECT * FROM events WHERE id=?',(data.get('id'),)).fetchone();event=json.loads(r['body']) if r and r['status']=='accepted' else simulated.receipt(app.central,data.get('id')) or ext.sale_view(app.central,data.get('id'))['original'];return self.pdf_reply(receipt_pdf(event,True),'E1-'+event['id'][:8]+'.pdf',data)
                                else:raise RuleError('Ruta no disponible.')
                                app.central.backup(app.data/'backups/central.sqlite3');return self.reply({'ok':True})
                        raise RuleError('Ruta no disponible.')
                    require(not post,'Ruta no disponible.')
                    entry='dashboard.html' if branch==0 else f'sucursal-{branch}.html'
                    name=entry if path=='/' else path.lstrip('/')
                    require(name in (entry,'receipt-view.html','receipt-view.js','receipt-view.css','brand-symbol.png','brand-name.png','app.js','extra.js','cash-reports.js','sales-model.js','sales-reports.js','orders-demo.js','orders-model.js','orders.js','styles.css','company-logo.png','Montserrat-Regular.ttf','Montserrat-Bold.ttf'),'Archivo no disponible.')
                    ctype='image/png' if name.endswith('.png') else 'font/ttf' if name.endswith('.ttf') else 'text/html; charset=utf-8' if name.endswith('.html') else 'text/css; charset=utf-8' if name.endswith('.css') else 'text/javascript; charset=utf-8'
                    return self.reply((STATIC/name).read_bytes(),ctype=ctype)
                except RuleError as e:self.reply({'error':str(e)},400)
                except (KeyError,ValueError,TypeError) as e:self.reply({'error':'Solicitud incompleta o inválida.'},400)
                except Exception as e:
                    import traceback;traceback.print_exc();self.reply({'error':'Error del laboratorio. La cola se conserva; revisa el registro del servidor.'},500)
        return Handler
    def start(self):
        for branch in (0,1,2):
            server=ThreadingHTTPServer(('127.0.0.1',self.port+branch),self.handler(branch));self.services.append(server)
            threading.Thread(target=server.serve_forever,daemon=True).start()
    def stop(self):
        for s in self.services:s.shutdown();s.server_close()
        for db in [self.central,*self.stores.values()]:db.db.close()

def main():
    p=argparse.ArgumentParser();p.add_argument('--port',type=int,default=8870);p.add_argument('--data',default=str(Path(__file__).parent/'data'));args=p.parse_args()
    os.umask(0o077);app=Application(args.data,args.port);app.start()
    print('Laboratorio E1 disponible:',flush=True)
    for b,name in [(0,'dashboard'),(1,'sucursal-1'),(2,'sucursal-2')]:print(f'http://127.0.0.1:{args.port+b}/{name}.html',flush=True)
    try:
        while True:time.sleep(1)
    except KeyboardInterrupt:app.stop()
if __name__=='__main__':main()
