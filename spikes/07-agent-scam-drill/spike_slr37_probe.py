# Spike 07-agent-scam-drill — SLR37 bn_bd.zip partial read via HTTP Range (2026-10-02)
# Q: can we confirm SLR37 TTS content (speakers, utterance count) WITHOUT downloading 586MB?
import urllib.request, zipfile, io, struct

URL = "https://openslr.trmal.net/resources/37/bn_bd.zip"

class RangedFile(io.RawIOBase):
    def __init__(self, url):
        self.url = url; self.pos = 0
        req = urllib.request.Request(url, method="HEAD")
        r = urllib.request.urlopen(req, timeout=60)
        self.size = int(r.headers["Content-Length"])
        print("remote size:", self.size, "bytes")
    def seekable(self): return True
    def readable(self): return True
    def seek(self, off, whence=0):
        self.pos = off if whence == 0 else (self.size + off if whence == 2 else self.pos + off)
        return self.pos
    def tell(self): return self.pos
    def read(self, n=-1):
        if n == -1: n = self.size - self.pos
        if n <= 0: return b""
        end = min(self.pos + n, self.size) - 1
        req = urllib.request.Request(self.url, headers={"Range": f"bytes={self.pos}-{end}"})
        data = urllib.request.urlopen(req, timeout=120).read()
        self.pos += len(data)
        return data

f = RangedFile(URL)
zf = zipfile.ZipFile(f)
names = zf.namelist()
print("zip entries:", len(names))
print([n for n in names if n.endswith(".tsv")])
tsv_name = [n for n in names if n.endswith("line_index.tsv")][0]
with zf.open(tsv_name) as tsv:
    lines = tsv.read().decode("utf-8").splitlines()
print("utterances in line_index.tsv:", len(lines))
print("first 3 lines:")
for l in lines[:3]: print(" ", l[:120])
# speaker count from file IDs (format typically: speaker-utterance)
speakers = set(l.split("\t")[0].split("_")[0] for l in lines if "\t" in l)
print("distinct speaker prefixes:", len(speakers), sorted(speakers)[:10])
