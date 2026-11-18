# Assemble app-android.html : design Material (android-top.html) + logique partagée de app.html
import pathlib
d = pathlib.Path(__file__).parent
top = (d / "android-top.html").read_text(encoding="utf-8")
src = (d / "app.html").read_text(encoding="utf-8")
js = src[src.index("<script>"):]
reps = [
  ('`<button class="chip" data-filter="${k}" aria-pressed="${k === filter}">${l} <span class="n">',
   '`<button class="chip" data-filter="${k}" aria-pressed="${k === filter}">${k === filter ? ic(\'check\') : \'\'}${l} <span class="n">'),
  ('      <button class="act primary" data-act="new">${ic(\'plus\')}Nouvelle tâche</button>\n', ''),
  ("$('#backLbl').textContent = tab === 'wifi' ? 'Wi-Fi' : 'Appartements';", "$('#backLbl').textContent = tab === 'wifi' ? 'Retour au Wi-Fi' : 'Retour aux appartements';"),
  ("onScroll($('#detail'), $('#detNav'), 150);", "onScroll($('#detail'), $('#detNav'), 8);"),
  ("$('#detail').addEventListener('scroll', e => onScroll(e.target, $('#detNav'), 150), {passive:true});",
   "$('#detail').addEventListener('scroll', e => onScroll(e.target, $('#detNav'), 8), {passive:true});"),
  ("/* ---------- Démarrage ---------- */",
   """/* ---------- Effet ripple Material ---------- */
document.addEventListener('pointerdown', ev => {
  const el = ev.target.closest('button,a.card,a.tab,label.plain-btn');
  if (!el || el.disabled) return;
  el.classList.add('rpl');
  const r = el.getBoundingClientRect(), s = Math.max(r.width, r.height) * 2.2;
  const sp = document.createElement('span'); sp.className = 'rp';
  sp.style.cssText = `width:${s}px;height:${s}px;left:${ev.clientX - r.left - s/2}px;top:${ev.clientY - r.top - s/2}px`;
  el.appendChild(sp); setTimeout(() => sp.remove(), 600);
}, {passive:true});

/* ---------- Démarrage ---------- */"""),
]
for a, b in reps:
    assert a in js, a[:60]
    js = js.replace(a, b)
top = top.replace(".actions{display:grid;grid-template-columns:repeat(3,1fr)", ".actions{display:grid;grid-template-columns:repeat(2,1fr)")
(d / "app-android.html").write_text(top + js, encoding="utf-8")
print("app-android.html OK")
