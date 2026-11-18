
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="220" viewBox="0 0 680 220" role="img">
<title>Neon Stadium</title><desc>3D стадион из календаря вкладов, неоновая обводка.</desc>
<rect width="680" height="220" rx="16" fill="#020617"/>
<g transform="translate(40,30)">
  <rect x="0" y="60" width="280" height="80" rx="12" fill="#0f172a" stroke="#334155"/>
  <!-- stepped bars like stadium -->
  <g>
    <rect x="18" y="92" width="18" height="28" rx="2" fill="#0e4429"/><rect x="40" y="84" width="18" height="36" rx="2" fill="#006d32"/><rect x="62" y="76" width="18" height="44" rx="2" fill="#26a641"/><rect x="84" y="68" width="18" height="52" rx="2" fill="#39d353"/>
    <rect x="106" y="86" width="18" height="34" rx="2" fill="#006d32"/><rect x="128" y="72" width="18" height="48" rx="2" fill="#26a641"/><rect x="150" y="80" width="18" height="40" rx="2" fill="#0e4429"/><rect x="172" y="64" width="18" height="56" rx="2" fill="#39d353"/>
    <rect x="194" y="76" width="18" height="44" rx="2" fill="#26a641"/><rect x="216" y="88" width="18" height="32" rx="2" fill="#006d32"/>
  </g>
  <path d="M8 48 L272 48 L272 140 L8 140 Z" fill="none" stroke="#38bdf8" stroke-width="1.4" opacity="0.9" stroke-dasharray="8 6"><animate attributeName="stroke-dashoffset" values="0;-28" dur="1s" repeatCount="indefinite"/></path>
</g>
<g font-family="system-ui, sans-serif">
  <text x="380" y="52" font-size="16" font-weight="800" fill="white" letter-spacing="2">NEON STADIUM</text>
  <text x="380" y="70" font-size="11" fill="#38bdf8">календарь как стадион · неоновая петля</text>
  <text x="380" y="90" font-size="9" fill="#94a3b8">1 square = 1 day · высота = intensity</text>
  <rect x="380" y="104" width="108" height="24" rx="12" fill="white" fill-opacity="0.08" stroke="#38bdf8" stroke-opacity="0.5"/><text x="434" y="120" text-anchor="middle" font-size="9" fill="white">◆ 3D · neon</text>
  <text x="380" y="150" font-size="8.5" fill="#475569">генератор: python3 atlas/samples/neon-stadium.py · идея Neon Arena</text>
</g>
<style>@media(prefers-reduced-motion:reduce){ animate{display:none}}</style>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"neon-stadium.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
