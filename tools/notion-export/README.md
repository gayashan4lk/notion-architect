# How this export was made

The pages in this repo were exported from the **Architect** Notion workspace in three steps.

1. **Crawl.** Every page was fetched through Claude's Notion connector, starting from the 7 top-level pages and following every subpage. Each page's raw Notion Markdown is saved unchanged in [`raw/`](raw/), one file per page ID, with a `<!-- meta -->` header holding its title, parent, and last-edited time.
2. **Fill gaps.** The connector doesn't return bookmark URLs. They were read from the live Notion pages and saved in [`bookmarks.json`](bookmarks.json).
3. **Convert.** [`manifest.py`](manifest.py) builds [`manifest.json`](manifest.json), the page tree with child counts, images, and bookmarks. [`convert.py`](convert.py) then turns `raw/` into the Markdown tree at the repo root.

## Re-running the conversion

The conversion is repeatable from the saved raw files, with no Notion access needed:

```bash
cd tools/notion-export
python3 manifest.py raw manifest.json
python3 convert.py . ../../
```

`convert.py` copies images from an `assets/` folder if one exists. Files there are named `<file-block-id>__<filename>`, using the block ID from the image's `notion-file-block://` reference.

To pick up new or edited Notion pages, the crawl (step 1) has to be run again through the Notion connector. Ask Claude to refresh the export.

## Layout rules

- A page with subpages becomes a folder with a `README.md`. A page without subpages becomes a single `<slug>.md` file.
- Slugs are lowercase titles with `&` → `and`, `+` → `p` (so `C++` → `cpp`), and every other symbol → `-`.
- Each file starts with frontmatter (`title`, `notion_id`, `notion_url`, `last_edited`) and a breadcrumb back to the root.
