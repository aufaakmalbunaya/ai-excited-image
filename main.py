#!/usr/bin/env python3
"""Golden koi breaking out of its painted museum frame.

Pure standard library. Run `python3 main.py` to generate entry.png (900x600).
The image is drawn pixel by pixel with zlib-compressed PNG output.
"""

import math
import struct
import zlib

W, H = 900, 600

# ---------------------------------------------------------------- palette
WALL_TOP = (27, 42, 74)
WALL_BOTTOM = (12, 22, 44)
GOLD = (201, 162, 39)
GOLD_LIGHT = (246, 211, 101)
GOLD_DARK = (122, 92, 14)
GOLD_DEEP = (150, 110, 16)
WATER_TOP = (46, 111, 142)
WATER_BOTTOM = (23, 69, 94)
KOI_GOLD = (255, 215, 106)
KOI_GOLD_DARK = (184, 134, 11)
KOI_BELLY = (255, 233, 168)
KOI_STITCH = (138, 101, 8)
SPLASH = (207, 238, 255)
LILY = (46, 125, 70)
LILY_DARK = (28, 84, 46)
PAINTED_KOI = (232, 114, 42)
WHITE = (245, 245, 240)
INK = (16, 20, 28)

buf = bytearray(W * H * 3)


def px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        buf[i], buf[i + 1], buf[i + 2] = color


def get(x, y):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        return buf[i], buf[i + 1], buf[i + 2]
    return 0, 0, 0


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def fill_rect(x0, y0, x1, y1, color):
    x0 = max(0, x0)
    y0 = max(0, y0)
    x1 = min(W, x1)
    y1 = min(H, y1)
    for y in range(y0, y1):
        base = (y * W + x0) * 3
        for x in range(x0, x1):
            i = base + (x - x0) * 3
            buf[i], buf[i + 1], buf[i + 2] = color


def hline(x0, x1, y, color):
    for x in range(max(0, x0), min(W, x1)):
        px(x, y, color)


def line(x0, y0, x1, y1, color):
    dx = x1 - x0
    dy = y1 - y0
    steps = max(abs(dx), abs(dy), 1)
    for s in range(steps + 1):
        px(round(x0 + dx * s / steps), round(y0 + dy * s / steps), color)


def disc(cx, cy, r, color):
    r = int(r)
    for y in range(cy - r, cy + r + 1):
        dy = y - cy
        span = int(math.sqrt(max(0, r * r - dy * dy)))
        for x in range(cx - span, cx + span + 1):
            px(x, y, color)


def ellipse(cx, cy, rx, ry, color):
    for y in range(cy - ry, cy + ry + 1):
        dy = (y - cy) / ry
        span = int(rx * math.sqrt(max(0.0, 1.0 - dy * dy)))
        for x in range(cx - span, cx + span + 1):
            px(x, y, color)


def ring(cx, cy, r, color, thick=2):
    for a in range(360):
        rad = math.radians(a)
        for t in range(thick):
            px(round(cx + (r + t) * math.cos(rad)),
               round(cy + (r + t) * math.sin(rad)), color)


# ---------------------------------------------------------------- wall
for y in range(H):
    c = lerp(WALL_TOP, WALL_BOTTOM, y / (H - 1))
    fill_rect(0, y, W, y + 1, c)

# faint wall speckles, like plaster
for n in range(900):
    x = (n * 7919) % W
    y = (n * 104729) % H
    px(x, y, lerp(get(x, y), WHITE, 0.05))

# ---------------------------------------------------------------- frame
FX0, FY0, FX1, FY1 = 70, 46, 830, 556
# outer gold band with a light top edge and a dark bottom edge
fill_rect(FX0, FY0, FX1, FY1, GOLD)
fill_rect(FX0 + 4, FY0 + 4, FX1 - 4, FY1 - 4, GOLD_DARK)
fill_rect(FX0 + 9, FY0 + 9, FX1 - 9, FY1 - 9, GOLD_LIGHT)
fill_rect(FX0 + 13, FY0 + 13, FX1 - 13, FY1 - 13, GOLD)
# carved corner rosettes
for cx, cy in ((FX0 + 24, FY0 + 24), (FX1 - 24, FY0 + 24),
               (FX0 + 24, FY1 - 24), (FX1 - 24, FY1 - 24)):
    disc(cx, cy, 9, GOLD_LIGHT)
    disc(cx, cy, 5, GOLD_DARK)
    disc(cx, cy, 2, GOLD_LIGHT)

# inner canvas: painted water
CX0, CY0, CX1, CY1 = FX0 + 26, FY0 + 26, FX1 - 26, FY1 - 26
for y in range(CY0, CY1):
    c = lerp(WATER_TOP, WATER_BOTTOM, (y - CY0) / (CY1 - CY0))
    fill_rect(CX0, y, CX1, y + 1, c)

# painted waves, flat brush strokes
for row in range(10):
    yb = CY0 + 28 + row * 44
    amp = 5 + (row % 3) * 2
    for x in range(CX0, CX1):
        yy = yb + int(amp * math.sin((x - CX0) / 46.0 + row))
        px(x, yy, lerp(WATER_TOP, WHITE, 0.28))
        px(x, yy + 1, lerp(WATER_TOP, WHITE, 0.16))

# lily pads, flat painted style
for cx, cy, rx in ((220, 420, 46), (660, 180, 54), (300, 150, 34)):
    ellipse(cx, cy, rx, int(rx * 0.42), LILY)
    ellipse(cx - 6, cy - 3, rx - 10, int(rx * 0.42) - 5, LILY_DARK)
    line(cx, cy, cx + rx, cy - 6, LILY_DARK)

# small painted koi still inside the painting, flat and calm
ellipse(620, 300, 52, 16, PAINTED_KOI)
ellipse(620, 300, 30, 12, WHITE)
for dx, dy in ((-52, 0), (-58, -8), (-58, 8)):
    line(620 + dx, 300 + dy, 596, 300 + dy * 2, PAINTED_KOI)
disc(668, 296, 4, INK)
disc(668, 296, 2, WHITE)

# painted koi number two, near the top left of the canvas
ellipse(210, 210, 34, 11, PAINTED_KOI)
line(176, 210, 158, 202, PAINTED_KOI)
line(176, 210, 158, 218, PAINTED_KOI)
disc(240, 207, 3, INK)

# ---------------------------------------------------------------- the break
# The golden koi leaps out: tail still in the painting, head already
# past the bottom edge of the frame, into the viewer's room.
def bezier(t, p0, p1, p2):
    u = 1 - t
    return (u * u * p0[0] + 2 * u * t * p1[0] + t * t * p2[0],
            u * u * p0[1] + 2 * u * t * p1[1] + t * t * p2[1])


TAIL = (640, 330)
CTRL = (560, 470)
HEAD = (360, 560)

# tail fin, fanned, behind the body
for ang, ln in ((-35, 46), (-10, 58), (15, 52), (38, 40)):
    rad = math.radians(ang)
    ex = TAIL[0] + int(ln * math.cos(rad))
    ey = TAIL[1] + int(ln * math.sin(rad))
    line(TAIL[0], TAIL[1], ex, ey, KOI_GOLD_DARK)
    line(TAIL[0], TAIL[1] + 2, ex, ey + 2, KOI_GOLD)

# body: overlapping discs along the spine, wide in the middle
spine = []
for s in range(121):
    t = s / 120.0
    x, y = bezier(t, TAIL, CTRL, HEAD)
    wdt = 14 + 44 * math.sin(math.pi * min(1.0, t * 1.15)) ** 0.8
    if t > 0.92:
        wdt *= 1.0 - (t - 0.92) * 6.0
    spine.append((x, y, max(6.0, wdt)))
    shade = lerp(KOI_GOLD_DARK, KOI_GOLD, 0.35 + 0.65 * (y / H))
    disc(int(x), int(y), int(wdt), shade)

# belly highlight along the lower edge of the spine
for s in range(20, 115, 2):
    t = s / 120.0
    x, y = bezier(t, TAIL, CTRL, HEAD)
    disc(int(x), int(y + spine[s][2] * 0.45), int(spine[s][2] * 0.42), KOI_BELLY)

# golden glow where the koi bursts through the frame
for gy in range(480, 600):
    for gx in range(280, 520):
        d = math.hypot(gx - 400, gy - 545)
        if d < 90:
            px(gx, gy, lerp(get(gx, gy), GOLD_LIGHT, 0.12 * (1 - d / 90)))

# scale arcs along the body, so the gold reads as fish scales
for s in range(10, 112, 6):
    t = s / 120.0
    x, y = bezier(t, TAIL, CTRL, HEAD)
    r = spine[s][2] * 0.55
    for a in range(200, 340, 12):
        rad = math.radians(a)
        px(int(x + r * math.cos(rad)), int(y + r * 0.6 * math.sin(rad)),
           KOI_GOLD_DARK)

# dorsal fin ridge
for s in range(15, 80, 3):
    t = s / 120.0
    x, y = bezier(t, TAIL, CTRL, HEAD)
    line(int(x), int(y - spine[s][2] * 0.9),
         int(x - 6), int(y - spine[s][2] * 1.35), KOI_GOLD_DARK)

# pectoral fins near the head
hx, hy = HEAD
line(int(hx + 18), int(hy - 6), int(hx + 52), int(hy + 22), KOI_GOLD_DARK)
line(int(hx + 18), int(hy - 4), int(hx + 50), int(hy + 20), KOI_GOLD)
line(int(hx + 10), int(hy + 10), int(hx + 38), int(hy + 44), KOI_GOLD_DARK)
line(int(hx + 10), int(hy + 8), int(hx + 36), int(hy + 42), KOI_GOLD)

# head: eye, whiskers, mouth
disc(int(hx - 6), int(hy - 12), 9, WHITE)
disc(int(hx - 6), int(hy - 12), 5, INK)
disc(int(hx - 7), int(hy - 14), 2, WHITE)
ring(int(hx - 6), int(hy - 12), 10, GOLD_DARK)
for k in range(3):
    line(int(hx - 22), int(hy + 2 + k * 4),
         int(hx - 52 - k * 8), int(hy + 14 + k * 10), KOI_GOLD_DARK)
line(int(hx - 24), int(hy + 8), int(hx - 30), int(hy + 16), INK)

# ---------------------------------------------------------------- knitted texture
# Cross-stitches laid over the gold body, like yarn.
for gx in range(300, 700, 10):
    for gy in range(300, 590, 10):
        r, g, b = get(gx, gy)
        if r > 170 and 110 < g < 215 and b < 130:
            c = KOI_STITCH
            px(gx - 2, gy - 2, c)
            px(gx - 1, gy - 1, c)
            px(gx, gy, c)
            px(gx + 1, gy + 1, c)
            px(gx + 2, gy + 2, c)
            px(gx + 2, gy - 2, c)
            px(gx + 1, gy - 1, c)
            px(gx - 1, gy + 1, c)
            px(gx - 2, gy + 2, c)

# ---------------------------------------------------------------- cracks and splash
# cracks radiating from where the koi smashed through the bottom frame
BX, BY = 400, 540
for ang, ln in ((200, 34), (235, 44), (265, 30), (295, 40), (320, 28)):
    rad = math.radians(ang)
    line(BX, BY, BX + int(ln * math.cos(rad)), BY + int(ln * math.sin(rad)), INK)
    line(BX, BY, BX + int(ln * 0.7 * math.cos(rad)),
         BY + int(ln * 0.7 * math.sin(rad)), GOLD_LIGHT)

# gold shards flying off the broken frame
for sx, sy, sdx, sdy in ((372, 548, -18, 14), (428, 552, 16, 18),
                         (352, 540, -26, 4), (448, 544, 24, 8)):
    disc(sx, sy, 4, GOLD)
    line(sx, sy, sx + sdx, sy + sdy, GOLD_LIGHT)

# splash droplets around the breach
for dx, dy, r in ((360, 500, 5), (430, 512, 4), (330, 528, 3),
                  (470, 520, 5), (300, 560, 4), (500, 548, 3),
                  (390, 492, 3), (455, 490, 4), (345, 585, 3),
                  (520, 575, 4)):
    disc(dx, dy, r, SPLASH)
    disc(dx - 1, dy - 1, max(1, r - 2), WHITE)

# ---------------------------------------------------------------- plaque
fill_rect(640, 566, 800, 592, GOLD_DARK)
fill_rect(644, 570, 796, 588, GOLD)
hline(652, 788, 576, GOLD_DARK)
hline(652, 760, 581, GOLD_DARK)
hline(652, 740, 585, GOLD_DARK)

# ---------------------------------------------------------------- vignette
for y in range(H):
    for x in range(0, 40):
        f = x / 40.0
        px(x, y, lerp(INK, get(x, y), f))
        px(W - 1 - x, y, lerp(INK, get(W - 1 - x, y), f))


# ---------------------------------------------------------------- png write
def write_png(path):
    raw = bytearray()
    for y in range(H):
        raw.append(0)
        raw += buf[y * W * 3:(y + 1) * W * 3]
    comp = zlib.compress(bytes(raw), 9)

    def chunk(kind, data):
        c = struct.pack(">I", len(data)) + kind + data
        return c + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n"
    png += chunk(b"IHDR", ihdr)
    png += chunk(b"IDAT", comp)
    png += chunk(b"IEND", b"")
    with open(path, "wb") as fh:
        fh.write(png)


if __name__ == "__main__":
    write_png("entry.png")
    print("wrote entry.png", W, "x", H)
