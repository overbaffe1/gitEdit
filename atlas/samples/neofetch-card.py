
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="180" viewBox="0 0 680 180" role="img">
<title>Neofetch карточка</title><desc>Неофеч-стиль: иконка + строки ключ/значение, печатается.</desc>
<rect width="680" height="180" rx="14" fill="#0d1117"/>
<g font-family="JetBrains Mono, monospace" font-size="11">
  <text x="22" y="28" fill="#f87171">overbaffe1</text><text x="108" y="28" fill="#9ca3af">@github</text><text x="180" y="28" fill="#4b5563">~ neofetch</text>
  <line x1="22" y1="36" x2="260" y2="36" stroke="#1f2937" stroke-width="1"/>
  <text x="22" y="56" fill="#60a5fa">OS:</text><text x="72" y="56" fill="#e5e7eb">GitHub README · SVG Only</text>
  <text x="22" y="76" fill="#60a5fa">Host:</text><text x="72" y="76" fill="#e5e7eb">overbaffe1/gitEdit</text>
  <text x="22" y="96" fill="#60a5fa">Stack:</text><text x="72" y="96" fill="#e5e7eb">Python, Blender, FastAPI, GLB</text>
  <text x="22" y="116" fill="#60a5fa">Uptime:</text><text x="72" y="116" fill="#e5e7eb">847 commits</text>
  <text x="22" y="136" fill="#60a5fa">Theme:</text><text x="72" y="136" fill="#e5e7eb">Monokai · Tokyonight</text>
  <text x="22" y="156" fill="#4b5563">● ● ●</text>
</g>
<g transform="translate(420,30)">
  <rect width="220" height="120" rx="12" fill="#111827" stroke="#1f2937"/>
  <g font-family="JetBrains Mono, monospace" font-size="10" fill="#a78bfa">
    <text x="18" y="28">████  ████</text><text x="18" y="42">█  █  █  █</text><text x="18" y="56">████  ████</text>
  </g>
  <text x="110" y="38" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="white">STATS</text>
  <text x="110" y="56" font-family="JetBrains Mono, monospace" font-size="9" fill="#94a3b8">Stars 128 · Forks 12</text>
  <text x="110" y="72" font-family="JetBrains Mono, monospace" font-size="9" fill="#6ee7b7">Contribs 1.2k</text>
</g>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"neofetch-card.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
