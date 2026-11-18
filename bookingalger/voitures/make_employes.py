# Génère une app par employé à partir de voitures/app.html
import pathlib, re, shutil
d = pathlib.Path(__file__).parent
base = (d / "app.html").read_text(encoding="utf-8")
A, M = "Auto", "Manuelle"
EMP = {
 "farid": ("Farid", [
  ("Dacia Sandero",M,"sandero","Blanche · 2023"),
  ("Citroën C3",M,"c3","Blanche et rouge · Samy"),
  ("Citroën C3",M,"c3","Grise"),
  ("Opel Corsa",M,"corsa","2023"),
  ("Seat Arona",M,"arona","Blanche"),
  ("Dacia Stepway",M,"stepway",""),
  ("Citroën C4",M,"c4","Blanche"),
  ("Peugeot 208",M,"p208-24","Blanche · 2024 · Samy"),
  ("Renault Captur",M,"captur","2021"),
  ("Kia KX1",A,"kx1",""),
  ("Renault Mégane",A,"megane","2022"),
  ("Citroën C4",A,"c4-auto","2023"),
  ("Fiat Tipo",A,"tipo","Grise"),
  ("Livan X3 Pro",M,"livan","2026"),
  ("Geely Coolray",A,"coolray","Sofiane"),
  ("Geely Coolray Full Options",A,"coolray-full","Farid"),
 ]),
 "ibrahim": ("Ibrahim", [
  ("Dacia Sandero",M,"sandero","Blanche · 2024"),
  ("Citroën C3",M,"c3","Blanche et rouge · ABK"),
  ("Citroën C3",M,"c3","Blanche et noire"),
  ("Citroën C3",M,"c3","Blanche"),
  ("Seat Arona",M,"arona","Bleue"),
  ("Citroën C4",M,"c4","Noire"),
  ("Volkswagen T-Cross",M,"tcross",""),
  ("Peugeot 208",M,"p208-24","Blanche · 2024"),
  ("Chevrolet Captiva",A,"captiva","7 places"),
  ("Peugeot 208",A,"p208-23","2023"),
  ("Kia KX1",A,"kx1",""),
  ("Fiat Tipo",A,"tipo","Bleue"),
  ("MG 5 n°1",M,"mg5","2026"),
  ("MG 5 n°2",M,"mg5","2026"),
 ]),
}
def js(v): return v.replace("\\","\\\\").replace("'","\\'")
for key, (person, cars) in EMP.items():
    out = d.parent / key; (out / "img").mkdir(parents=True, exist_ok=True)
    for f in ["logo.png","mark.png","icon-180.png","icon-192.png","icon-512.png"]: shutil.copy(d/"img"/f, out/"img"/f)
    rows = []
    for n,(name,typ,img,det) in enumerate(cars, 1):
        cid = f"{key[0]}{n:02d}"
        shutil.copy(d/"img"/f"{img}.jpg", out/"img"/f"{cid}.jpg")
        boite = "Boîte auto" if typ == A else "Boîte manuelle"
        tag = det if det else boite
        rows.append(f"  {{id:'{cid}', name:'{js(name)}', type:'{typ}', year:'{js(det)}', price:0, tag:'{js(tag)}'}}")
    s = re.sub(r"const APTS = \[.*?\n\];", "const APTS = [\n" + ",\n".join(rows) + "\n];", base, count=1, flags=re.S)
    def rep(a, b):
        global s_
    reps = [
      ("<title>BookingAlger Voitures</title>", f"<title>BookingAlger {person}</title>"),
      ("const LS = 'bookingalger.voitures.v1';", f"const LS = 'bookingalger.{key}.v1';"),
      ("$('#homeSub').textContent = date.charAt(0).toUpperCase() + date.slice(1);",
       f"$('#homeSub').textContent = '{person} · ' + date.charAt(0).toUpperCase() + date.slice(1);"),
      ("<p><span class=\"glass\">${a.type}</span>${esc(a.year)} · <b>${price(a.price)} DA/jour</b></p>",
       "<p><span class=\"glass\">${a.type}</span>${esc(a.tag)}</p>"),
      ("fold([a.name, a.type, a.year].join(' '))", "fold([a.name, a.type, a.tag].join(' '))"),
    ]
    for a,b in reps:
        assert a in s, a[:60]; s = s.replace(a, b)
    assert s.count("${a.type} · ${esc(a.year)}") >= 2
    s = s.replace("${a.type} · ${esc(a.year)}", "${a.type} · ${esc(a.tag)}")
    (out / "app.html").write_text(s, encoding="utf-8")
    idx = (d / "index.html").read_text(encoding="utf-8")
    head = idx[:idx.index("<body>") + len("<body>\n")].replace("BA Voitures", f"BA {person}")
    (out / "index.html").write_text(head + s + "\n</body>\n</html>\n", encoding="utf-8")
    (out / "manifest.webmanifest").write_text((d / "manifest.webmanifest").read_text().replace("BookingAlger Voitures", f"BookingAlger {person}").replace("BA Voitures", f"BA {person}"))
    print(key, len(cars), "véhicules OK")
