# madreach

A self-contained static page (`index.html`) for browsing and exporting
technical-leader contacts at robotics / AI / physical-AI companies.

## The page

`index.html` is fully standalone — all CSS, JS, and data are inlined, with no
network requests. Open it in any browser, or deploy it anywhere static.

Features:
- Filter by **search, country, field/industry, email confidence, and profiles**
  (has LinkedIn / X / both). Filters drive both the viewer and the downloads.
- Each company shows its **field(s)**, plus **company LinkedIn / website / email**.
- Export the current selection to **Markdown / CSV / JSON / vCard**, or grab a
  single column (just emails, just LinkedIn, or just X handles).

## Data pipeline

The embedded dataset is generated, not hand-edited:

- **Source:** `companies_enriched_partial.csv` (companies + up to 3 people each,
  with company LinkedIn/email and per-person LinkedIn/X/email).
- **Importer:** `build_data.py` merges the CSV into the data blob inside
  `index.html`. It's idempotent (companies keyed by name), de-dupes people by
  normalized name, enriches companies that already exist, and bakes a
  multi-valued `fields` array into every company.

```bash
python3 build_data.py          # re-run after editing the CSV
cp index.html leaders.html     # keep the mirror copy in sync
```

## Deploy on Vercel

Pure static site (no build step). Import the repo at
[vercel.com/new](https://vercel.com/new), framework preset **Other**, deploy.
Vercel serves `index.html` at the root URL. Pushing to `main` auto-redeploys.
