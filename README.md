# madreach

A self-contained static page (`index.html`) listing technical leaders, plus the
Remotion video project used to build related assets.

## The static page

`index.html` is fully standalone — all CSS, JS, and data are inlined, with no
network requests. Just open it in a browser, or deploy it anywhere static.

## Deploy on Vercel

This repo is configured to serve as a static site (see `vercel.json`):

1. Import the repo at [vercel.com/new](https://vercel.com/new).
2. Framework Preset: **Other** (no build step).
3. Deploy — Vercel serves `index.html` at the root URL.

Share the resulting URL.

## Source

- `index.html` / `leaders.html` — the generated static page.
- `generate_site.py`, `build_sheet.py`, `technical_leaders.xlsx` — data + generator.
- `src/` — Remotion video components (`npm start` to open Remotion Studio).
