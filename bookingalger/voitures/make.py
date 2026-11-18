# Génère voitures/app.html (et index.html installable) à partir de la version Android des appartements.
import pathlib, re
d = pathlib.Path(__file__).parent
s = (d.parent / "app-android.html").read_text(encoding="utf-8")

def rep(a, b, count=1):
    global s
    assert a in s, "introuvable: " + a[:80]
    s = s.replace(a, b) if count == 0 else s.replace(a, b, count)

# ---------- Données ----------
CARS = [
  ("clio","Renault Clio 5","Manuelle","2021",7000),
  ("c3","Citroën C3","Manuelle","2022/23",6500),
  ("sandero","Dacia Sandero","Manuelle","2024",6000),
  ("stepway","Dacia Stepway","Manuelle","2024",7000),
  ("arona","Seat Arona","Manuelle","2022/23",7000),
  ("corsa","Opel Corsa","Manuelle","2023",7000),
  ("p208-24","Peugeot 208","Manuelle","2024",8000),
  ("livan","Livan X3 Pro","Manuelle","2026",7000),
  ("mg5","MG 5","Manuelle","2026",7000),
  ("captur","Renault Captur","Manuelle","2021",9000),
  ("c4","Citroën C4","Manuelle","2023",8000),
  ("tcross","Volkswagen T-Cross","Manuelle","2022",8000),
  ("captiva","Chevrolet Captiva","Auto","2022 · 7 places",12000),
  ("kx1","Kia KX1","Auto","2025",7000),
  ("tipo","Fiat Tipo","Auto","2023",9000),
  ("coolray","Geely Coolray","Auto","2026",9000),
  ("p208-23","Peugeot 208","Auto","2023",9000),
  ("megane","Renault Mégane","Auto","2023",10000),
  ("c4-auto","Citroën C4","Auto","2023",11000),
  ("coolray-full","Geely Coolray Full Options","Auto","2026",12000),
]
def price(n): return f"{n:,}".replace(",", " ")
rows = ",\n".join(
  f"  {{id:'{i}', name:'{n}', type:'{t}', year:'{y}', price:{p}, tag:'{y} · {price(p)} DA/j'}}" for i,n,t,y,p in CARS)
s = re.sub(r"const APTS = \[.*?\n\];", "const APTS = [\n" + rows + "\n];", s, count=1, flags=re.S)

s = re.sub(r"const hasWifi = w => w && \(w\.line \|\| w\.ssid \|\| w\.pass\);\n", "", s, count=1)
assert "w.line || w.ssid" not in s
# ---------- Icônes et catégories ----------
rep("const IC = {", """const IC = {
  lavage:'<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
  meca:'<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"/>',
  carro:'<path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/>',
  carbu:'<path d="M3 22h12"/><path d="M4 9h10"/><path d="M14 22V4a2 2 0 0 0-2-2H6a2 2 0 0 0-2 2v18"/><path d="M14 13h2a2 2 0 0 1 2 2v2a2 2 0 0 0 4 0V9.83a2 2 0 0 0-.59-1.42L18 5"/>',
  papiers:'<path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/><path d="M16 13H8"/><path d="M16 17H8"/>',
  vidanges:'<path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/>',
  gauge:'<path d="m12 14 4-4"/><path d="M3.34 19a10 10 0 1 1 17.32 0"/>',""")
rep("const CATS = {menage:'Ménage', linge:'Linge', maint:'Maintenance', courses:'Courses', accueil:'Accueil', autre:'Autre'};",
    "const CATS = {lavage:'Lavage', meca:'Mécanique', carro:'Carrosserie', carbu:'Carburant', papiers:'Papiers', autre:'Autre'};")
rep("cat:'menage', urgent:false, due:'', note:''}", "cat:'lavage', urgent:false, due:'', note:''}")

# ---------- Checklists ----------
s = re.sub(r"const TPL = \{.*?\n\};", """const TPL = {
  depart: car => [
    ['Relever le kilométrage et le carburant','carbu'],
    ['Inspecter la carrosserie : rayures, chocs','carro'],
    ['Vérifier pneus et jantes','meca'],
    ['Lavage extérieur','lavage'],
    ['Aspirateur et nettoyage intérieur','lavage'],
    ['Vérifier les objets oubliés','autre'],
    ['Récupérer clés et papiers','papiers'],
  ],
  arrivee: car => [
    ['Faire le plein ou vérifier le niveau','carbu'],
    ['Pression des pneus','meca'],
    ['Niveaux : huile, lave-glace, refroidissement','meca'],
    ['Carte grise et assurance dans la voiture','papiers'],
    ['Photos de l’état du véhicule','carro'],
    ['Préparer le contrat de location','papiers'],
    ['Remettre les clés au client','papiers'],
  ],
};""", s, count=1, flags=re.S)
rep("${ic('depart')}Après départ", "${ic('depart')}Retour client")
rep("${ic('arrivee')}Avant arrivée", "${ic('arrivee')}Avant location")

# ---------- Section vidange dans la fiche ----------
rep("""    <div class="sec-h"><span>Box Wi-Fi</span>${hasWifi(w) ? `<span><button data-wifi="${a.id}">Modifier</button></span>` : ''}</div>
    <div class="wcard">${hasWifi(w) ? wifiLines(a, w).replace('<div class="wl">', '<div class="wl" style="border-top:0">') : `<button class="add-w" style="border-top:0" data-wifi="${a.id}">${ic('wifi')}Ajouter la box Wi-Fi</button>`}</div>""",
"""    <div class="sec-h"><span>Vidange</span>${vpill(a.id)}</div>
    ${vidCard(a, false)}""")

# ---------- Onglet Vidanges (remplace le Wi-Fi) ----------
start = s.index("/* ---------- Onglet Wi-Fi ---------- */"); end = s.index("/* ---------- Détail ---------- */")
s = s[:start] + r"""/* ---------- Onglet Vidanges ---------- */
let wquery = '';
const shown = new Set();
const INTERVALS = ['5000','7500','10000','15000'];
const num = v => { const n = parseInt(String(v ?? '').replace(/\D/g,''), 10); return isNaN(n) ? '' : n; };
const fmtKm = n => Number(n).toLocaleString('fr-FR').replace(/[  ]/g,' ') + ' km';
const fmtDate = iso => new Date(iso + 'T00:00:00').toLocaleDateString('fr-FR', {day:'numeric', month:'short', year:'numeric'});
const monthsSince = iso => { const d = new Date(iso + 'T00:00:00'), n = new Date(); return (n.getFullYear()-d.getFullYear())*12 + n.getMonth()-d.getMonth() - (n.getDate() < d.getDate() ? 1 : 0); };
const hasWifi = w => !!(w && (w.km || w.lastKm || w.lastDate));
function vidStatus(id){
  const w = wifi[id];
  if (!w || (!w.lastKm && !w.lastDate)) return {level:-1, label:'À renseigner', cls:'todo'};
  const next = w.lastKm ? Number(w.lastKm) + (Number(w.op) || 10000) : null;
  const rem = next !== null && w.km ? next - Number(w.km) : null;
  const months = w.lastDate ? monthsSince(w.lastDate) : 0;
  if (rem !== null && rem <= 0) return {level:2, next, rem, label:`Dépassée de ${fmtKm(-rem)}`, cls:'urg'};
  if (months >= 6) return {level:2, next, rem, label:`Faite il y a ${months} mois`, cls:'urg'};
  if (rem !== null && rem <= 1000) return {level:1, next, rem, label:`Dans ${fmtKm(rem)}`, cls:'soon'};
  return {level:0, next, rem, label: rem !== null ? `Dans ${fmtKm(rem)}` : 'À jour', cls:'ok'};
}
const vpill = id => { const st = vidStatus(id); return `<span class="vpill ${st.cls}">${st.level === 2 ? ic('alert') : st.level === 0 ? ic('check') : ''}${st.label}</span>`; };
function wifiLines(a, w){
  const st = vidStatus(a.id), r = [];
  if (w.km) r.push(`<div class="wl"><span class="k">Kilométrage</span><span class="v">${fmtKm(w.km)}</span></div>`);
  if (w.lastDate || w.lastKm) r.push(`<div class="wl"><span class="k">Dernière vidange</span><span class="v">${[w.lastDate ? fmtDate(w.lastDate) : '', w.lastKm ? fmtKm(w.lastKm) : ''].filter(Boolean).join(' · ')}</span></div>`);
  if (st.next) r.push(`<div class="wl"><span class="k">Prochaine</span><span class="v"><b>${fmtKm(st.next)}</b> <small style="color:var(--on-var)">(tous les ${fmtKm(Number(w.op) || 10000)})</small></span></div>`);
  if (w.note) r.push(`<div class="wl"><span class="k">Note</span><span class="v" style="font-size:15px;color:var(--on-var)">${esc(w.note)}</span></div>`);
  return r.join('');
}
function vidCard(a, head){
  const w = wifi[a.id] || {}, filled = hasWifi(w);
  return `<div class="wcard">
    ${head ? `<div class="wh"><img src="img/${a.id}.jpg" alt="" width="76" height="48" loading="lazy"><div class="wh-t"><b>${esc(a.name)}</b><small>${a.type} · ${esc(a.year)}</small></div>${vpill(a.id)}</div>` : ''}
    ${filled ? wifiLines(a, w) : (head ? '' : `<div class="wl"><span class="v" style="color:var(--on-var);font-size:15px">Aucune vidange enregistrée pour cette voiture.</span></div>`)}
    <div class="vact"><button class="vbtn" data-wifi="${a.id}">${ic('gauge')}${filled ? 'Mettre à jour' : 'Renseigner'}</button><button class="vbtn primary" data-vdone="${a.id}">${ic('vidanges')}Vidange faite</button></div>
  </div>`;
}
function renderWifi(){
  const sts = Object.fromEntries(APTS.map(a => [a.id, vidStatus(a.id)]));
  const due = APTS.filter(a => sts[a.id].level >= 1).length, filled = APTS.filter(a => sts[a.id].level !== -1).length;
  $('#wifiSub').textContent = `${due ? plural(due, 'vidange') + ' à prévoir' : 'Aucune vidange urgente'} · ${filled} sur ${APTS.length} renseignées`;
  const q = fold(wquery.trim()), rank = {2:0, 1:1, 0:2, '-1':3};
  const list = APTS.filter(a => !q || fold([a.name, a.type, a.year].join(' ')).includes(q))
    .sort((x, y) => (rank[sts[x.id].level] - rank[sts[y.id].level]) || ((sts[x.id].rem ?? 1e9) - (sts[y.id].rem ?? 1e9)));
  $('#wifiLabel').textContent = q ? `${list.length} résultat${list.length > 1 ? 's' : ''}` : 'Les plus urgentes en premier';
  $('#wifiList').innerHTML = list.length ? list.map(a => vidCard(a, true)).join('') : `<div class="empty"><strong>Aucun résultat</strong>Essayez un autre nom de voiture.</div>`;
}

""" + s[end:]

# ---------- Feuille vidange (remplace la feuille Wi-Fi) ----------
start = s.index("function wifiSheet(aptId){"); end = s.index("function settingsSheet(){")
s = s[:start] + r"""function wifiSheet(aptId, done){
  const a = byId[aptId], w = {...(wifi[aptId] || {})};
  editingWifi = {apt: aptId, op: String(w.op || '10000')};
  if (done) { w.lastDate = todayISO(); w.lastKm = w.km || ''; }
  openSheet(`
    <div class="sheet-h"><button class="nbtn" data-act="close" style="justify-self:start">Annuler</button><h2 id="sheetTitle">${done ? 'Vidange faite' : 'Vidange'}</h2><button class="nbtn strong" data-act="saveWifi">OK</button></div>
    <form class="sheet-b" id="wifiForm" novalidate>
      <div class="list-f" style="padding:10px 14px;display:flex;gap:12px;align-items:center;margin-bottom:4px">
        <img src="img/${a.id}.jpg" alt="" width="64" height="40" style="width:64px;height:40px;border-radius:10px;object-fit:cover">
        <div><b style="font-size:16px">${esc(a.name)}</b><div style="color:var(--on-var);font-size:13px">${a.type} · ${esc(a.year)}</div></div>
      </div>
      <div class="lbl">Compteur</div>
      <div class="fields"><div class="field"><label for="wKm">Kilométrage actuel</label><input type="text" id="wKm" inputmode="numeric" value="${w.km ? fmtKm(w.km).replace(' km','') : ''}" placeholder="Ex. 45 200" autocomplete="off"></div></div>
      <div class="lbl">Dernière vidange</div>
      <div class="fields">
        <div class="field"><label for="wLastKm">Kilométrage à la vidange</label><input type="text" id="wLastKm" inputmode="numeric" value="${w.lastKm ? fmtKm(w.lastKm).replace(' km','') : ''}" placeholder="Ex. 40 000" autocomplete="off"></div>
        <div class="field"><label for="wLastDate">Date</label><input type="date" id="wLastDate" value="${esc(w.lastDate || '')}"></div>
      </div>
      <button type="button" class="danger-btn" style="color:var(--primary);margin-top:10px" data-act="vNow">${ic('vidanges')} Vidange faite aujourd’hui au km actuel</button>
      <p class="err" id="vErr" hidden></p>
      <div class="lbl" id="opLbl">Vidange tous les</div>
      <div class="ops" role="radiogroup" aria-labelledby="opLbl">${INTERVALS.map(o => `<button type="button" class="op" role="radio" aria-checked="${editingWifi.op === o}" data-op="${o}">${fmtKm(o)}</button>`).join('')}</div>
      <div class="lbl">Note</div>
      <div class="fields"><div class="field"><label for="wNote">Huile, filtres, garage…</label><input type="text" id="wNote" value="${esc(w.note || '')}" placeholder="Ex. 5W30, filtre à huile changé" autocomplete="off"></div></div>
      ${hasWifi(wifi[aptId]) ? `<button type="button" class="danger-btn" data-act="delWifi">Effacer le suivi de cette voiture</button>` : ''}
    </form>`, done ? '#wKm' : '#wKm');
}
function saveWifi(){
  const e = editingWifi; if (!e) return;
  if (!e.op) e.op = '10000';
  const km = num($('#wKm').value), lastKm = num($('#wLastKm').value);
  if (km !== '' && lastKm !== '' && lastKm > km) { const er = $('#vErr'); er.textContent = 'Le kilométrage de la vidange ne peut pas dépasser le kilométrage actuel.'; er.hidden = false; $('#wLastKm').focus(); return; }
  const w = {km, lastKm, lastDate: $('#wLastDate').value || '', op: e.op, note: $('#wNote').value.trim()};
  closeSheet(); putWifi(e.apt, w); buzz(); toast('Vidange enregistrée');
}

""" + s[end:]

# ---------- Clics ----------
rep("[data-cat],[data-op],[data-wifi],", "[data-cat],[data-op],[data-wifi],[data-vdone],")
rep("  if (el.dataset.wifi) { wifiSheet(el.dataset.wifi); return; }",
    "  if (el.dataset.wifi) { wifiSheet(el.dataset.wifi); return; }\n  if (el.dataset.vdone) { wifiSheet(el.dataset.vdone, true); return; }")
rep("    case 'saveWifi': saveWifi(); break;", """    case 'saveWifi': saveWifi(); break;
    case 'vNow': {
      const km = $('#wKm').value.trim();
      if (!km) { const er = $('#vErr'); er.textContent = 'Indiquez d’abord le kilométrage actuel.'; er.hidden = false; $('#wKm').focus(); break; }
      $('#wLastKm').value = km; $('#wLastDate').value = todayISO(); $('#vErr').hidden = true; buzz(); break;
    }""")
rep("{ const apt = editingWifi.apt, old = wifi[apt]; closeSheet(); delete wifi[apt]; lsWrite(); renderAll(); dbDel('wifi', apt); toast('Infos effacées', () => putWifi(apt, old)); }",
    "{ const apt = editingWifi.apt, old = wifi[apt]; closeSheet(); delete wifi[apt]; lsWrite(); renderAll(); dbDel('wifi', apt); toast('Suivi effacé', () => putWifi(apt, old)); }")

# ---------- Accueil ----------
rep("<button class=\"sum-chip\" data-filter=\"ok\">${ic('check')}${counts.ok} à jour</button>",
    "<button class=\"sum-chip\" data-filter=\"ok\">${ic('check')}${counts.ok} à jour</button>\n      ${(() => { const v = APTS.filter(a => vidStatus(a.id).level >= 1).length; return v ? `<a class=\"sum-chip red\" href=\"#wifi\">${ic('vidanges')}${plural(v, 'vidange')}</a>` : ''; })()}")
rep("dans ${plural(counts.todo, 'appartement')}", "sur ${plural(counts.todo, 'voiture')}")
rep("{all:'Tous les appartements', todo:'Avec des tâches', urgent:'Avec de l’urgent', ok:'À jour'}", "{all:'Toutes les voitures', todo:'Avec des tâches', urgent:'Avec de l’urgent', ok:'À jour'}")
rep("<strong>Aucun appartement</strong>", "<strong>Aucune voiture</strong>")
rep("Ajoutez une tâche, ou chargez la checklist « Après départ » pour préparer le ménage.", "Ajoutez une tâche, ou chargez la checklist « Retour client » pour contrôler la voiture.")
rep("placeholder=\"Ex. Changer l’ampoule du salon\"", "placeholder=\"Ex. Changer les essuie-glaces\"")
rep("Notes de l’appartement", "Notes du véhicule")
rep("placeholder=\"Code de la porte, contact du gardien, compteurs…\"", "placeholder=\"Assurance, contrôle technique, défauts connus…\"")
rep("'Retour au Wi-Fi' : 'Retour aux appartements'", "'Retour aux vidanges' : 'Retour aux voitures'")
rep("const LS = 'bookingalger.v1';", "const LS = 'bookingalger.voitures.v1';")
rep("<img src=\"img/${a.id}.jpg\" alt=\"Photo de ${esc(a.name)}\" width=\"124\" height=\"124\">", "<img src=\"img/${a.id}.jpg\" alt=\"Photo de la ${esc(a.name)}\" width=\"360\" height=\"180\">")
rep("<p><span class=\"glass\">${a.type}</span>${esc(a.tag)}</p>", "<p><span class=\"glass\">${a.type}</span>${esc(a.year)} · <b>${price(a.price)} DA/jour</b></p>")
rep("const plural =", "const price = n => Number(n).toLocaleString('fr-FR').replace(/[\\u202f\\u00a0]/g,' ');\nconst plural =")

# ---------- Page HTML ----------
rep("<title>BookingAlger Material</title>", "<title>BookingAlger Voitures</title>")
rep('<main id="home" class="view tabview" aria-label="Tableau de bord">', '<main id="home" class="view tabview" aria-label="Voitures">')
rep('placeholder="Rechercher un appartement"', 'placeholder="Rechercher une voiture"')
rep('<span class="sr">Rechercher un appartement</span>', '<span class="sr">Rechercher une voiture</span>')
rep('<main id="wifi" class="view tabview" aria-label="Box Wi-Fi" hidden>', '<main id="wifi" class="view tabview" aria-label="Vidanges" hidden>')
rep('<span class="nav-title">BOX WI-FI</span>', '<span class="nav-title">VIDANGES</span>')
rep('<h1>Box Wi-Fi</h1>', '<h1>Vidanges</h1>')
rep('placeholder="Appartement, numéro, réseau…"', 'placeholder="Rechercher une voiture"')
rep('<section id="detail" class="view" aria-label="Détail de l’appartement" aria-hidden="true">', '<section id="detail" class="view" aria-label="Détail de la voiture" aria-hidden="true">')
s = re.sub(r'(<a class="tab" href="#" data-tab="home" aria-current="page">)<svg.*?</svg>Appartements</a>',
  r'\1<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 17h2c.6 0 1-.4 1-1v-3c0-.9-.7-1.7-1.5-1.9C18.7 10.6 16 10 16 10s-1.3-1.4-2.2-2.3c-.5-.4-1.1-.7-1.8-.7H5c-.6 0-1.1.4-1.4.9l-1.4 2.9A3.7 3.7 0 0 0 2 12v4c0 .6.4 1 1 1h2"/><circle cx="7" cy="17" r="2"/><path d="M9 17h6"/><circle cx="17" cy="17" r="2"/></svg>Voitures</a>', s, count=1, flags=re.S)
s = re.sub(r'(<a class="tab" href="#wifi" data-tab="wifi">)<svg.*?</svg>Wi-Fi</a>',
  r'\1<svg class="ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z"/></svg>Vidanges</a>', s, count=1, flags=re.S)

# Ancre d'onglet et collection : "wifi" -> "vidanges"
s = s.replace("'wifi'", "'vidanges'").replace('"#wifi"', '"#vidanges"').replace("'#wifi'", "'#vidanges'").replace('href=\\"#wifi\\"', 'href=\\"#vidanges\\"')
s = s.replace('id="wifi" class="view tabview"', 'id="vidanges" class="view tabview"').replace('data-tab="wifi"', 'data-tab="vidanges"')
s = s.replace("$('#wifi')", "$('#vidanges')")

# ---------- Styles propres aux voitures ----------
rep("@media (prefers-reduced-motion: reduce){\n  *,*::before", """/* Voitures : photo en haut, infos en bas */
.card{background:var(--s-c)}
.card img{height:60%;object-fit:cover;object-position:center 62%}
.card::after{display:none}
.card-b{left:0;right:0;bottom:0;top:60%;background:var(--s-c);-webkit-backdrop-filter:none;backdrop-filter:none;border-radius:0;padding:8px 12px;display:flex;flex-direction:column;justify-content:center}
.card-t{font-size:15px;line-height:1.2}
.card-s{font-size:13px;font-weight:700;color:var(--primary);margin-top:3px}
.banner img{width:min(100%,360px);height:auto;border-radius:24px}
.wh img{width:76px;height:48px;border-radius:12px}
.wl .k{width:120px}
.vpill{display:inline-flex;align-items:center;gap:4px;height:28px;padding:0 10px;border-radius:14px;font-size:12px;font-weight:700;white-space:nowrap;letter-spacing:0;text-transform:none;flex:none}
.vpill .ic{width:14px;height:14px;stroke-width:2.6}
.vpill.ok{background:var(--sc);color:var(--on-sc)}
.vpill.soon{background:var(--tc);color:var(--on-tc)}
.vpill.urg{background:var(--error);color:#fff}
.vpill.todo{background:var(--s-highest);color:var(--on-var)}
.vact{display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:10px}
.vbtn{min-height:44px;border-radius:22px;background:var(--surface);color:var(--primary);font-size:14px;font-weight:700;display:inline-flex;align-items:center;justify-content:center;gap:6px;padding:0 10px;box-shadow:inset 0 0 0 1px var(--outline-var)}
.vbtn .ic{width:18px;height:18px}
.vbtn.primary{background:var(--primary);color:var(--on-primary);box-shadow:none}
.sum-chip{text-decoration:none}
@media (prefers-reduced-motion: reduce){
  *,*::before""")

(d / "app.html").write_text(s, encoding="utf-8")

head = """<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="#FFFFFF">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="BA Voitures">
<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" href="img/icon-192.png">
<link rel="apple-touch-icon" href="img/icon-180.png">
</head>
<body>
"""
(d / "index.html").write_text(head + s + "\n</body>\n</html>\n", encoding="utf-8")
print("voitures/app.html + index.html OK")
