"""Per-product pricing rules; no executable spreadsheet formulas."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP, ROUND_CEILING
from domain import require, money, RuleError

def calculate(data, cost, weight):
 mode=data.get('price_mode','fixed')
 require(mode in ('fixed','formula'),'Selecciona precio fijo o por fórmula.')
 if mode=='fixed':
  price=money(data.get('price'));require(price>0,'Precio mayor a cero requerido.')
  return price,{'price_mode':'fixed','price_rule':None}
 base=data.get('price_base');ending=str(data.get('price_ending',''))
 require(base in ('cost','weight'),'Selecciona costo o peso como base de cálculo.')
 require(ending in ('none','50','90'),'Selecciona terminación 50, 90 o sin redondeo comercial.')
 raw=str(data.get('price_multiplier','')).strip()
 try:factor=Decimal(raw)
 except InvalidOperation:raise RuleError('Multiplicador inválido.')
 require(factor.is_finite() and 0<factor<=1000000 and factor.as_tuple().exponent>=-6,'Multiplicador mayor a cero, máximo 1000000 y hasta seis decimales.')
 value=Decimal(cost)/100 if base=='cost' else Decimal(str(weight or 0))
 require(value.is_finite() and value>0,'La base de cálculo debe ser mayor a cero; completa el costo o peso.')
 amount=value*factor
 if ending!='none':
  # Smallest whole-peso amount ending in 50/90 which is not below the result.
  end=Decimal(ending);amount=((amount-end)/100).to_integral_value(rounding=ROUND_CEILING)*100+end
 cents=int((amount*100).quantize(Decimal('1'),rounding=ROUND_HALF_UP))
 require(0<cents<=9999999999,'El precio calculado está fuera del rango permitido.')
 return cents,{'price_mode':'formula','price_rule':{'base':base,'multiplier':str(factor),'ending':ending}}
