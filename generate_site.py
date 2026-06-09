import json

SRC = "/private/tmp/claude-501/-Users-user-Documents-remotoinvids/7d12e0e4-40d8-4e7b-9271-7e1828501dae/tasks/wbjdk8hzv.output"
OUT = "/Users/user/Documents/remotoinvids/leaders.html"

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
    raw = json.load(f)["result"]["companies"]

def country(loc):
    return loc.split(",")[-1].strip()

companies = []
for i,(req,loc) in enumerate(REQUESTED):
    c = raw[i] if i < len(raw) else {}
    people = []
    for p in (c.get("people") or []):
        nm = (p.get("name","") or "").strip()
        if not nm or nm == "— none found —":
            continue
        ln = (p.get("linkedin","") or "").strip()
        tw = (p.get("twitter","") or "").strip()
        em = (p.get("email","") or "").strip()
        people.append({
            "name": nm,
            "title": (p.get("title","") or "").strip(),
            "linkedin": ln if ln.lower().startswith("http") else "",
            "twitter": tw if tw.lower().startswith("http") else "",
            "twitterRaw": tw if tw and tw.lower() != "not found" else "",
            "email": em if em and em.lower() != "unknown" else "",
            "emailConfidence": (p.get("emailConfidence","") or "").lower(),
            "sourceConfidence": (p.get("sourceConfidence","") or "").lower(),
        })
    companies.append({
        "company": req,
        "researched": c.get("company",""),
        "location": loc,
        "country": country(loc),
        "domain": c.get("domain",""),
        "emailPattern": c.get("emailPattern",""),
        "notes": c.get("notes",""),
        "people": people,
    })

DATA_JSON = json.dumps(companies, ensure_ascii=False).replace("</", "<\\/")

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Technical Leaders — Export</title>
<style>
:root{
  --bg:#f6f7fb; --panel:#fff; --ink:#1b2330; --muted:#6b7689; --line:#e6e9f0;
  --brand:#2f4bff; --brand-d:#1f3864; --good:#1a8a4a; --good-bg:#e6f6ec;
  --warn:#9a6a00; --warn-bg:#fff4d6; --bad:#b42318; --bad-bg:#fde9e7; --grey-bg:#eef0f4;
  --shadow:0 1px 2px rgba(16,24,40,.06),0 1px 3px rgba(16,24,40,.1);
}
*{box-sizing:border-box}
body{margin:0;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  background:var(--bg);color:var(--ink);font-size:14px;line-height:1.45}
a{color:var(--brand);text-decoration:none}
a:hover{text-decoration:underline}
header.top{position:sticky;top:0;z-index:30;background:var(--brand-d);color:#fff;
  padding:14px 20px;box-shadow:var(--shadow)}
header.top h1{margin:0;font-size:18px;font-weight:700;letter-spacing:.2px}
header.top .sub{font-size:12px;opacity:.85;margin-top:2px}
.wrap{max-width:1180px;margin:0 auto;padding:18px 20px 80px}
.bar{position:sticky;top:60px;z-index:20;background:var(--panel);border:1px solid var(--line);
  border-radius:14px;box-shadow:var(--shadow);padding:14px;margin-bottom:16px;
  display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end}
.field{display:flex;flex-direction:column;gap:4px}
.field label{font-size:11px;font-weight:600;color:var(--muted);text-transform:uppercase;letter-spacing:.4px}
input[type=text],select{font:inherit;padding:8px 10px;border:1px solid var(--line);border-radius:9px;
  background:#fff;color:var(--ink);min-width:150px}
input[type=text]{min-width:230px}
.grow{flex:1}
.btn{font:inherit;font-weight:600;border:1px solid var(--line);background:#fff;color:var(--ink);
  padding:8px 13px;border-radius:9px;cursor:pointer;white-space:nowrap}
.btn:hover{border-color:#c7cede;background:#fafbff}
.btn.sm{padding:5px 9px;font-size:12px;border-radius:8px}
.btn.primary{background:var(--brand);border-color:var(--brand);color:#fff}
.btn.primary:hover{background:#2440e6}
.btn.ghost{background:transparent;border-color:transparent;color:var(--muted)}
.count-pill{font-size:12px;color:var(--muted)}
.count-pill b{color:var(--ink)}
.export{display:flex;flex-wrap:wrap;gap:12px;align-items:flex-end;
  border-top:1px dashed var(--line);margin-top:4px;padding-top:12px;width:100%}
.company{background:var(--panel);border:1px solid var(--line);border-radius:14px;
  box-shadow:var(--shadow);margin-bottom:12px;overflow:hidden}
.chead{display:flex;align-items:center;gap:11px;padding:12px 14px;cursor:pointer;user-select:none}
.chead:hover{background:#fafbff}
.chead .nm{font-weight:700;font-size:15px}
.chead .loc{color:var(--muted);font-size:12px}
.chead .cnt{margin-left:auto;font-size:12px;color:var(--muted);background:var(--grey-bg);
  padding:3px 9px;border-radius:20px;white-space:nowrap}
.chead .caret{color:var(--muted);transition:transform .15s;font-size:12px}
.company.collapsed .caret{transform:rotate(-90deg)}
.company.collapsed .people{display:none}
.tagwarn{font-size:11px;color:var(--bad);background:var(--bad-bg);padding:2px 7px;border-radius:6px;margin-left:4px}
.people{border-top:1px solid var(--line)}
.person{display:grid;grid-template-columns:26px 1.4fr 1.7fr 1fr;gap:10px;align-items:center;
  padding:10px 14px;border-bottom:1px solid #f1f3f8}
.person:last-child{border-bottom:none}
.person:hover{background:#fafbff}
.person .who .nm{font-weight:600}
.person .who .ti{color:var(--muted);font-size:12px}
.links{display:flex;gap:8px;flex-wrap:wrap;font-size:12.5px}
.links .lk{display:inline-flex;align-items:center;gap:4px;padding:3px 8px;border-radius:7px;
  background:#f1f4ff;color:var(--brand);font-weight:600}
.links .lk.dim{background:#f3f4f7;color:#aeb6c5;font-weight:500}
.email{font-size:12.5px;word-break:break-all}
.chips{display:flex;gap:5px;margin-top:3px;flex-wrap:wrap}
.chip{font-size:10.5px;font-weight:700;padding:2px 7px;border-radius:20px;text-transform:capitalize}
.chip.verified,.chip.high{background:var(--good-bg);color:var(--good)}
.chip.inferred,.chip.medium{background:var(--warn-bg);color:var(--warn)}
.chip.unknown{background:var(--grey-bg);color:var(--muted)}
.chip.low{background:var(--bad-bg);color:var(--bad)}
input[type=checkbox]{width:17px;height:17px;accent-color:var(--brand);cursor:pointer}
.notes{padding:0 14px 12px 51px;color:var(--muted);font-size:12px;display:none}
.company.shownotes .notes{display:block}
.notetoggle{font-size:11px;color:var(--brand);cursor:pointer;margin-left:8px}
.empty{padding:30px;text-align:center;color:var(--muted)}
.toast{position:fixed;bottom:22px;left:50%;transform:translateX(-50%) translateY(20px);
  background:var(--ink);color:#fff;padding:11px 18px;border-radius:10px;font-weight:600;
  opacity:0;transition:.25s;z-index:50;box-shadow:var(--shadow)}
.toast.show{opacity:1;transform:translateX(-50%) translateY(0)}
@media(max-width:760px){.person{grid-template-columns:24px 1fr;gap:6px}
  .person .links,.person .emailcell{grid-column:2}}
</style>
</head>
<body>
<header class="top">
  <h1>Technical Leaders — Contact Exporter</h1>
  <div class="sub">Robotics &amp; AI-data companies · pick who you want, export to Markdown / CSV / JSON / vCard · runs fully offline</div>
</header>

<div class="wrap">
  <div class="bar">
    <div class="field grow">
      <label>Search</label>
      <input type="text" id="q" placeholder="name, company, title, email…">
    </div>
    <div class="field">
      <label>Country</label>
      <select id="country"></select>
    </div>
    <div class="field">
      <label>Email</label>
      <select id="emailf">
        <option value="">all</option>
        <option value="verified">verified only</option>
        <option value="inferred">inferred only</option>
        <option value="has">has any email</option>
      </select>
    </div>
    <button class="btn sm" id="selVisible">Select shown</button>
    <button class="btn sm" id="deselVisible">Deselect shown</button>
    <button class="btn sm ghost" id="expandAll">Expand</button>
    <button class="btn sm ghost" id="collapseAll">Collapse</button>
    <span class="count-pill" id="counter"></span>

    <div class="export">
      <div class="field">
        <label>Format</label>
        <select id="fmt">
          <option value="md">Markdown (.md)</option>
          <option value="csv">CSV (.csv)</option>
          <option value="json">JSON (.json)</option>
          <option value="vcf">vCard (.vcf)</option>
        </select>
      </div>
      <div class="field">
        <label>File structure</label>
        <select id="structure">
          <option value="single">Single file</option>
          <option value="company">One file per company (.zip)</option>
          <option value="country">One file per country (.zip)</option>
        </select>
      </div>
      <button class="btn primary" id="download">⬇ Download selected</button>
      <button class="btn" id="copy">Copy to clipboard</button>
      <button class="btn ghost" id="preview">Preview</button>
    </div>
  </div>

  <div id="list"></div>
</div>

<div class="toast" id="toast"></div>

<script id="data" type="application/json">__DATA__</script>
<script>
const DATA = JSON.parse(document.getElementById('data').textContent);
// assign ids
DATA.forEach((c,ci)=>{c.id='c'+ci;c.people.forEach((p,pi)=>p.id='c'+ci+'p'+pi);});
const ALLP = DATA.flatMap(c=>c.people.map(p=>({...p, company:c.company, location:c.location, country:c.country, researched:c.researched})));
const selected = new Set(ALLP.map(p=>p.id)); // all selected by default
const collapsed = new Set();

const $ = s=>document.querySelector(s);
const list=$('#list'), q=$('#q'), countrySel=$('#country'), emailf=$('#emailf'), counter=$('#counter');

// populate country filter
const countries=[...new Set(DATA.map(c=>c.country))].sort();
countrySel.innerHTML='<option value="">all countries</option>'+countries.map(c=>`<option>${c}</option>`).join('');

function esc(s){return (s||'').replace(/[&<>"]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[m]));}
function matchPerson(c,p){
  const term=q.value.trim().toLowerCase();
  if(countrySel.value && c.country!==countrySel.value) return false;
  const ef=emailf.value;
  if(ef==='verified' && p.emailConfidence!=='verified') return false;
  if(ef==='inferred' && p.emailConfidence!=='inferred') return false;
  if(ef==='has' && !p.email) return false;
  if(term){
    const hay=(p.name+' '+p.title+' '+c.company+' '+c.researched+' '+p.email).toLowerCase();
    if(!hay.includes(term)) return false;
  }
  return true;
}
function visiblePeople(){
  const out=[];
  DATA.forEach(c=>c.people.forEach(p=>{if(matchPerson(c,p))out.push(p);}));
  return out;
}
function twHandle(p){
  if(p.twitter) return '@'+p.twitter.replace(/\/$/,'').split('/').pop();
  if(p.twitterRaw) return p.twitterRaw;
  return '';
}

function render(){
  let html='';
  let shown=0;
  DATA.forEach(c=>{
    const ppl=c.people.filter(p=>matchPerson(c,p));
    if(!ppl.length) return;
    shown+=ppl.length;
    const warn=/Indianapolis|research project|not a company|could not be confirmed/i.test(c.notes)?'<span class="tagwarn">check notes</span>':'';
    const isCol=collapsed.has(c.id);
    html+=`<div class="company ${isCol?'collapsed':''}" data-c="${c.id}">
      <div class="chead">
        <input type="checkbox" class="cbox" data-c="${c.id}">
        <span class="caret">▼</span>
        <span class="nm">${esc(c.company)}</span>
        <span class="loc">· ${esc(c.location)}</span>${warn}
        <span class="notetoggle" data-note="${c.id}">notes</span>
        <span class="cnt">${ppl.length} shown</span>
      </div>
      <div class="notes">${esc(c.notes)||'—'}</div>
      <div class="people">`;
    ppl.forEach(p=>{
      const ln=p.linkedin?`<a class="lk" href="${esc(p.linkedin)}" target="_blank" rel="noopener">in ↗</a>`:`<span class="lk dim">in —</span>`;
      const th=twHandle(p);
      const tw=p.twitter?`<a class="lk" href="${esc(p.twitter)}" target="_blank" rel="noopener">${esc(th)} ↗</a>`:(th?`<span class="lk dim">${esc(th)}</span>`:`<span class="lk dim">x —</span>`);
      const em=p.email?`<a href="mailto:${esc(p.email)}">${esc(p.email)}</a>`:'<span style="color:#aeb6c5">no email</span>';
      const chips=`<div class="chips">${p.emailConfidence?`<span class="chip ${p.emailConfidence}">${p.emailConfidence} email</span>`:''}${p.sourceConfidence?`<span class="chip ${p.sourceConfidence}">${p.sourceConfidence} conf</span>`:''}</div>`;
      html+=`<div class="person">
        <input type="checkbox" class="pbox" data-p="${p.id}" ${selected.has(p.id)?'checked':''}>
        <div class="who"><div class="nm">${esc(p.name)}</div><div class="ti">${esc(p.title)}</div></div>
        <div class="links">${ln}${tw}</div>
        <div class="emailcell"><div class="email">${em}</div>${chips}</div>
      </div>`;
    });
    html+=`</div></div>`;
  });
  list.innerHTML=html||'<div class="empty">No people match your filters.</div>';
  syncCompanyBoxes();
  updateCounter(shown);
}
function updateCounter(shown){
  counter.innerHTML=`<b>${selected.size}</b> selected · ${shown} shown · ${ALLP.length} total`;
}
function syncCompanyBoxes(){
  document.querySelectorAll('.company').forEach(el=>{
    const c=DATA.find(x=>x.id===el.dataset.c);
    const vis=c.people.filter(p=>matchPerson(c,p));
    const box=el.querySelector('.cbox');
    const sel=vis.filter(p=>selected.has(p.id)).length;
    box.checked = vis.length>0 && sel===vis.length;
    box.indeterminate = sel>0 && sel<vis.length;
  });
}

list.addEventListener('change',e=>{
  if(e.target.classList.contains('pbox')){
    const id=e.target.dataset.p;
    e.target.checked?selected.add(id):selected.delete(id);
    syncCompanyBoxes();updateCounter(visiblePeople().length);
  }
  if(e.target.classList.contains('cbox')){
    const c=DATA.find(x=>x.id===e.target.dataset.c);
    const vis=c.people.filter(p=>matchPerson(c,p));
    vis.forEach(p=>e.target.checked?selected.add(p.id):selected.delete(p.id));
    render();
  }
});
list.addEventListener('click',e=>{
  if(e.target.classList.contains('notetoggle')){
    e.target.closest('.company').classList.toggle('shownotes');return;
  }
  if(e.target.closest('.chead') && !e.target.classList.contains('cbox')){
    const el=e.target.closest('.company');
    const id=el.dataset.c;
    collapsed.has(id)?collapsed.delete(id):collapsed.add(id);
    el.classList.toggle('collapsed');
  }
});
[q,countrySel,emailf].forEach(el=>el.addEventListener('input',render));
$('#selVisible').onclick=()=>{visiblePeople().forEach(p=>selected.add(p.id));render();};
$('#deselVisible').onclick=()=>{visiblePeople().forEach(p=>selected.delete(p.id));render();};
$('#expandAll').onclick=()=>{collapsed.clear();render();};
$('#collapseAll').onclick=()=>{DATA.forEach(c=>collapsed.add(c.id));render();};

/* ---------- export ---------- */
function selectedPeople(){
  // keep DATA order, respect current filters AND selection
  const out=[];
  DATA.forEach(c=>c.people.forEach(p=>{if(selected.has(p.id))out.push({...p,company:c.company,researched:c.researched,location:c.location,country:c.country});}));
  return out;
}
function fname(s){return (s||'untitled').replace(/[\/\\:*?"<>|]+/g,'-').replace(/\s+/g,'_').slice(0,80);}

function personMD(p){
  const ln=p.linkedin?`[${p.linkedin}](${p.linkedin})`:'—';
  const th=p.twitter?`[${twHandle(p)}](${p.twitter})`:(p.twitterRaw||'—');
  const em=p.email?`${p.email} _(${p.emailConfidence})_`:'—';
  return `### ${p.name} — ${p.title}\n`+
    `- **Company:** ${p.company} (${p.location})\n`+
    `- **LinkedIn:** ${ln}\n`+
    `- **X / Twitter:** ${th}\n`+
    `- **Email:** ${em}\n`+
    `- **Source confidence:** ${p.sourceConfidence||'—'}\n`;
}
function groupBy(arr,key){const m=new Map();arr.forEach(x=>{const k=x[key];if(!m.has(k))m.set(k,[]);m.get(k).push(x);});return m;}
function mdDoc(people,title){
  let s=`# ${title}\n\n_${people.length} contacts · exported ${new Date().toISOString().slice(0,10)}_\n\n`;
  const g=groupBy(people,'company');
  for(const [comp,ppl] of g){
    s+=`## ${comp} — ${ppl[0].location}\n\n`;
    ppl.forEach(p=>{s+=personMD(p)+'\n';});
  }
  return s;
}
function csvDoc(people){
  const cols=['Company','Location','Researched as','Name','Title','LinkedIn','X/Twitter','Email','Email confidence','Source confidence'];
  const q=v=>{v=(v==null?'':String(v));return /[",\n]/.test(v)?'"'+v.replace(/"/g,'""')+'"':v;};
  const rows=people.map(p=>[p.company,p.location,p.researched,p.name,p.title,p.linkedin,p.twitter||p.twitterRaw,p.email,p.emailConfidence,p.sourceConfidence].map(q).join(','));
  return cols.join(',')+'\n'+rows.join('\n');
}
function jsonDoc(people){
  return JSON.stringify(people.map(p=>({name:p.name,title:p.title,company:p.company,location:p.location,
    linkedin:p.linkedin,twitter:p.twitter||p.twitterRaw,email:p.email,
    emailConfidence:p.emailConfidence,sourceConfidence:p.sourceConfidence})),null,2);
}
function vcfDoc(people){
  return people.map(p=>{
    let v='BEGIN:VCARD\nVERSION:3.0\n';
    v+=`FN:${p.name}\n`;
    const parts=p.name.split(' ');v+=`N:${parts.slice(1).join(' ')};${parts[0]};;;\n`;
    v+=`ORG:${p.company}\n`;
    if(p.title)v+=`TITLE:${p.title}\n`;
    if(p.email)v+=`EMAIL;TYPE=WORK:${p.email}\n`;
    if(p.linkedin)v+=`URL:${p.linkedin}\n`;
    if(p.twitter||p.twitterRaw)v+=`X-SOCIALPROFILE;TYPE=twitter:${p.twitter||p.twitterRaw}\n`;
    v+=`NOTE:${p.location} | email:${p.emailConfidence} | conf:${p.sourceConfidence}\n`;
    v+='END:VCARD';
    return v;
  }).join('\n');
}
const EXT={md:'md',csv:'csv',json:'json',vcf:'vcf'};
function buildOne(people,fmt,title){
  if(fmt==='md')return mdDoc(people,title);
  if(fmt==='csv')return csvDoc(people);
  if(fmt==='json')return jsonDoc(people);
  if(fmt==='vcf')return vcfDoc(people);
}

function currentText(){ // for single-file / copy / preview
  return buildOne(selectedPeople(),$('#fmt').value,'Technical Leaders');
}
function dl(blob,name){
  const a=document.createElement('a');a.href=URL.createObjectURL(blob);a.download=name;
  document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(a.href),2000);
}
function toast(m){const t=$('#toast');t.textContent=m;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),1900);}

$('#download').onclick=()=>{
  const ppl=selectedPeople();
  if(!ppl.length){toast('Nothing selected');return;}
  const fmt=$('#fmt').value, ext=EXT[fmt], struct=$('#structure').value;
  if(struct==='single'){
    dl(new Blob([buildOne(ppl,fmt,'Technical Leaders')],{type:'text/plain;charset=utf-8'}),`technical-leaders.${ext}`);
    toast(`Downloaded ${ppl.length} contacts`);return;
  }
  const key=struct==='company'?'company':'country';
  const g=groupBy(ppl,key);
  const files=[];
  for(const [k,arr] of g){
    files.push({name:`${fname(k)}.${ext}`,data:new TextEncoder().encode(buildOne(arr,fmt,k))});
  }
  dl(makeZip(files),`technical-leaders-by-${key}.zip`);
  toast(`Downloaded ${files.length} files (${ppl.length} contacts)`);
};
$('#copy').onclick=async()=>{
  const ppl=selectedPeople();if(!ppl.length){toast('Nothing selected');return;}
  try{await navigator.clipboard.writeText(currentText());toast('Copied to clipboard');}
  catch(e){toast('Clipboard blocked — use Download');}
};
$('#preview').onclick=()=>{
  const ppl=selectedPeople();if(!ppl.length){toast('Nothing selected');return;}
  const w=window.open('','_blank');
  w.document.write('<pre style="white-space:pre-wrap;font:13px/1.5 ui-monospace,Menlo,monospace;padding:24px;max-width:900px;margin:auto">'+
    currentText().replace(/[&<>]/g,m=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[m]))+'</pre>');
  w.document.title='Preview';
};

/* ---------- minimal store-only ZIP (no deps) ---------- */
function crc32(b){let c,crc=0xFFFFFFFF;if(!crc32.t){const t=[];for(let n=0;n<256;n++){c=n;for(let k=0;k<8;k++)c=c&1?(0xEDB88320^(c>>>1)):(c>>>1);t[n]=c>>>0;}crc32.t=t;}
  const t=crc32.t;for(let i=0;i<b.length;i++)crc=t[(crc^b[i])&0xff]^(crc>>>8);return (crc^0xFFFFFFFF)>>>0;}
function makeZip(files){
  const u16=n=>[n&255,(n>>8)&255],u32=n=>[n&255,(n>>8)&255,(n>>16)&255,(n>>24)&255];
  const enc=new TextEncoder();const parts=[];const central=[];let off=0;
  for(const f of files){
    const nb=enc.encode(f.name),d=f.data,crc=crc32(d);
    const lh=new Uint8Array([].concat(u32(0x04034b50),u16(20),u16(0x0800),u16(0),u16(0),u16(0),
      u32(crc),u32(d.length),u32(d.length),u16(nb.length),u16(0)));
    parts.push(lh,nb,d);
    central.push({nb,crc,size:d.length,off});
    off+=lh.length+nb.length+d.length;
  }
  const cdStart=off;const cd=[];let cdSize=0;
  for(const c of central){
    const h=new Uint8Array([].concat(u32(0x02014b50),u16(20),u16(20),u16(0x0800),u16(0),u16(0),u16(0),
      u32(c.crc),u32(c.size),u32(c.size),u16(c.nb.length),u16(0),u16(0),u16(0),u16(0),u32(0),u32(c.off)));
    cd.push(h,c.nb);cdSize+=h.length+c.nb.length;
  }
  const eocd=new Uint8Array([].concat(u32(0x06054b50),u16(0),u16(0),u16(central.length),u16(central.length),
    u32(cdSize),u32(cdStart),u16(0)));
  return new Blob([...parts,...cd,eocd],{type:'application/zip'});
}

render();
</script>
</body>
</html>
"""

with open(OUT, "w") as f:
    f.write(HTML.replace("__DATA__", DATA_JSON))

total = sum(len(c["people"]) for c in companies)
print(f"Wrote {OUT}  ({len(companies)} companies, {total} people)")
