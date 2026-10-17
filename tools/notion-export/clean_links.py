"""Strip tracking parameters from URLs, leaving everything else exactly as written.

Used by convert.py on every page it writes. It can also be run on its own to
clean existing files in place:

    python3 clean_links.py FILE_OR_DIR [...]      # rewrites .md / .json files
    python3 clean_links.py --check FILE_OR_DIR    # only reports what would change
"""
import re
import sys
from pathlib import Path

# Query parameters that only identify the sharer or the ad campaign.
TRACKING_EXACT = {
    "gclid", "gbraid", "wbraid", "gad_source", "gad_campaignid", "dclid", "msclkid",
    "fbclid", "igshid", "mc_cid", "mc_eid", "srsltid", "ef_id", "s_kwcid", "sc_channel",
    "trk", "kcgid", "kcwbid", "kcgbid", "_hsenc", "_hsmi", "ref_src",
}
TRACKING_PREFIXES = ("utm_", "hsa_")
# "si" is only a tracking ID on these hosts; elsewhere it can mean something.
SHARE_ID_HOSTS = ("youtube.com", "youtu.be", "spotify.com")
# Google search links: keep only the query itself.
GOOGLE_SEARCH = re.compile(r"^https?://(?:www\.)?google\.[a-z.]+/search$")

URL_RE = re.compile(r"https?://[^\s)\]<>\"'|`]+")


def _is_tracking(key, host, base):
    k = key.lower()
    if GOOGLE_SEARCH.match(base):
        return k != "q"
    if k in TRACKING_EXACT or k.startswith(TRACKING_PREFIXES):
        return True
    return k == "si" and any(host == h or host.endswith("." + h) for h in SHARE_ID_HOSTS)


def clean_url(url):
    """Return url without tracking parameters or text-fragment anchors."""
    base, sep, rest = url.partition("?")
    if sep:
        query, hsep, frag = rest.partition("#")
    else:
        base, hsep, frag = url.partition("#")
        query = ""
    host = re.sub(r"^https?://", "", base).split("/")[0].lower()
    if frag.startswith(":~:text="):        # Chrome "copy link to highlight" fragment
        hsep, frag = "", ""
    kept = [p for p in query.split("&") if p and not _is_tracking(p.split("=", 1)[0], host, base)] if query else []
    return base + ("?" + "&".join(kept) if kept else "") + (hsep + frag if hsep else "")


def clean_text(text):
    return URL_RE.sub(lambda m: clean_url(m.group(0)), text)


def _files(paths):
    for p in map(Path, paths):
        if p.is_dir():
            yield from (f for f in p.rglob("*") if f.suffix in (".md", ".json") and ".git" not in f.parts)
        elif p.is_file():
            yield p


if __name__ == "__main__":
    args = sys.argv[1:]
    check = "--check" in args
    args = [a for a in args if a != "--check"]
    changed = 0
    for f in _files(args):
        old = f.read_text(encoding="utf-8")
        new = clean_text(old)
        if new != old:
            changed += 1
            if not check:
                f.write_text(new, encoding="utf-8")
    print(f"{'would change' if check else 'cleaned'} {changed} file(s)")
