
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="120" viewBox="0 0 680 120" role="img">
<title>Now Playing</title><desc>Карточка трека с эквалайзером, обложка инлайн.</desc>
<rect width="680" height="120" rx="14" fill="#0f172a"/>
<rect x="16" y="16" width="88" height="88" rx="10" fill="#1e293b" stroke="#334155"/>
<circle cx="60" cy="60" r="22" fill="#1db954" opacity="0.95"/><text x="60" y="66" text-anchor="middle" font-size="18" fill="white">♫</text>
<g font-family="system-ui, sans-serif">
  <text x="124" y="38" font-size="13" font-weight="700" fill="white">Starlight — overbaffe1</text>
  <text x="124" y="56" font-size="10" fill="#94a3b8">gitEdit Radio · 02:14 / 03:47</text>
  <rect x="124" y="68" width="240" height="4" rx="2" fill="#1e293b"/><rect x="124" y="68" width="138" height="4" rx="2" fill="#1db954"/>
  <g transform="translate(520,42)">
    <rect width="4" height="14" rx="2" fill="#1db954"><animate attributeName="height" values="14;22;10;18;14" dur="0.7s" repeatCount="indefinite"/></rect>
    <rect x="8" width="4" height="10" rx="2" fill="#1db954"><animate attributeName="height" values="10;16;8;20;10" dur="0.85s" repeatCount="indefinite"/></rect>
    <rect x="16" width="4" height="18" rx="2" fill="#1db954"><animate attributeName="height" values="18;8;18;12;18" dur="0.9s" repeatCount="indefinite"/></rect>
    <rect x="24" width="4" height="12" rx="2" fill="#1db954"><animate attributeName="height" values="12;18;14;8;12" dur="0.75s" repeatCount="indefinite"/></rect>
  </g>
  <text x="560" y="82" font-size="8" fill="#475569">NOW PLAYING · bars 0.7-0.9s</text>
</g>
<style>@media(prefers-reduced-motion:reduce){ animate{display:none}}</style>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"spotify-card.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
