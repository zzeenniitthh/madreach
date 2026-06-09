# madreach

A self-contained static page (`index.html`) listing technical leaders.

## The page

`index.html` is fully standalone — all CSS, JS, and data are inlined, with no
network requests. Open it in any browser, or deploy it anywhere static.

## Deploy on Vercel

Pure static site (no build step). Import the repo at
[vercel.com/new](https://vercel.com/new), pick framework preset **Other**, and
deploy. Vercel serves `index.html` at the root URL.

## Source

- `index.html` / `leaders.html` — the generated static page.
- `generate_site.py`, `build_sheet.py`, `technical_leaders.xlsx` — data + generator.
