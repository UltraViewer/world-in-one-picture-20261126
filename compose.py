#!/usr/bin/env python3
"""Render the 26 November 2026 front page: 'The World in One Picture'.

A single-file PIL drawing. Everything is drawn with vector shapes and
Liberation fonts; no photos, no network, no randomness outside a fixed
seed, so repeated runs produce byte-identical PNG output.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 241, 227)
INK = (26, 26, 26)
RED = (178, 34, 34)
GRAY = (110, 105, 92)
RULE = (40, 40, 40)
FONT_DIR = "/usr/share/fonts/truetype/liberation/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: font("LiberationSerif-Regular.ttf", s)
SANS_B = lambda s: font("LiberationSans-Bold.ttf", s)
SANS = lambda s: font("LiberationSans-Regular.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, color=INK):
    """Draw wrapped text, return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += leading
    return y


def star(d, cx, cy, r_out, r_in, points, color):
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color)


def night_panel(d, x, y, w, h):
    """Kuwait night scene: dark sky, moon, radar tower, blast, drones."""
    for i in range(h):
        t = i / h
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(26 + (13 - 26) * t), int(42 + (21 - 42) * t),
                     int(68 + (38 - 68) * t)))
    rng = random.Random(26)
    for _ in range(46):
        sx, sy = x + rng.randint(4, w - 4), y + rng.randint(4, h - 90)
        r = rng.choice([1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=(235, 235, 220) if rng.random() < 0.7 else (180, 180, 170))
    # Moon with craters, upper right.
    mx, my, mr = x + w - 62, y + 52, 26
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(232, 224, 200))
    d.ellipse([mx - 12, my - 6, mx + 2, my + 8], fill=(205, 196, 168))
    d.ellipse([mx + 6, my + 8, mx + 16, my + 18], fill=(210, 202, 176))
    # Ground strip with a dashed road line.
    gy = y + h - 34
    d.rectangle([x, gy, x + w, y + h], fill=(10, 15, 28))
    for dx in range(x + 8, x + w - 8, 26):
        d.line([(dx, gy + 17), (dx + 13, gy + 17)], fill=(90, 100, 120), width=2)
    # Radar tower silhouette, left third.
    d.polygon([(x + 62, gy), (x + 78, y + 118), (x + 104, y + 118),
               (x + 120, gy)], fill=(8, 10, 18))
    d.rectangle([x + 70, y + 112, x + 112, y + 120], fill=(8, 10, 18))
    # Radar dish arcs above the tower.
    d.arc([x + 52, y + 62, x + 130, y + 140], start=200, end=340,
          fill=(200, 200, 190), width=3)
    d.arc([x + 66, y + 76, x + 116, y + 126], start=200, end=340,
          fill=(200, 200, 190), width=2)
    # Blast starburst at the dish.
    star(d, x + 92, y + 96, 44, 18, 8, (245, 166, 35))
    star(d, x + 92, y + 96, 26, 11, 8, (255, 220, 90))
    d.ellipse([x + 80, y + 84, x + 104, y + 108], fill=(255, 240, 170))
    # Two small drones with red navigation lights.
    for dx, dy in ((x + 268, y + 96), (x + 330, y + 150)):
        d.rounded_rectangle([dx - 26, dy - 4, dx + 26, dy + 4], radius=4,
                            fill=(210, 210, 200))
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(220, 40, 40))
    # Second, smaller tower silhouette on the right.
    d.polygon([(x + 398, gy), (x + 408, y + 168), (x + 428, y + 168),
               (x + 438, gy)], fill=(8, 10, 18))
    d.ellipse([x + 402, y + 156, x + 434, y + 178], fill=(8, 10, 18))


def city_panel(d, x, y, w, h):
    """Gaza dusk: orange sky, dark building silhouettes, smoke."""
    for i in range(h):
        t = i / h
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(198 + (122 - 198) * t), int(138 + (74 - 138) * t),
                     int(61 + (30 - 61) * t)))
    rng = random.Random(7)
    # Low sun disc behind the skyline.
    d.ellipse([x + w - 96, y + 18, x + w - 36, y + 78], fill=(240, 200, 120))
    heights = [62, 88, 54, 96, 70, 84, 58, 92]
    bw = w // len(heights)
    for i, bh in enumerate(heights):
        bx = x + i * bw
        d.rectangle([bx, y + h - bh, bx + bw - 3, y + h], fill=(46, 26, 14))
        d.polygon([(bx, y + h - bh), (bx + (bw - 3) // 2, y + h - bh - 14),
                   (bx + bw - 3, y + h - bh)], fill=(46, 26, 14))
    for _ in range(7):
        sx, sy = x + rng.randint(20, w - 20), y + rng.randint(2, 26)
        r = rng.randint(9, 16)
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(120, 105, 88))


def virus_panel(d, x, y, w, h):
    """Ebola panel: deep red field with a stylised virus glyph."""
    d.rectangle([x, y, x + w, y + h], fill=(122, 22, 32))
    cx, cy = x + 96, y + h // 2
    for k in range(12):
        a = math.pi * 2 * k / 12
        ex, ey = cx + 44 * math.cos(a), cy + 44 * math.sin(a)
        d.line([(cx + 26 * math.cos(a), cy + 26 * math.sin(a)), (ex, ey)],
               fill=(205, 90, 90), width=4)
        d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=(225, 130, 120))
    d.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(196, 70, 70))
    d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(225, 120, 110))
    for k in range(5):
        a = math.pi * 2 * k / 5 + 0.6
        d.ellipse([cx + 40 * math.cos(a) - 4, cy + 40 * math.sin(a) - 4,
                   cx + 40 * math.cos(a) + 4, cy + 40 * math.sin(a) + 4],
                  fill=(215, 110, 100))


def eu_flag(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(0, 51, 153))
    cx, cy, r = x + s / 2, y + s / 2, s * 0.32
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        star(d, cx + r * math.cos(a), cy + r * math.sin(a), 5, 2, 5,
             (255, 204, 0))


def balloons(d, x, y, w, h):
    """Macy's thumbnail: grey sky, one red and one blue balloon."""
    for i in range(h):
        t = i / h
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(120 + (70 - 120) * t), int(128 + (80 - 128) * t),
                     int(140 + (95 - 140) * t)))
    d.ellipse([x + 6, y + 8, x + 52, y + h - 8], fill=(200, 60, 60))
    d.line([(x + 14, y + 12), (x + 44, y + h - 12)], fill=(120, 20, 20),
           width=3)
    d.line([(x + 44, y + 12), (x + 14, y + h - 12)], fill=(120, 20, 20),
           width=3)
    d.ellipse([x + w - 52, y + 10, x + w - 8, y + h - 10], fill=(50, 110, 200))
    d.line([(x + w - 44, y + 14), (x + w - 16, y + h - 14)],
           fill=(20, 60, 140), width=3)


def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)
    mx = 28  # side margin

    # Masthead.
    title = "The World in One Picture"
    f_title = SERIF_B(62)
    d.text(((W - d.textlength(title, font=f_title)) / 2, 18), title,
           font=f_title, fill=INK)
    d.line([(mx, 100), (W - mx, 100)], fill=RULE, width=3)
    d.line([(mx, 106), (W - mx, 106)], fill=RULE, width=1)

    # Dateline row.
    f_date = SANS_B(24)
    d.text((mx, 116), "THURSDAY 26 NOVEMBER 2026", font=f_date, fill=RED)
    tag = "THE DAY'S WORLD NEWS, IN ONE IMAGE"
    f_tag = SANS(19)
    d.text((W - mx - d.textlength(tag, font=f_tag), 119), tag,
           font=f_tag, fill=GRAY)

    # Hero: night panel left, headline block right.
    hx, hy, hw, hh = mx, 146, 490, 284
    night_panel(d, hx, hy, hw, hh)
    tx = hx + hw + 18
    tw = W - mx - tx
    d.text((tx, hy + 2), "THE GULF", font=SANS_B(25), fill=RED)
    y = hy + 34
    for line in ("DRONES OVER", "KUWAIT"):
        d.text((tx, y), line, font=SERIF_B(58), fill=INK)
        y += 62
    y = para(d, tx, y + 8,
             "Two Italians killed as drones hit a Kuwait air-defence site",
             SERIF_B(27), tw, 32)
    para(d, tx, y + 6,
         "Two Rheinmetall Italia technicians, 36 and 65, were servicing "
         "Skyguard radar when the site was hit. Two more wounded; Tehran "
         "denies any role.",
         SERIF(21), tw, 26)
    d.text((hx, hy + hh + 8),
           "An Iranian drone attack on a Kuwait air-defence site, Thursday.",
           font=SERIF(17), fill=GRAY)

    d.line([(mx, 470), (W - mx, 470)], fill=RULE, width=1)

    # Middle panels.
    py, ph = 482, 114
    city_panel(d, mx, py, 480, ph)
    virus_panel(d, mx + 488, py, 480, ph)

    # Middle headlines and bodies, two columns.
    col_w = 480
    y = 606
    for line in ("ISRAEL KILLS HAMAS", "MINISTER IN GAZA STRIKES"):
        d.text((mx, y), line, font=SERIF_B(30), fill=INK)
        y += 34
    para(d, mx, 678,
         "At least 9 killed overnight, including deputy education minister "
         "Khaled Abu Nada and his wife in Deir al-Balah — a third straight "
         "night of strikes despite a year-old ceasefire.",
         SERIF(20), col_w, 24)
    y = 606
    for line in ("EBOLA PASSES 12,000 CASES", "IN CONGO"):
        d.text((mx + 488, y), line, font=SERIF_B(30), fill=INK)
        y += 34
    para(d, mx + 488, 678,
         "12,021 confirmed cases in the east, and nearly half of them have "
         "died — the fastest-growing Ebola outbreak in history, the health "
         "ministry says. No approved vaccine for this strain.",
         SERIF(20), col_w, 24)

    d.line([(mx, 812), (W - mx, 812)], fill=RULE, width=1)

    # EU row.
    eu_flag(d, mx, 824, 64)
    d.text((mx + 80, 824), "EU DEADLOCKED ON €1.58 TRILLION BUDGET",
           font=SERIF_B(30), fill=INK)
    para(d, mx + 80, 860,
         "Leaders fail to agree after 12 hours in Brussels; no deal on "
         "Thursday. Next try: 17–18 December. A $49bn loan for Ukraine is "
         "stuck too.",
         SERIF(20), W - mx - (mx + 80), 24)

    d.line([(mx, 906), (W - mx, 906)], fill=RULE, width=1)

    # Macy's row.
    balloons(d, mx, 914, 64, 58)
    d.text((mx + 80, 914), "NO PARADE ON THANKSGIVING",
           font=SERIF_B(30), fill=INK)
    para(d, mx + 80, 948,
         "The 100th Macy's parade is postponed for the first time ever — a "
         "nor'easter gusting to 60 mph moves it to Saturday 28 November.",
         SERIF(20), W - mx - (mx + 80), 23)

    d.line([(mx, 996), (W - mx, 996)], fill=RULE, width=1)
    d.text((mx, 1004),
           "ALSO: Houthis claim strikes on Jeddah and Jazan · Serbia votes "
           "27 Dec · Russia OKs record military budget",
           font=SANS(16), fill=GRAY)
    return img


if __name__ == "__main__":
    page = build()
    page.save("entry.png", format="PNG")
    print("wrote entry.png", page.size)
