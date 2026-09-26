"""Read-only source audit; generate E0 traceability from literal req() records.
No source Python execution, database access or external network.
"""
import ast, hashlib, json, re
from pathlib import Path
from html import unescape
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
pdf=ROOT/'output/pdf/Requerimientos_POS_Frida_Blancas_Mexico_v2.pdf'
source=ROOT/'tmp/pdfs/crear_requerimientos_v2.py'
plan=(ROOT/'docs/Plan_desarrollo_POS_Frida_Blancas_v1.md').read_text()
clean=lambda t:unescape(re.sub('<[^>]+>','',t)).strip()
norm=lambda t:re.sub(r'\s+','',t).replace('­','')
pages=[p.extract_text() for p in PdfReader(pdf).pages]
rx=r'\b[A-Z]{3}-\d{2}(?:-[A-Z])?(?:/\d{2})*'
actual={}
for page_no,text in enumerate(pages,1):
    for m in re.finditer(r'(?m)^('+rx+r')\s*·',text):
        actual[m.group(1)]=page_no
records={}
for node in ast.walk(ast.parse(source.read_text())):
    if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='req':
        code,text=map(ast.literal_eval,node.args[:2]);records[code]=clean(text)
assert set(actual)==set(records),{'pdf_only':sorted(set(actual)-set(records)),'source_only':sorted(set(records)-set(actual))}
for code,text in records.items():
    assert norm(text) in norm(pages[actual[code]-1]),'Text differs from PDF: '+code

# Every printed grouped identifier is retained as one record (e.g. DAS-40/42).
tasks={
'E0-01':('E0','Documento de alcance','GEN,ALM','Ninguna','A01,A28,A30','Base para E1'),
'E1-01':('E1','Acceso y autorización','ACC','D18','A01','E0-03,E0-05'),
'E1-02':('E1','Estado de conexión y sincronización','ARQ,OFF','D17,D19','A02,A03,A04','E0-03,E0-04,E1-01'),
'E1-03':('E1','Impresión y recuperación','TIC,RES','D20,D21,D22','A05,A06,A30','E1-02,equipos'),
'E2-01':('E2','P06/D04 Catálogo y etiquetas','INV','D09,D10,D11,D21','A07','E1-01,E1-03'),
'E2-02':('E2','P06/D04 Inventario por estado','MOV,MIN','D13','A04,A10','E1-02,E2-01'),
'E2-03':('E2','P06 Ingresos Excel/recurrentes','IMP,ING','D09,D12','A08,A09','E2-01,E2-02'),
'E3-01':('E3','P01 Venta y pago','VTA,PAG,VEN','D01,D18','A11,A14','E1-02,E2-02; saldo E4'),
'E3-02':('E3','P02/D03 Caja','CAJ','D19','A02,A12,A13','E1-02,E3-01'),
'E4-01':('E4','P05/D08 Clientes y códigos','','D08,D18','A16,A17','E1-01,E3-01'),
'E4-02':('E4','P05 Saldo a favor','','D06,D07','A15','E4-01,E3-02'),
'E5-01':('E5','P03/D05 Apartados','APA','D02,D05','A18,A19,A25','E2,E3,E4; cambios E6'),
'E5-02':('E5','P04/D05 Reparaciones','REP','D05,D22','A20,A21,A22,A25','E3,E4; cambios E6'),
'E6-01':('E6','P07 Cambios','CAM','D01,D03,D06','A19,A22,A23','E2,E3,E4,E5'),
'E6-02':('E6','P08 Correcciones','COR','D04,D05,D07','A24,A25','E3,E4,E5'),
'E7-01':('E7','D01/D06 Resumen y reportes','CAL,RPT','D01,D02,D03,D06,D16','A14,A26,A28','E3,E4,E5,E6'),
'E7-02':('E7','D02-D05/D07 Consultas y alertas','DAS','D22,D23','A27,A28','E2,E3,E4,E5,E6'),
'E8-01':('E8','Migración y validación','MIG','D14,D15,D16','A29','Modelo estable E2-E6'),
}
prefix_task={p:t for t,v in tasks.items() for p in v[2].split(',') if p}
cases={m.group(1):m.group(2).strip() for m in re.finditer(r'^\*\*(A\d{2}) · (.*?)\n(?=\n)',plan,re.M|re.S)}
assert len(cases)==30,len(cases)
decisions={m.group(1):m.group(2).strip() for m in re.finditer(r'^\*\*(D\d{2}) · (.*?)\n(?=\n)',plan,re.M|re.S)}
assert len(decisions)==24,len(decisions)
rows=[]
for code in sorted(records,key=lambda k:(actual[k],list(records).index(k))):
    prefix=code.split('-')[0];num=int(code.split('-')[1].split('/')[0])
    if prefix=='CLI': task='E4-01' if 12<=num<=19 or num>=26 else 'E4-02'
    elif prefix=='DAS' and num<=9: task='E7-01'
    else: task=prefix_task[prefix]
    stage,screen,_,decision,test,depends=tasks[task]
    if prefix in ('APA','REP','CAM','COR','IMP','ING','MOV','CLI'):connection='Con conexión para operaciones del módulo; consulta de saldos vigente también online.'
    elif prefix in ('VTA','PAG','CAJ','VEN'):connection='Ventas/caja permitidas offline; saldo y operaciones de órdenes requieren conexión.'
    elif prefix in ('DAS','CAL','RPT','MIN'):connection='Consulta central: indicar última sincronización y datos incompletos.'
    else:connection='Aplicar contexto de ARQ/OFF y matriz de disponibilidad (PDF p. 6).'
    rows.append(dict(id=code,source_page=actual[code],rule=records[code],task=task,stage=stage,screen=screen,dependencies=depends,decisions=[] if decision=='Ninguna' else decision.split(','),tests=test.split(','),connectivity=connection,business_status='Regla confirmada en PDF; detalles pendientes según decisiones',spec_status='Diseño E0 para revisión',implementation_status='Pendiente de implementación/validación v2; ver revisión estática',acceptance='Verificar esta regla íntegra dentro de los escenarios '+test+'; conservar resultado esperado/obtenido y evidencia por requisito.'))

metadata={'date':'2026-09-23','source':pdf.name,'sha256':hashlib.sha256(pdf.read_bytes()).hexdigest(),'printed_identifiers':len(rows),'status':'E0 diseñado, revisión del negocio pendiente','requirements':rows}
(OUT/'requisitos.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
parts=['# Matriz de requisitos por identificador\n\nE0 v1.0 · 23/09/2026\n',f'**{len(rows)} identificadores impresos**, incluidos grupos exactamente como aparecen en el PDF. Se cotejaron texto y página contra el PDF real; los IDs agrupados no se expanden a números inventados. Fuente SHA-256: `{metadata["sha256"]}`.\n', 'Esta es trazabilidad de diseño, no evidencia de implementación. Las pruebas A01-A30 se encuentran en [08-pruebas-aceptacion.md](08-pruebas-aceptacion.md). Las tareas están definidas en [06-tareas-y-puerta-e1.md](06-tareas-y-puerta-e1.md). Los acuerdos sin ID (tablas, notas, fórmulas) se conservan por las reglas transversales, flujos y decisiones E0; consultar siempre la página fuente completa.\n']
for r in rows:
    parts += [f'## {r["id"]}\n',f'**Fuente:** PDF v2, p. {r["source_page"]}. **Regla:** {r["rule"]}\n',f'**Tarea:** {r["task"]} ({r["stage"]}). **Pantalla:** {r["screen"]}. **Depende de:** {r["dependencies"]}.\n',f'**Decisiones relacionadas:** {", ".join(r["decisions"]) or "Ninguna para definir alcance"}. **Pruebas:** {", ".join(r["tests"])}.\n',f'**Conectividad:** {r["connectivity"]}\n',f'**Aceptación:** {r["acceptance"]}\n','**Estado:** diseño para revisión; no certificado como implementado.\n']
(OUT/'01-matriz-requisitos.md').write_text('\n'.join(parts))
case_md=['# Casos de aceptación vinculados\n\nA01-A30 del plan v1, conservados como escenarios por ejecutar. No confundir con las pruebas locales de la maqueta. Cada caso se desglosa por requisito al implementar.\n']
for code,content in cases.items():case_md.append(f'## {code} · '+content.replace('**','')+'\n')
(OUT/'08-pruebas-aceptacion.md').write_text('\n'.join(case_md))
(OUT/'casos-aceptacion.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'requirements':len(rows),'source_pages':len(set(actual.values())),'cases':len(cases),'decisions':len(decisions),'source_sha256':metadata['sha256']},ensure_ascii=False))
