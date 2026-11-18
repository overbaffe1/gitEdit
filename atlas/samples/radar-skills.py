
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="420" height="320" viewBox="0 0 420 320" role="img">
<title>Радар скиллов</title><desc>Шестиугольный радар, заполнение анимируется.</desc>
<rect width="420" height="320" rx="14" fill="#020617"/>
<g transform="translate(210,150)" stroke="#1e293b" fill="none">
  <polygon points="0,-90 78,-45 78,45 0,90 -78,45 -78,-45" stroke-width="0.8" opacity="0.9"/>
  <polygon points="0,-65 56,-32 56,32 0,65 -56,32 -56,-32" stroke-width="0.8" opacity="0.6"/>
  <polygon points="0,-40 34,-20 34,20 0,40 -34,20 -34,-20" stroke-width="0.8" opacity="0.4"/>
  <line x1="0" y1="-90" x2="0" y2="90" stroke-width="0.6" opacity="0.5"/><line x1="-78" y1="-45" x2="78" y2="45" stroke-width="0.6" opacity="0.5"/><line x1="78" y1="-45" x2="-78" y2="45" stroke-width="0.6" opacity="0.5"/>
</g>
<g transform="translate(210,150)" fill="#7c3aed" fill-opacity="0.35" stroke="#a78bfa" stroke-width="1.6">
  <polygon points="0,-78 68,-32 62,38 -12,82 -66,22 -58,-38">
    <animate attributeName="points" values="0,-78 68,-32 62,38 -12,82 -66,22 -58,-38; 0,-62 52,-24 48,28 -8,64 -50,16 -44,-28; 0,-78 68,-32 62,38 -12,82 -66,22 -58,-38" dur="4s" repeatCount="indefinite"/>
  </polygon>
</g>
<g font-family="system-ui, sans-serif" font-size="9" fill="#cbd5e1" text-anchor="middle">
  <text x="210" y="42">Python</text><text x="300" y="100">TS</text><text x="300" y="205">Blender</text><text x="210" y="268">Docker</text><text x="120" y="205">FastAPI</text><text x="120" y="100">Git</text>
</g>
<text x="210" y="300" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="#475569">radar · SMIL morph · respect reduced-motion</text>
<style>@media(prefers-reduced-motion:reduce){ animate{display:none}}</style>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"radar-skills.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
