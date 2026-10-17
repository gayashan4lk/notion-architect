"""Convert raw Notion fetch dumps into a GitHub-friendly Markdown tree.

Usage: python3 convert.py <export_dir> <out_dir>

<export_dir> holds:
  raw/<page_id>.md   raw Notion "enhanced markdown" from the Notion connector
  manifest.json      built by manifest.py
  bookmarks.json     optional {block_id: {"url": ..., "title": ...}}
  assets/            optional; files named <file_block_id>__<name>, copied into _assets/
  roots.json         optional list of top-level page IDs in sidebar order (else alphabetical)

Layout rules:
  page with subpages -> <slug>/README.md
  page without       -> <slug>.md
"""
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path
from posixpath import relpath

EXPORT = Path(sys.argv[1])
OUT = Path(sys.argv[2])

pages = json.loads((EXPORT / "manifest.json").read_text(encoding="utf-8"))
bm_file = EXPORT / "bookmarks.json"
bookmarks = json.loads(bm_file.read_text(encoding="utf-8")) if bm_file.exists() else {}
asset_dir = EXPORT / "assets"
available_assets = {}
if asset_dir.exists():
    for f in asset_dir.iterdir():
        if "__" not in f.name:
            continue
        block_id, _, name = f.name.partition("__")
        available_assets[block_id.replace("-", "")] = f

# A copied image block gets a new block ID but keeps its file ID, so also index assets by file ID.
FILE_REF_RE = re.compile(r"notion-file-block://([0-9a-f-]+)/([0-9a-f-]+)")
assets_by_file = {}
index_file = asset_dir / "files.json"  # {file_id: asset filename}, kept so moved/copied images still match
if index_file.exists():
    for fid, fname in json.loads(index_file.read_text(encoding="utf-8")).items():
        if (asset_dir / fname).exists():
            assets_by_file[fid] = asset_dir / fname
for raw_file in (EXPORT / "raw").glob("*.md"):
    for blk, fid in FILE_REF_RE.findall(raw_file.read_text(encoding="utf-8")):
        if blk.replace("-", "") in available_assets:
            assets_by_file[fid] = available_assets[blk.replace("-", "")]

report = {"bookmarks_missing": [], "images_missing": [], "embeds": [], "highlights": []}


def notion_url(pid, block=None):
    return f"https://www.notion.so/{pid}" + (f"#{block}" if block else "")


def slugify(title):
    s = title.lower().replace("&", " and ").replace("+", "p")
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "untitled"


# ---------- path assignment ----------
roots = [pid for pid, p in pages.items() if not p["parent"]]
order = {}  # child order as it appears in parent content
for pid, p in pages.items():
    for i, c in enumerate(p["children"]):
        order[c] = i
roots_file = EXPORT / "roots.json"
if roots_file.exists():
    sidebar = json.loads(roots_file.read_text(encoding="utf-8"))
    roots.sort(key=lambda pid: (sidebar.index(pid) if pid in sidebar else len(sidebar), pages[pid]["title"].lower()))
else:
    roots.sort(key=lambda pid: pages[pid]["title"].lower())

paths = {}  # pid -> path of the page's .md (posix, relative to OUT)


def assign(pid, parent_dir):
    p = pages[pid]
    siblings_taken = assign.taken.setdefault(parent_dir, set())
    base = slugify(p["title"])
    slug, n = base, 2
    while slug in siblings_taken:
        slug, n = f"{base}-{n}", n + 1
    siblings_taken.add(slug)
    if p["children"]:
        d = f"{parent_dir}/{slug}" if parent_dir else slug
        paths[pid] = f"{d}/README.md"
        for c in p["children"]:
            assign(c, d)
    else:
        paths[pid] = f"{parent_dir}/{slug}.md" if parent_dir else f"{slug}.md"


assign.taken = {"": {"readme", "tools", "_assets", "_export-report", "archive"}}
for r in roots:
    assign(r, "")


def link(from_pid, to_pid):
    src_dir = str(Path(paths[from_pid]).parent)
    return relpath(paths[to_pid], src_dir if src_dir != "." else ".")


# ---------- inline fixes ----------
BOLD_RE = re.compile(r"\*\*(.+?)\*\*")
EDGE_RE = re.compile(r"^((?:\s|<br>)*)(.*?)((?:\s|<br>)*)$", re.S)


def fix_bold(text):
    """Notion puts spaces/<br> just inside ** markers, which GFM won't render as bold."""
    def repl(m):
        inner = m.group(1)
        lead, core, trail = EDGE_RE.match(inner).groups()
        if not core.strip():
            return lead + trail
        return f"{lead}**{core}**{trail}"
    return BOLD_RE.sub(repl, text)


SPAN_RE = re.compile(r'<span color="([^"]+)">(.*?)</span>', re.S)
IMG_RE = re.compile(r"!\[([^\]]*)\]\((notion-file-block://([0-9a-f-]+)/([0-9a-f-]+)[^)]*?name=([^)&]+)[^)]*)\)")
PAGE_RE = re.compile(r'^<page url="https://app\.notion\.com/p/([0-9a-f]{32})">(.*?)</page>$')
UNKNOWN_RE = re.compile(r'^<unknown url="https://app\.notion\.com/p/([0-9a-f]{32})#([0-9a-f]{32})" alt="([^"]+)"/>$')
PREVIEW_RE = re.compile(r'^<link-preview url="[^"]*" source="([^"]+)" />$')
CALLOUT_OPEN_RE = re.compile(r'^<callout icon="([^"]*)" color="[^"]*">$')
MENTION_RE = re.compile(r'<mention-page url="https://app\.notion\.com/p/([0-9a-f]{32})"\s*/>')
NOTION_LINK_RE = re.compile(r'\]\(https://(?:app\.notion\.com|www\.notion\.so)/p/([0-9a-f]{32})\)')
TD_RE = re.compile(r"<td>(.*?)</td>", re.S)
SUMMARY_RE = re.compile(r"^<summary>(.*)</summary>$")


def inline(text, pid):
    def span(m):
        report["highlights"].append(pages[pid]["title"])
        return m.group(2)
    text = SPAN_RE.sub(span, text)
    text = MENTION_RE.sub(lambda m: f"[{pages[m.group(1)]['title']}]({link(pid, m.group(1))})"
                          if m.group(1) in pages else f"[Notion page]({notion_url(m.group(1))})", text)
    text = NOTION_LINK_RE.sub(lambda m: f"]({link(pid, m.group(1))})" if m.group(1) in pages
                              else f"]({notion_url(m.group(1))})", text)

    def img(m):
        alt, _ref, block, file_id, name = m.groups()
        f = available_assets.get(block.replace("-", "")) or assets_by_file.get(file_id)
        if f:
            page = Path(paths[pid])
            base = page.parent if page.name == "README.md" else page.with_suffix("")
            asset_rel = f"_assets/{base.as_posix()}/{name}"
            dest = OUT / asset_rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(f, dest)
            return f"![{alt or name}]({relpath(asset_rel, str(Path(paths[pid]).parent))})"
        report["images_missing"].append((pages[pid]["title"], name))
        return f"[🖼️ Image: {name} (view in Notion)]({notion_url(pid, block.replace('-', ''))})"
    text = IMG_RE.sub(img, text)
    return fix_bold(text)


def gh_anchor(heading):
    """GitHub's heading anchor: lowercase, drop punctuation, spaces to hyphens."""
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", heading)
    text = text.replace("**", "").replace("`", "").strip().lower()
    return re.sub(r"[^\w\- ]", "", text).replace(" ", "-")


INDENT = "   "  # 3 spaces nests correctly under both "- " and "1. " list items


# ---------- block conversion ----------
def convert_page(pid):
    raw = (EXPORT / "raw" / f"{pid}.md").read_text(encoding="utf-8")
    content = raw.split("<content>\n", 1)[1].rsplit("</content>", 1)[0]
    lines = content.split("\n")
    out = []          # list of (kind, text) blocks
    code = None       # {"indent": str, "lines": [...]} while inside a fenced block
    callout = None
    table = None
    details = None
    toc_at = None
    for line in lines:
        body = line.lstrip("\t")
        depth = len(line) - len(body)
        if code is not None:
            code["lines"].append(line if not body.startswith("```") else body)
            if body.startswith("```"):
                out.append(("list" if code["indent"] else "code",
                            "\n".join(code["indent"] + l if l else l for l in code["lines"])))
                code = None
            continue
        if body.startswith("```"):
            code = {"indent": INDENT * depth, "lines": [body]}
            continue
        if callout is not None:
            if line == "</callout>":
                # a heading can't follow the icon on the same line, so headings inside callouts become plain text
                body_lines = [inline(l.lstrip("#").strip() if l.startswith("#") else l, pid) for l in callout["lines"]]
                text = "\n>\n".join(f"> {l}" for l in body_lines)
                text = text.replace("> ", f"> {callout['icon']} ", 1) if callout["icon"] else text
                out.append(("quote", text))
                callout = None
            else:
                callout["lines"].append(line[1:] if line.startswith("\t") else line)
            continue
        m = CALLOUT_OPEN_RE.match(line)
        if m:
            callout = {"icon": m.group(1), "lines": []}
            continue
        if table is not None:
            if line.startswith("</table>"):
                rows = table["rows"]
                if rows:
                    width = max(len(r) for r in rows)
                    rows = [r + [""] * (width - len(r)) for r in rows]
                    head, rest = (rows[0], rows[1:]) if table["header"] else ([""] * width, rows)
                    md_rows = ["| " + " | ".join(head) + " |", "|" + "---|" * width]
                    md_rows += ["| " + " | ".join(r) + " |" for r in rest]
                    out.append(("table", "\n".join(md_rows)))
                table = None
            elif body.startswith("<tr>"):
                table["rows"].append([])
            elif body.startswith("<td>"):
                cell = TD_RE.search(body).group(1)
                table["rows"][-1].append(inline(cell, pid).replace("|", "\\|"))
            continue
        if body.startswith("<table ") or body.startswith("<table>"):
            table = {"header": 'header-row="true"' in body, "rows": []}
            continue
        if details is not None:
            if body.startswith("</details>"):
                inner = "\n\n".join(inline(l, pid) for l in details["lines"] if l.strip())
                out.append(("details", f"<details>\n<summary>{inline(details['summary'], pid)}</summary>\n\n{inner}\n\n</details>"))
                details = None
            elif SUMMARY_RE.match(body):
                details["summary"] = SUMMARY_RE.match(body).group(1)
            else:
                details["lines"].append(body)
            continue
        if body.startswith("<details"):
            details = {"summary": "", "lines": []}
            continue
        if body.strip() == "<table_of_contents/>":
            toc_at = len(out)
            out.append(("toc", ""))
            continue
        if line.strip() == "<empty-block/>" or not line.strip():
            out.append(("blank", ""))
            continue
        m = PAGE_RE.match(line.strip())
        if m:
            cid, title = m.groups()
            out.append(("list", f"- 📄 [{title}]({link(pid, cid)})"))
            continue
        m = UNKNOWN_RE.match(line.strip())
        if m:
            _page, block, kind = m.groups()
            if kind == "bookmark":
                b = bookmarks.get(block)
                if b and b.get("url"):
                    label = b.get("title") or b["url"]
                    out.append(("para", f"🔖 [{label}]({b['url']})"))
                else:
                    report["bookmarks_missing"].append((pages[pid]["title"], block))
                    out.append(("para", f"🔖 [Bookmark — link not exported (open in Notion)]({notion_url(pid, block)})"))
            else:
                report["embeds"].append((pages[pid]["title"], kind, block))
                out.append(("para", f"> ⚠️ Embedded content not exported — [view in Notion]({notion_url(pid, block)})"))
            continue
        m = PREVIEW_RE.match(line.strip())
        if m:
            out.append(("para", f"🔗 [{m.group(1)}]({m.group(1)})"))
            continue

        # indentation: tabs mean "child of previous block"
        if body.startswith("- - "):          # Notion's flattened nested bullet
            depth, body = depth + 1, body[2:]
        is_list = bool(re.match(r"^(- |\d+\. )", body))
        if body.startswith("#"):
            hashes = len(body) - len(body.lstrip("#"))
            body = "#" * min(hashes + 1, 6) + body[hashes:]
            out.append(("heading", inline(body, pid)))
        elif body.strip() == "---":
            out.append(("hr", "---"))
        elif is_list:
            out.append(("list", INDENT * depth + inline(body, pid)))
        elif depth and out and out[-1][0] == "list":
            # an indented line under a list item continues that item on its own line
            prev_kind, prev = out[-1]
            sep = "\n\n" if prev.rstrip().endswith("```") else "<br>\n"
            out[-1] = (prev_kind, prev + sep + INDENT * depth + inline(body, pid))
        elif body.startswith(">"):
            out.append(("quote", inline(body, pid)))
        else:
            out.append(("para", inline(body, pid)))

    if toc_at is not None:
        heads = [t for k, t in out if k == "heading"]
        entries = []
        for h in heads:
            level = len(h) - len(h.lstrip("#"))
            text = h.lstrip("#").strip()
            entries.append(f"{INDENT * (level - 2)}- [{re.sub(r'[*`]', '', text)}](#{gh_anchor(text)})")
        out[toc_at] = ("toc", "**Contents**\n\n" + "\n".join(entries))

    # join blocks: lists stay tight, everything else separated by blank lines
    md, prev = [], None
    for kind, text in out:
        if kind == "blank":
            prev = "blank"
            continue
        if md and not (kind == "list" and prev == "list"):
            md.append("")
        md.append(text)
        prev = kind
    return "\n".join(md).strip() + "\n"


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def breadcrumb(pid):
    chain, cur = [], pages[pid]["parent"]
    while cur:
        chain.append(cur)
        cur = pages[cur]["parent"]
    crumbs = [f"[Architect]({relpath('README.md', str(Path(paths[pid]).parent))})"]
    crumbs += [f"[{pages[c]['title']}]({link(pid, c)})" for c in reversed(chain)]
    return " / ".join(crumbs)


written = 0
for pid, p in pages.items():
    fm = ["---", f"title: {yaml_str(p['title'])}", f"notion_id: {pid}",
          f"notion_url: {notion_url(pid)}", f"last_edited: {p['last_edited']}"]
    if p.get("icon"):
        fm.append(f"icon: {yaml_str(p['icon'])}")
    if p.get("cover"):
        fm.append(f"cover: {yaml_str(p['cover'])}")
    fm.append("---")
    title = f"{p['icon']} {p['title']}" if p.get("icon") else p["title"]
    body = convert_page(pid)
    doc = "\n".join(fm) + f"\n\n{breadcrumb(pid)}\n\n# {title}\n\n" + body
    dest = OUT / paths[pid]
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(doc, encoding="utf-8")
    written += 1


# ---------- root README (workspace map) ----------
def tree(pid, depth):
    p = pages[pid]
    lines = [f"{'  ' * depth}- [{p['title']}]({paths[pid]})"]
    for c in p["children"]:
        lines += tree(c, depth + 1)
    return lines


today = date.today().isoformat()
readme = [
    "# Architect — Notion workspace backup", "",
    f"A Markdown snapshot of the **Architect** Notion workspace, exported on {today}. "
    f"{len(pages)} pages across {len(roots)} top-level sections.", "",
    "Every page keeps its Notion ID and URL in its frontmatter, so anything here can be traced back to the original. "
    "Pages that have subpages are folders with a `README.md`; the rest are single `.md` files."
    + (" Images live in [`_assets/`](_assets/), mirroring the page structure." if (OUT / "_assets").exists() else ""), "",
    "See [`_export-report.md`](_export-report.md) for anything that could not be carried over, "
    "and [`tools/notion-export/`](tools/notion-export/) for how this was produced.", "",
] + ([
    "Earlier snapshots of the workspace, from before it was reorganized, are kept unchanged in [`archive/`](archive/).", "",
] if (OUT / "archive").exists() else []) + [
    "## Workspace map", "",
]
for r in roots:
    readme += tree(r, 0)
(OUT / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

# ---------- export report ----------
rep = [
    "# Export report", "",
    f"Snapshot taken {today} from the Notion workspace **Architect**.", "",
    "## Counts", "",
    "| | |", "|---|---|",
    f"| Pages exported | {written} |",
    f"| Top-level sections | {len(roots)} |",
    f"| Databases | {sum(p['has_database'] for p in pages.values())} |",
    f"| Images | {sum(p['images'] for p in pages.values())} ({sum(p['images'] for p in pages.values()) - len(report['images_missing'])} downloaded) |",
    f"| Bookmarks | {sum(len(p['bookmarks']) for p in pages.values())} ({sum(len(p['bookmarks']) for p in pages.values()) - len(report['bookmarks_missing'])} with recovered URLs) |",
    "",
]
if report["embeds"]:
    rep += ["## Embedded content not exported", "",
            "Notion's connector doesn't expose these blocks; each spot links back to Notion.", ""]
    rep += [f"- **{t}** — {k} (`{b}`)" for t, k, b in report["embeds"]] + [""]
if report["bookmarks_missing"]:
    rep += ["## Bookmarks without a recovered URL", "",
            "These render as a link back to the bookmark in Notion.", ""]
    rep += [f"- **{t}** — `{b}`" for t, b in report["bookmarks_missing"]] + [""]
if report["images_missing"]:
    rep += ["## Images not downloaded", "", "These render as a link back to Notion.", ""]
    rep += [f"- **{t}** — {n}" for t, n in report["images_missing"]] + [""]
rep += [
    "## What changes in the conversion", "",
    "- Callouts become blockquotes that keep their emoji.",
    "- Text highlight colours are dropped (the text itself is kept)"
    + (f": {', '.join(sorted(set(report['highlights'])))}." if report["highlights"] else "."),
    "- Headings shift down one level, since each page's title is its `#` heading.",
    "- Link previews become plain links.",
    "- Toggles become collapsible `<details>` sections, and a Notion table of contents becomes a linked list of the page's headings.",
    "- Comments are not included.",
    "",
]
(OUT / "_export-report.md").write_text("\n".join(rep), encoding="utf-8")

print(f"wrote {written} pages to {OUT}")
print(f"bookmarks missing: {len(report['bookmarks_missing'])}, images missing: {len(report['images_missing'])}, embeds: {len(report['embeds'])}")
