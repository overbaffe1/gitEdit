
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="64" viewBox="0 0 680 64" role="img">
<title>Бегущая строка иконок</title><desc>Иконки едут влево бесшовно, на паузу при reduced-motion.</desc>
<rect width="680" height="64" rx="12" fill="#020617"/>
<clipPath id="clipM"><rect x="8" y="8" width="664" height="48" rx="8"/></clipPath>
<g clip-path="url(#clipM)">
  <g id="track">
    <g transform="translate(0,16)">
      <g><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#38bdf8">PY</text></g>
      <g transform="translate(60,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#f59e0b">TS</text></g>
      <g transform="translate(120,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#22d3ee">RE</text></g>
      <g transform="translate(180,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#fb923c">BL</text></g>
      <g transform="translate(240,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#60a5fa">DO</text></g>
      <g transform="translate(300,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#34d399">FA</text></g>
      <g transform="translate(360,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#818cf8">PG</text></g>
      <g transform="translate(420,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#facc15">LI</text></g>
      <!-- duplicate for seamless -->
      <g transform="translate(480,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#38bdf8">PY</text></g>
      <g transform="translate(540,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#f59e0b">TS</text></g>
      <g transform="translate(600,0)"><rect width="44" height="32" rx="8" fill="#0f172a" stroke="#1e293b"/><text x="22" y="21" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="10" fill="#22d3ee">RE</text></g>
    </g>
    <animateTransform attributeName="transform" type="translate" values="0,0; -240,0" dur="8s" repeatCount="indefinite"/>
  </g>
</g>
<style>@media(prefers-reduced-motion:reduce){ animateTransform{display:none}}</style>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"marquee-icons.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
