
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="32" viewBox="0 0 680 32" role="img">
<title>Волнистый разделитель</title><desc>Волна с бегущей кометой.</desc>
<rect width="680" height="32" rx="8" fill="#020617"/>
<path d="M0 16 Q 85 0 170 16 T 340 16 T 510 16 T 680 16" fill="none" stroke="#1e293b" stroke-width="1.2"/>
<path d="M0 16 Q 85 0 170 16 T 340 16 T 510 16 T 680 16" fill="none" stroke="#38bdf8" stroke-width="1.8" stroke-linecap="round" stroke-dasharray="18 32" opacity="0.9">
  <animate attributeName="stroke-dashoffset" values="0;-50" dur="1.2s" repeatCount="indefinite"/>
</path>
<circle r="3.2" fill="#7dd3fc" filter="none"><animateMotion dur="2.4s" repeatCount="indefinite" path="M0 16 Q 85 0 170 16 T 340 16 T 510 16 T 680 16"/></circle>
<style>@media (prefers-reduced-motion: reduce){ animate, animateMotion{display:none}}</style>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"wave-divider.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
