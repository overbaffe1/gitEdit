"""Эквалайзер — 8 столбиков, каждый со своим темпом, чистый CSS, без JS."""
from pathlib import Path
ASSETS = Path(__file__).resolve().parents[2] / "assets"

SVG = """<svg xmlns="http://www.w3.org/2000/svg" width="680" height="120" viewBox="0 0 680 120" role="img">
  <title>Эквалайзер</title><desc>Восемь столбиков танцуют как аудио-метр, каждый со своим темпом.</desc>
  <defs>
    <linearGradient id="barGrad" x1="0" y1="100%" x2="0" y2="0%"><stop offset="0%" stop-color="#7c3aed"/><stop offset="50%" stop-color="#ec4899"/><stop offset="100%" stop-color="#06b6d4"/></linearGradient>
    <filter id="glowEq"><feGaussianBlur stdDeviation="2.5"/><feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <rect width="680" height="120" rx="14" fill="#020617"/>
  <g font-family="JetBrains Mono, monospace">
    <text x="22" y="22" font-size="9" letter-spacing="3" fill="#64748b">NOW PLAYING — GITEDIT RADIO</text>
    <text x="658" y="22" text-anchor="end" font-size="9" fill="#334155">● LIVE</text>
  </g>
  <!-- bars container -->
  <g transform="translate(32,38)" filter="url(#glowEq)">
    <!-- each bar: x, base h, anim duration, delay -->
    <g class="b1"><rect x="0" width="62" height="62" y="18" rx="4" fill="url(#barGrad)"/></g>
    <g class="b2"><rect x="78" width="62" height="46" y="34" rx="4" fill="url(#barGrad)"/></g>
    <g class="b3"><rect x="156" width="62" height="78" y="2" rx="4" fill="url(#barGrad)"/></g>
    <g class="b4"><rect x="234" width="62" height="54" y="26" rx="4" fill="url(#barGrad)"/></g>
    <g class="b5"><rect x="312" width="62" height="70" y="10" rx="4" fill="url(#barGrad)"/></g>
    <g class="b6"><rect x="390" width="62" height="38" y="42" rx="4" fill="url(#barGrad)"/></g>
    <g class="b7"><rect x="468" width="62" height="58" y="22" rx="4" fill="url(#barGrad)"/></g>
    <g class="b8"><rect x="546" width="62" height="66" y="14" rx="4" fill="url(#barGrad)"/></g>
    <!-- fine horizontal lines for equalizer look -->
    <g stroke="white" stroke-opacity="0.08" stroke-width="0.8">
      <line x1="0" x2="608" y1="10" y2="10"/><line x1="0" x2="608" y1="22" y2="22"/><line x1="0" x2="608" y1="34" y2="34"/><line x1="0" x2="608" y1="46" y2="46"/><line x1="0" x2="608" y1="58" y2="58"/><line x1="0" x2="608" y1="70" y2="70"/>
    </g>
  </g>
  <g font-family="system-ui, sans-serif" font-size="8" fill="#475569" text-anchor="middle">
    <text x="340" y="112">чистый CSS · 8 bars · desync 0.7–1.4s · уважает reduced-motion</text>
  </g>
  <style>
    /* DJ-calendar style: each bar own duration + negative delay */
    .b1 rect{ animation: pulse1 0.92s ease-in-out infinite; }
    .b2 rect{ animation: pulse2 1.18s ease-in-out infinite -0.2s; }
    .b3 rect{ animation: pulse3 0.78s ease-in-out infinite -0.5s; }
    .b4 rect{ animation: pulse4 1.05s ease-in-out infinite -0.8s; }
    .b5 rect{ animation: pulse5 0.88s ease-in-out infinite -0.3s; }
    .b6 rect{ animation: pulse6 1.32s ease-in-out infinite -0.6s; }
    .b7 rect{ animation: pulse7 0.96s ease-in-out infinite -0.1s; }
    .b8 rect{ animation: pulse8 1.12s ease-in-out infinite -0.4s; }
    @keyframes pulse1{0%,100%{transform:translateY(0) scaleY(1)}50%{transform:translateY(6px) scaleY(0.62)}}
    @keyframes pulse2{0%,100%{transform:translateY(0) scaleY(1)}50%{transform:translateY(8px) scaleY(1.35)}}
    @keyframes pulse3{0%,100%{transform:translateY(0) scaleY(1)}50%{transform:translateY(4px) scaleY(0.48)}}
    @keyframes pulse4{0%,100%{transform:translateY(0) scaleY(1)}50%{transform:translateY(10px) scaleY(0.7)}}
    @keyframes pulse5{0%,100%{transform:translateY(0) scaleY(1)}50%{transform:translateY(5px) scaleY(1.28)}}
    @keyframes pulse6{0%,100%{transform:translateY(0) scaleY(1)}50%{transform:translateY(7px) scaleY(0.55)}}
    @keyframes pulse7{0%,100%{transform:translateY(0) scaleY(1)}50%{transform:translateY(9px) scaleY(1.18)}}
    @keyframes pulse8{0%,100%{transform:translateY(0) scaleY(1)}50%{transform:translateY(3px) scaleY(0.82)}}
    g rect{ transform-origin: 50% 80px; }
    @media (prefers-reduced-motion: reduce){ .b1 rect,.b2 rect,.b3 rect,.b4 rect,.b5 rect,.b6 rect,.b7 rect,.b8 rect{ animation:none; } }
  </style>
</svg>
"""
if __name__ == "__main__":
    out = ASSETS / "equalizer.svg"
    out.write_text(SVG, encoding="utf-8")
    print(f"written {out} {out.stat().st_size}")
