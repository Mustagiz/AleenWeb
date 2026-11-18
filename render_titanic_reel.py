import math
import subprocess
import os
from PIL import Image, ImageDraw, ImageFont

WIDTH = 1080
HEIGHT = 1920
FPS = 30
DURATION = 15 # 15 seconds punchy short reel
TOTAL_FRAMES = FPS * DURATION
OUTPUT_FILE = "/Users/faeez/faeez.c/titanic_sinking_reel.mp4"

def get_font(size):
    try:
        # Standard macOS fonts
        return ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", size)
    except:
        try:
            return ImageFont.truetype("/System/Library/Fonts/SFCompact.ttf", size)
        except:
            return ImageFont.load_default()

font_title = get_font(72)
font_caption = get_font(52)
font_highlight = get_font(58)
font_hud = get_font(34)
font_sub = get_font(28)

def render_frame(frame_idx):
    t = frame_idx / FPS
    progress = t / DURATION

    img = Image.new("RGB", (WIDTH, HEIGHT), "#050912")
    draw = ImageDraw.Draw(img)

    # 1. Background Gradient / Stars
    for y in range(HEIGHT):
        if y % 8 == 0:
            ratio = y / HEIGHT
            r = int(5 + ratio * 8)
            g = int(9 + ratio * 20)
            b = int(18 + ratio * 45)
            draw.line([(0, y), (WIDTH, y)], fill=(r, g, b), width=8)

    # 2. Stars
    for i in range(35):
        sx = int((math.sin(i * 123) * 0.5 + 0.5) * WIDTH)
        sy = int((math.cos(i * 77) * 0.5 + 0.5) * (HEIGHT * 0.35))
        draw.rectangle([sx, sy, sx + 3, sy + 3], fill=(255, 255, 255))

    # 3. Iceberg in distance
    draw.polygon([
        (int(WIDTH * 0.72), int(HEIGHT * 0.44)),
        (int(WIDTH * 0.85), int(HEIGHT * 0.28)),
        (int(WIDTH * 0.94), int(HEIGHT * 0.34)),
        (int(WIDTH * 0.99), int(HEIGHT * 0.44))
    ], fill=(45, 95, 140))

    # 4. Telemetry Header (HUD)
    hud_time = "11:40 PM" if t < 3.5 else ("12:20 AM" if t < 7.5 else ("01:40 AM" if t < 11.5 else "02:18 AM"))
    hud_stat = "IMPACT DETECTED" if t < 3.5 else ("BULKHEAD SPILLOVER" if t < 7.5 else ("KEEL OVERBURDEN" if t < 11.5 else "HULL FRACTURE"))

    # Top Tag
    draw.rounded_rectangle([60, 90, 430, 150], radius=30, fill=(15, 25, 45), outline=(0, 240, 255), width=2)
    draw.ellipse([85, 114, 97, 126], fill=(255, 51, 68))
    draw.text((115, 102), "TITANIC ANATOMY", font=font_sub, fill=(0, 240, 255))

    # Top Clock
    draw.rounded_rectangle([WIDTH - 360, 90, WIDTH - 60, 165], radius=15, fill=(12, 18, 30), outline=(50, 70, 95), width=1)
    draw.text((WIDTH - 340, 98), hud_time, font=font_hud, fill=(255, 255, 255))
    draw.text((WIDTH - 340, 134), hud_stat, font=get_font(20), fill=(140, 160, 185))

    # 5. Sinking Simulation (Cross-Section)
    angle = (progress ** 1.8) * 40 # Up to 40 degree angle
    sink_depth = progress * 320
    center_x = WIDTH * 0.48
    center_y = HEIGHT * 0.48 + sink_depth

    # Ship Body
    rad = math.radians(-angle)
    cos_a = math.cos(rad)
    sin_a = math.sin(rad)

    def rot(px, py):
        return (center_x + (px * cos_a - py * sin_a), center_y + (px * sin_a + py * cos_a))

    # Hull Points
    stern = -420
    bow = 420
    p1 = rot(stern, 0)
    p2 = rot(bow - 60, 0)
    p3 = rot(bow + 20, -30)
    p4 = rot(bow + 10, 60)
    p5 = rot(stern + 40, 60)

    # Keel (Red)
    draw.polygon([p1, p2, p3, p4, p5], fill=(140, 28, 28), outline=(210, 50, 50))

    # Upper Hull (Black)
    u1 = rot(stern - 15, -60)
    u2 = rot(bow - 30, -60)
    draw.polygon([u1, u2, p3, p1], fill=(16, 22, 32), outline=(45, 60, 80))

    # Funnels
    for fx in [stern + 220, stern + 330, stern + 440, stern + 550]:
        f_base = rot(fx, -60)
        f_top = rot(fx + 15, -130)
        draw.line([f_base, f_top], fill=(215, 155, 85), width=28)
        f_tip = rot(fx + 10, -108)
        draw.line([f_tip, f_top], fill=(20, 20, 20), width=28)

    # Watertight Bulkheads & Flood level
    num_bulkheads = 12
    step = 700 / num_bulkheads
    flooded = min(num_bulkheads, int(progress * 15))
    for b_idx in range(num_bulkheads):
        bx = bow - 60 - (b_idx * step)
        bt = rot(bx, -60)
        bb = rot(bx, 50)
        draw.line([bt, bb], fill=(80, 110, 140), width=3)
        if b_idx < flooded:
            # Water in compartment
            w_top = rot(bx - step * 0.5, 45 - min(90, (flooded - b_idx) * 28))
            draw.ellipse([w_top[0]-14, w_top[1]-14, w_top[0]+14, w_top[1]+14], fill=(0, 240, 255))

    # Breakup Stress Line at high angle
    if t > 10.5:
        b_x = stern + 380
        bp1 = rot(b_x, -160)
        bp2 = rot(b_x, 90)
        draw.line([bp1, bp2], fill=(255, 51, 68), width=8)
        draw.text((WIDTH * 0.5 - 280, HEIGHT * 0.38), "KEEL SNAP POINT", font=font_title, fill=(255, 51, 68))

    # 6. Water Surface Line
    sea_y = int(HEIGHT * 0.46)
    draw.rectangle([0, sea_y, WIDTH, HEIGHT], fill=(4, 18, 38))
    for x in range(0, WIDTH, 40):
        wave = int(math.sin(x * 0.02 + t * 4) * 8)
        draw.line([(x, sea_y + wave), (x + 40, sea_y + wave)], fill=(0, 180, 255), width=4)

    # 7. Kinetic Captions
    if t < 3.5:
        cap_line1 = "THE TITANIC"
        cap_line2 = "DIDN'T SINK JUST FROM ICE"
        c_fill = (255, 190, 59)
    elif t < 7.5:
        cap_line1 = "THE FATAL DESIGN FLAW:"
        cap_line2 = "BULKHEADS OPEN AT CEILING"
        c_fill = (0, 240, 255)
    elif t < 11.5:
        cap_line1 = "THE ICE CUBE EFFECT"
        cap_line2 = "WATER SPILLED WALL TO WALL"
        c_fill = (255, 190, 59)
    else:
        cap_line1 = "40,000 TONS OF WATER"
        cap_line2 = "SNAPPED THE SHIP IN HALF"
        c_fill = (255, 51, 68)

    # Center Caption Box
    box_y = int(HEIGHT * 0.72)
    draw.rounded_rectangle([70, box_y, WIDTH - 70, box_y + 190], radius=24, fill=(4, 8, 16), outline=(60, 85, 120), width=2)
    draw.text((WIDTH * 0.5 - draw.textlength(cap_line1, font=font_caption)*0.5, box_y + 25), cap_line1, font=font_caption, fill=(255, 255, 255))
    draw.text((WIDTH * 0.5 - draw.textlength(cap_line2, font=font_highlight)*0.5, box_y + 100), cap_line2, font=font_highlight, fill=c_fill)

    # 8. Bottom Telemetry Cards
    draw.rounded_rectangle([70, HEIGHT - 180, 360, HEIGHT - 80], radius=16, fill=(12, 18, 30), outline=(40, 60, 85))
    draw.text((100, HEIGHT - 165), f"{int(min(45, angle))}°", font=font_title, fill=(255, 255, 255))
    draw.text((100, HEIGHT - 105), "BOW TILT", font=font_sub, fill=(130, 150, 175))

    draw.rounded_rectangle([380, HEIGHT - 180, 690, HEIGHT - 80], radius=16, fill=(12, 18, 30), outline=(40, 60, 85))
    draw.text((410, HEIGHT - 165), f"{flooded}/16", font=font_title, fill=(0, 240, 255))
    draw.text((410, HEIGHT - 105), "COMPARTMENTS", font=font_sub, fill=(130, 150, 175))

    draw.rounded_rectangle([710, HEIGHT - 180, WIDTH - 70, HEIGHT - 80], radius=16, fill=(12, 18, 30), outline=(40, 60, 85))
    draw.text((740, HEIGHT - 165), "400T/m", font=font_title, fill=(255, 51, 68))
    draw.text((740, HEIGHT - 105), "INRUSH RATE", font=font_sub, fill=(130, 150, 175))

    return img

def main():
    print("Starting reel render with ffmpeg...")
    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-", # stdin
        # Generate dramatic audio synth: deep sub-bass drone and sonar tone
        "-f", "lavfi",
        "-i", f"aevalsrc=0.15*sin(2*PI*55*t)+0.04*sin(2*PI*220*t):d={DURATION}",
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        OUTPUT_FILE
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    for i in range(TOTAL_FRAMES):
        frame = render_frame(i)
        proc.stdin.write(frame.tobytes())
        if i % (FPS * 2) == 0:
            print(f"Rendered {i}/{TOTAL_FRAMES} frames ({int(i/TOTAL_FRAMES*100)}%)...")

    proc.stdin.close()
    proc.wait()
    print(f"Video created successfully at: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
