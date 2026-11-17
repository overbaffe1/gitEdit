"""Publish ordinary exhibit files plus static README plates; no network or third-party packages."""

import json
import math
from html import escape
from pathlib import Path
from shutil import copyfile

SAMPLES = Path(__file__).resolve().parent
ASSETS = SAMPLES.parents[1] / "assets"


def label(x, y, text, size=14, bold=False):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{700 if bold else 400}">{escape(str(text))}</text>'


def plate(title, desc, code, marks, legend):
    legend = "".join(
        label(365, 106 + 25 * i, line, 14, i == 0) for i, line in enumerate(legend)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="560" height="246" viewBox="0 0 560 246" role="img" aria-labelledby="t d" xml:lang="ru">
<title id="t">{escape(title)}</title><desc id="d">{escape(desc)}</desc>
<defs><pattern id="grid" width="16" height="16" patternUnits="userSpaceOnUse"><path d="M16 0H0V16" fill="none" stroke="#d7d7c6" stroke-width=".65"/></pattern></defs>
<rect width="560" height="246" rx="6" fill="#faf5e6"/><rect x="12" y="46" width="536" height="188" fill="url(#grid)" stroke="#d4cdb7"/>
<g fill="#264843" font-family="DejaVu Sans, sans-serif">{label(20, 31, title, 20, True)}{label(441, 29, code, 12)}{marks}{legend}</g>
</svg>\n"""


def points(coords):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)


def publish_skyline(samples=SAMPLES, assets=ASSETS):
    src = samples / "weekly-skyline.stl"
    copyfile(src, assets / src.name)
    # The two horizontal triangles of each roof have the same XY bounds and height.
    roofs = set()
    tri = []
    for line in src.read_text(encoding="ascii").splitlines():
        fields = line.split()
        if fields[:1] == ["vertex"]:
            tri.append(tuple(map(float, fields[1:])))
        elif fields[:1] == ["endfacet"]:
            xs, ys, zs = zip(*tri)
            if min(zs) == max(zs) and zs[0] > 0:
                roofs.add((min(xs), min(ys), max(xs), max(ys), zs[0]))
            tri = []

    def iso(x, y, z):
        return 197 + (x - y) * 2.5, 131 + (x + y) * 0.84 - z * 1.96

    shapes = []
    for x, y, u, v, h in sorted(roofs, key=lambda box: (box[0] + box[1], box[0])):
        base = [iso(a, b, 0) for a, b in ((x, y), (u, y), (u, v), (x, v))]
        top = [iso(a, b, h) for a, b in ((x, y), (u, y), (u, v), (x, v))]
        for pts, col in [
            (top, "#edca90"),
            ([base[1], base[2], top[2], top[1]], "#568d7a"),
            ([base[2], base[3], top[3], top[2]], "#355c57"),
        ]:
            shapes.append(
                f'<polygon points="{points(pts)}" fill="{col}" stroke="#2e4944" stroke-width=".8"/>'
            )
    svg = plate(
        "Квартал LazyGit",
        "Аксонометрия башен из weekly-skyline.stl: каждая высота равна числу коммитов за неделю.",
        "АТЛАС / STL",
        "".join(shapes),
        [
            f"{len(roofs)} домов",
            "1 дом — неделя",
            "1 этаж — коммит",
            f"Всего: {sum(b[4] for b in roofs):.0f}",
        ],
    )
    (assets / "weekly-skyline.svg").write_text(svg, encoding="utf-8")


def projection(coords):
    # Local equirectangular drawing of these small sample areas, north up.
    lon, lat = zip(*coords)
    x0 = (min(lon) + max(lon)) / 2
    y0 = (min(lat) + max(lat)) / 2
    k = math.cos(math.radians(y0))
    scale = min(260 / ((max(lon) - min(lon)) * k), 135 / (max(lat) - min(lat)))
    return lambda p: (176 + (p[0] - x0) * k * scale, 141 - (p[1] - y0) * scale)


def publish_maps(samples=SAMPLES, assets=ASSETS):
    for data in ("survey.geojson", "sheets.topojson"):
        copyfile(samples / data, assets / data)
    features = json.loads((samples / "survey.geojson").read_text())["features"]
    (route,) = [
        f["geometry"]["coordinates"]
        for f in features
        if f["geometry"]["type"] == "LineString"
    ]
    project = projection(route)
    line = f'<polyline points="{points(map(project, route))}" fill="none" stroke="#78578c" stroke-width="4" stroke-linejoin="round"/>'
    for point in route:
        x, y = project(point)
        line += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#fff9ed" stroke="#593e72" stroke-width="2"/>'
    for f in features:
        if f["geometry"]["type"] == "Point":
            x, y = project(f["geometry"]["coordinates"])
            line += label(x + 8, y - 6, f["properties"]["title"].split()[-1], 17, True)
    (assets / "survey.svg").write_text(
        plate(
            "Маршрут A — B",
            "Две отмеченные точки и профиль по четырём отсчётам.",
            "GEO / 01",
            line,
            ["Учебный профиль", "Север ↑", "Долгота, широта"],
        ),
        encoding="utf-8",
    )
    topo = json.loads((samples / "sheets.topojson").read_text())
    arcs = topo["arcs"]
    project = projection([p for arc in arcs for p in arc])
    shapes = []
    used = []
    for f in topo["objects"]["sheets"]["geometries"]:
        (ring,) = f["arcs"]
        used.append({i if i >= 0 else ~i for i in ring})
        coords = [p for i in ring for p in (arcs[i] if i >= 0 else reversed(arcs[~i]))]
        shapes.append(
            f'<polygon points="{points(map(project, coords))}" fill="{f["properties"]["fill"]}" fill-opacity=".77" stroke="#38544e" stroke-width="2"/>'
        )
    (shared,) = set.intersection(*used)
    shapes.append(
        f'<polyline points="{points(map(project, arcs[shared]))}" fill="none" stroke="#ffda99" stroke-width="4" stroke-dasharray="6 3"/>'
    )
    (assets / "sheets.svg").write_text(
        plate(
            "Два соседних листа",
            "Два полигона. Пунктиром отмечена общая дуга.",
            "TOPO / 02",
            "".join(shapes),
            ["Два полигона", "Пунктир —", "общая граница"],
        ),
        encoding="utf-8",
    )


if __name__ == "__main__":
    copyfile(
        SAMPLES / "crystal.stl", ASSETS / "crystal.stl"
    )  # keep published and notebook paths usable
    publish_maps()
    publish_skyline()
