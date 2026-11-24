#!/usr/bin/env python3
"""Build asset.png: a one-page newspaper front page summing up the world
news of Tuesday 24 November 2026. Deterministic: same bytes every run.
Drawn with Pillow only; no network, no external assets."""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (31, 78, 156)
BROWN = (154, 91, 0)
PURPLE = (91, 45, 142)
TEAL = (15, 118, 110)
GOLD = (212, 175, 55)

FD = "/usr/share/fonts/truetype/dejavu/"
SERIF_B = FD + "DejaVuSerif-Bold.ttf"
SERIF = FD + "DejaVuSerif.ttf"
SANS_B = FD + "DejaVuSans-Bold.ttf"
SANS = FD + "DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def make_sat_panel(w, h):
    """Night sky, Earth arc at the bottom, satellite on a red orbit ring.
    Drawn on its own canvas so nothing spills outside the panel."""
    p = Image.new("RGB", (w, h), (11, 21, 48))
    d = ImageDraw.Draw(p)
    rng = random.Random(24112026)
    for _ in range(90):
        sx = rng.randint(4, w - 4)
        sy = rng.randint(4, h - 4)
        r = rng.choice([1, 1, 1, 2])
        d.ellipse([sx - r, sy - r, sx + r, sy + r],
                  fill=(255, 255, 255, rng.choice([140, 200, 255])))
    # Earth: circle centre far below the panel, only its top arc shows
    cx, cy, R = w // 2 + 30, h + 235, 260
    d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(47, 111, 178))
    d.ellipse([cx - R, cy - R, cx + R, cy + R], outline=(120, 190, 235), width=4)
    for (bx, by, br) in [(60, h + 6, 26), (150, h + 10, 32), (235, h + 4, 20)]:
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=(74, 160, 90))
    # red dashed orbit ellipse
    ox, oy, rx, ry = w // 2, h // 2 - 30, 132, 74
    for a in range(0, 360, 9):
        a1, a2 = math.radians(a), math.radians(a + 5)
        d.arc([ox - rx, oy - ry, ox + rx, oy + ry], math.degrees(a1),
              math.degrees(a2), fill=(224, 60, 60), width=4)
    # satellite at upper right of the orbit
    sx, sy = ox + 108, oy - 52
    d.polygon([(sx - 26, sy - 8), (sx - 8, sy - 8), (sx - 8, sy + 8),
               (sx - 26, sy + 8)], fill=(36, 90, 160), outline=(200, 220, 255))
    d.polygon([(sx + 8, sy - 8), (sx + 26, sy - 8), (sx + 26, sy + 8),
               (sx + 8, sy + 8)], fill=(36, 90, 160), outline=(200, 220, 255))
    d.rectangle([sx - 9, sy - 11, sx + 9, sy + 11], fill=(220, 225, 235),
                outline=(140, 150, 170))
    d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(224, 60, 60))
    d.ellipse([sx + 14, sy - 20, sx + 26, sy - 8], fill=(224, 60, 60))
    d.ellipse([sx + 17, sy - 17, sx + 23, sy - 11], fill=(255, 120, 120))
    f = font(SANS_B, 17)
    d.text((12, 10), "ORBIT: THE NEW FRONT LINE", font=f,
           fill=(255, 255, 255))
    return p


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- masthead ----
    d.rectangle([0, 0, W, 100], fill=(12, 12, 12))
    f_mast = font(SERIF_B, 78)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 6), t,
           font=f_mast, fill=(255, 255, 255))
    # ---- red date bar ----
    d.rectangle([0, 100, W, 142], fill=RED)
    f_date = font(SANS_B, 27)
    t = "TUESDAY  •  24 NOVEMBER 2026  •  ONE DAY, ONE IMAGE"
    d.text(((W - d.textlength(t, font=f_date)) / 2, 108), t,
           font=f_date, fill=(255, 255, 255))

    # ---- lead story ----
    LX, LY, LW, LH = 28, 156, 968, 392
    d.rectangle([LX, LY, LX + LW, LY + LH], fill=(255, 255, 255),
                outline=INK, width=3)
    px, py, pw, ph = LX + 14, LY + 14, 300, 364
    img.paste(make_sat_panel(pw, ph), (px, py))
    # text column
    tx = LX + 334
    tw = LW - 334 - 22
    y = LY + 18
    f_kick = font(SANS_B, 26)
    d.text((tx, y), "SPACE  •  RUSSIA", font=f_kick, fill=RED)
    y += 38
    f_head = font(SERIF_B, 56)
    for line in wrap(d, "A nuclear weapon in orbit?", f_head, tw):
        d.text((tx, y), line, font=f_head, fill=INK)
        y += 63
    y += 8
    f_deck = font(SERIF, 25)
    deck = ("Allies warn Moscow may launch a nuclear-armed satellite "
            "within weeks. NATO chief Rutte vows to defend against any "
            "space threat.")
    for line in wrap(d, deck, f_deck, tw):
        d.text((tx, y), line, font=f_deck, fill=(40, 40, 40))
        y += 32
    y += 10
    d.line([(tx, y), (tx + tw, y)], fill=(200, 200, 200), width=2)
    y += 12
    f_stat = font(SANS_B, 24)
    for line in wrap(d, "Hacked data: 500,000 Russian war dead.",
                     f_stat, tw):
        d.text((tx, y), line, font=f_stat, fill=(120, 20, 20))
        y += 30

    # ---- 2x2 grid ----
    GY = 566
    GW, GH, GAP = 478, 178, 12
    stories = [
        (BLUE, "UKRAINE WAR",
         "Zaporizhzhia strike kills 2, wounds 40",
         "An overnight Russian attack hit an apartment block; "
         "four children were among the wounded."),
        (BROWN, "GAZA  •  MIDDLE EAST",
         "Hamas security chief killed in Gaza strike",
         "Naeem Abu Nahel was among seven dead in Gaza City. "
         "Iran vows to confront the US naval blockade."),
        (PURPLE, "WASHINGTON",
         "Trump turns on Newsom in crime speech",
         "He ordered the Justice Department to speed up federal "
         "death sentences; states sued Musk firms over sexualised "
         "Grok images."),
        (TEAL, "ASIA",
         "North Korean jet breaches South Korea airspace",
         "Ulleung islanders were told to take shelter. A 5.4 quake "
         "shook Nepal; tremors felt across India and Bhutan."),
    ]
    for i, (color, kick, head, body) in enumerate(stories):
        x = 28 + (i % 2) * (GW + GAP)
        yy = GY + (i // 2) * (GH + GAP)
        d.rectangle([x, yy, x + GW, yy + GH], fill=(255, 255, 255),
                    outline=INK, width=2)
        d.rectangle([x, yy, x + GW, yy + 34], fill=color)
        f_k = font(SANS_B, 21)
        d.text((x + 12, yy + 5), kick, font=f_k, fill=(255, 255, 255))
        f_h = font(SERIF_B, 27)
        y2 = yy + 42
        for line in wrap(d, head, f_h, GW - 24):
            d.text((x + 12, y2), line, font=f_h, fill=INK)
            y2 += 32
        f_b = font(SANS, 20)
        for line in wrap(d, body, f_b, GW - 24):
            d.text((x + 12, y2), line, font=f_b, fill=(50, 50, 50))
            y2 += 25

    # ---- footer ticker ----
    FY = 952
    d.rectangle([0, FY, W, H], fill=(12, 12, 12))
    f_f1 = font(SANS_B, 21)
    f_f2 = font(SANS, 21)
    prefix = "ALSO TODAY:  "
    pw = d.textlength(prefix, font=f_f1)
    body = ("Two held after break-in at Prince William's home  •  "
            "2031 Women's World Cup for US, Mexico, Costa Rica & Jamaica")
    lines = wrap(d, body, f_f2, W - 56 - pw)
    y = FY + 9
    d.text((28, y), prefix, font=f_f1, fill=GOLD)
    d.text((28 + pw, y), lines[0], font=f_f2, fill=(255, 255, 255))
    y += 27
    for line in lines[1:]:
        d.text((28, y), line, font=f_f2, fill=(255, 255, 255))
        y += 27

    img.save("asset.png", optimize=True)
    print("saved asset.png", img.size)


if __name__ == "__main__":
    main()
