import json
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SRC = "/private/tmp/claude-501/-Users-user-Documents-remotoinvids/7d12e0e4-40d8-4e7b-9271-7e1828501dae/tasks/wbjdk8hzv.output"
OUT = "/Users/user/Documents/remotoinvids/technical_leaders.xlsx"

# Requested company -> location (source of truth for the location column)
REQUESTED = [
    ("Roboto AI","Seattle, WA, USA"),("Teleo","Palo Alto, CA, USA"),
    ("Rose City Robotics","Portland, OR, USA"),("Surge AI","San Francisco, CA, USA"),
    ("Labelbox","San Francisco, CA, USA"),("Datasaur","San Francisco, CA, USA"),
    ("Prunt.ai","San Francisco, CA, USA"),("Dextrous Robotics","Memphis, TN, USA"),
    ("Foxglove","San Francisco, CA, USA"),("Wandelbots","Dresden, Germany"),
    ("Wayve","London, UK"),("Mobius Labs","Berlin, Germany"),
    ("Datagen","Tel Aviv, Israel"),("Robovise","San Francisco, CA, USA"),
    ("Covariant","Emeryville, CA, USA"),("Voxel51","Ann Arbor, MI, USA"),
    ("Intrinsic","Mountain View, CA, USA"),("Tangram Vision","Pittsburgh, PA, USA"),
    ("Osaro","San Francisco, CA, USA"),("Robust.AI","Redwood City, CA, USA"),
    ("Apple AIML (EgoDex)","Cupertino, CA, USA"),("Pronto","Bengaluru, India"),
    ("Enchanted Tools","Paris, France"),("Photoneo","Bratislava, Slovakia"),
    ("Gestalt Robotics","Berlin, Germany"),("Nnaisense","Lugano, Switzerland"),
    ("Accenture (AI data operations)","Dublin, Ireland"),("Papercup","London, UK"),
    ("Robco","Munich, Germany"),("Rapid Robotics","San Francisco, CA, USA"),
    ("Embodied AI / teleoperation startup","Zurich, Switzerland"),
    ("Sanctuary AI","Vancouver, BC, Canada"),("Kindred AI","Vancouver, BC, Canada"),
    ("Anolytics","New Delhi, India"),("DataAnnotation.tech","Bengaluru, India"),
    ("iMerit","Kolkata, India"),("Playment","Bengaluru, India"),
    ("Quadrant Resource","Hyderabad, India"),("MUJIN","Tokyo, Japan"),
    ("Preferred Networks","Tokyo, Japan"),("Cyberdyne","Tsukuba, Japan"),
    ("Naver Labs","Seongnam, South Korea"),("Rainbow Robotics","Daejeon, South Korea"),
    ("SenseTime","Shanghai, China"),("UBTECH Robotics","Shenzhen, China"),
    ("Fourier Intelligence","Shanghai, China"),("Unitree Robotics","Hangzhou, China"),
    ("LEJU Robotics","Shenzhen, China"),("CloudMinds","Beijing, China"),
    ("Horizon Robotics","Beijing, China"),
    ("Beijing Humanoid Robot Innovation Center (Tiangong)","Beijing, China"),
    ("DataSource Intelligent","Shanghai, China"),
    ("Shanghai AI Lab (OpenDriveLab)","Shanghai, China"),
    ("Galbot (银河通用)","Beijing, China"),("RoboSense","Shenzhen, China"),
    ("Mech-Mind Robotics","Beijing, China"),("DEEP Robotics","Hangzhou, China"),
    ("Lingchu Intelligence (灵初智能)","Shanghai, China"),("XYZ Robotics","Shanghai, China"),
    ("Dorabot","Shenzhen, China"),("Wandercraft","Paris, France"),
    ("Galaxy General Robot (银河通用)","Beijing, China"),("Youibot (优艾智合)","Shenzhen, China"),
    ("Dexforce","Shenzhen, China"),("Humanoid Robot Innovation Center (HRIC)","Beijing, China"),
    ("Robot data-collection operators","Beijing/Tianjin, China"),
    ("Neurovia AI","Dubai, UAE"),("G42","Abu Dhabi, UAE"),
    ("Mercor","San Francisco, CA, USA"),("Appen","Sydney, Australia"),
    ("Lionbridge AI","Waltham, MA, USA"),("TELUS International AI","Vancouver, BC, Canada"),
    ("TaskUs","New Braunfels, TX, USA"),("Sama","San Francisco, CA, USA"),
    ("Hive AI (thehive.ai)","San Francisco, CA, USA"),
]

with open(SRC) as f:
    data = json.load(f)
companies = data["result"]["companies"]

wb = Workbook()

# ---- Sheet 1: Contacts ----
ws = wb.active
ws.title = "Technical Leaders"

headers = ["#","Company (requested)","Location","Company (as researched)",
           "Name","Title","LinkedIn","X / Twitter","Email","Email confidence",
           "Source confidence"]

FONT = "Calibri"
header_fill = PatternFill("solid", fgColor="1F3864")
header_font = Font(name=FONT, bold=True, color="FFFFFF", size=11)
center = Alignment(horizontal="center", vertical="center", wrap_text=True)
left = Alignment(horizontal="left", vertical="center", wrap_text=True)
thin = Side(style="thin", color="D9D9D9")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

conf_fill = {
    "verified": PatternFill("solid", fgColor="C6EFCE"),
    "inferred": PatternFill("solid", fgColor="FFEB9C"),
    "unknown":  PatternFill("solid", fgColor="F2F2F2"),
    "high":     PatternFill("solid", fgColor="C6EFCE"),
    "medium":   PatternFill("solid", fgColor="FFEB9C"),
    "low":      PatternFill("solid", fgColor="FFC7CE"),
}

for c, h in enumerate(headers, 1):
    cell = ws.cell(1, c, h)
    cell.fill = header_fill; cell.font = header_font
    cell.alignment = center; cell.border = border

# build a lookup of researched companies in requested order
by_name = {c["company"]: c for c in companies}
# they came back in the same order as requested, so zip
row = 2
person_idx = 0
band_a = PatternFill("solid", fgColor="FFFFFF")
band_b = PatternFill("solid", fgColor="EDF1F7")

for i, (req_name, loc) in enumerate(REQUESTED):
    comp = companies[i] if i < len(companies) else None
    if comp is None:
        continue
    researched = comp.get("company","")
    people = comp.get("people") or []
    band = band_a if i % 2 == 0 else band_b
    if not people:
        person_idx += 1
        vals = [person_idx, req_name, loc, researched, "— none found —","","","","","",""]
        for c, v in enumerate(vals,1):
            cell = ws.cell(row, c, v); cell.border = border
            cell.alignment = left if c in (2,3,4,5,6) else center
            cell.font = Font(name=FONT, size=10, italic=True, color="888888")
            cell.fill = band
        row += 1
        continue
    for p in people:
        person_idx += 1
        ln = p.get("linkedin","") or ""
        tw = p.get("twitter","") or ""
        em = p.get("email","") or ""
        econf = (p.get("emailConfidence","") or "").lower()
        sconf = (p.get("sourceConfidence","") or "").lower()
        vals = [person_idx, req_name, loc, researched,
                p.get("name",""), p.get("title",""),
                ln if ln.lower().startswith("http") else "",
                tw, em, econf, sconf]
        for c, v in enumerate(vals,1):
            cell = ws.cell(row, c, v); cell.border = border
            cell.font = Font(name=FONT, size=10)
            cell.alignment = left if c in (2,3,4,5,6,7,8,9) else center
            cell.fill = band
        # hyperlinks
        if ln.lower().startswith("http"):
            lc = ws.cell(row,7); lc.hyperlink = ln; lc.value = "LinkedIn"
            lc.font = Font(name=FONT, size=10, color="0563C1", underline="single")
        if tw.lower().startswith("http"):
            tc = ws.cell(row,8); tc.hyperlink = tw
            tc.value = "@" + tw.rstrip("/").split("/")[-1]
            tc.font = Font(name=FONT, size=10, color="0563C1", underline="single")
        if em and em.lower() != "unknown":
            ec = ws.cell(row,9); ec.hyperlink = "mailto:"+em
            ec.font = Font(name=FONT, size=10, color="0563C1", underline="single")
        # confidence colouring
        if econf in conf_fill:
            ws.cell(row,10).fill = conf_fill[econf]
        if sconf in conf_fill:
            ws.cell(row,11).fill = conf_fill[sconf]
        row += 1

ws.freeze_panes = "A2"
ws.auto_filter.ref = f"A1:{get_column_letter(len(headers))}1"
widths = [5,26,20,30,24,34,14,22,32,15,15]
for c, w in enumerate(widths,1):
    ws.column_dimensions[get_column_letter(c)].width = w
ws.row_dimensions[1].height = 30

# ---- Sheet 2: Notes / caveats ----
ws2 = wb.create_sheet("Company notes")
h2 = ["Company (requested)","Location","Researched as","Domain","Email pattern","Researcher notes / caveats"]
for c,h in enumerate(h2,1):
    cell = ws2.cell(1,c,h); cell.fill=header_fill; cell.font=header_font
    cell.alignment=center; cell.border=border
r = 2
for i,(req_name,loc) in enumerate(REQUESTED):
    comp = companies[i] if i < len(companies) else {}
    vals=[req_name,loc,comp.get("company",""),comp.get("domain",""),
          comp.get("emailPattern",""),comp.get("notes","")]
    band = band_a if i%2==0 else band_b
    for c,v in enumerate(vals,1):
        cell=ws2.cell(r,c,v); cell.border=border; cell.fill=band
        cell.font=Font(name=FONT,size=10); cell.alignment=left
    r+=1
ws2.freeze_panes="A2"
for c,w in enumerate([26,20,28,22,22,90],1):
    ws2.column_dimensions[get_column_letter(c)].width=w
ws2.row_dimensions[1].height=30

# ---- Sheet 3: Legend ----
ws3 = wb.create_sheet("README", 0)
ws3.sheet_view.showGridLines = False
ws3.column_dimensions['A'].width = 2
ws3.column_dimensions['B'].width = 110
def line(r, text, **kw):
    cell = ws3.cell(r,2,text)
    cell.font = Font(name=FONT, **kw)
    cell.alignment = Alignment(wrap_text=True, vertical="top")
line(2,"Technical Leaders — Robotics & AI-Data Companies", bold=True, size=16, color="1F3864")
line(3,"Compiled via automated multi-source web research, June 2026. Read the caveats below before using.", size=10, italic=True, color="555555")
line(5,"WHAT THIS IS", bold=True, size=12, color="1F3864")
line(6,"For each of the 75 requested companies, 3+ technical leaders (CEO / CTO / co-founders / VP-Head of Engineering / Chief Scientist / Technical Director). See the 'Technical Leaders' tab for contacts and 'Company notes' for per-company caveats.", size=10)
line(8,"EMAIL CONFIDENCE — READ THIS", bold=True, size=12, color="C00000")
line(9,"• verified  = the address was found published on a concrete source (company page, RocketReach/ZoomInfo, GitHub commits, etc.).", size=10)
line(10,"• inferred  = CONSTRUCTED from the company's known email domain + observed naming pattern (e.g. first@ or first.last@). These are EDUCATED GUESSES, not confirmed. Validate before sending (Hunter.io / a verification tool) — patterns and personal exceptions vary.", size=10)
line(11,"• unknown   = no reliable domain or address could be determined.", size=10)
line(13,"SOURCE CONFIDENCE", bold=True, size=12, color="1F3864")
line(14,"high / medium / low = how confident the researcher was that the person and their stated role are real and current. Many of these companies are fast-moving startups; titles change, founders leave. Verify the LinkedIn before outreach.", size=10)
line(16,"KNOWN DATA-QUALITY FLAGS (details in 'Company notes')", bold=True, size=12, color="1F3864")
line(17,"• Several companies are acquired / defunct (Covariant, Photoneo, Papercup, Rapid Robotics, Mobius Labs, Dextrous Robotics, Nnaisense, Gestalt, etc.) — leaders listed may have moved on.", size=10)
line(18,"• 'Robovise (SF)' could not be confirmed as a robotics company — the match found is an Indianapolis fintech; treat as unverified.", size=10)
line(19,"• 'Apple AIML (EgoDex)' is a research project, not a company — listed people are Apple AI/ML org leaders + EgoDex contributors.", size=10)
line(20,"• 'Pruna.ai' is actually based in Munich, Germany (not SF).  'Embodied AI (Zurich)' resolved to a Lausanne/Delft startup, formerly Helix Robotics.", size=10)
line(21,"• Chinese / Japanese / Korean firms: founders are usually verifiable, but LinkedIn/X coverage is thin (WeChat/Weibo used instead) — expect more 'not found' handles and inferred emails there.", size=10)
line(23,"COLOR KEY", bold=True, size=12, color="1F3864")
for rr,(txt,col) in enumerate([("verified / high","C6EFCE"),("inferred / medium","FFEB9C"),("unknown","F2F2F2"),("low","FFC7CE")]):
    c=ws3.cell(24+rr,2,txt); c.fill=PatternFill("solid",fgColor=col)
    c.font=Font(name=FONT,size=10); c.alignment=Alignment(horizontal="left")

wb.save(OUT)

total_people = sum(len(c.get("people") or []) for c in companies)
verified = sum(1 for c in companies for p in (c.get("people") or []) if (p.get("emailConfidence","")or"").lower()=="verified")
print(f"Saved {OUT}")
print(f"Companies: {len(companies)} | People rows: {total_people} | Verified emails: {verified}")
