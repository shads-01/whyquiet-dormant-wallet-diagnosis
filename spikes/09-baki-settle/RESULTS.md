# Spike 09 results — Baki-Settle OCR floor test (2026-10-02)

## Environment
- Python 3.14.6, pip 26.2.1 (checked: `python --version`, `pip --version`)
- Tesseract NOT preinstalled → installed via `winget install --id UB-Mannheim.TesseractOCR` → tesseract v5.4.0.20240606 (eng+osd only)
- Downloaded `ben.traineddata` (tessdata_fast, 856 KB) from https://github.com/tesseract-ocr/tessdata_fast into `tessdata/`
- `pip install pillow pytesseract` (pillow 12.3.0)
- Bangla font: Windows Fonts copy was permission-blocked; downloaded Noto Sans Bengali Regular (OFL) from https://github.com/notofonts/notofonts.github.io

## What ran
`python spike_ocr.py` — renders 3 khata-style lines (Bangla name + item + Bangla-digit amount) with PIL, OCRs with tesseract `lang=ben --psm 6`.

## REAL results
```
করমি মি চাল ৫ কজেটি ৪৫০        <- truth: করিম মিয়া চাল ৫ কেজি ৪৫০
রহমা বগেম সরষার তলে ১ লটার ৩২০
আব্দুল জললি ডমি ১২টি ১৬৮
RESULT: 3/3 amounts recovered on CLEAN printed Bangla lines
```
- Amounts (the money-critical field): **3/3 exact**.
- Names/items: heavily degraded even on CLEAN PRINTED text (vowel signs dropped: মিয়া→মি, বেগম→বগেম).

## Interpretation
- This is an **upper-bound floor test** (printed, clean, 36px). Real khata pages are handwritten, skewed, mixed-script → accuracy will be materially worse. UNVERIFIED until real pages are photographed.
- Implication for Baki-Settle: digit/amount extraction is feasible even LLM-free; name matching needs a better engine (NumtaDB fine-tune or LLM-vision) — the critique's falsifier (≥90% entry accuracy) is NOT met by tesseract alone on names.

## Commands run
```
winget install --id UB-Mannheim.TesseractOCR
Invoke-WebRequest https://github.com/tesseract-ocr/tessdata_fast/raw/main/ben.traineddata -OutFile spikes\09-baki-settle\tessdata\ben.traineddata
pip install pillow pytesseract
python spikes\09-baki-settle\spike_ocr.py
```
