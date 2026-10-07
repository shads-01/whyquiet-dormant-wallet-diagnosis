# Spike 09: minimal khata-line OCR floor test (tesseract, LLM-free)
# Synthesizes 3 khata-style lines (printed Bangla, NOT handwriting - this is an
# upper-bound floor test; real khata pages are handwritten and will be worse).
# Run: python spike_ocr.py
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from PIL import Image, ImageDraw, ImageFont
import pytesseract
import os

TESS = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
TESSDATA = os.path.abspath(r"spikes\09-baki-settle\tessdata")
pytesseract.pytesseract.tesseract_cmd = TESS
FONT = r"spikes\09-baki-settle\NotoSansBengali-Regular.ttf"  # downloaded Noto Sans Bengali (OFL)

# 3 khata-style lines: customer name (Bangla) + item + amount (Bangla digits)
lines = [
    "করিম মিয়া      চাল ৫ কেজি     ৪৫০",
    "রহিমা বেগম    সরিষার তেল ১ লিটার  ৩২০",
    "আব্দুল জলিল   ডিম ১২টি        ১৬৮",
]
truth_amounts = ["৪৫০", "৩২০", "১৬৮"]

font = ImageFont.truetype(FONT, 36, index=0)  # Nirmala.ttc collection; index 0 = Bangla
img = Image.new("RGB", (900, 60 * len(lines) + 40), "white")
d = ImageDraw.Draw(img)
for i, ln in enumerate(lines):
    d.text((20, 20 + i * 60), ln, fill="black", font=font)
img.save(r"spikes\09-baki-settle\khata_synth.png")

out = pytesseract.image_to_string(
    img, lang="ben", config=f"--tessdata-dir {TESSDATA} --psm 6")
print("=== RAW OCR OUTPUT ===")
print(out)
print("=== AMOUNT MATCH CHECK ===")
ok = 0
for t in truth_amounts:
    hit = t in out
    ok += hit
    print(f"truth {t}: {'FOUND' if hit else 'MISSING'}")
print(f"RESULT: {ok}/3 amounts recovered on CLEAN printed Bangla lines")
