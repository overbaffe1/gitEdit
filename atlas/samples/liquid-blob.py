"""Жидкая капля — одна форма перетекает в другую (circle → squircle → star → цветок), SMIL на d."""
from pathlib import Path
ASSETS = Path(__file__).resolve().parents[2] / "assets"

# 4 morph states, all centered at 240,110, keep same point count for smooth morph: 4 cubic beziers approximating blobs
P0 = "M 240 42 C 288 42 336 62 336 110 C 336 158 288 178 240 178 C 192 178 144 158 144 110 C 144 62 192 42 240 42 Z"
P1 = "M 240 48 C 285 48 332 68 332 112 C 332 156 285 172 240 168 C 195 172 148 156 148 112 C 148 68 195 48 240 48 Z"
P2 = "M 240 38 C 278 52 326 78 318 116 C 310 154 272 176 240 176 C 208 176 170 154 162 116 C 154 78 202 52 240 38 Z"
P3 = "M 240 44 C 292 44 340 70 334 114 C 328 158 290 180 240 180 C 190 180 152 158 146 114 C 140 70 188 44 240 44 Z"

SVG = f"""<svg xmlns="http://www.w3.org/2000/svg" width="680" height="260" viewBox="0 0 680 260" role="img">
<title>Жидкая капля</title><desc>Одна капля морфит между четырьмя формами — чистый SMIL на path d.</desc>
<defs>
  <radialGradient id="blobGrad" cx="35%" cy="30%"><stop offset="0%" stop-color="#c4b5fd"/><stop offset="55%" stop-color="#7c3aed"/><stop offset="100%" stop-color="#0f172a"/></radialGradient>
  <linearGradient id="bgGrad" x1="0" y1="0" x2="100%" y2="0%"><stop offset="0%" stop-color="#020617"/><stop offset="100%" stop-color="#1e1b4b"/></linearGradient>
  <filter id="soft"><feGaussianBlur stdDeviation="8" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<rect width="680" height="260" rx="16" fill="url(#bgGrad)"/>
<!-- left blob -->
<g filter="url(#soft)">
  <path d="{P0}" fill="url(#blobGrad)" stroke="white" stroke-opacity="0.14" stroke-width="1.2">
    <animate attributeName="d" values="{P0};{P1};{P2};{P3};{P0}" dur="7s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1;0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.28;0.55;0.82;1"/>
  </path>
  <!-- eyes that stay inside -->
  <g fill="white" fill-opacity="0.92">
    <ellipse cx="218" cy="108" rx="10" ry="12" fill="white"/>
    <ellipse cx="262" cy="108" rx="10" ry="12" fill="white"/>
    <circle cx="221" cy="111" r="5" fill="#0f172a"><animate attributeName="r" values="5;0.5;5" dur="4.2s" repeatCount="indefinite" begin="1s"/></circle>
    <circle cx="265" cy="111" r="5" fill="#0f172a"><animate attributeName="r" values="5;0.5;5" dur="4.2s" repeatCount="indefinite" begin="1s"/></circle>
    <ellipse cx="240" cy="132" rx="7" ry="4" fill="#0f172a" opacity="0.85"/>
  </g>
</g>
<!-- small satellite blobs morph too -->
<g filter="url(#soft)" opacity="0.8">
  <path d="M 470 90 C 486 90 498 98 498 114 C 498 130 486 138 470 138 C 454 138 442 130 442 114 C 442 98 454 90 470 90 Z" fill="#38bdf8" fill-opacity="0.9">
    <animate attributeName="d" values="M 470 90 C 486 90 498 98 498 114 C 498 130 486 138 470 138 C 454 138 442 130 442 114 C 442 98 454 90 470 90 Z;M 470 96 C 490 96 504 104 498 118 C 492 132 478 142 466 138 C 452 134 438 122 442 108 C 446 94 458 90 470 96 Z;M 470 90 C 486 90 498 98 498 114 C 498 130 486 138 470 138 C 454 138 442 130 442 114 C 442 98 454 90 470 90 Z" dur="5s" repeatCount="indefinite"/>
  </path>
  <path d="M 540 140 C 552 140 562 148 562 160 C 562 172 552 180 540 180 C 528 180 518 172 518 160 C 518 148 528 140 540 140 Z" fill="#f472b6" fill-opacity="0.9">
    <animate attributeName="d" values="M 540 140 C 552 140 562 148 562 160 C 562 172 552 180 540 180 C 528 180 518 172 518 160 C 518 148 528 140 540 140 Z;M 540 134 C 556 134 568 144 566 162 C 564 178 552 186 540 182 C 528 178 516 168 516 154 C 516 140 528 134 540 134 Z;M 540 140 C 552 140 562 148 562 160 C 562 172 552 180 540 180 C 528 180 518 172 518 160 C 518 148 528 140 540 140 Z" dur="6s" repeatCount="indefinite"/>
  </path>
</g>
<g font-family="JetBrains Mono, monospace" fill="white">
  <text x="390" y="88" font-size="13" font-weight="700" letter-spacing="2" fill="white">ЖИДКАЯ КАПЛЯ</text>
  <text x="390" y="106" font-size="10" fill="#a5b4fc">одна форма · 4 состояния · морфит по d</text>
  <text x="390" y="128" font-size="9" fill="white" fill-opacity="0.65">SMIL &lt;animate d&gt; · без JS · глаза — маска внутри</text>
  <g transform="translate(390,148)">
    <rect width="86" height="24" rx="12" fill="white" fill-opacity="0.08" stroke="white" stroke-opacity="0.18"/>
    <text x="43" y="16" text-anchor="middle" font-size="9" fill="white">● MORPH 7s</text>
    <rect x="96" width="88" height="24" rx="12" fill="white" fill-opacity="0.08" stroke="white" stroke-opacity="0.18"/>
    <text x="140" y="16" text-anchor="middle" font-size="9" fill="white">◐ BLINK 4s</text>
  </g>
  <text x="390" y="200" font-size="8.5" fill="white" fill-opacity="0.45">пересобрать: python3 atlas/samples/liquid-blob.py · можно вставить в профиль как аватара</text>
</g>
<style>@media (prefers-reduced-motion: reduce){{ animate{{ display:none; }} }}</style>
</svg>
"""

if __name__ == "__main__":
    out = ASSETS / "liquid-blob.svg"
    out.write_text(SVG, encoding="utf-8")
    print(f"written {out} {out.stat().st_size}")

