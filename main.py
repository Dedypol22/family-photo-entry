#!/usr/bin/env python3
"""The Family Photo With One Machine Member - make.fun entry.
Draws a warm family-at-home scene with PIL only. Deterministic, no network.
Saves entry.png to MAKEFUN_OUTPUT_DIR (default /output).
"""
import os
from PIL import Image, ImageDraw

W, H = 1024, 768

# Palette
WALL = (245, 234, 214)
FLOOR = (186, 140, 96)
FLOOR_LINE = (150, 108, 70)
SKIRT = (232, 218, 192)
MUSTARD = (216, 168, 64)
MUSTARD_DARK = (186, 140, 48)
MUSTARD_LIGHT = (232, 190, 92)
TEAL = (62, 140, 137)
TEAL_DARK = (46, 112, 110)
CREAM_ENAMEL = (246, 240, 224)
DARK_SCREEN = (38, 48, 58)
SKIN1 = (198, 134, 88)
SKIN2 = (232, 178, 138)
SKIN3 = (168, 108, 72)
SKIN4 = (242, 196, 152)
HAIR_DARK = (62, 42, 32)
HAIR_BROWN = (110, 72, 44)
HAIR_BLACK = (32, 28, 26)


def shadow(d, cx, cy, w, h):
    d.ellipse([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], fill=(0, 0, 0))
    # soft shadow simulated with semi-transparent overlay via separate layer handled by caller;
    # here draw muted brown ellipse
    d.ellipse([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], fill=(196, 168, 138))


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def face(d, cx, cy, r, skin, hair_color, hair_style="cap"):
    # head
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=skin)
    # hair
    if hair_style == "cap":
        d.pieslice([cx - r, cy - r, cx + r, cy + r], start=180, end=360, fill=hair_color)
        d.rectangle([cx - r, cy - r // 2, cx + r, cy - r // 3], fill=hair_color)
    elif hair_style == "bun":
        d.pieslice([cx - r, cy - r, cx + r, cy + r], start=180, end=360, fill=hair_color)
        d.ellipse([cx - 10, cy - r - 12, cx + 10, cy - r + 8], fill=hair_color)
        # sides
        d.rectangle([cx - r, cy - r // 2, cx - r + 8, cy + r // 2], fill=hair_color)
        d.rectangle([cx + r - 8, cy - r // 2, cx + r, cy + r // 2], fill=hair_color)
    elif hair_style == "short":
        d.pieslice([cx - r, cy - r - 2, cx + r, cy + r], start=180, end=360, fill=hair_color)
    # eyes
    d.ellipse([cx - r // 2 - 3, cy - 2, cx - r // 2 + 3, cy + 4], fill=(30, 30, 30))
    d.ellipse([cx + r // 2 - 3, cy - 2, cx + r // 2 + 3, cy + 4], fill=(30, 30, 30))
    # smile arc
    d.arc([cx - r // 2, cy + 2, cx + r // 2, cy + r - 4], start=15, end=165, fill=(90, 50, 40), width=3)


def main():
    img = Image.new("RGB", (W, H), WALL)
    d = ImageDraw.Draw(img, "RGBA")

    floor_y = int(H * 0.62)  # 476

    # --- Room: wall + floor ---
    d.rectangle([0, 0, W, floor_y], fill=WALL)
    d.rectangle([0, floor_y, W, H], fill=FLOOR)
    # floor planks
    for yy in (floor_y + 55, floor_y + 115, floor_y + 175, floor_y + 235):
        d.line([(0, yy), (W, yy)], fill=FLOOR_LINE, width=2)
    for xx in (180, 420, 660, 880):
        d.line([(xx, floor_y), (xx - 30, H)], fill=FLOOR_LINE, width=2)
    # skirting
    d.rectangle([0, floor_y - 10, W, floor_y + 4], fill=SKIRT)
    d.line([(0, floor_y - 10), (W, floor_y - 10)], fill=(200, 180, 150), width=2)

    # --- Window left ---
    d.rounded_rectangle([52, 62, 272, 342], radius=10, fill=(255, 252, 244), outline=(150, 130, 100), width=4)
    # panes pale daylight
    d.rectangle([68, 78, 160, 200], fill=(208, 234, 246))
    d.rectangle([168, 78, 256, 200], fill=(218, 240, 248))
    d.rectangle([68, 208, 160, 316], fill=(218, 240, 248))
    d.rectangle([168, 208, 256, 316], fill=(208, 234, 246))
    # simple sun / cloud shapes in panes (abstract, no text)
    d.ellipse([185, 95, 225, 135], fill=(250, 220, 130))
    d.ellipse([80, 110, 130, 132], fill=(255, 255, 255))
    d.ellipse([105, 100, 150, 128], fill=(255, 255, 255))
    # sill
    d.rectangle([44, 332, 280, 348], fill=(232, 218, 192), outline=(150, 130, 100))
    # curtains
    d.polygon([(52, 62), (92, 62), (82, 342), (52, 342)], fill=(198, 90, 78))
    d.polygon([(272, 62), (232, 62), (242, 342), (272, 342)], fill=(198, 90, 78))
    d.rectangle([52, 62, 272, 76], fill=(168, 72, 62))
    # potted plant on sill
    d.polygon([(118, 332), (152, 332), (146, 306), (124, 306)], fill=(188, 96, 62))
    d.ellipse([108, 272, 138, 306], fill=(72, 148, 84))
    d.ellipse([130, 262, 162, 300], fill=(88, 164, 96))
    d.ellipse([122, 282, 150, 308], fill=(64, 132, 76))

    # --- Radiator under window + laundry ---
    d.rounded_rectangle([70, 372, 254, 462], radius=8, fill=(238, 236, 228), outline=(170, 168, 158), width=3)
    for xx in range(88, 250, 22):
        d.line([(xx, 380), (xx, 454)], fill=(190, 188, 178), width=4)
    # laundry item 1 - teal towel
    d.polygon([(92, 372), (142, 372), (146, 428), (96, 432)], fill=TEAL)
    d.line([(96, 398), (144, 396)], fill=(255, 255, 255), width=4)
    # laundry item 2 - cream/ striped cloth
    d.polygon([(176, 372), (228, 372), (224, 420), (180, 424)], fill=(250, 244, 220))
    d.line([(180, 392), (226, 390)], fill=(198, 90, 78), width=4)
    d.line([(181, 404), (225, 402)], fill=(198, 90, 78), width=3)

    # --- Framed pictures (abstract, no text) ---
    # frame 1
    d.rectangle([352, 88, 512, 218], fill=(120, 84, 54), outline=(90, 62, 38), width=3)
    d.rectangle([364, 100, 500, 206], fill=(232, 240, 232))
    d.ellipse([386, 118, 446, 178], fill=(232, 168, 64))
    d.polygon([(430, 206), (468, 140), (500, 206)], fill=TEAL)
    d.polygon([(364, 206), (410, 156), (448, 206)], fill=(122, 168, 110))
    # frame 2
    d.rectangle([690, 92, 836, 202], fill=(120, 84, 54), outline=(90, 62, 38), width=3)
    d.rectangle([702, 104, 824, 190], fill=(250, 238, 210))
    d.ellipse([716, 118, 766, 168], fill=(198, 90, 78))
    d.rectangle([778, 124, 810, 176], fill=TEAL)
    d.arc([730, 130, 800, 185], start=0, end=180, fill=(62, 42, 32), width=4)

    # --- Floor lamp right ---
    shadow(d, 928, 640, 90, 18)
    d.rectangle([922, 300, 934, 632], fill=(90, 78, 66))
    d.ellipse([896, 622, 960, 642], fill=(90, 78, 66))
    # glowing shade (trapezoid)
    d.polygon([(884, 300), (972, 300), (954, 218), (902, 218)], fill=(252, 208, 110))
    d.polygon([(884, 300), (972, 300), (954, 218), (902, 218)], outline=(196, 150, 60))
    # glow halo
    d.ellipse([862, 196, 994, 322], fill=(252, 220, 140, 60))

    # --- Rug ---
    d.ellipse([230, 606, 700, 726], fill=(178, 84, 74))
    d.ellipse([252, 618, 678, 714], fill=(222, 178, 140))
    d.ellipse([286, 632, 644, 700], fill=(178, 84, 74))

    # --- Sofa center-left ---
    shadow(d, 400, 592, 470, 26)
    # back
    rrect(d, [168, 396, 632, 540], 28, fill=MUSTARD)
    # arms
    rrect(d, [150, 452, 216, 584], 18, fill=MUSTARD_DARK)
    rrect(d, [584, 452, 650, 584], 18, fill=MUSTARD_DARK)
    # seat base
    rrect(d, [168, 512, 632, 590], 16, fill=MUSTARD_DARK)
    # cushions
    rrect(d, [224, 500, 392, 560], 14, fill=MUSTARD_LIGHT)
    rrect(d, [408, 500, 576, 560], 14, fill=MUSTARD_LIGHT)
    # back cushion dividers
    d.line([(400, 410), (400, 505)], fill=MUSTARD_DARK, width=4)
    # legs
    d.rectangle([196, 590, 214, 612], fill=(90, 62, 38))
    d.rectangle([586, 590, 604, 612], fill=(90, 62, 38))

    # --- Side table (right of sofa, behind mum) with books + vase ---
    shadow(d, 668, 592, 110, 16)
    d.rectangle([620, 520, 716, 536], fill=(120, 84, 54))
    d.rectangle([632, 536, 644, 590], fill=(90, 62, 38))
    d.rectangle([692, 536, 704, 590], fill=(90, 62, 38))
    # books
    d.rectangle([628, 498, 676, 520], fill=TEAL)
    d.rectangle([630, 480, 672, 500], fill=(198, 90, 78))
    # vase
    d.polygon([(688, 520), (708, 520), (704, 488), (692, 488)], fill=(150, 190, 200))
    d.ellipse([682, 456, 700, 492], fill=(88, 164, 96))
    d.ellipse([696, 450, 716, 488], fill=(72, 148, 84))

    # --- Potted plant on floor (robot watering target) ---
    shadow(d, 838, 648, 80, 14)
    d.polygon([(812, 648), (864, 648), (856, 606), (820, 606)], fill=(188, 96, 62))
    d.rectangle([808, 600, 868, 614], fill=(160, 78, 50))
    d.ellipse([800, 548, 844, 606], fill=(72, 148, 84))
    d.ellipse([830, 538, 876, 600], fill=(88, 164, 96))
    d.ellipse([818, 562, 860, 608], fill=(64, 132, 76))

    # === PEOPLE ===

    # --- DAD seated on sofa ---
    shadow(d, 318, 566, 170, 18)
    # legs relaxed (trousers) - seated, knees forward then down
    d.line([(292, 528), (262, 566), (262, 596)], fill=(74, 88, 110), width=22)
    d.line([(352, 528), (382, 562), (396, 592)], fill=(74, 88, 110), width=22)
    # shoes
    d.ellipse([240, 590, 278, 606], fill=(62, 42, 32))
    d.ellipse([380, 586, 418, 602], fill=(62, 42, 32))
    # torso leaning slightly back - shirt teal-blue
    rrect(d, [268, 408, 372, 536], 22, fill=(92, 128, 158))
    # arm resting on sofa arm (left)
    d.line([(278, 442), (196, 486)], fill=SKIN1, width=16)
    d.line([(278, 442), (210, 478)], fill=(92, 128, 158), width=20)
    # other arm holding mug
    d.line([(362, 448), (410, 492)], fill=(92, 128, 158), width=20)
    d.line([(410, 492), (424, 500)], fill=SKIN1, width=14)
    # mug
    rrect(d, [416, 482, 448, 512], 5, fill=(250, 250, 246), outline=(170, 168, 158))
    d.arc([442, 488, 460, 506], start=270, end=90, fill=(170, 168, 158), width=3)
    # head
    face(d, 320, 372, 38, SKIN1, HAIR_DARK, "cap")

    # --- MUM standing right of sofa holding TODDLER ---
    shadow(d, 682, 646, 110, 16)
    # legs / skirt + legs
    d.polygon([(648, 512), (716, 512), (728, 592), (636, 592)], fill=(198, 120, 96))
    d.line([(660, 592), (660, 632)], fill=SKIN2, width=14)
    d.line([(700, 592), (700, 632)], fill=SKIN2, width=14)
    d.ellipse([640, 630, 676, 644], fill=(62, 42, 32))
    d.ellipse([684, 630, 720, 644], fill=(62, 42, 32))
    # torso - warm rust top
    rrect(d, [642, 396, 724, 520], 20, fill=(178, 92, 74))
    # free hand resting on sofa back (arm to left)
    d.line([(648, 430), (610, 470)], fill=(178, 92, 74), width=18)
    d.line([(610, 470), (598, 478)], fill=SKIN2, width=12)
    # arm cradling toddler (to front)
    d.line([(716, 436), (742, 478)], fill=(178, 92, 74), width=18)
    # TODDLER against hip (on mum's left-front side, viewer's right of mum torso lower)
    # toddler body
    rrect(d, [700, 452, 756, 522], 16, fill=(250, 200, 90))
    # toddler legs dangling
    d.line([(716, 520), (710, 548)], fill=(110, 150, 190), width=12)
    d.line([(742, 520), (750, 546)], fill=(110, 150, 190), width=12)
    # toddler head
    face(d, 728, 428, 26, SKIN4, HAIR_BROWN, "short")
    # mum head
    face(d, 683, 356, 36, SKIN2, HAIR_DARK, "bun")

    # --- KID 1 cross-legged on rug with toy blocks ---
    shadow(d, 360, 682, 150, 16)
    # crossed legs
    d.line([(310, 676), (366, 652)], fill=(88, 140, 110), width=16)
    d.line([(410, 676), (354, 652)], fill=(88, 140, 110), width=16)
    # torso
    rrect(d, [322, 580, 398, 662], 18, fill=(240, 168, 72))
    # arms reaching to blocks
    d.line([(330, 606), (302, 646)], fill=(240, 168, 72), width=16)
    d.line([(390, 606), (420, 640)], fill=(240, 168, 72), width=16)
    d.ellipse([294, 640, 312, 656], fill=SKIN3)
    d.ellipse([412, 634, 430, 650], fill=SKIN3)
    # head
    face(d, 360, 548, 32, SKIN3, HAIR_BLACK, "short")
    # toy blocks in front
    d.rectangle([428, 648, 458, 678], fill=(198, 90, 78))
    d.rectangle([462, 648, 492, 678], fill=TEAL)
    d.polygon([(446, 618), (476, 648), (416, 648)], fill=(250, 200, 90))

    # --- KID 2 standing center-right facing robot ---
    shadow(d, 566, 650, 80, 14)
    # legs
    d.line([(552, 548), (552, 630)], fill=(74, 88, 110), width=15)
    d.line([(582, 548), (582, 630)], fill=(74, 88, 110), width=15)
    d.ellipse([532, 628, 564, 642], fill=(62, 42, 32))
    d.ellipse([570, 628, 602, 642], fill=(62, 42, 32))
    # torso - green top
    rrect(d, [532, 452, 602, 556], 18, fill=(110, 168, 110))
    # one hand raised toward robot (right arm up-right)
    d.line([(596, 472), (636, 438)], fill=(110, 168, 110), width=16)
    d.line([(636, 438), (648, 430)], fill=SKIN4, width=12)
    d.ellipse([640, 418, 660, 438], fill=SKIN4)
    # other arm down
    d.line([(538, 472), (522, 524)], fill=(110, 168, 110), width=16)
    d.ellipse([514, 520, 532, 538], fill=SKIN4)
    # head (profile-ish toward robot: still front simple face)
    face(d, 567, 416, 32, SKIN4, HAIR_BROWN, "cap")

    # === THE ROBOT — one machine member, center-right ===
    # Position: body center x ~ 790, from y ~ 350 to 650. Mum height minus a head.
    shadow(d, 790, 652, 150, 18)
    # wheeled base
    rrect(d, [742, 606, 838, 642], 16, fill=(90, 98, 108))
    d.ellipse([756, 624, 786, 654], fill=(38, 42, 48))
    d.ellipse([764, 632, 778, 646], fill=(140, 148, 158))
    d.ellipse([794, 624, 824, 654], fill=(38, 42, 48))
    d.ellipse([802, 632, 816, 646], fill=(140, 148, 158))
    # capsule body cream enamel
    rrect(d, [736, 402, 844, 616], 44, fill=CREAM_ENAMEL, outline=(188, 178, 158), width=3)
    # teal belly panel
    rrect(d, [758, 470, 822, 556], 18, fill=TEAL, outline=TEAL_DARK, width=2)
    d.ellipse([782, 492, 798, 508], fill=(250, 220, 130))
    d.rectangle([772, 524, 808, 532], fill=(246, 240, 224))
    # faint scuff lines
    d.line([(748, 440), (766, 446)], fill=(198, 188, 168), width=2)
    d.line([(820, 576), (806, 586)], fill=(198, 188, 168), width=2)
    d.arc([748, 556, 772, 580], start=200, end=320, fill=(198, 188, 168), width=2)
    # neck
    d.rectangle([778, 388, 802, 408], fill=(140, 148, 158))
    # dome head
    d.pieslice([742, 286, 838, 384], start=180, end=360, fill=CREAM_ENAMEL, outline=(188, 178, 158))
    d.rectangle([742, 334, 838, 386], fill=CREAM_ENAMEL, outline=(188, 178, 158), width=2)
    # face screen dark rounded-rect
    rrect(d, [756, 316, 824, 376], 14, fill=DARK_SCREEN)
    # soft dot eyes + smile on screen
    d.ellipse([772, 336, 784, 348], fill=(140, 240, 220))
    d.ellipse([796, 336, 808, 348], fill=(140, 240, 220))
    d.arc([778, 342, 802, 366], start=15, end=165, fill=(140, 240, 220), width=3)
    # left arm (viewer left) with folded tea towel draped
    d.line([(740, 448), (700, 500)], fill=(140, 148, 158), width=12)
    d.ellipse([736, 440, 752, 456], fill=TEAL_DARK)
    d.ellipse([692, 492, 708, 508], fill=(140, 148, 158))
    # tea towel over forearm
    d.polygon([(688, 478), (724, 486), (720, 534), (692, 530)], fill=(250, 244, 220), outline=(198, 188, 168))
    d.line([(694, 500), (720, 504)], fill=(198, 90, 78), width=3)
    d.line([(694, 514), (719, 518)], fill=TEAL, width=3)
    # right arm holding watering can over floor plant
    d.line([(840, 448), (872, 500)], fill=(140, 148, 158), width=12)
    d.ellipse([832, 440, 848, 456], fill=TEAL_DARK)
    # watering can tilted above plant
    rrect(d, [852, 492, 902, 532], 8, fill=TEAL, outline=TEAL_DARK, width=2)
    d.polygon([(852, 506), (832, 524), (852, 524)], fill=TEAL_DARK)
    d.arc([896, 492, 918, 524], start=270, end=90, fill=TEAL_DARK, width=4)
    # water drops to plant
    for (wx, wy) in [(840, 536), (848, 552), (836, 564)]:
        d.ellipse([wx, wy, wx + 6, wy + 10], fill=(120, 190, 225))

    # --- Dog bowl + sleeping dog beside sofa (front-left floor) ---
    shadow(d, 132, 640, 130, 16)
    # curled dog: oval body, head on paws, closed-eye arc
    d.ellipse([62, 588, 182, 644], fill=(206, 164, 110))
    d.ellipse([78, 578, 148, 622], fill=(222, 182, 126))
    # ear
    d.ellipse([84, 582, 112, 610], fill=(150, 108, 70))
    # tail curl
    d.arc([150, 596, 190, 640], start=300, end=120, fill=(150, 108, 70), width=6)
    # paws
    d.ellipse([92, 624, 132, 638], fill=(222, 182, 126))
    # closed eye arc
    d.arc([100, 596, 124, 610], start=0, end=180, fill=(62, 42, 32), width=3)
    # nose
    d.ellipse([80, 604, 90, 612], fill=(40, 32, 28))
    # dog bowl
    d.polygon([(196, 624), (248, 624), (240, 646), (204, 646)], fill=(198, 90, 78))
    d.ellipse([196, 616, 248, 630], fill=(232, 120, 108))
    d.ellipse([208, 619, 236, 627], fill=(150, 108, 70))

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.png")
    img.save(out_path, format="PNG")
    print(f"Saved {out_path}")


if __name__ == "__main__":
    main()
