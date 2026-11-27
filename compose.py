#!/usr/bin/env python3
"""Draw the 26 November 2026 world-news front page, 'The World in One Picture'.

Every fact on the page was verified against Reuters / AP / BBC / DW reporting
of Thursday 26 November 2026 before drawing. No figure is invented: captions
carry only numbers that appear in those reports. The picture is drawn with PIL
primitives only -- no photos, no network, no randomness -- so two runs produce
identical bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (17, 17, 17)
RED = (163, 22, 33)
NAVY = (27, 42, 74)
GREY = (90, 88, 80)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, f, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, text, f, x, y, width, leading, color=INK):
    for line in wrap(d, text, f, width):
        d.text((x, y), line, font=f, fill=color)
        y += leading
    return y


def rule(d, x0, y, x1, width=2, color=INK):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


def gradient(d, box, top, bottom):
    x0, y0, x1, y1 = box
    n = y1 - y0
    for i in range(n):
        t = i / max(1, n - 1)
        c = tuple(int(top[k] + (bottom[k] - top[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def hero_panel(d, box):
    """Night over the Gulf: radar station, drones, one blast. Pure drawing."""
    x0, y0, x1, y1 = box
    gradient(d, box, (13, 27, 46), (39, 65, 86))
    # stars, fixed positions
    for sx, sy, r in [(60, 30, 2), (150, 55, 1), (240, 25, 2), (330, 60, 1),
                      (420, 35, 2), (490, 70, 1), (110, 90, 1), (290, 95, 2),
                      (450, 110, 1), (200, 120, 1)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(220, 225, 235))
    # moon
    d.ellipse([x1 - 90, y0 + 22, x1 - 40, y0 + 72], fill=(232, 228, 205))
    d.ellipse([x1 - 82, y0 + 30, x1 - 58, y0 + 54], fill=(205, 200, 175))
    # sea horizon
    d.rectangle([x0, y1 - 78, x1, y1], fill=(16, 28, 40))
    d.line([(x0, y1 - 78), (x1, y1 - 78)], fill=(120, 140, 165), width=2)
    for gx in range(x0 + 20, x1 - 10, 46):
        d.line([(gx, y1 - 72), (gx + 26, y1 - 72)], fill=(70, 90, 115), width=1)
    # radar tower silhouette
    tx = x0 + 130
    d.polygon([(tx - 16, y1 - 78), (tx + 16, y1 - 78), (tx + 7, y1 - 200),
               (tx - 7, y1 - 200)], fill=(8, 12, 18))
    d.rectangle([tx - 34, y1 - 216, tx + 34, y1 - 200], fill=(8, 12, 18))
    # radar dish
    d.arc([tx - 58, y1 - 268, tx + 58, y1 - 176], start=200, end=340,
          fill=(200, 205, 215), width=5)
    d.line([(tx, y1 - 216), (tx - 46, y1 - 258)], fill=(200, 205, 215), width=4)
    d.line([(tx, y1 - 216), (tx + 46, y1 - 258)], fill=(200, 205, 215), width=4)
    # second, smaller tower
    tx2 = x0 + 400
    d.polygon([(tx2 - 10, y1 - 78), (tx2 + 10, y1 - 78), (tx2 + 4, y1 - 150),
               (tx2 - 4, y1 - 150)], fill=(8, 12, 18))
    d.ellipse([tx2 - 16, y1 - 172, tx2 + 16, y1 - 140], fill=(8, 12, 18))
    # drones: small quadcopters with red lights
    for dx, dy in [(x0 + 300, y0 + 60), (x0 + 360, y0 + 105)]:
        d.ellipse([dx - 9, dy - 5, dx + 9, dy + 5], fill=(30, 34, 40))
        d.line([(dx - 20, dy - 8), (dx + 20, dy - 8)], fill=(160, 165, 175), width=3)
        d.line([(dx - 20, dy + 8), (dx + 20, dy + 8)], fill=(160, 165, 175), width=3)
        d.ellipse([dx - 2, dy - 2, dx + 2, dy + 2], fill=(255, 60, 50))
    # explosion burst at the dish
    bx, by = tx + 30, y1 - 240
    for r, col in [(46, (255, 122, 26)), (32, (255, 176, 32)),
                   (18, (255, 232, 150))]:
        pts = []
        for k in range(16):
            ang = 3.14159 * k / 8
            rr = r if k % 2 == 0 else r * 0.55
            pts.append((bx + rr * 1.0 * __import__("math").cos(ang),
                        by + rr * 1.0 * __import__("math").sin(ang)))
        d.polygon(pts, fill=col)


def gaza_panel(d, box):
    """Dusk skyline, damaged buildings, smoke. Pure drawing."""
    x0, y0, x1, y1 = box
    gradient(d, box, (122, 74, 52), (196, 138, 84))
    d.ellipse([x1 - 70, y0 + 12, x1 - 26, y0 + 56], fill=(238, 200, 140))
    for bx, bw, bh in [(0, 70, 46), (78, 52, 66), (138, 84, 38),
                       (230, 60, 58), (298, 74, 42), (380, 56, 62)]:
        d.rectangle([x0 + bx, y1 - bh, x0 + bx + bw, y1], fill=(52, 34, 28))
        d.polygon([(x0 + bx, y1 - bh), (x0 + bx + bw // 2, y1 - bh - 12),
                   (x0 + bx + bw, y1 - bh)], fill=(52, 34, 28))
    for sx, sy, r in [(150, 18, 14), (168, 4, 18), (300, 22, 12), (316, 8, 15)]:
        d.ellipse([x0 + sx - r, y0 + sy - r, x0 + sx + r, y0 + sy + r],
                  fill=(120, 105, 95))


def ebola_panel(d, box):
    """Abstract virus motif on deep red. No numbers drawn here."""
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(104, 16, 22))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for k in range(12):
        ang = 3.14159 * k / 6
        ex = cx + 34 * __import__("math").cos(ang)
        ey = cy + 34 * __import__("math").sin(ang)
        d.line([(cx, cy), (ex, ey)], fill=(214, 90, 80), width=4)
        d.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=(232, 140, 125))
    d.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(168, 40, 44))
    d.ellipse([cx - 14, cy - 14, cx + 14, cy + 14], fill=(214, 90, 80))
    for dx, dy, r in [(-58, -16, 4), (62, 14, 5), (-40, 22, 3), (44, -22, 4)]:
        d.ellipse([cx + dx - r, cy + dy - r, cx + dx + r, cy + dy + r],
                  fill=(232, 140, 125))


def eu_stars(d, cx, cy, r):
    d.rectangle([cx - 42, cy - 42, cx + 42, cy + 42], fill=(0, 51, 153))
    for k in range(12):
        ang = -3.14159 / 2 + 3.14159 * k / 6
        sx = cx + int(r * __import__("math").cos(ang))
        sy = cy + int(r * __import__("math").sin(ang))
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 204, 0))


def macys_panel(d, box):
    """Storm clouds and two grounded balloons. Pure drawing."""
    x0, y0, x1, y1 = box
    gradient(d, box, (70, 78, 92), (140, 148, 160))
    for cx, cy, r in [(50, 22, 26), (90, 14, 30), (130, 26, 22), (200, 18, 28)]:
        d.ellipse([x0 + cx - r, y0 + cy - r // 2, x0 + cx + r, y0 + cy + r // 2],
                  fill=(88, 96, 110))
    # deflated balloon on the ground, tilted
    d.ellipse([x0 + 30, y1 - 46, x0 + 120, y1 - 6], fill=(200, 60, 70))
    d.line([(x0 + 55, y1 - 40), (x0 + 95, y1 - 12)], fill=(120, 30, 40), width=3)
    d.line([(x0 + 95, y1 - 40), (x0 + 55, y1 - 12)], fill=(120, 30, 40), width=3)
    d.ellipse([x0 + 165, y1 - 40, x0 + 225, y1 - 8], fill=(60, 110, 200))
    d.line([(x0 + 180, y1 - 36), (x0 + 210, y1 - 12)], fill=(30, 60, 120), width=3)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28
    X1 = W - M

    # ---- masthead ----
    f_mast = font(SERIF_B, 62)
    title = "The World in One Picture"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 18), title, font=f_mast, fill=INK)
    rule(d, M, 96, X1, 3)
    rule(d, M, 102, X1, 1)
    f_date = font(SANS_B, 22)
    d.text((M, 114), "THURSDAY 26 NOVEMBER 2026", font=f_date, fill=RED)
    f_tag = font(SANS, 19)
    tag = "THE DAY'S WORLD NEWS, IN ONE IMAGE"
    d.text((X1 - d.textlength(tag, font=f_tag), 116), tag, font=f_tag, fill=GREY)

    # ---- hero: panel left, headline right ----
    hy = 150
    hero_panel(d, (M, hy, 528, hy + 302))
    d.text((M, hy + 308), "An Iranian drone attack on a Kuwait air-defence site, Thursday.",
           font=font(SANS, 16), fill=GREY)
    hx = 552
    d.text((hx, hy + 2), "THE GULF", font=font(SANS_B, 22), fill=RED)
    y = para(d, "DRONES OVER KUWAIT", font(SERIF_B, 48), hx, hy + 30, X1 - hx,
             52)
    y = para(d, "Two Italians killed as drones hit a Kuwait air-defence site",
             font(SERIF_B, 25), hx, y + 8, X1 - hx, 31)
    y = para(d, "Two Rheinmetall Italia technicians, 36 and 65, were servicing "
                "Skyguard radar when the site was hit. Two more wounded; "
                "Tehran denies any role.",
             font(SERIF, 19), hx, y + 10, X1 - hx, 24)
    rule(d, M, 508, X1, 2)

    # ---- middle row: Gaza | Ebola ----
    my = 522
    col_w = (X1 - M - 24) // 2
    # Gaza, left column
    gaza_panel(d, (M, my, M + col_w, my + 84))
    gy = para(d, "ISRAEL KILLS HAMAS MINISTER IN GAZA STRIKES",
              font(SERIF_B, 26), M, my + 92, col_w, 29)
    para(d, "At least 9 killed overnight, including deputy education minister "
            "Khaled Abu Nada and his wife in Deir al-Balah — a third straight "
            "night of strikes despite a year-old ceasefire.",
         font(SERIF, 18), M, gy + 4, col_w, 22)
    # Ebola, right column
    ex = M + col_w + 24
    ebola_panel(d, (ex, my, ex + col_w, my + 84))
    ey = para(d, "EBOLA PASSES 12,000 CASES IN CONGO",
              font(SERIF_B, 26), ex, my + 92, col_w, 29)
    para(d, "12,021 confirmed cases in the east, and nearly half of them have "
            "died — the fastest-growing Ebola outbreak in history, the health "
            "ministry says. No approved vaccine for this strain.",
         font(SERIF, 18), ex, ey + 4, col_w, 22)
    rule(d, M, 788, X1, 2)

    # ---- EU strip ----
    eu_stars(d, M + 42, 842, 26)
    para(d, "EU DEADLOCKED ON €1.58 TRILLION BUDGET",
         font(SERIF_B, 27), M + 104, 802, X1 - M - 104, 33)
    para(d, "Leaders fail to agree after 12 hours in Brussels; no deal on Thursday. "
            "Next try: 17–18 December. A $49bn loan for Ukraine is stuck too.",
         font(SERIF, 18), M + 104, 840, X1 - M - 104, 22)
    rule(d, M, 896, X1, 2)

    # ---- Macy's strip ----
    macys_panel(d, (M, 908, M + 250, 908 + 72))
    para(d, "NO PARADE ON THANKSGIVING",
         font(SERIF_B, 24), M + 270, 908, X1 - M - 270, 30)
    para(d, "The 100th Macy's parade is postponed for the first time ever — a "
            "nor'easter gusting to 60 mph moves it to Saturday 28 November.",
         font(SERIF, 17), M + 270, 940, X1 - M - 270, 21)

    # ---- footer briefs ----
    rule(d, M, 992, X1, 1)
    d.text((M, 998), "ALSO: Houthis claim strikes on Jeddah and Jazan  ·  Serbia votes "
                     "27 Dec  ·  Russia OKs record military budget",
           font=font(SANS, 14), fill=GREY)
    return img


if __name__ == "__main__":
    build().save("entry.png", optimize=True)
