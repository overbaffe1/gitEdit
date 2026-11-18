
from pathlib import Path
ASSETS=Path(__file__).resolve().parents[2]/"assets"
SVG="""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="140" viewBox="0 0 680 140" role="img">
<title>Полка трофеев</title><desc>Трофеи по уровням, как в играх.</desc>
<rect width="680" height="140" rx="14" fill="#020617"/>
<g transform="translate(20,22)">
  <g><rect width="148" height="96" rx="12" fill="#0f172a" stroke="#334155"/><text x="74" y="36" text-anchor="middle" font-size="28">🏆</text><text x="74" y="58" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="white">First PR</text><text x="74" y="74" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="#94a3b8">×12 merged</text></g>
  <g transform="translate(164,0)"><rect width="148" height="96" rx="12" fill="#0f172a" stroke="#f59e0b"/><text x="74" y="36" text-anchor="middle" font-size="28">⚡</text><text x="74" y="58" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="white">Streak 42</text><text x="74" y="74" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="#fbbf24">days</text></g>
  <g transform="translate(328,0)"><rect width="148" height="96" rx="12" fill="#0f172a" stroke="#a78bfa"/><text x="74" y="36" text-anchor="middle" font-size="28">🧩</text><text x="74" y="58" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="white">100 Commits</text><text x="74" y="74" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="#c4b5fd">this year</text></g>
  <g transform="translate(492,0)"><rect width="148" height="96" rx="12" fill="#0f172a" stroke="#34d399"/><text x="74" y="36" text-anchor="middle" font-size="28">🚀</text><text x="74" y="58" text-anchor="middle" font-family="system-ui, sans-serif" font-size="11" font-weight="700" fill="white">Launch</text><text x="74" y="74" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="#6ee7b7">v1.0 shipped</text></g>
</g>
<text x="340" y="132" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="8" fill="#475569">trophies · 4 cards · copy SVG · swap emoji</text>
</svg>
"""
if __name__=="__main__":
    out=ASSETS/"trophy-shelf.svg"; out.write_text(SVG,encoding="utf-8"); print(f"written {out} {out.stat().st_size}")
