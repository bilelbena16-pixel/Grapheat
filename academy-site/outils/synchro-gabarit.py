#!/usr/bin/env python3
"""Synchronise l'en-tête, le pied de page et le bouton WhatsApp sur toutes les pages.

Usage (depuis le dossier academy-site) :  python3 outils/synchro-gabarit.py [sombre|clair]

Modifier le menu ou le pied de page ICI, puis relancer le script : chaque page .html
est réécrite entre <header class="site-header ...> … </header>, entre
<footer class="site-footer"> … </footer> et sur la ligne du bouton WhatsApp.
"""
import pathlib
import re
import sys

# Thème du site : "clair" (fond blanc, par défaut) ou "sombre" (fond vert foncé).
# On peut aussi le passer en argument : python3 outils/synchro-gabarit.py clair
THEME = "clair"
if len(sys.argv) > 1:
    THEME = sys.argv[1]
assert THEME in ("sombre", "clair"), "Thème attendu : sombre ou clair"

RACINE = pathlib.Path(__file__).resolve().parent.parent

FORMATIONS = [
    ("formations/ia-marketing.html", "IA Marketing – RS7439"),
    ("formations/ia-conversationnelle-cycle-de-vente.html", "IA conversationnelle et vente – RS6792"),
    ("formations/marketing-digital.html", "Marketing digital – RS6702"),
]
INFOS = [
    ("index.html#a-propos", "Qui sommes-nous ?"),
    ("index.html#equipe", "Notre équipe"),
    ("mentions-legales.html", "Mentions légales"),
    ("cgv.html", "Conditions générales de vente"),
    ("reglement-interieur.html", "Règlement intérieur"),
    ("politique-de-confidentialite.html", "Politique de confidentialité"),
]

WA_ICON = ('<svg width="30" height="30" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2a9.9 9.9 0 0 0-8.5 15l-1.4 5.1 5.2-1.4A9.9 9.9 0 1 0 12.04 2Zm0 18.1a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3.1.8.8-3-.2-.3a8.2 8.2 0 1 1 7 3.9Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z"/></svg>')


def header(p, page):
    def cur(target):
        return ' aria-current="page"' if page == target else ''
    return f'''<header class="site-header glass rise">
<a class="brand" href="{p}index.html" aria-label="Academy Formation – accueil">
<img src="{p}assets/img/logo-academy-formation.png" width="36" height="36" alt="">
<span>Academy Formation</span>
</a>
<button class="nav-toggle" type="button" aria-expanded="false" aria-controls="nav" aria-label="Ouvrir le menu"><span class="bars" aria-hidden="true"><span class="bar"></span><span class="bar"></span><span class="bar"></span></span></button>
<nav id="nav" class="nav" aria-label="Navigation principale">
<a href="{p}index.html#formations">Formations</a>
<a href="{p}formations/ia-marketing.html"{cur("formations/ia-marketing.html")}>Programme IA Marketing</a>
<a href="{p}index.html#a-propos">À propos</a>
<a href="{p}index.html#inscription">Inscription</a>
<a href="{p}index.html#contact">Contact</a>
<a class="btn btn-main btn-sm" href="{p}index.html#contact">Prendre rendez-vous</a>
</nav>
</header>'''


def footer(p, page):
    def li(href, label):
        cur = ' aria-current="page"' if page == href else ''
        return f'<li><a href="{p}{href}"{cur}>{label}</a></li>'
    forms = "\n".join(li(h, l) for h, l in FORMATIONS)
    infos = "\n".join(li(h, l) for h, l in INFOS)
    return f'''<footer class="site-footer">
<div>
<a class="brand" href="{p}index.html"><img src="{p}assets/img/logo-academy-formation.png" width="32" height="32" alt="" loading="lazy"><span>Academy Formation</span></a>
<p>Organisme de formation à Bron (Lyon). Formations certifiantes en classe virtuelle.</p>
<a class="logo-plate sm" href="{p}assets/docs/certificat-qualiopi-F3659-2.pdf" style="margin-top:16px" aria-label="Certificat Qualiopi (PDF)"><img src="{p}assets/img/logo-qualiopi.png" width="82" height="44" alt="Qualiopi – processus certifié – République française" loading="lazy"></a>
<p style="margin-top:10px">La certification qualité a été délivrée au titre de la catégorie d’action suivante : actions de formation.</p>
</div>
<div>
<h2>Formations</h2>
<ul>
{forms}
</ul>
</div>
<div>
<h2>Contact</h2>
<ul>
<li><a href="tel:+33758635791">07 58 63 57 91</a></li>
<li><a href="https://wa.me/33758635791" rel="noopener">WhatsApp</a></li>
<li><a href="mailto:academyformation69@gmail.com">academyformation69@gmail.com</a></li>
<li>47 rue de la Batterie, 69500 Bron</li>
</ul>
</div>
<div>
<h2>Informations</h2>
<ul>
{infos}
<li><a href="https://academyformation.talentlms.com/plus/login" rel="noopener">Espace apprenant</a></li>
</ul>
</div>
<div class="legal-bar">
<div><span style="font-family:var(--font-title);font-weight:700;color:var(--title)">Academy Formation</span> · SASU au capital de 100 € · RCS Lyon 920 303 351 · SIRET 92030335100034 · NAF 8559A</div>
<div>NDA 84692050969 – enregistrée auprès du préfet de région Auvergne-Rhône-Alpes</div>
<div style="flex-basis:100%">Copyright © 2026 Academy Formation France · Tous droits réservés</div>
</div>
</footer>'''


WA = '<a class="wa-float" href="https://wa.me/33758635791" rel="noopener" aria-label="Nous écrire sur WhatsApp">' + WA_ICON + '</a>'

for f in sorted(RACINE.rglob("*.html")):
    rel = f.relative_to(RACINE).as_posix()
    p = "../" * rel.count("/")
    s = f.read_text(encoding="utf-8")
    s = re.sub(r'<header class="site-header.*?</header>', lambda m: header(p, rel), s, count=1, flags=re.S)
    s = re.sub(r'<footer class="site-footer">.*?</footer>', lambda m: footer(p, rel), s, count=1, flags=re.S)
    s = re.sub(r'\n<a class="wa-float"[^\n]*', '', s)
    s = s.replace('</footer>\n', '</footer>\n' + WA + '\n', 1)
    s = re.sub(r'<html lang="fr"[^>]*>', '<html lang="fr" data-theme="light">' if THEME == "clair" else '<html lang="fr">', s, count=1)
    s = re.sub(r'<meta name="theme-color" content="[^"]*">', '<meta name="theme-color" content="%s">' % ("#FFFFFF" if THEME == "clair" else "#06140D"), s, count=1)
    f.write_text(s, encoding="utf-8")
    print("ok", rel)
