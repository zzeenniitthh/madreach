#!/usr/bin/env python3
"""Merge companies_enriched_partial.csv into the data blob embedded in index.html.

Idempotent: new companies are keyed by name; re-running won't double-add.
Bakes a multi-valued `fields` array into every company so the page can be
fully data-driven (old 8-field taxonomy + new industry categories).
"""
import csv, json, re, sys, html, unicodedata

HTML_FILE = "index.html"
CSV_FILE = "companies_enriched_partial.csv"

US_STATES = {
    # abbreviations
    "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
    "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
    "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
    "VA","WA","WV","WI","WY","DC",
    # full names
    "Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut",
    "Delaware","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa",
    "Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan",
    "Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada",
    "New Hampshire","New Jersey","New Mexico","New York","North Carolina",
    "North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island",
    "South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont",
    "Virginia","Washington","West Virginia","Wisconsin","Wyoming",
}
# normalize a few country spellings to match the existing dataset's style
COUNTRY_ALIAS = {"United Kingdom": "UK", "United States": "USA", "USA": "USA"}


def derive_location_country(city, state):
    city = (city or "").strip()
    state = (state or "").strip()
    country = ""
    if state in US_STATES:
        country = "USA"
    elif "," in state:                       # e.g. "Ontario, Canada"
        country = state.split(",")[-1].strip()
    elif state:
        country = state
    country = COUNTRY_ALIAS.get(country, country)
    loc_parts = [p for p in (city, state) if p]
    location = ", ".join(loc_parts) if loc_parts else "—"
    if not country:
        country = "—"
    return location, country


def domain_from(website, email):
    for src in (website or "", email or ""):
        if not src:
            continue
        if "@" in src and "//" not in src:
            return src.split("@")[-1].strip().lower()
        m = re.sub(r"^https?://", "", src.strip()).lstrip("www.")
        m = m.split("/")[0].strip().lower()
        if m:
            return m
    return ""


def norm_name(s):
    """Accent- and case-insensitive name key for de-duping people."""
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", s).strip().lower()


def person_from(row, i):
    name = (row.get(f"person{i}_name") or "").strip()
    if not name:
        return None
    x = (row.get(f"person{i}_x") or "").strip()
    return {
        "name": name,
        "title": (row.get(f"person{i}_role") or "").strip(),
        "linkedin": (row.get(f"person{i}_linkedin") or "").strip(),
        "twitter": x,
        "twitterRaw": x,
        "email": (row.get(f"person{i}_email") or "").strip(),
        "emailConfidence": (row.get(f"person{i}_email_conf") or "").strip(),
        "sourceConfidence": (row.get(f"person{i}_conf") or "").strip(),
    }


def company_from(row):
    name = (row.get("name") or "").strip()
    city, state = row.get("city"), row.get("state")
    location, country = derive_location_country(city, state)
    website = (row.get("website") or "").strip()
    company_email = (row.get("company_email") or "").strip()
    cats = [c.strip() for c in (row.get("category") or "").split(",") if c.strip()] or ["Other"]
    people = [p for i in (1, 2, 3) if (p := person_from(row, i))]
    return {
        "company": name,
        "researched": name,
        "location": location,
        "country": country,
        "domain": domain_from(website, company_email),
        "website": website,
        "companyLinkedin": (row.get("linkedin_url") or "").strip(),
        "companyEmail": company_email,
        "companyEmailConf": (row.get("company_email_conf") or "").strip(),
        "fields": cats,
        "subcategory": (row.get("subcategory") or "").strip(),
        "notes": (row.get("description") or "").strip(),
        "people": people,
    }


def main():
    src = open(HTML_FILE, encoding="utf-8").read()

    # 1) extract the embedded data array
    start_tag = '<script id="data" type="application/json">'
    s = src.index(start_tag) + len(start_tag)
    e = src.index("</script>", s)
    existing = json.loads(src[s:e])

    # 2) extract the old company->field map and bake `fields` into existing companies
    m = re.search(r"const COMPANY_FIELD=(\{.*?\});", src, re.DOTALL)
    field_map = json.loads(m.group(1)) if m else {}
    for c in existing:
        if "fields" not in c:
            c["fields"] = [field_map.get(c["company"], "Other")]
        c.setdefault("website", ("https://" + c["domain"]) if c.get("domain") else "")
        c.setdefault("companyLinkedin", "")
        c.setdefault("companyEmail", "")

    by_name = {c["company"]: c for c in existing}

    # 3) parse the CSV; append new companies, ENRICH overlapping ones
    rows = list(csv.DictReader(open(CSV_FILE, encoding="utf-8")))
    new, enriched = [], []
    for r in rows:
        nm = (r.get("name") or "").strip()
        if not nm:
            continue
        obj = company_from(r)
        if nm in by_name:                       # overlap -> merge into existing
            cur = by_name[nm]
            for k in ("companyLinkedin", "companyEmail", "companyEmailConf", "website"):
                if not cur.get(k) and obj.get(k):
                    cur[k] = obj[k]
            cur["fields"] = list(dict.fromkeys(cur["fields"] + obj["fields"]))  # union, ordered
            seen = {norm_name(p["name"]) for p in cur["people"]}
            for p in obj["people"]:
                if norm_name(p["name"]) not in seen:
                    cur["people"].append(p)
                    seen.add(norm_name(p["name"]))
            enriched.append(nm)
        else:
            new.append(obj)
            by_name[nm] = obj
            existing.append(obj)

    merged = existing

    # 4) integrity check: every CSV person is present in its merged company
    missing = []
    for r in rows:
        nm = (r.get("name") or "").strip()
        comp = by_name.get(nm)
        names = {norm_name(p["name"]) for p in comp["people"]} if comp else set()
        for i in (1, 2, 3):
            pn = (r.get(f"person{i}_name") or "").strip()
            if pn and norm_name(pn) not in names:
                missing.append((nm, pn))
    assert not missing, f"people missing after merge: {missing[:10]}"
    assert all(c.get("fields") for c in merged), "every company must have >=1 field"

    # 5) write the new blob back (compact, single line like the original)
    blob = json.dumps(merged, ensure_ascii=False, separators=(",", ":"))
    out = src[:s] + blob + src[e:]
    open(HTML_FILE, "w", encoding="utf-8").write(out)

    print(f"new companies added : {len(new)}")
    print(f"enriched (overlap)  : {enriched}")
    print(f"total companies     : {len(merged)}")
    print(f"total people        : {sum(len(c['people']) for c in merged)}")
    print(f"distinct fields     : {len(set(f for c in merged for f in c['fields']))}")


if __name__ == "__main__":
    main()
