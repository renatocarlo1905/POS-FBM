"""Draw original transparent brand assets without altering their pixels."""
from pathlib import Path
from reportlab.lib.utils import ImageReader
ROOT=Path(__file__).parent/'static'

def draw_brand(canvas,width,top):
    symbol=ImageReader(str(ROOT/'brand-symbol.png'));name=ImageReader(str(ROOT/'brand-name.png'))
    sw,sh=symbol.getSize();nw,nh=name.getSize()
    symbol_width=min(82,width*.43);symbol_height=symbol_width*sh/sw
    name_width=width-24;name_height=name_width*nh/nw
    canvas.drawImage(symbol,(width-symbol_width)/2,top-symbol_height,symbol_width,symbol_height,mask='auto')
    canvas.drawImage(name,12,top-symbol_height-5-name_height,name_width,name_height,mask='auto')
    return symbol_height+5+name_height
