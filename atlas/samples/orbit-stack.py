"""Орбита скиллов — два кольца с иконками, чисто SVG+CSS, без внешних картинок."""

from pathlib import Path

ASSETS = Path(__file__).resolve().parents[2] / "assets"

STACK = [
    ("py", "PY", "#3776AB"),
    ("ts", "TS", "#3178C6"),
    ("react", "Re", "#61DAFB"),
    ("blender", "Bl", "#EA7600"),
    ("docker", "Do", "#2496ED"),
    ("fastapi", "Fa", "#009688"),
    ("pg", "PG", "#4169E1"),
    ("linux", "Li", "#FCC624"),
]

SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="680" height="320" viewBox="0 0 680 320" role="img" aria-labelledby="t d">
  <title id="t">Орбита стека</title><desc id="d">Восемь технологий на двух орбитах вокруг ядра STACK. Кольца медленно вращаются.</desc>
  <defs>
    <radialGradient id="core" cx="50%" cy="35%"><stop offset="0%" stop-color="#1e1b4b"/><stop offset="100%" stop-color="#0f172a"/></radialGradient>
    <radialGradient id="orbitGlow" cx="50%" cy="50%"><stop offset="85%" stop-color="transparent"/><stop offset="100%" stop-color="#6366f1" stop-opacity="0.18"/></radialGradient>
    <filter id="glow"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="680" height="320" rx="16" fill="#0a0a0f"/>
  <!-- faint grid -->
  <g stroke="#1f2937" stroke-width="0.7" opacity="0.35">
    <path d="M0 160H680"/><path d="M340 0V320"/>
    <circle cx="340" cy="160" r="72" fill="none"/><circle cx="340" cy="160" r="112" fill="none"/>
  </g>
  <!-- orbits -->
  <circle cx="340" cy="160" r="72" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="6 6" opacity="0.7"/>
  <circle cx="340" cy="160" r="112" fill="none" stroke="#334155" stroke-width="1" stroke-dasharray="6 6" opacity="0.5"/>
  <!-- core -->
  <g filter="url(#glow)">
    <circle cx="340" cy="160" r="48" fill="url(#core)" stroke="#6366f1" stroke-width="2"/>
    <circle cx="340" cy="160" r="46" fill="none" stroke="#818cf8" stroke-width="0.8" opacity="0.35"/>
  </g>
  <text x="340" y="155" text-anchor="middle" font-family="JetBrains Mono, monospace" font-size="13" font-weight="700" fill="#a5b4fc" letter-spacing="3">STACK</text>
  <text x="340" y="172" text-anchor="middle" font-family="system-ui, sans-serif" font-size="8.5" fill="#64748b" letter-spacing="1.2">8 ТЕХНОЛОГИЙ</text>

  <style>
    @media (prefers-reduced-motion: no-preference) {
      .r1 { animation: spin 22s linear infinite; transform-origin: 340px 160px; }
      .r2 { animation: spinR 32s linear infinite; transform-origin: 340px 160px; }
      .c1 { animation: counter 22s linear infinite; transform-origin: 0 0; }
      .c2 { animation: counterR 32s linear infinite; transform-origin: 0 0; }
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes spinR { to { transform: rotate(-360deg); } }
    @keyframes counter { to { transform: rotate(-360deg); } }
    @keyframes counterR { to { transform: rotate(360deg); } }
  </style>

  <!-- inner ring 4 items at 0,90,180,270deg radius 72 -->
  <g class="r1">
    <g transform="translate(412,160)"><circle r="22" fill="#0f172a" stroke="#38bdf8" stroke-width="1.4"/><text text-anchor="middle" dy="5" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#e0f2fe">PY</text><g class="c1" transform="rotate(0)"><circle r="22" fill="none"/></g></g>
    <g transform="translate(340,88)"><circle r="22" fill="#0f172a" stroke="#f59e0b" stroke-width="1.4"/><text text-anchor="middle" dy="5" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#fef3c7">TS</text><g class="c1"/></g>
    <g transform="translate(268,160)"><circle r="22" fill="#0f172a" stroke="#22d3ee" stroke-width="1.4"/><text text-anchor="middle" dy="5" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#cffafe">Re</text></g>
    <g transform="translate(340,232)"><circle r="22" fill="#0f172a" stroke="#fb923c" stroke-width="1.4"/><text text-anchor="middle" dy="5" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#ffedd5">Bl</text></g>
  </g>
  <!-- outer ring 4 items at 45,135,225,315 radius 112 -->
  <g class="r2">
    <g transform="translate(419,81)"><circle r="22" fill="#0f172a" stroke="#60a5fa" stroke-width="1.4"/><text text-anchor="middle" dy="5" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#dbeafe">Do</text></g>
    <g transform="translate(261,81)"><circle r="22" fill="#0f172a" stroke="#34d399" stroke-width="1.4"/><text text-anchor="middle" dy="5" font-family="JetBrains Mono, monospace" font-size="10" font-weight="700" fill="#d1fae5">Fa</text></g>
    <g transform="translate(261,239)"><circle r="22" fill="#0f172a" stroke="#818cf8" stroke-width="1.4"/><text text-anchor="middle" dy="5" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#e0e7ff">PG</text></g>
    <g transform="translate(419,239)"><circle r="22" fill="#0f172a" stroke="#facc15" stroke-width="1.4"/><text text-anchor="middle" dy="5" font-family="JetBrains Mono, monospace" font-size="11" font-weight="700" fill="#fef9c3">Li</text></g>
  </g>

  <!-- labels bottom -->
  <g font-family="system-ui, sans-serif" font-size="9" fill="#94a3b8" text-anchor="middle">
    <text x="110" y="298">наведи — кольца крутятся, иконки остаются прямо</text>
    <text x="570" y="298" font-size="8" fill="#475569">SMIL+CSS · без JS · уважает reduced-motion</text>
  </g>
</svg>
"""

if __name__ == "__main__":
    out = ASSETS / "orbit-stack.svg"
    out.write_text(SVG, encoding="utf-8")
    print(f"written {out} ({out.stat().st_size} bytes)")

