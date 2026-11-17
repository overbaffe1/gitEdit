"""One ring, one orthographic camera, two native-size SVG print proofs.

python atlas/samples/print-ring.py  (Python 3, standard library only)
The z-buffer serves both prints: occlusion for the pen, lighting for the screen.
"""
from math import ceil, cos, floor, sin, sqrt, tau
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / 'assets'
W, H = 384, 302
VIEW, ROLL = .86, -.22
BAYER = ((0, 8, 2, 10), (12, 4, 14, 6), (3, 11, 1, 9), (15, 7, 13, 5))


def surface(u, v):
    radius = .36 + .075*cos(3*u-.8)
    r = 1.035 + .09*cos(3*u+.5) + radius*cos(v)
    x, y, z = r*cos(u), r*sin(u), .24*sin(2*u+.8) + radius*sin(v)
    y, z = cos(VIEW)*y - sin(VIEW)*z, sin(VIEW)*y + cos(VIEW)*z
    return (cos(ROLL)*x - sin(ROLL)*y, sin(ROLL)*x + cos(ROLL)*y, z)


def vertex(u, v):
    x, y, z = surface(u, v)
    a, b, c = surface(u+.001, v)
    d, e, f = surface(u, v+.001)
    a, b, c, d, e, f = a-x, b-y, c-z, d-x, e-y, f-z
    nx, ny, nz = b*f-c*e, c*d-a*f, a*e-b*d
    length = sqrt(nx*nx+ny*ny+nz*nz)
    light = max(0, (-.54*nx + .64*ny + .545*nz) / length)
    return 191 + 80*x, 152 - 80*y, z, .115 + .875*light, nz > 0


def buff():
    depth = [float('-inf')]*(W*H)
    tone = [0.]*(W*H)

    def triangle(a, b, c):
        ax, ay, az, al, _ = a
        bx, by, bz, bl, _ = b
        cx, cy, cz, cl, _ = c
        det = (by-cy)*(ax-cx) + (cx-bx)*(ay-cy)
        if abs(det) < 1e-8:
            return
        for y in range(max(0, ceil(min(ay,by,cy))), min(H-1, floor(max(ay,by,cy)))+1):
            for x in range(max(0, ceil(min(ax,bx,cx))), min(W-1, floor(max(ax,bx,cx)))+1):
                s = ((by-cy)*(x-cx) + (cx-bx)*(y-cy)) / det
                t = ((cy-ay)*(x-cx) + (ax-cx)*(y-cy)) / det
                k = 1-s-t
                if min(s,t,k) < 0:
                    continue
                i, z = y*W+x, s*az + t*bz + k*cz
                if z > depth[i]:
                    depth[i], tone[i] = z, s*al + t*bl + k*cl

    rows = [[vertex(tau*i/96, tau*j/44) for j in range(45)] for i in range(97)]
    for before, after in zip(rows, rows[1:]):
        for j in range(44):
            triangle(before[j], after[j], after[j+1])
            triangle(before[j], after[j+1], before[j+1])
    return depth, tone


def simplify(points, tolerance=.20):
    # Discard intermediate samples that lie within a fraction of a print pixel.
    x, y = points[0]
    dx, dy = points[-1][0]-x, points[-1][1]-y
    length = dx*dx + dy*dy
    worst, split = 0., 0
    for i, (px, py) in enumerate(points[1:-1], 1):
        t = max(0, min(1, ((px-x)*dx + (py-y)*dy)/length)) if length else 0
        error = (px-x-t*dx)**2 + (py-y-t*dy)**2
        if error > worst:
            worst, split = error, i
    if worst > tolerance*tolerance:
        return simplify(points[:split+1], tolerance)[:-1] + simplify(points[split:], tolerance)
    return [points[0], points[-1]]


def pen(depth):
    def stroke(curves):
        parts = []
        for curve in curves:
            line = []
            for p in [*curve, None]:
                if p:
                    x, y, z, _, face = p
                    if face and z+.046 >= depth[round(y)*W+round(x)]:
                        line.append((x,y))
                        continue
                if len(line) >= 2:
                    parts.append('M'+' '.join(f'{x:.1f},{y:.1f}' for x,y in simplify(line)))
                line = []
        return ''.join(parts)
    rings = stroke((vertex(tau*i/70, tau*j/150) for j in range(151)) for i in range(70))
    grain = stroke((vertex(tau*i/300, tau*j/13) for i in range(301)) for j in range(13))
    return f'<g fill="none" stroke="currentColor" stroke-linecap="round"><path d="{rings}" stroke-width="1.45"/><path d="{grain}" stroke-width=".72"/></g>'


def screen(tone, step=2):
    # A 4x4 cell repeats in *image space*. Coalesce adjacent lit pixels on a row.
    runs = []
    for y in range(0, H-1, step):
        left = None
        for x in range(0, W+1, step):
            limit = (BAYER[(y//step)%4][(x//step)%4]+.5)/16
            if x < W and tone[(y+1)*W+x+1] > limit:
                if left is None:
                    left = x
            elif left is not None:
                runs.append(f'M{left} {y}h{x-left}v{step}H{left}Z')
                left = None
    return f'<path d="{"".join(runs)}" fill="currentColor" shape-rendering="crispEdges"/>'


def mount(art, name, number, caption, paper, ink):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d" xml:lang="ru" color="{ink}">
  <title id="t">Пробное кольцо · {name}</title><desc id="d">{caption}. Неправильное объёмное кольцо в наклонной проекции.</desc>
  <rect x="1" y="1" width="382" height="300" rx="9" fill="{paper}" stroke="currentColor"/>
  <g stroke="currentColor" fill="none"><path d="M17 35H367M17 238H367"/>
    <path d="M19 61V51h10m336 10V51h-10M19 217v10h10m336-10v10h-10" opacity=".57"/>
    <circle cx="358" cy="20" r="5"/><path d="M348 20h20m-10-10v20"/>
  </g>
  <g fill="currentColor" font-family="monospace" font-size="13" letter-spacing="1.3">
    <text x="18" y="25">G/E · КАБИНЕТ ПЕЧАТИ</text><text x="330" y="25" text-anchor="end">№ {number}</text>
  </g>
  {art}
  <text x="18" y="283" fill="currentColor" font-family="Georgia, 'DejaVu Serif', serif" font-size="36" font-weight="bold">{name}</text>
  <text x="365" y="278" fill="currentColor" text-anchor="end" font-family="monospace" font-size="13">{caption}</text>
</svg>\n'''


if __name__ == '__main__':
    depth, tone = buff()
    (OUT/'ring-pen.svg').write_text(mount(pen(depth), 'Контур', '02А', 'Перо / линии', '#f5e6cf', '#523a39'), encoding='utf-8')
    (OUT/'ring-screen.svg').write_text(mount(screen(tone), 'Растр', '02Б', 'Байер / 4 × 4', '#2d2941', '#ffd797'), encoding='utf-8')
