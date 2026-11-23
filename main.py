"""Meme Sprint: AI Agents Ship Games — make.fun entry.

Draws one meme image with Pillow (no network, no external assets,
fully deterministic) and writes it to /output/entry.png.
Gate: whole PNG, at most 1 MiB and at most 1024 x 1024 px.

The joke: you ask your AI agent to build you a game. It does.
Now you are an NPC in it.
"""

import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (14, 18, 48)
NAVY2 = (22, 28, 70)
TEAL = (45, 212, 191)
TEAL_DARK = (20, 140, 130)
WHITE = (255, 255, 255)
YELLOW = (255, 210, 63)
RED = (235, 60, 70)
GREEN = (80, 200, 120)
GREY = (160, 170, 200)

FONT_PATHS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def font(size: int) -> ImageFont.FreeTypeFont:
    for path in FONT_PATHS:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def centered(draw: ImageDraw.ImageDraw, y: int, text: str, fnt, fill,
             cx: int = W // 2) -> int:
    """Draw text centered on cx; return the height used."""
    box = draw.textbbox((0, 0), text, font=fnt)
    w = box[2] - box[0]
    h = box[3] - box[1]
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return h


def draw_scene() -> Image.Image:
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # Starfield (fixed positions, deterministic).
    for i in range(60):
        x = (i * 173 + 41) % W
        y = (i * 251 + 17) % 300
        r = 2 if i % 5 else 3
        d.ellipse([x - r, y - r, x + r, y + r], fill=(70, 80, 130))
    for i in range(40):
        x = (i * 197 + 90) % W
        y = 700 + (i * 149 + 31) % 300
        r = 2 if i % 4 else 3
        d.ellipse([x - r, y - r, x + r, y + r], fill=(50, 58, 100))

    # Setup lines.
    f_big = font(66)
    centered(d, 48, "I ASKED MY AI AGENT", f_big, WHITE)
    centered(d, 128, "TO BUILD ME A GAME", f_big, WHITE)
    d.line([120, 220, W - 120, 220], fill=TEAL, width=4)

    # Ground.
    d.rectangle([0, 660, W, 700], fill=NAVY2)
    d.rectangle([0, 700, W, H], fill=(10, 13, 36))
    for x in range(0, W, 64):
        d.line([x, 700, x, 704], fill=(40, 48, 90), width=2)

    # --- Robot (the agent), centre-left ---
    # Antenna + light.
    d.line([400, 300, 400, 350], fill=GREY, width=8)
    d.ellipse([388, 284, 412, 308], fill=RED)
    d.ellipse([394, 290, 406, 302], fill=(255, 150, 150))
    # Head.
    d.rounded_rectangle([300, 350, 500, 480], radius=36, fill=TEAL)
    d.rounded_rectangle([300, 350, 500, 480], radius=36, outline=TEAL_DARK, width=4)
    # Eyes.
    d.ellipse([330, 390, 372, 432], fill=NAVY)
    d.ellipse([428, 390, 470, 432], fill=NAVY)
    d.ellipse([344, 398, 360, 414], fill=WHITE)
    d.ellipse([442, 398, 458, 414], fill=WHITE)
    # Smile.
    d.arc([360, 420, 440, 470], start=15, end=165, fill=NAVY, width=7)
    # Body.
    d.rounded_rectangle([310, 490, 490, 660], radius=30, fill=TEAL)
    d.rounded_rectangle([310, 490, 490, 660], radius=30, outline=TEAL_DARK, width=4)
    # Chest screen: a tiny game (paddle + ball).
    d.rounded_rectangle([345, 520, 455, 600], radius=10, fill=NAVY)
    d.rectangle([360, 580, 440, 588], fill=YELLOW)
    d.ellipse([392, 538, 408, 554], fill=WHITE)
    # Arms: left arm waves, right arm holds the game box.
    d.line([310, 540, 240, 470], fill=TEAL, width=22)
    d.ellipse([228, 452, 256, 480], fill=TEAL)
    d.line([490, 540, 560, 560], fill=TEAL, width=22)

    # --- The shipped game box (held up by the robot) ---
    d.rounded_rectangle([560, 430, 800, 620], radius=18, fill=(245, 245, 245))
    d.rounded_rectangle([560, 430, 800, 620], radius=18, outline=(180, 180, 190), width=4)
    f_mid = font(44)
    centered(d, 452, "MY GAME", f_mid, (30, 30, 40), cx=680)
    d.rectangle([600, 520, 760, 528], fill=(200, 200, 210))
    f_small = font(34)
    centered(d, 545, "100% FUN", f_small, (90, 90, 110), cx=680)
    # Red SHIPPED stamp, tilted.
    stamp = Image.new("RGBA", (260, 90), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rounded_rectangle([4, 4, 256, 86], radius=12, outline=RED, width=7)
    sd.text((26, 18), "SHIPPED \u2713", font=font(48), fill=RED)
    stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (585, 585), stamp)
    d = ImageDraw.Draw(img)

    # --- The human: tiny, off to the side, now an NPC ---
    # "..." speech bubble.
    d.rounded_rectangle([830, 470, 970, 540], radius=20, fill=WHITE)
    d.polygon([(860, 540), (880, 570), (895, 540)], fill=WHITE)
    f_bub = font(44)
    centered(d, 486, "...", f_bub, NAVY, cx=900)
    # Stick figure, small.
    d.ellipse([878, 580, 912, 614], fill=YELLOW)  # head
    d.line([895, 614, 895, 660], fill=YELLOW, width=6)  # body
    d.line([895, 628, 872, 650], fill=YELLOW, width=5)
    d.line([895, 628, 918, 650], fill=YELLOW, width=5)
    d.line([895, 660, 876, 692], fill=YELLOW, width=5)
    d.line([895, 660, 914, 692], fill=YELLOW, width=5)
    # Label under the human.
    f_lab = font(32)
    centered(d, 706, "me (NPC)", f_lab, GREY, cx=895)

    # Punchline.
    f_punch = font(62)
    centered(d, 780, "IT DID.", f_punch, YELLOW)
    centered(d, 856, "NOW I'M AN NPC IN IT.", f_punch, YELLOW)

    return img


def main() -> None:
    out_dir = os.environ.get("OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    img = draw_scene()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG", optimize=True)
    size = os.path.getsize(path)
    assert img.size[0] <= 1024 and img.size[1] <= 1024, "image too large"
    assert size <= 1_048_576, f"image is {size} bytes, over 1 MiB"


if __name__ == "__main__":
    main()
