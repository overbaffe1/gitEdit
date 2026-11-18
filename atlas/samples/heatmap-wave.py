
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="140" viewBox="0 0 680 140" role="img">
<title>Heatmap волна</title><desc>53 недели календарь, клетки проявляются по диагонали.</desc>
<rect width="680" height="140" rx="14" fill="#020617"/>
<g font-family="JetBrains Mono, monospace" font-size="8" fill="#64748b"><text x="18" y="18">LESS</text><g transform="translate(54,10)"><rect width="10" height="10" rx="2" fill="#1f2937"/><rect x="14" width="10" height="10" rx="2" fill="#0e4429"/><rect x="28" width="10" height="10" rx="2" fill="#006d32"/><rect x="42" width="10" height="10" rx="2" fill="#26a641"/><rect x="56" width="10" height="10" rx="2" fill="#39d353"/></g><text x="124" y="18">MORE</text><text x="520" y="18" fill="#475569">9 847 contributions in the last year</text></g>
<g transform="translate(18,30)">
  <!-- generate 53x7 grid with css stagger -->
  <!-- we fake with pattern -->
  <rect width="608" height="84" rx="8" fill="#0f172a" stroke="#1e293b"/>
  <!-- cells -->
  <g id="grid">
    <rect x="8" y="8" width="10" height="10" rx="2" fill="#39d353" opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" begin="0.1s" fill="freeze"/></rect>
    <rect x="20" y="8" width="10" height="10" rx="2" fill="#26a641" opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" begin="0.15s" fill="freeze"/></rect>
    <rect x="32" y="8" width="10" height="10" rx="2" fill="#006d32" opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" begin="0.2s" fill="freeze"/></rect>
    <rect x="44" y="8" width="10" height="10" rx="2" fill="#0e4429" opacity="0"><animate attributeName="opacity" values="0;1" dur="0.3s" begin="0.25s" fill="freeze"/></rect>
    <!-- more cells static for visual density -->
    <g opacity="0.95">
      <rect x="8" y="20" width="10" height="10" rx="2" fill="#1f2937"/><rect x="20" y="20" width="10" height="10" rx="2" fill="#39d353"/><rect x="32" y="20" width="10" height="10" rx="2" fill="#26a641"/><rect x="44" y="20" width="10" height="10" rx="2" fill="#006d32"/>
      <rect x="8" y="32" width="10" height="10" rx="2" fill="#006d32"/><rect x="20" y="32" width="10" height="10" rx="2" fill="#0e4429"/><rect x="32" y="32" width="10" height="10" rx="2" fill="#39d353"/><rect x="44" y="32" width="10" height="10" rx="2" fill="#26a641"/>
      <rect x="8" y="44" width="10" height="10" rx="2" fill="#26a641"/><rect x="20" y="44" width="10" height="10" rx="2" fill="#006d32"/><rect x="32" y="44" width="10" height="10" rx="2" fill="#0e4429"/><rect x="44" y="44" width="10" height="10" rx="2" fill="#1f2937"/>
    </g>
  </g>
  <text x="304" y="78" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8" fill="#334155">53 недели · диагональный reveal · без JS · static fallback</text>
</g>
<style>@media (prefers-reduced-motion: reduce){ animate{display:none} [opacity="0"]{opacity:1}}</style>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"heatmap-wave.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
