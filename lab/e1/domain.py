"""Shared validation, time and exact monetary primitives."""
import json
from datetime import datetime
from zoneinfo import ZoneInfo
from decimal import Decimal, InvalidOperation
class RuleError(Exception): pass


def require(ok, message):
    if not ok: raise RuleError(message)


def now(): return datetime.now(ZoneInfo('America/Mexico_City')).isoformat(timespec='microseconds')


def pack(x): return json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':'))


def money(v):
    try: n=Decimal(str(v).replace(',','.'))
    except InvalidOperation: raise RuleError('Importe inválido.')
    require(n.is_finite() and 0<=n<=Decimal('99999999.99') and n*100==(n*100).to_integral_value(),'Usa un importe positivo con hasta dos decimales.')
    return int(n*100)


def percent(v):
    n=money(v); require(n<=10000,'El porcentaje debe estar entre 0 y 100.'); return n


def cleantext(v,limit):
    require(isinstance(v,str) and len(v)<=limit,'Texto demasiado largo o inválido.');return v.strip()
