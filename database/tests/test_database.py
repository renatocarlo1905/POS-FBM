"""Real PostgreSQL integration tests; always uses a disposable database."""
import sys, uuid, json, subprocess, concurrent.futures
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from manage import sql, migrate

db='pos_test_'+uuid.uuid4().hex[:12]
def q(s): return sql(s,db)
def literal(v): return "'"+str(v).replace("'","''")+"'"
def assert_equal(actual,expected):
    assert actual==str(expected), (actual,expected)
def rejected(statement):
    try: q(statement)
    except subprocess.CalledProcessError: return
    raise AssertionError('Expected failure')

sql('CREATE DATABASE '+db)
passed=[]
try:
    migrate(db)
    ids={k:str(uuid.uuid4()) for k in ['staff','product','t1','t2','s1','s2']}
    q(f"""
    INSERT INTO pos.staff(id,code,display_name) VALUES('{ids['staff']}','TEST','Persona de prueba');
    INSERT INTO pos.products(id,barcode,short_description,reference_price) VALUES('{ids['product']}','0000123','Anillo de prueba',100.25);
    INSERT INTO pos.terminals(id,branch_id,location_id,code) VALUES
      ('{ids['t1']}','00000000-0000-4000-8000-000000000001','20000000-0000-4000-8000-000000000001','T1'),
      ('{ids['t2']}','00000000-0000-4000-8000-000000000002','20000000-0000-4000-8000-000000000002','T2');
    INSERT INTO pos.cash_sessions(id,terminal_id,opened_by,opened_at,opening_cash) VALUES
      ('{ids['s1']}','{ids['t1']}','{ids['staff']}','2026-09-14T08:00:00-06:00',500),
      ('{ids['s2']}','{ids['t2']}','{ids['staff']}','2026-09-14T08:00:00-06:00',500);
    INSERT INTO pos.stock_movements(location_id,product_id,quantity_delta,kind,occurred_at,actor_id,reason) VALUES
      ('20000000-0000-4000-8000-000000000001','{ids['product']}',3,'opening',now(),'{ids['staff']}','Conteo ficticio'),
      ('20000000-0000-4000-8000-000000000002','{ids['product']}',2,'opening',now(),'{ids['staff']}','Conteo ficticio');
    """)
    def payload(seq=1,terminal=1):
        return dict(sale_id=str(uuid.uuid4()),cash_session_id=ids['s'+str(terminal)],
            cashier_id=ids['staff'],local_sequence=seq,occurred_at='2026-09-14T09:43:21-06:00',
            captured_offline=True,discount='0.25',
            lines=[dict(product_id=ids['product'],barcode='0000123',description='Anillo de prueba',quantity=1,unit_price='100.25')],
            payments=[dict(id=str(uuid.uuid4()),method='cash',amount='100.00')],sellers=[ids['staff']])
    def call(op,p,terminal=1):
        return f"SELECT pos.receive_sale('{op}','{ids['t'+str(terminal)]}',{literal(json.dumps(p))}::jsonb)"
    p=payload(); op=str(uuid.uuid4()); statement=call(op,p)
    assert_equal(q(statement),p['sale_id'])
    assert_equal(q("SELECT quantity FROM pos.stock_balances WHERE location_id='20000000-0000-4000-8000-000000000001'"),2)
    assert_equal(q("SELECT total FROM pos.sales"),'100.00')
    assert_equal(q("SELECT barcode_snapshot FROM pos.sale_lines"),'0000123')
    assert_equal(q("SELECT occurred_at AT TIME ZONE 'America/Mexico_City' FROM pos.sales"),'2026-09-14 09:43:21')
    passed.append('venta completa, decimales, código con ceros, hora exacta y decremento local')
    assert_equal(q(statement),p['sale_id']); assert_equal(q('SELECT count(*) FROM pos.sales'),1)
    assert_equal(q('SELECT count(*) FROM pos.stock_movements WHERE kind=\'sale\''),1)
    passed.append('reenvío no duplica venta, pago ni inventario')
    changed=json.loads(json.dumps(p));changed['discount']='0.00'
    rejected(call(op,changed)); passed.append('mismo identificador con contenido distinto rechazado')
    bad=payload(2);bad['payments'][0]['amount']='99.00'
    rejected(call(str(uuid.uuid4()),bad)); assert_equal(q('SELECT count(*) FROM pos.sales'),1)
    passed.append('pago incorrecto revierte operación completa')
    bad=payload(2);bad['payments'][0]['method']='nonexistent'
    rejected(call(str(uuid.uuid4()),bad)); assert_equal(q('SELECT count(*) FROM pos.sale_lines'),1)
    assert_equal(q('SELECT count(*) FROM pos.stock_movements'),3)
    passed.append('fallo tardío de pago revierte partidas e inventario')
    rejected(call(str(uuid.uuid4()),payload(1)));passed.append('folio por terminal no se puede duplicar')
    for key,value in [('occurred_at','2026-09-14T09:43:21'),('local_sequence',1.5)]:
        bad=payload(2);bad[key]=value; rejected(call(str(uuid.uuid4()),bad))
    bad=payload(2);bad['lines'][0]['quantity']=1.5;rejected(call(str(uuid.uuid4()),bad))
    passed.append('hora sin zona y cantidades/secuencias fraccionarias rechazadas')
    rejected(call(str(uuid.uuid4()),payload(2),terminal=2))
    passed.append('sesión de caja de otra terminal rechazada')
    p2=payload(1,2);op2=str(uuid.uuid4()); statement2=call(op2,p2,2)
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        results=list(executor.map(q,[statement2,statement2]))
    assert results==[p2['sale_id']]*2
    assert_equal(q('SELECT count(*) FROM pos.sales'),2)
    assert_equal(q("SELECT quantity FROM pos.stock_balances WHERE location_id='20000000-0000-4000-8000-000000000002'"),1)
    passed.append('dos reintentos simultáneos crean una sola venta en el segundo local')
    # Two different simultaneous sales consume the remaining two units of local 1.
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        list(executor.map(q,[call(str(uuid.uuid4()),payload(2)),call(str(uuid.uuid4()),payload(3))]))
    assert_equal(q("SELECT quantity FROM pos.stock_balances WHERE location_id='20000000-0000-4000-8000-000000000001'"),0)
    passed.append('ventas simultáneas de una ubicación mantienen el saldo correcto')
    q(call(str(uuid.uuid4()),payload(4)))
    assert_equal(q("SELECT count(*) FROM pos.sync_issues WHERE code='STOCK_SHORTAGE'"),1)
    assert_equal(q('SELECT count(*) FROM pos.sales'),5)
    passed.append('venta ya cobrada con discrepancia se conserva y genera incidencia')
    rejected("UPDATE pos.sales SET total=0")
    rejected("DELETE FROM pos.stock_movements")
    passed.append('historial y movimientos no admiten sobrescritura ni borrado')
    rejected(f"INSERT INTO pos.terminals(branch_id,location_id,code) VALUES('00000000-0000-4000-8000-000000000001','20000000-0000-4000-8000-000000000001','DUPLICADA')")
    passed.append('una asignación local no se comparte entre dos terminales')
    rejected(f"UPDATE pos.cash_sessions SET closed_by='{ids['staff']}',counted_cash=500 WHERE id='{ids['s1']}'")
    passed.append('cierre de caja incompleto rechazado')
    assert_equal(q("SELECT quantity FROM pos.warehouse_balances WHERE warehouse_id='10000000-0000-4000-8000-000000000001'"),0)
    passed.append('total Coyoacán suma sus ubicaciones sin duplicarlas')
    # Restore verification is performed separately on the clean development dump.
    print('\n'.join('PASS '+s for s in passed))
    print(f'{len(passed)} grupos de pruebas pasaron')
finally:
    sql('DROP DATABASE '+db+' WITH (FORCE)')
