"""A pinhole eye, a vertical *circular* mirror and a sheet. All lengths in mm.

Paper lies at z=0. The eye is in front (negative y); printed rows run toward the eye.
The plate maker starts on the paper; the viewer starts at the eye. Neither needs a
lookup table from the other. NumPy arguments may be pixel grids or scalars.
"""

import math

import numpy as np

PAGE = (297, 210)
AXIS = (148.5, 57)  # from left and top of the landscape sheet
R, TOP = 25.0, 80.0
DIST, EYE, AIM = 280.0, 240.0, 44.0
CARD = (37.6, 47.0)
SCALE = 8  # printed samples per mm


def paper_to_card(x, y):
    """Inverse design: find the specular point between sheet point Q and the eye.

    In plan view, the two tangential components of the unit light directions must
    agree. Bisect only the arc visible from *both* endpoints. Vertical slope is
    preserved by this vertical mirror, giving z from the two horizontal distances.
    """
    rho = np.maximum(np.hypot(x, y), R + 0.00001)
    beta = np.arctan2(np.abs(x), -y)
    lo = np.maximum(0, beta - np.arccos(R / rho))
    hi = np.minimum(beta, math.acos(R / DIST))
    visible = (lo <= hi) & (np.hypot(x, y) > R)
    for _ in range(22):
        th = (lo + hi) / 2
        other = beta - th
        a = np.sqrt(DIST**2 + R**2 - 2 * DIST * R * np.cos(th))
        b = np.sqrt(np.maximum(1e-12, rho**2 + R**2 - 2 * rho * R * np.cos(other)))
        go_right = DIST * np.sin(th) * b < rho * np.sin(other) * a
        lo, hi = np.where(go_right, th, lo), np.where(go_right, hi, th)
    th = (lo + hi) / 2
    mx = R * np.sin(th) * np.sign(x)
    my = -R * np.cos(th)
    a = np.hypot(mx, my + DIST)
    b = np.hypot(mx - x, my - y)
    mz = EYE * b / (a + b)
    focal = math.hypot(DIST - R, EYE - AIM)
    c = (DIST - R) / focal
    s = (EYE - AIM) / focal
    depth = (my + DIST) * c - (mz - EYE) * s
    u = focal * mx / depth
    v = focal * ((my + DIST) * s + (mz - EYE) * c) / depth
    return u, v, visible & (mz <= TOP)


def sight(u, v, yaw=0.0, height=EYE):
    """Shoot camera rays; return both unobstructed paper hits and side reflections.

    u,v are coordinates on the focal plane measured from the aiming point, not
    unwrapped angles around the cylinder. yaw moves the observer, not the print.
    """
    angle = math.radians(yaw)
    ca, sa = math.cos(angle), math.sin(angle)
    focal = math.hypot(DIST - R, height - AIM)
    c = (DIST - R) / focal
    s = (height - AIM) / focal
    # Do the intersection in eye-aligned coordinates, rotate hits into sheet space last.
    dx = u
    dy = DIST - R + v * s
    dz = AIM - height + v * c
    qa = dx * dx + dy * dy
    qb = -DIST * dy
    discr = qb * qb - qa * (DIST**2 - R**2)
    t = (-qb - np.sqrt(np.maximum(0, discr))) / qa
    mx, my, mz = t * dx, -DIST + t * dy, height + t * dz
    nx, ny = mx / R, my / R
    twice = 2 * (dx * nx + dy * ny)
    rx, ry = dx - twice * nx, dy - twice * ny
    q = -mz / dz
    px, py = mx + q * rx, my + q * ry
    k = -height / dz
    fx, fy = k * dx, -DIST + k * dy
    tcap = (TOP - height) / dz
    cap = (tcap * dx) ** 2 + (tcap * dy - DIST) ** 2 <= R**2
    side = (discr >= 0) & (mz >= 0) & (mz <= TOP) & (t > 0) & (dz < 0) & ~cap
    return {
        'x': ca * px - sa * py,
        'y': sa * px + ca * py,
        'floor_x': ca * fx - sa * fy,
        'floor_y': sa * fx + ca * fy,
        'side': side,
        'cap': cap,
        'z': mz,
        'nx': nx,
        'ny': ny,
    }


def sample(texture, x, y):
    """Bilinear RGB sampling in pixel coordinates (centres at integer positions)."""
    h, w = texture.shape[:2]
    x = np.clip(x, 0, w - 1)
    y = np.clip(y, 0, h - 1)
    ix = x.astype(np.int32)
    iy = y.astype(np.int32)
    jx = np.minimum(ix + 1, w - 1)
    jy = np.minimum(iy + 1, h - 1)
    a = (x - ix)[..., None]
    b = (y - iy)[..., None]
    return (texture[iy, ix] * (1 - a) + texture[iy, jx] * a) * (1 - b) + (
        texture[jy, ix] * (1 - a) + texture[jy, jx] * a
    ) * b


def from_sheet(sheet, x, y):
    """Sample the saved print, including registration marks. Never read the subject."""
    return sample(
        sheet, (AXIS[0] + x) * sheet.shape[1] / PAGE[0] - 0.5, (AXIS[1] - y) * sheet.shape[0] / PAGE[1] - 0.5
    )
