"""Build manifest.json from raw Notion fetch dumps and report crawl completeness."""
import json
import re
import sys
from pathlib import Path

RAW = Path(sys.argv[1])
OUT = Path(sys.argv[2])

META_RE = re.compile(r"^<!-- meta: (\{.*\}) -->", re.M)
CHILD_RE = re.compile(r'<page url="https://app\.notion\.com/p/([0-9a-f]{32})">(.*?)</page>')
DB_RE = re.compile(r"<database|<data-source")
IMG_RE = re.compile(r"!\[[^\]]*\]\(notion-file-block://[^)]*\)")
BOOKMARK_RE = re.compile(r'<unknown url="[^"]*#([0-9a-f]{32})" alt="bookmark"/>')
OTHER_UNKNOWN_RE = re.compile(r'<unknown url="[^"]*#([0-9a-f]{32})" alt="(?!bookmark)([^"]+)"/>')

pages = {}
for f in sorted(RAW.glob("*.md")):
    text = f.read_text(encoding="utf-8")
    meta = json.loads(META_RE.search(text).group(1))
    content = text.split("<content>", 1)[1].rsplit("</content>", 1)[0]
    children = [(cid, title) for cid, title in CHILD_RE.findall(content)]
    pages[meta["id"]] = {
        **meta,
        "children": [c for c, _ in children],
        "images": len(IMG_RE.findall(content)),
        "bookmarks": BOOKMARK_RE.findall(content),
        "other_unknown": OTHER_UNKNOWN_RE.findall(content),
        "has_database": bool(DB_RE.search(content)),
    }

missing = []
for pid, p in pages.items():
    for c in p["children"]:
        if c not in pages:
            missing.append((pid, c))
        elif pages[c]["parent"] != pid:
            print(f"PARENT MISMATCH: {c} meta parent={pages[c]['parent']} but listed under {pid}")

orphans = [pid for pid, p in pages.items() if p["parent"] and p["parent"] not in pages]

OUT.write_text(json.dumps(pages, indent=2, ensure_ascii=False), encoding="utf-8")

print(f"pages: {len(pages)}")
print(f"top-level: {sum(1 for p in pages.values() if not p['parent'])}")
print(f"databases: {sum(p['has_database'] for p in pages.values())}")
print(f"images: {sum(p['images'] for p in pages.values())}")
print(f"bookmarks: {sum(len(p['bookmarks']) for p in pages.values())} across {sum(1 for p in pages.values() if p['bookmarks'])} pages")
print(f"other unknown blocks: {[(p['title'], u) for p in pages.values() for u in p['other_unknown']]}")
print(f"missing children: {missing}")
print(f"orphans: {orphans}")

def depth(pid):
    d = 0
    while pages[pid]["parent"]:
        pid = pages[pid]["parent"]
        d += 1
    return d
print(f"max depth: {max(depth(p) for p in pages)}")
