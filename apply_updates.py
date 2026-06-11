#!/usr/bin/env python3
"""Apply manual/researched contact updates to the data blob in index.html.

updates.json shape:
{
  "addPeople": [ {company, name, title, linkedin, x, email, emailConfidence, sourceConfidence} ],
  "setLinks":  [ {company, name, linkedin?, x?} ]   # fills ONLY empty fields
}
Matching is by company name + accent/case-insensitive person name. Idempotent.
"""
import json, re, sys, unicodedata

P = "index.html"
UP = sys.argv[1] if len(sys.argv) > 1 else "updates.json"

def norm(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", s).strip().lower()

src = open(P, encoding="utf-8").read()
tag = '<script id="data" type="application/json">'
s = src.index(tag) + len(tag)
e = src.index("</script>", s)
data = json.loads(src[s:e])
by_company = {norm(c["company"]): c for c in data}

up = json.load(open(UP, encoding="utf-8"))
added = filled_ln = filled_x = skipped = 0
warn = []

for r in up.get("addPeople", []):
    c = by_company.get(norm(r["company"]))
    if not c:
        warn.append(f"addPeople: company not found: {r['company']}"); continue
    if any(norm(p["name"]) == norm(r["name"]) for p in c["people"]):
        # already there -> treat as setLinks
        up.setdefault("setLinks", []).append(r); continue
    x = (r.get("x") or "").strip()
    c["people"].append({
        "name": r["name"], "title": r.get("title", ""),
        "linkedin": (r.get("linkedin") or "").strip(),
        "twitter": x, "twitterRaw": x,
        "email": (r.get("email") or "").strip(),
        "emailConfidence": (r.get("emailConfidence") or "").strip(),
        "sourceConfidence": (r.get("sourceConfidence") or "high").strip(),
    })
    added += 1

for r in up.get("setLinks", []):
    c = by_company.get(norm(r["company"]))
    if not c:
        warn.append(f"setLinks: company not found: {r['company']}"); continue
    p = next((p for p in c["people"] if norm(p["name"]) == norm(r["name"])), None)
    if not p:
        warn.append(f"setLinks: person not found: {r['name']} @ {r['company']}"); continue
    ln = (r.get("linkedin") or "").strip()
    x = (r.get("x") or "").strip()
    if ln and not (p.get("linkedin") or "").strip():
        p["linkedin"] = ln; filled_ln += 1
    if x and not (p.get("twitter") or p.get("twitterRaw") or "").strip():
        p["twitter"] = x; p["twitterRaw"] = x; filled_x += 1

blob = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
open(P, "w", encoding="utf-8").write(src[:s] + blob + src[e:])
open("leaders.html", "w", encoding="utf-8").write(src[:s] + blob + src[e:])

print(f"added people : {added}")
print(f"filled LinkedIn: {filled_ln}")
print(f"filled X       : {filled_x}")
for w in warn:
    print("  WARN:", w)
