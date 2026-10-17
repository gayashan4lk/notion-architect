# Export report

Snapshot taken 2026-10-17 from the Notion workspace **Architect**.

## Counts

| | |
|---|---|
| Pages exported | 77 |
| Top-level sections | 9 |
| Databases | 0 |
| Images | 10 (10 downloaded) |
| Bookmarks | 44 (44 with recovered URLs) |

## Embedded content not exported

Notion's connector doesn't expose these blocks; each spot links back to Notion.

- **BMAD Method** — external_object_instance (`2fcebef13b8480afbc5dd08c277e8ee3`)

## What changes in the conversion

- Callouts become Obsidian callouts that keep their emoji.
- Text highlight colours are dropped (the text itself is kept): First Bug.
- Headings shift down one level, since each page's title is its `#` heading.
- Link previews become plain links.
- **Obsidian format:** links between pages are full-path wikilinks (`[[folder/page|Title]]`), images are `![[…]]` embeds, callouts use `> [!type]` (picked from the Notion colour), toggles are folded `> [!faq]-` callouts, the table of contents links to headings with `[[#…]]`, and each note lists its Notion title under `aliases`.
- Tracking parameters (`utm_*`, `gclid`, YouTube `si=` and similar) are removed from every link by [`clean_links.py`](tools/notion-export/clean_links.py).
- Comments are not included.
