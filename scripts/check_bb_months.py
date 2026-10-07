import http.cookiejar
import re
import time
import urllib.parse
import urllib.request

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [
    ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"),
    ("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8"),
]

url = "https://www.bb.org.bd/en/index.php/financialactivity/mfsdata"

# GET page
resp = opener.open(url, timeout=30)
html = resp.read().decode("utf-8", errors="ignore")
stmt = re.search(r"comparative summary statement of ([^<\n\r]+)", html)
print(f"Default GET statement: {stmt.group(1).strip() if stmt else 'None'}")
time.sleep(1.0)

for yr in [2025, 2026]:
    for mo in range(1, 13):
        mo_str = f"{mo:02d}"
        data = urllib.parse.urlencode({
            "select_month": mo_str,
            "select_year": str(yr),
            "mfssearch_submit": "Search"
        }).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Origin": "https://www.bb.org.bd",
                "Referer": url,
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        h = opener.open(req, timeout=30).read().decode("utf-8", errors="ignore")
        ths = re.findall(r"<th>Amount in ([^<]+)</th>", h)
        stmt_m = re.search(r"comparative summary statement of ([^<\n\r]+)", h)
        stmt_txt = stmt_m.group(1).strip() if stmt_m else "None"
        has_table = "<table" in h
        print(f"{yr}-{mo_str}: table={has_table} | ths={ths} | stmt='{stmt_txt}'", flush=True)
        time.sleep(1.2)
