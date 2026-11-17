"""Pack the published studio as a single offline HTML. The reference ship stays remote."""
import base64
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs'

def pack():
    page = (SITE/'index.html').read_text(encoding='utf-8')
    def embed(path): return base64.b64encode((SITE/path).read_bytes()).decode('ascii')
    script = (SITE/'stage.js').read_text(encoding='utf-8').replace('</script', r'<\/script')
    css = (SITE/'studio.css').read_text(encoding='utf-8')
    license = (SITE/'three-LICENSE.txt').read_text(encoding='utf-8')
    page = page.replace('<link rel="stylesheet" href="studio.css">', '<style>'+css+'</style>')
    page = page.replace('src="poster.jpg"','src="data:image/jpeg;base64,'+embed('poster.jpg')+'"')
    page = page.replace('<script src="stage.js"></script>', '<!-- Three.js license:\n'+license+'\n-->\n<script id="embedded-glb" type="application/octet-stream">'+embed('malachite.glb')+'</script>\n<script>'+script+'</script>')
    with ZipFile(ROOT/'assets/crystal-view.zip','w') as z:
        z.writestr(ZipInfo('crystal.html'),page,compress_type=ZIP_DEFLATED)

if __name__=='__main__': pack()
