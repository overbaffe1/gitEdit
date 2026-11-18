
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="100" viewBox="0 0 680 100" role="img">
<title>Печатающий баннер</title><desc>Текст печатается с мигающим курсором, как на профиле.</desc>
<defs><linearGradient id="gradT" x1="0" y1="0" x2="100%" y2="0%"><stop offset="0%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#06b6d4"/></linearGradient></defs>
<rect width="680" height="100" rx="14" fill="#020617"/>
<text x="340" y="48" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="18" font-weight="700" fill="url(#gradT)">Building tools that actually work</text>
<rect x="98" y="58" width="2.5" height="20" rx="1" fill="white"><animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/></rect>
<text x="340" y="78" text-anchor="middle" font-family="system-ui, sans-serif" font-size="9" fill="#475569">печаталка · курсор blink 0.8s · градиент · без внешних API</text>
<style>@media(prefers-reduced-motion:reduce){ animate{display:none}}</style>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"typing-banner.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
