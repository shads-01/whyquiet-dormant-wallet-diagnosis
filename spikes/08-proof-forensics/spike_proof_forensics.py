# Spike 08-proof-forensics — real-vs-forged screenshot statistics (2026-10-02)
# Q: do simple image statistics separate REAL app screenshots from EDITED ones?
# Method: render 3 mock "real" bKash-style payment screenshots with PIL (fresh render = clean
# single-encode JPEG, like a phone screenshot), then forge 3 by editing a rendered one
# (paste new amount digits, re-save = double JPEG compression). Compare: EXIF presence,
# quantization tables, ELA (error-level analysis) mean, local noise variance.
import os, io, json
from PIL import Image, ImageDraw, ImageFont, ImageChops, ImageFilter

OUT = "spikes/08-proof-forensics"
os.makedirs(OUT, exist_ok=True)

def get_font(size):
    for p in [r"C:\Windows\Fonts\arialbd.ttf", r"C:\Windows\Fonts\arial.ttf", r"C:\Windows\Fonts\segoeui.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except Exception: pass
    return ImageFont.load_default()

def render_proof(amount, txn, sender, path):
    """Mock MFS payment-success screenshot (green header, white body)."""
    W, H = 720, 1280
    img = Image.new("RGB", (W, H), (237, 240, 244))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 220], fill=(224, 32, 82))          # brand header
    d.text((40, 60), "Payment Successful", font=get_font(44), fill=(255, 255, 255))
    d.text((40, 130), "Send Money", font=get_font(28), fill=(255, 220, 230))
    d.text((40, 280), f"৳ {amount}", font=get_font(72), fill=(20, 20, 20))
    d.text((40, 400), f"TrxID {txn}", font=get_font(30), fill=(60, 60, 60))
    d.text((40, 460), f"Sender {sender}", font=get_font(30), fill=(60, 60, 60))
    d.text((40, 520), "Fee ৳ 0.00   Balance ৳ 8,542.17", font=get_font(26), fill=(90, 90, 90))
    d.text((40, 620), "02 Oct 2026, 09:41 PM", font=get_font(26), fill=(90, 90, 90))
    # subtle screen noise like a real phone capture
    import random
    random.seed(hash(path) % 2**31)
    px = img.load()
    for _ in range(4000):
        x, y = random.randrange(W), random.randrange(H)
        r, g, b = px[x, y]
        j = random.randint(-3, 3)
        px[x, y] = (max(0, min(255, r + j)), max(0, min(255, g + j)), max(0, min(255, b + j)))
    img.save(path, "JPEG", quality=92)  # single encode, like a phone screenshot
    return img

def forge(src_img, path, new_amount="৯,৯৯৯"):
    """Edit the amount region and re-save -> double JPEG compression artefacts."""
    img = src_img.copy()
    d = ImageDraw.Draw(img)
    d.rectangle([30, 260, 500, 380], fill=(237, 240, 244))   # wipe amount
    d.text((40, 280), f"৳ {new_amount}", font=get_font(72), fill=(20, 20, 20))
    img.save(path, "JPEG", quality=88)  # re-encode at different quality = double compression

def ela_mean(path, quality=90):
    img = Image.open(path).convert("RGB")
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=quality)
    resaved = Image.open(buf).convert("RGB")
    ela = ImageChops.difference(img, resaved)
    stat = ela.convert("L")
    hist = stat.histogram()
    total = sum(hist); mean = sum(i * c for i, c in enumerate(hist)) / total
    return mean

def noise_var(path):
    img = Image.open(path).convert("L")
    high = ImageChops.difference(img, img.filter(ImageFilter.GaussianBlur(1)))
    h = high.histogram(); total = sum(h)
    mean = sum(i * c for i, c in enumerate(h)) / total
    var = sum(((i - mean) ** 2) * c for i, c in enumerate(h)) / total
    return var

def has_exif(path):
    return len(Image.open(path).getexif()) > 0

def qtable(path):
    return Image.open(path).quantization

reals, forgeries = [], []
specs = [("1,500", "BJK4P9X2T1", "017XXXXXXXX"), ("850", "9NA G7T2KQ", "018XXXXXXXX"), ("12,000", "C4HK2M8PZQ", "019XXXXXXXX")]
for i, (amt, txn, snd) in enumerate(specs, 1):
    rp = f"{OUT}/real_{i}.jpg"
    img = render_proof(amt, txn, snd, rp)
    reals.append(rp)
    fp = f"{OUT}/forge_{i}.jpg"
    forge(img, fp)
    forgeries.append(fp)

print(f"{'file':16s} {'EXIF':5s} {'ELA_mean':9s} {'noise_var':10s} {'qtables':8s}")
rows = []
for p in reals + forgeries:
    e, ela, nv, q = has_exif(p), ela_mean(p), noise_var(p), len(qtable(p))
    label = "REAL" if "real" in p else "FORGE"
    print(f"{os.path.basename(p):16s} {str(e):5s} {ela:9.3f} {nv:10.3f} {q:8d}  {label}")
    rows.append({"file": p, "label": label, "exif": e, "ela_mean": round(ela, 3), "noise_var": round(nv, 3), "qtables": q})

# simple threshold classifier on ELA mean: pick midpoint between group means
import statistics
r_ela = [r["ela_mean"] for r in rows if r["label"] == "REAL"]
f_ela = [r["ela_mean"] for r in rows if r["label"] == "FORGE"]
thr = (statistics.mean(r_ela) + statistics.mean(f_ela)) / 2
correct = sum((r["ela_mean"] > thr) == (r["label"] == "FORGE") for r in rows)
print(f"\nELA threshold {thr:.3f}: {correct}/6 classified correctly")
print(f"REAL ELA means: {[round(x,3) for x in r_ela]}  FORGED ELA means: {[round(x,3) for x in f_ela]}")
json.dump({"rows": rows, "ela_threshold": round(thr, 3), "ela_acc": correct / 6},
          open(f"{OUT}/results.json", "w"), indent=2)
print("saved spikes/08-proof-forensics/results.json")
