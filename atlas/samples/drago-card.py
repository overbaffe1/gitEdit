
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="160" viewBox="0 0 680 160" role="img">
<title>Drago — дракон</title><desc>Дракон эволюционирует от активности, HUD уровня.</desc>
<rect width="680" height="160" rx="16" fill="#020617"/>
<g transform="translate(90,80)">
  <text font-size="48" text-anchor="middle" dominant-baseline="middle">🐉</text>
  <animateTransform attributeName="transform" type="translate" values="90,80;90,76;90,80" dur="1.4s" repeatCount="indefinite"/>
  <circle r="38" fill="none" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="6 6" opacity="0.6"><animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/></circle>
</g>
<g font-family="system-ui, sans-serif">
  <text x="200" y="48" font-size="15" font-weight="800" fill="white" letter-spacing="2">DRAGO · LVL 7</text>
  <text x="200" y="68" font-size="10" fill="#fbbf24">эволюция от коммитов · 13 стадий</text>
  <rect x="200" y="82" width="220" height="10" rx="5" fill="#1e293b"/><rect x="200" y="82" width="148" height="10" rx="5" fill="#f59e0b"><animate attributeName="width" values="148;162;148" dur="2s" repeatCount="indefinite"/></rect>
  <text x="200" y="108" font-size="9" fill="#94a3b8">HUD: commits 1.2k · streak 18 · PRs 47</text>
  <rect x="200" y="120" width="92" height="20" rx="10" fill="white" fill-opacity="0.08" stroke="#f59e0b" stroke-opacity="0.5"/><text x="246" y="134" text-anchor="middle" font-size="8" fill="white">● BREATH</text>
</g>
<style>@media(prefers-reduced-motion:reduce){ animateTransform,animate{display:none}}</style>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"drago-card.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
