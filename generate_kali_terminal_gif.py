from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import textwrap

# Place this file in your repository and run:
#   pip install pillow
#   python generate_kali_terminal_gif.py

OUT = Path("assets/kali-terminal-animated.gif")
OUT.parent.mkdir(parents=True, exist_ok=True)

W, H = 1100, 610
FONT_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"

font_title = ImageFont.truetype(FONT_BOLD, 24)
font_label = ImageFont.truetype(FONT_BOLD, 18)
font_prompt = ImageFont.truetype(FONT_BOLD, 19)
font_text = ImageFont.truetype(FONT_REG, 18)
font_heading = ImageFont.truetype(FONT_BOLD, 28)

BG = "#070b12"
TOP = "#111827"
BORDER = "#253247"
BLUE = "#58a6ff"
GREEN = "#7ee787"
PINK = "#ff4da6"
WHITE = "#e6edf3"

about_items = [
    "Currently working on BioAuth, a continuous behavioral authentication project.",
    "Developing cybersecurity tools and automation mainly with Python.",
    "Interested in offensive security, defensive security and threat intelligence.",
    "Working with penetration testing, monitoring and vulnerability management tools.",
    "Interested in malware analysis, digital forensics and OSINT.",
    "Coffee-powered cybersecurity enthusiast.",
]

visual_lines = []
for idx, item in enumerate(about_items, start=1):
    wrapped = textwrap.wrap(item, width=82, break_long_words=False)
    for j, line in enumerate(wrapped):
        visual_lines.append((f"[{idx:02d}] " if j == 0 else "     ", line))

prefix_text = "┌──(dorian㉿kali)-[~/profile]\n└─$ cat about_me.txt\n\nABOUT ME\n\n"
body_text = "\n".join(prefix + line for prefix, line in visual_lines)
full_text = prefix_text + body_text

def base_image():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((8, 8, W - 8, H - 8), radius=18, fill=BG, outline=BORDER, width=2)
    d.rounded_rectangle((8, 8, W - 8, 76), radius=18, fill=TOP)
    d.rectangle((8, 54, W - 8, 76), fill=TOP)
    d.rounded_rectangle((28, 22, 72, 58), radius=8, fill="#2777ff")
    d.text((38, 29), ">_", font=font_label, fill="white")
    d.text((92, 29), "dorian@kali: ~/profile", font=font_title, fill=WHITE)
    d.text((915, 31), "KALI LINUX", font=font_label, fill=BLUE)
    return img

def draw_terminal_text(img, visible_chars, cursor_on=True):
    d = ImageDraw.Draw(img)
    text = full_text[:visible_chars]
    x, y, line_h = 48, 103, 31
    lines = text.split("\n")

    for i, line in enumerate(lines):
        yy = y + i * line_h
        if yy > H - 42:
            break
        if line.startswith("┌──") or line.startswith("└─$"):
            if line.startswith("└─$") and " " in line:
                prompt_part, command = line.split(" ", 1)
                d.text((x, yy), prompt_part, font=font_prompt, fill=BLUE)
                pw = d.textlength(prompt_part + " ", font=font_prompt)
                d.text((x + pw, yy), command, font=font_prompt, fill=WHITE)
            else:
                d.text((x, yy), line, font=font_prompt, fill=BLUE)
        elif line == "ABOUT ME":
            d.text((x, yy), line, font=font_heading, fill=PINK)
        elif line.startswith("["):
            prefix, rest = line[:5], line[5:]
            d.text((x, yy), prefix, font=font_text, fill=GREEN)
            pw = d.textlength(prefix, font=font_text)
            d.text((x + pw, yy), rest, font=font_text, fill=WHITE)
        else:
            d.text((x, yy), line, font=font_text, fill=WHITE)

    if cursor_on:
        last_line = lines[-1] if lines else ""
        cy = y + (len(lines) - 1) * line_h + 3
        cx = x + d.textlength(last_line, font=font_text)
        if cy < H - 28:
            d.rectangle((cx + 2, cy, cx + 13, cy + 22), fill=BLUE)

frames, durations = [], []

for _ in range(6):
    img = base_image()
    draw_terminal_text(img, 0, cursor_on=(_ % 2 == 0))
    frames.append(img)
    durations.append(120)

for visible in range(0, len(full_text) + 4, 4):
    img = base_image()
    draw_terminal_text(img, min(visible, len(full_text)), cursor_on=True)
    frames.append(img)
    durations.append(55)

for i in range(18):
    img = base_image()
    draw_terminal_text(img, len(full_text), cursor_on=(i % 2 == 0))
    frames.append(img)
    durations.append(220)

palette_frames = [f.convert("P", palette=Image.Palette.ADAPTIVE, colors=64) for f in frames]
palette_frames[0].save(
    OUT,
    save_all=True,
    append_images=palette_frames[1:],
    duration=durations,
    loop=0,
    optimize=True,
    disposal=2,
)

print(f"Created: {OUT}")
