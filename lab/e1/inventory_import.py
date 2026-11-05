"""Validated, atomic import of NEW products from a Sheets/Excel template."""
import base64, csv, hashlib, io, json, unicodedata, uuid, zipfile
from decimal import Decimal, InvalidOperation
from pathlib import Path
from domain import RuleError, require, cleantext, money, pack, now
import extensions as ext

HEADERS=['Descripción corta','Descripción larga','Material','Categoría','Proveedor','Precio de venta (MXN)','Costo (MXN)','Peso (g)','Cantidad inicial','Almacén','Precio en etiqueta','Tipo de precio','Base de cálculo','Multiplicador','Terminación']
MAX_ROWS=500
MAX_FILE=450000

def norm(value):
 return ' '.join(unicodedata.normalize('NFKC',str(value or '')).strip().casefold().split())

def authorize(c,actor):
 user=next((u for u in c.get('users') if u['id']==actor),None)
 require(user and user['active'] and c.policy(user).get('inventory_view') and c.policy(user).get('product_create'),'Necesitas permisos de inventario y creación de productos para importar.')

def catalogs(c):
 return {'materials':c.get('materials'),'categories':{x['id']:' > '.join(n['name'] for n in ext.category_path(c,x['id'])) for x in c.get('categories',[])},'providers':{str(x['id']):x['name'] for x in c.get('providers') if x.get('approved',True)},'warehouses':ext.WAREHOUSES}

def read_rows(data):
 filename=cleantext(data.get('filename',''),200)
 content=data.get('content','');require(isinstance(content,str) and len(content)<=MAX_FILE*4//3+8,'Archivo demasiado grande. Máximo 450 KB y 500 productos.')
 try:raw=base64.b64decode(content,validate=True)
 except (ValueError,TypeError):raise RuleError('Archivo inválido.')
 require(raw and len(raw)<=MAX_FILE,'Archivo vacío o demasiado grande.')
 suffix=Path(filename).suffix.lower()
 if suffix=='.xlsx':
  from openpyxl import load_workbook
  try:
   with zipfile.ZipFile(io.BytesIO(raw)) as archive:
    require(len(archive.infolist())<=2000 and sum(x.file_size for x in archive.infolist())<=12000000,'El Excel supera el tamaño permitido al abrirlo.')
   wb=load_workbook(io.BytesIO(raw),read_only=False,data_only=False,keep_links=False)
   try:
    require('Productos' in wb.sheetnames,'El Excel debe contener la hoja Productos.')
    sheet=wb['Productos'];require(sheet.max_column<=100,'La hoja contiene demasiadas columnas.')
    require(sheet.max_row<=2000,'La hoja Productos tiene demasiadas filas. Máximo 500 productos por carga.')
    rows=[]
    for row in sheet.iter_rows():
     require(not any(cell.data_type=='f' for cell in row),'No uses fórmulas de celdas en Productos. Para calcular el precio utiliza Tipo de precio, Base de cálculo, Multiplicador y Terminación.')
     values=[cell.value for cell in row]
     while len(values)>len(HEADERS) and values[-1] is None:values.pop()
     rows.append(values)
   finally:wb.close()
  except RuleError:raise
  except Exception:raise RuleError('No se pudo leer el Excel. Descarga la plantilla como Microsoft Excel (.xlsx).')
 elif suffix in ('.csv','.tsv'):
  try:
   text=raw.decode('utf-8-sig');delimiter='\t' if suffix=='.tsv' else (';' if text.splitlines()[0].count(';')>text.splitlines()[0].count(',') else ',')
   rows=list(csv.reader(io.StringIO(text),delimiter=delimiter));require(len(rows)<=2000,'Demasiadas filas.')
  except (UnicodeError,csv.Error,IndexError):raise RuleError('Usa un CSV UTF-8 o un archivo Excel (.xlsx).')
 else:raise RuleError('Selecciona un archivo .xlsx, .csv o .tsv.')
 require(rows and [norm(x) for x in rows[0]]==[norm(x) for x in HEADERS],'Las columnas deben coincidir con la plantilla Productos, sin cambiar su orden.')
 result=[]
 for number,row in enumerate(rows[1:],2):
  if not any(str(x).strip() for x in row if x is not None):continue
  require(len(row)<=len(HEADERS),f'Fila {number}: hay columnas adicionales.')
  row=list(row)+['']*(len(HEADERS)-len(row))
  values=['' if v is None else str(v).strip() for v in row]
  require(all(len(v)<=1000 for v in values),f'Fila {number}: texto demasiado largo.')
  result.append((number,values))
 require(len(result)<=MAX_ROWS,'Máximo 500 filas con datos por carga.')
 return result

def resolve(mapping,label,field):
 matches=[key for key,value in mapping.items() if norm(value)==norm(label)]
 require(len(matches)==1,f'{field}: selecciona una opción vigente y sin ambigüedades de la plantilla.')
 return matches[0]

def yesno(value,field):
 value=norm(value)
 require(value in ('sí','si','no'),f'{field}: selecciona Sí o No.')
 return value!='no'

def signature(p):
 return (norm(p['name']),str(p['material_id']),str(p.get('category_id') or p['type_id']),str(p['provider']),str(Decimal(str(p.get('weight') or 0)).normalize()))

def preview(c,actor,data):
 authorize(c,actor)
 reference=cleantext(data.get('reference',''),100);require(reference,'Escribe una referencia de recepción, por ejemplo la factura o remisión.')
 rows=read_rows(data);digest=hashlib.sha256(pack({'reference':norm(reference),'rows':[row for _,row in rows]}).encode()).hexdigest()
 key='inventory-import:'+hashlib.sha256(norm(reference).encode()).hexdigest()
 previous=c.get(key)
 if previous:
  require(previous['digest']==digest,'Esta referencia ya se usó con otro contenido. Consulta el ingreso anterior o usa la referencia de una recepción nueva.')
  return {'already_imported':True,'result':previous['result'],'digest':digest,'key':key}
 maps=catalogs(c);existing={signature(p):p for p in ext.catalog(c,True)};seen=set();valid=[];errors=[]
 for number,row in rows:
  try:
   name=cleantext(row[0],100);description=cleantext(row[1],1000);require(name and description,'Las dos descripciones son obligatorias.')
   material=resolve(maps['materials'],row[2],'Material');category=resolve(maps['categories'],row[3],'Categoría');provider=resolve(maps['providers'],row[4],'Proveedor');warehouse=resolve(maps['warehouses'],row[9],'Almacén')
   require(row[6],'El costo es obligatorio (puede ser 0 para precio fijo).')
   cost=money(row[6])
   weight=row[7].replace(',','.');w=Decimal(weight) if weight else None
   require(w is None or w.is_finite() and 0<=w<=999 and w*1000==(w*1000).to_integral_value(),'Peso: usa de 0 a 999 g, con hasta tres decimales.')
   q=Decimal(row[8]);require(q.is_finite() and q==q.to_integral_value() and 1<=q<=100000,'Cantidad inicial: usa un entero de 1 a 100000.')
   mode=norm(row[11]);require(mode in ('','fijo','fórmula','formula'),'Tipo de precio: selecciona Fijo o Fórmula.')
   settings={'price':row[5],'price_mode':'fixed' if mode in ('','fijo') else 'formula','price_base':{'costo':'cost','peso':'weight'}.get(norm(row[12])),'price_multiplier':row[13],'price_ending':'none' if norm(row[14]) in ('','sin redondeo') else row[14]}
   price,_=ext.calculate_product_price(settings,cost,w)
   product={'name':name,'description':description,'material_id':material,'category_id':category,'provider':int(provider),'cost':str(Decimal(cost)/100),'weight':str(w) if w is not None else '', 'quantity':int(q),'warehouse':warehouse,'print_price':yesno(row[10],'Precio en etiqueta'),**settings,'price':str(Decimal(price)/100)}
   sig=signature(product);require(sig not in existing,'Ya existe un producto con esa descripción corta, material, categoría, proveedor y peso. Esta carga solo admite productos nuevos.');require(sig not in seen,'Producto repetido dentro del archivo. Agrupa sus unidades en una sola fila.');seen.add(sig)
   valid.append({'row':number,'product':product,'material':maps['materials'][material],'category':maps['categories'][category],'provider_name':maps['providers'][provider],'warehouse_name':maps['warehouses'][warehouse]})
  except (RuleError,InvalidOperation,ValueError) as e:errors.append({'row':number,'message':str(e) if isinstance(e,RuleError) else 'Número inválido. Usa cantidades y precios sin símbolos de moneda.'})
 require(valid or errors,'No hay productos en el archivo.')
 result={'reference':reference,'digest':digest,'key':key,'rows':valid,'errors':errors,'count':len(valid),'units':sum(r['product']['quantity'] for r in valid),'cost_total':sum(money(r['product']['cost'])*r['product']['quantity'] for r in valid)}
 result['preview_hash']=hashlib.sha256(pack({'rows':valid,'errors':errors,'digest':digest}).encode()).hexdigest()
 return result

@ext.transaction
def confirm(c,actor,data):
 current=preview(c,actor,data)
 if current.get('already_imported'):return {**current['result'],'duplicate':True}
 require(not current['errors'],'Corrige todas las filas antes de importar. No se guardó ningún producto.')
 require(data.get('preview_hash')==current['preview_hash'],'Los datos o catálogos cambiaron. Revisa el archivo nuevamente.')
 products=[]
 for row in current['rows']:
  d={**row['product'],'request_id':str(uuid.uuid5(uuid.NAMESPACE_URL,current['key']+':'+str(row['row'])))}
  created=ext.create_product.__wrapped__(c,actor,d)
  products.append({'row':row['row'],'id':created['product']['id'],'code':created['product']['code'],'name':created['product']['name'],'quantity':d['quantity'],'warehouse':d['warehouse']})
 result={'reference':current['reference'],'at':now(),'actor':actor,'count':len(products),'units':current['units'],'products':products}
 c.put(current['key'],{'digest':current['digest'],'result':result});c.audit(actor,'inventory_import',result)
 return result
