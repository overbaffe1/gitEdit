"""A moon jelly drawn by stereo PCM. Only the Python standard library; L = X, R = Y.

Each scan is one closed pen stroke, including the return along every tentacle.
There is no pen-up signal, image data or sequence of keyframes in the WAV.
"""

import sys
import wave
from array import array
from bisect import bisect_right
from itertools import accumulate, pairwise
from math import cos, dist, pi, sin, tau

RATE = 48_000
SCAN = 800  # 60 complete traces per second
SCANS = 240  # four-second loop
GAIN = 4500  # deliberately quiet: these are coordinates, not a mastered song


def line(fn, start, end, steps):
    return [fn(start + (end - start) * i / steps) for i in range(steps + 1)]


def stroke(phase):
    """Bell meridians and trailing arms meet at shared points on the rim."""
    open_bell = (1 + cos(2 * phase)) / 2
    width = 0.63 + 0.21 * open_bell
    height = 0.60 - 0.23 * open_bell
    depth = 0.09 + 0.045 * open_bell

    def bell(v, angle):
        ring = sin(v)
        a = angle + 0.10 * sin(2 * v) * sin(2 * angle + phase)
        x = width * ring * cos(a)
        y = height * cos(v) - depth * ring * sin(a) - 0.022 * ring**8 * (1 - cos(12 * angle))
        return x, y

    def rim(a):
        return bell(pi / 2, a)

    def tentacle(a, number):
        x0, y0 = rim(a)
        length = 0.50 + 0.44 * sin(a) + 0.09 * cos(3 * a - phase)

        def edge(frac, side):
            sway = 0.14 * sin(phase - 6 * frac + a) + 0.067 * sin(2 * phase - 12 * frac + 3 * a)
            center = x0 * (1 - 0.36 * frac) + frac * sway + 0.13 * frac**2 * sin(phase)
            ribbon = (0.041 if number in (2, 4) else 0.009) * sin(pi * frac) * cos(9 * frac - 2 * phase + a)
            return center + side * ribbon, y0 - length * frac

        return line(lambda s: edge(s, 1), 0, 1, 36) + line(lambda s: edge(s, -1), 1, 0, 36)

    def meridian(a, lo, hi):
        return line(lambda v: bell(v, a), lo, hi, 28)

    # A continuous four-lobed rosette, like the rings inside a moon jelly's bell.
    cx, cy = bell(0.92, pi / 2)

    def petal(t):
        reach = sin(2 * t) ** 2
        return cx + 0.29 * width * reach * cos(t), cy + 0.25 * height * reach * sin(t)

    path = meridian(0, 0, 1.08)
    path += line(lambda a: bell(1.08, a), 0, tau, 72)  # one latitude of the translucent bell
    path += meridian(0, 1.08, pi / 2)
    prev = 0
    for i in range(7):
        a = pi * (i + 0.70) / 7.4
        path += line(rim, prev, a, 12)
        path += tentacle(a, i)
        prev = a
    path += line(rim, prev, pi, 12) + line(rim, pi, tau, 72)
    path += meridian(0, pi / 2, 0)
    path += meridian(0.18 * pi, 0, pi / 2) + line(rim, 0.18 * pi, pi / 2, 18)
    path += meridian(pi / 2, pi / 2, 0.92) + line(petal, 0, tau, 96) + meridian(pi / 2, 0.92, 0)
    path += (
        meridian(0.67 * pi, 0, pi / 2) + line(rim, 0.67 * pi, 0.85 * pi, 18) + meridian(0.85 * pi, pi / 2, 0)
    )
    # The left outer meridian wasn't part of a front rib. Traverse it and retrace it.
    path += meridian(pi, 0, pi / 2) + meridian(pi, pi / 2, 0)
    tilt = 0.16 + 0.18 * sin(phase)
    return [(x * cos(tilt) - y * sin(tilt), x * sin(tilt) + y * cos(tilt)) for x, y in path]


def scan_samples(phase):
    """Uniform travel by arc length, gentle corner filtering and no per-scan DC offset."""
    path = stroke(phase)
    lengths = [0.0, *accumulate(dist(a, b) for a, b in pairwise(path))]
    samples = []
    for i in range(SCAN):
        d = i * lengths[-1] / SCAN
        j = bisect_right(lengths, d) - 1
        u = (d - lengths[j]) / (lengths[j + 1] - lengths[j])
        samples.append(tuple(a + u * (b - a) for a, b in zip(path[j], path[j + 1], strict=True)))
    mean = [sum(p[k] for p in samples) / SCAN for k in (0, 1)]
    for i, p in enumerate(samples):
        yield tuple(
            round(GAIN * ((samples[i - 1][k] + 2 * p[k] + samples[(i + 1) % SCAN][k]) / 4 - mean[k]))
            for k in (0, 1)
        )


def write_wav(path):
    pcm = array('h')
    for i in range(SCANS):
        for pair in scan_samples(tau * i / SCANS):
            pcm.extend(pair)
    if sys.byteorder != 'little':
        pcm.byteswap()
    with wave.open(str(path), 'wb') as wav:
        wav.setparams((2, 2, RATE, 0, 'NONE', 'not compressed'))
        wav.writeframes(pcm.tobytes())


def read_wav(path):
    with wave.open(str(path), 'rb') as wav:
        if (wav.getnchannels(), wav.getsampwidth(), wav.getframerate(), wav.getnframes()) != (
            2,
            2,
            RATE,
            SCANS * SCAN,
        ):
            raise ValueError('Expected the four-second, 48 kHz stereo PCM16 specimen')
        pcm = array('h', wav.readframes(wav.getnframes()))
    if sys.byteorder != 'little':
        pcm.byteswap()
    if len(pcm) != 2 * SCAN * SCANS:
        raise ValueError('Incomplete PCM data')
    return pcm
