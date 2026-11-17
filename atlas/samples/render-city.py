"""Re-export yoshi389111's pinned night-view SVG as a looping GIF + still PNG.

python -m pip install pillow playwright; python -m playwright install chromium
python atlas/samples/render-city.py profile-night-view.svg [path/to/chromium]
See the README source credits and assets/licenses/contribution-city-MIT.txt.
"""
import hashlib
import io
import sys
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright

ASSETS = Path(__file__).resolve().parents[2] / 'assets'
svg = Path(sys.argv[1]).read_bytes()
# This recipe injects the known MIT-licensed drawing, not arbitrary active HTML.
if hashlib.sha1(b'blob '+str(len(svg)).encode()+b'\0'+svg).hexdigest() != '96a0886aa2e0f84017e1e34f3ea0a52ceec9ba0f':
    raise SystemExit('Use the pinned profile-night-view.svg from the README source table.')
with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=sys.argv[2] if len(sys.argv)>2 else None)
    page = browser.new_page(viewport={'width':768,'height':510},device_scale_factor=1)
    page.route('**/*', lambda route: route.abort())
    page.set_content('<style>*{margin:0}svg{display:block;width:768px;height:510px}</style>'+svg.decode())
    page.eval_on_selector('svg','svg => svg.pauseAnimations()')
    shots = []
    for i in range(25):
        page.eval_on_selector('svg','(svg,t) => svg.setCurrentTime(t)',3*i/24)
        shots.append(Image.open(io.BytesIO(page.screenshot())).convert('RGB'))
    browser.close()

# Begin and dwell on the complete skyline. Retrace, then replay the original rise.
shots[-1].save(ASSETS/'contribution-city.png', optimize=True)
palette = shots[-1].quantize(colors=192)
frames = [f.quantize(palette=palette,dither=Image.Dither.NONE) for f in shots]
order = [24, *range(22,0,-2), *range(24)]
frames[24].save(ASSETS/'contribution-city.gif',save_all=True,append_images=[frames[i] for i in order[1:]],
                duration=[1950]+[100]*11+[120]*24,loop=0,optimize=True,disposal=1)
