"""Render authoritative receipts for browser preview and explicit printing."""
import base64
import subprocess
import tempfile
from pathlib import Path
from PIL import Image
from core import RuleError

def render_pages(pdf):
    with tempfile.TemporaryDirectory(prefix='frida-receipt-') as directory:
        root=Path(directory); source=root/'receipt.pdf';source.write_bytes(pdf)
        try:
            subprocess.run(['pdftoppm','-r','300','-png',str(source),str(root/'page')],check=True,timeout=30,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
        except (OSError,subprocess.SubprocessError) as exc:
            raise RuleError('No se pudo preparar la vista previa. Revisa que Poppler esté instalado e inténtalo de nuevo.') from exc
        pages=[]
        for path in sorted(root.glob('page-*.png'),key=lambda p:int(p.stem.split('-')[-1])):
            with Image.open(path) as image:w,h=image.size
            pages.append({'src':'data:image/png;base64,'+base64.b64encode(path.read_bytes()).decode(),'width':w*25.4/300,'height':h*25.4/300})
        return pages
