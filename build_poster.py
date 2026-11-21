#!/usr/bin/env python3
"""Render the 21 November 2026 one-image world-news poster.

Running this file writes ``entry.png`` (1024 x 1024) next to the script.
It uses Pillow and the system DejaVu fonts only. Everything is fixed at
authoring time -- no network, no clock, no randomness that is not seeded
-- so a re-run reproduces the same PNG byte for byte.

Layout, top to bottom: a broadsheet masthead naming the day; a lead
panel on Russia's overnight barrage and the missiles that landed in
Poland, with a drawn map graphic; two feature panels (the AI stock
rout, the ICJ genocide ruling); three story cards (COP31 overtime,
the Riyadh intercepts, the UK-EU deals); a markets ticker; an
also-today strip; and a sources footer. A fine paper grain is drawn
over the whole sheet so the image stays dense at full size.
"""

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")

W, H = 1024, 1024

# Palette: deep navy broadsheet, signal red, warm paper, gold accent.
NAVY = (13, 34, 56)
NAVY_DARK = (8, 22, 38)
NAVY_MID = (21, 52, 80)
TEAL = (16, 66, 84)
PAPER = (247, 242, 232)
CARD = (255, 253, 247)
CARD_BLUE = (232, 240, 246)
RED = (186, 48, 38)
RED_DARK = (140, 32, 26)
GOLD = (214, 158, 46)
WHITE = (255, 255, 255)
INK = (22, 28, 36)
MUTED = (92, 97, 106)
RULE = (205, 196, 180)
SKY = (158, 196, 224)
LAND = (74, 110, 138)


def load_font(name, size):
    return ImageFont.truetype(str(FONT_DIR / name), size)


SERIF_B = lambda s: load_font("DejaVuSerif-Bold.ttf", s)  # noqa: E731
SANS = lambda s: load_font("DejaVuSans.ttf", s)  # noqa: E731
SANS_B = lambda s: load_font("DejaVuSans-Bold.ttf", s)  # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, xy, text, fnt, max_w, fill, leading=None):
    """Draw wrapped paragraph, return y just below the last line."""
    x, y = xy
    leading = leading or int(fnt.size * 1.28)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, xy, text, fnt, max_w, fill, leading=None):
    return para(draw, xy, text, fnt, max_w, fill, leading)


def kicker(draw, xy, text, fill=RED):
    draw.text(xy, text.upper(), font=SANS_B(15), fill=fill)


def rule(draw, x0, y, x1, fill=RULE, width=2):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def grain(img, seed=210621):
    """Deterministic fine paper grain: lifts PNG density, keeps text clean."""
    rnd = random.Random(seed)
    px = img.load()
    for _ in range(52000):
        x = rnd.randrange(W)
        y = rnd.randrange(H)
        r, g, b = px[x, y]
        d = rnd.randint(-14, 14)
        px[x, y] = (
            max(0, min(255, r + d)),
            max(0, min(255, g + d)),
            max(0, min(255, b + d)),
        )


def draw_map(draw, box):
    """Stylised night map of Europe: land blobs, sea grid, missile arcs."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=NAVY_DARK, outline=NAVY_MID, width=2)
    # Sea grid of dots.
    for gx in range(x0 + 14, x1 - 8, 18):
        for gy in range(y0 + 14, y1 - 8, 18):
            draw.ellipse([gx, gy, gx + 2, gy + 2], fill=(38, 74, 104))
    # Land masses as rounded blobs (abstract Europe).
    blobs = [
        (x0 + 18, y0 + 26, x0 + 150, y0 + 96),
        (x0 + 120, y0 + 66, x0 + 250, y0 + 150),
        (x0 + 210, y0 + 20, x0 + 330, y0 + 88),
        (x0 + 60, y0 + 130, x0 + 190, y0 + 196),
        (x0 + 235, y0 + 120, x0 + 335, y0 + 190),
    ]
    for b in blobs:
        draw.rounded_rectangle(b, radius=26, fill=LAND, outline=(96, 138, 168), width=2)
    # Missile arcs from the east, converging on Kyiv and Warsaw.
    kyiv = (x0 + 262, y0 + 118)
    warsaw = (x0 + 168, y0 + 82)
    for start, end, col in [
        ((x1 - 6, y0 + 30), kyiv, RED),
        ((x1 - 6, y0 + 70), kyiv, (232, 120, 60)),
        ((x1 - 6, y0 + 110), warsaw, RED),
        ((x1 - 6, y0 + 150), kyiv, (232, 120, 60)),
    ]:
        mx = (start[0] + end[0]) // 2
        my = min(start[1], end[1]) - 34
        pts = []
        for t in range(21):
            u = t / 20
            px = (1 - u) ** 2 * start[0] + 2 * (1 - u) * u * mx + u * u * end[0]
            py = (1 - u) ** 2 * start[1] + 2 * (1 - u) * u * my + u * u * end[1]
            pts.append((px, py))
        draw.line(pts, fill=col, width=3)
        draw.ellipse([start[0] - 4, start[1] - 4, start[0] + 4, start[1] + 4], fill=col)
    # Impact bursts.
    for cx, cy, r in [(kyiv[0], kyiv[1], 16), (warsaw[0], warsaw[1], 12)]:
        for k in range(8):
            ang = k * math.pi / 4
            draw.line(
                [(cx, cy), (cx + r * math.cos(ang), cy + r * math.sin(ang))],
                fill=GOLD, width=3,
            )
        draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED, outline=GOLD, width=2)
    draw.text((kyiv[0] - 18, kyiv[1] + 22), "KYIV", font=SANS_B(14), fill=WHITE)
    draw.text((warsaw[0] - 78, warsaw[1] - 12), "WARSAW", font=SANS_B(14), fill=WHITE)
    draw.text((x0 + 12, y0 + 8), "UKRAINE  •  POLAND  •  OVERNIGHT", font=SANS_B(13), fill=SKY)


def draw_chart(draw, box):
    """Falling market line chart: steep red descent, shaded area below."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD_BLUE, outline=RULE, width=2)
    vals = [0.92, 0.88, 0.90, 0.78, 0.68, 0.58, 0.48, 0.38, 0.30, 0.18]
    pts = []
    for i, v in enumerate(vals):
        px = x0 + 16 + i * (x1 - x0 - 32) // (len(vals) - 1)
        py = y1 - 22 - int(v * (y1 - y0 - 48))
        pts.append((px, py))
    area = pts + [(pts[-1][0], y1 - 22), (pts[0][0], y1 - 22)]
    draw.polygon(area, fill=(232, 190, 182))
    draw.line(pts, fill=RED, width=4, joint="curve")
    for px, py in pts:
        draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED_DARK)
    draw.line([(x0 + 10, y1 - 22), (x1 - 10, y1 - 22)], fill=INK, width=2)
    draw.text((x0 + 12, y0 + 6), "S&P 500  −3.7%  •  NASDAQ  −5.3%", font=SANS_B(14), fill=RED_DARK)


def draw_scales(draw, box):
    """Compact scales of justice, sized to fit its panel exactly."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=TEAL, outline=RULE, width=2)
    cx = (x0 + x1) // 2
    top = y0 + 16
    arm = 44
    draw.line([(cx, top), (cx, y1 - 26)], fill=GOLD, width=4)
    draw.line([(cx - arm, top + 10), (cx + arm, top + 10)], fill=GOLD, width=4)
    draw.ellipse([cx - 6, top - 4, cx + 6, top + 8], fill=GOLD)
    for sx in (cx - arm, cx + arm):
        draw.line([(sx, top + 10), (sx, top + 40)], fill=GOLD, width=2)
        draw.arc([sx - 18, top + 34, sx + 18, top + 62], 0, 180, fill=GOLD, width=3)
        draw.line([(sx - 18, top + 48), (sx + 18, top + 48)], fill=GOLD, width=2)
    draw.rectangle([cx - 34, y1 - 28, cx + 34, y1 - 20], fill=GOLD)
    draw.text((x0 + 10, y0 + 4), "THE HAGUE", font=SANS_B(12), fill=(190, 220, 232))


def card(draw, box, kick, head, body, head_size=30):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD, outline=RULE, width=2)
    draw.rectangle([x0, y0, x1, y0 + 6], fill=RED)
    kicker(draw, (x0 + 16, y0 + 18), kick)
    y = headline(draw, (x0 + 16, y0 + 44), head, SANS_B(head_size), x1 - x0 - 32, INK)
    para(draw, (x0 + 16, y + 4), body, SANS(16), x1 - x0 - 32, (52, 58, 66))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 112, W, 118], fill=GOLD)
    d.text((28, 12), "THE WORLD IN ONE IMAGE", font=SERIF_B(30), fill=WHITE)
    d.text((28, 50), "SATURDAY  21  NOVEMBER  2026", font=SANS_B(40), fill=GOLD)
    d.text((W - 28 - d.textlength("ONE DAY  •  ONE IMAGE  •  WORLD NEWS", font=SANS_B(15)),
            22), "ONE DAY  •  ONE IMAGE  •  WORLD NEWS", font=SANS_B(15), fill=SKY)
    d.text((W - 28 - d.textlength("SATURDAY EDITION", font=SANS(15)),
            52), "SATURDAY EDITION", font=SANS(15), fill=(200, 214, 228))

    # ---- Lead panel ----
    d.rectangle([16, 132, 1008, 436], fill=CARD, outline=RULE, width=2)
    d.rectangle([16, 132, 1008, 140], fill=RED)
    kicker(d, (32, 150), "LEAD  •  WAR IN EUROPE")
    headline(d, (32, 176), "MISSILES FALL\nON POLAND", SERIF_B(54), 560, INK, leading=58)
    y = para(d, (32, 296), "Russia fired 400+ drones and 110 missiles at "
             "Ukraine overnight — its biggest barrage this year. At "
             "least 8 people were killed in Kyiv as bridges and power "
             "lines were hit.", SANS(18), 540, (44, 50, 58))
    para(d, (32, y + 6), "Two missiles and a suspected drone came down in "
           "Poland. Warsaw calls it a deliberate provocation.",
           SANS_B(18), 540, RED_DARK)
    draw_map(d, (600, 152, 992, 420))

    # ---- Two features ----
    # Markets feature
    d.rectangle([16, 450, 500, 670], fill=CARD, outline=RULE, width=2)
    d.rectangle([16, 450, 500, 456], fill=RED)
    kicker(d, (32, 466), "MARKETS  •  NEW YORK")
    headline(d, (32, 490), "AI ROUT: S&P IN\nCORRECTION", SANS_B(30), 452, INK, leading=33)
    draw_chart(d, (32, 562, 484, 658))
    # ICJ feature
    d.rectangle([516, 450, 1008, 670], fill=CARD, outline=RULE, width=2)
    d.rectangle([516, 450, 1008, 456], fill=RED)
    kicker(d, (532, 466), "JUSTICE  •  THE HAGUE")
    headline(d, (532, 490), "MYANMAR GUILTY\nOF GENOCIDE", SANS_B(30), 456, INK, leading=33)
    para(d, (532, 566), "The world court rules Myanmar committed "
           "genocide against the Rohingya — the first time it has "
           "held a state responsible.", SANS(17), 296, (52, 58, 66))
    draw_scales(d, (852, 566, 992, 658))

    # ---- Three story cards ----
    card(d, (16, 684, 336, 858), "CLIMATE  •  ANTALYA",
         "COP31 RUNS INTO OVERTIME",
         "Talks in Turkey run past deadline as ~200 nations stay "
         "deadlocked over fossil fuels.", head_size=25)
    card(d, (352, 684, 672, 858), "MIDDLE EAST  •  RIYADH",
         "MISSILES AT RIYADH STOPPED",
         "Saudi-led coalition intercepts three Houthi missiles aimed "
         "at the capital — the third night running.", head_size=25)
    card(d, (688, 684, 1008, 858), "EUROPE  •  BRUSSELS",
         "UK–EU'S BIGGEST STEP SINCE BREXIT",
         "Three deals signed: food trade, carbon markets and youth "
         "mobility for 100,000 young Britons.", head_size=25)

    # ---- Also today strip ----
    d.rectangle([16, 872, 1008, 962], fill=NAVY_MID, outline=NAVY_DARK, width=2)
    d.text((32, 880), "ALSO TODAY", font=SANS_B(17), fill=GOLD)
    also = [
        "WASHINGTON — Trump defends calling Putin “my friend” after the Shenzhen summit with Xi.",
        "TECH — FBI criminal database hacked, CNN reports, amid continuing US outages.",
        "SCIENCE — Pancreatic-cancer pill trial: tumours undetectable in 1 in 12 patients.",
        "PERU — 6.9 quake shakes the Andes.  •  BASRA — Power-plant fire kills at least 4.",
    ]
    yy = 906
    for line in also:
        d.text((32, yy), "•  " + line, font=SANS(14), fill=(228, 236, 244))
        yy += 14
    # ---- Footer ----
    d.text((16, 972), "Sources: Reuters, AP, BBC, Al Jazeera, France 24, The Guardian, FT — "
           "21 November 2026", font=SANS(14), fill=MUTED)
    d.text((16, 992), "S&P 500 6,910.39  −3.7%   •   Nasdaq −5.3%   •   Nvidia −14% on report "
           "of SEC probe   •   Bitcoin toward $62,000",
           font=SANS_B(14), fill=RED_DARK)

    grain(img)
    out = HERE / "entry.png"
    img.save(out, format="PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
