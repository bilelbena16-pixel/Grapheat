# Academy Formation – site vitrine

Site statique (HTML/CSS/JS, sans dépendance ni étape de build).

## Prévisualiser en local
```bash
cd academy-site
python3 -m http.server 8000
# puis ouvrir http://localhost:8000
```

## Mettre en ligne
Déposer le contenu du dossier `academy-site/` à la racine de l'hébergement (OVH, o2switch, Netlify, Vercel, GitHub Pages…).
Activer la compression gzip/brotli et un cache long pour `assets/` côté hébergeur.

Voir `CLAUDE.md` pour la charte, la structure et les points à vérifier.

## Modifier le menu ou le pied de page
Ils sont communs à toutes les pages : éditer `outils/synchro-gabarit.py` puis lancer `python3 outils/synchro-gabarit.py`.
