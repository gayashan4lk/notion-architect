# How this export was made

The pages in this repo are exported from the **Architect** Notion workspace. The current snapshot was taken on 2026-10-17, after the workspace was reorganized into hubs, and is formatted for Obsidian. Earlier versions are frozen, each with the tools that produced it: the pre-reorganization snapshot in [`archive/2026-10-16/`](../../archive/2026-10-16/), and the GitHub-flavored version of this snapshot in [`archive/2026-10-17/`](../../archive/2026-10-17/).

## Steps

1. **Crawl.** Every page was fetched through Claude's Notion connector, starting from the 9 top-level pages in the sidebar and following every subpage. Each page's raw Notion Markdown is saved in [`raw/`](raw/), one file per page ID, with a `<!-- meta -->` header holding its title, parent, and last-edited time. Pages whose content hadn't changed since the previous crawl were carried over from it, with their new title and parent.
2. **Fill gaps.** The connector doesn't return bookmark URLs, so they were read from the live Notion pages and saved in [`bookmarks.json`](bookmarks.json). Images were captured from Notion in the browser and saved in [`assets/`](assets/) at full resolution. PNGs are lossless. JPEGs were re-saved at 92% quality, so camera metadata (EXIF) is not kept. [`assets/files.json`](assets/files.json) maps each Notion file ID to its image, so an image still matches after its block is moved or copied.
3. **Convert.** [`manifest.py`](manifest.py) builds [`manifest.json`](manifest.json), the page tree with child counts, images, and bookmarks. [`convert.py`](convert.py) then turns `raw/` into the Markdown tree at the repo root, listing the top-level pages in the order given in [`roots.json`](roots.json), which matches the Notion sidebar.

## Link cleaning

[`clean_links.py`](clean_links.py) removes tracking parameters from every link: `utm_*`, `gclid`, `fbclid`, ad-campaign IDs, YouTube and Spotify `si=` share IDs, and Chrome's `#:~:text=` highlight anchors. Google search links keep only the search term. Everything else in a URL stays as written. `convert.py` applies it to every page it writes, and the raw dumps, `bookmarks.json` and the archive have been cleaned the same way. Run `python3 clean_links.py --check <path>` to see whether anything still needs cleaning.

## Re-running the conversion

The conversion is repeatable from the saved files, with no Notion access needed:

```bash
cd tools/notion-export
python3 manifest.py raw manifest.json
python3 convert.py . ../../ --obsidian
```

Leave out `--obsidian` to get GitHub-style output instead: relative Markdown links, `<details>` toggles, blockquote callouts and GitHub heading anchors.

To pick up new or edited Notion pages, the crawl (step 1) has to be run again through the Notion connector. Ask Claude to refresh the export. New bookmarks and images need the built-in browser on your computer, signed in to Notion.

## Obsidian format

The root is an Obsidian vault. `convert.py --obsidian` writes:

- links between pages, breadcrumbs and @-mentions as full-path wikilinks such as `[[software-engineering/fastapi|FastAPI]]`. Full paths are needed because many notes share a file name (every `README`).
- images as `![[_assets/…]]` embeds.
- Notion callouts as Obsidian callouts. The type comes from the Notion colour (red → `danger`, yellow → `warning`, blue → `info`, green → `success`, grey → `note`, or `tip` when the icon is 💡).
- toggles as callouts folded by default (`> [!faq]- …`), and the table of contents as `[[#Heading]]` links.
- each page's Notion title under `aliases`, so search and link autocomplete find notes by title even though files keep their slug names.

[`.obsidian/app.json`](../../.obsidian/app.json) hides `tools/` and `archive/` from search, the graph and the quick switcher. It makes new links wikilinks with full paths, puts pasted images in `_assets/`, updates links when a note is renamed, and turns off the inline file-name title, since every page already has its title as a heading. Per-device files (`workspace.json`, the cache) are git-ignored.

## Layout rules

- A page with subpages becomes a folder with a `README.md`. A page without subpages becomes a single `<slug>.md` file.
- Slugs are lowercase titles with `&` → `and`, `+` → `p` (so `C++` → `cpp`), and every other symbol → `-`.
- Each file starts with frontmatter (`title`, `notion_id`, `notion_url`, `last_edited`) and a breadcrumb back to the root.
- Tables become Markdown tables in both formats.
