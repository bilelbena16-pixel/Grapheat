# Academy Formation – Refonte du site

## Contexte
Site vitrine d'Academy Formation, organisme de formation à Bron (Lyon). Il présente des formations IA certifiantes, 100 % en classe virtuelle.
Site actuel : https://www.academyformation-france.fr/
Maquette de référence : `index.html` d'origine (désormais intégrée et découpée, voir « Structure des fichiers »). Elle est complète et autonome : c'est la source de vérité pour le design et les textes.

## Ce que je veux
1. Intégrer la maquette `index.html` dans le site (ou en faire le nouveau site si on repart de zéro).
2. Conserver exactement le design : fond vert sombre, effet verre (glassmorphism) sur les sections, motion design.
3. Ajouter la nouvelle formation **IA Marketing (RS7439)** sur le site, en plus de la formation existante.
4. Rendre le site responsive (mobile d'abord) et rapide.

## Charte graphique
- Fond : `#06140D`
- Accent principal : `#4ADE80` (boutons, chiffres, puces). Texte sur l'accent : `#052E16`
- Texte : `#ECFDF3` (titres), `#C6E9D4` (paragraphes), `#A7D7B9` (secondaire)
- Halos animés : `#16A34A`, `#0D9488`, `#15803D`, `#0F766E`, `#166534`
- Polices : **Sora** (titres, 600–800) et **Manrope** (texte, 400–700), via Google Fonts
- Effet verre : `.glass` / `.glass-strong` = fond blanc 6–9 %, bordure blanche 14–20 %, `backdrop-filter: blur(18–24px)`
- Rayons : 999px (boutons, pastilles), 22–32px (cartes et sections)

## Motion design (déjà dans `index.html`)
- Halos flous qui dérivent en fond (`.orb` + `drift1/2/3`)
- Apparition en fondu vers le haut au chargement (`.rise` + délais `.d1` à `.d5`)
- Carte du hero qui flotte (`.float`)
- Dégradé qui balaie le titre (`.shine`)
- Point vert pulsant sur le badge « Nouveau » (`.pulse`)
- Bandeau de points clés qui défile en continu (`.marquee`)
- Cartes qui se soulèvent au survol (`.lift`)
- Respecter `prefers-reduced-motion` (déjà en place)
- **Amélioration à faire :** déclencher les apparitions au scroll avec un `IntersectionObserver`, au lieu de tout animer au chargement.

## Structure de la page
1. Header sticky en verre : logo AF, menu (Formations, Programme IA Marketing, Inscription, Contact), bouton « Prendre rendez-vous »
2. Hero : badge nouvelle formation, titre « Maîtrisez l'IA. Certifiez vos compétences. », 2 boutons, carte IA Marketing (21 h · 8 modules · 1500 €)
3. Bandeau défilant des points clés
4. Formations : 2 cartes
   - Intégrer l'IA conversationnelle dans le cycle de vente – RS6792 – 21 h 30 – **1490 €**
   - IA Marketing : développer visibilité et acquisition – RS7439 – 21 h – **1500 €** (badge Nouveau)
5. Programme IA Marketing sur 3 jours
   - Jour 1 (9h–12h30 / 13h30–17h30) : Avant formation 0 h 30 · M1 Analyser son environnement 4 h · M2 Contenus partie 1 3 h
   - Jour 2 (9h–12h30 / 13h30–17h30) : M2 partie 2 2 h · M3 Conformité 2 h · M4 Communauté 3 h 30
   - Jour 3 (9h–12h / 13h–16h) : M5 Opportunités commerciales 3 h · M6 Pilotage 2 h · M7 Synthèse RS7439 1 h
6. Inscription en 4 étapes : contact → entretien gratuit → validation sous 48 h → démarrage sous 11 à 30 jours ouvrés. Puis encarts Assistance (≤ 2 h) et Accessibilité PSH
7. Contact : Nour-El-Dine HAKKAR · academyformation69@gmail.com · 07 58 63 57 91 · 47 rue de la Batterie, 69500 Bron
8. Footer : SASU au capital de 100 € · SIRET 92030335100034 · NAF 8559A · NDA 84692050969

## Tâches pour Claude Code
- [x] Analyser le projet existant : le site actuel est un WordPress (Elementor). Choix retenu : nouveau site **HTML statique** (aucun build, hébergeable partout), dans ce dossier `academy-site/`
- [x] Intégrer le design et les animations (+ apparitions au scroll via `IntersectionObserver`)
- [x] Créer une page dédiée par formation, avec le programme complet et un lien vers le PDF du programme
- [x] Ajouter un formulaire de contact (nom, e-mail, téléphone, formation souhaitée)
- [x] Reprendre du site actuel : logo, avis (3), financement (8 dispositifs). Pas repris : la formation « Marketing Digital » RS6702 (voir « Points à vérifier »)
- [x] SEO : title/meta, Open Graph, données structurées `Course` + `BreadcrumbList`, `sitemap.xml`, `robots.txt`
- [x] Vérifier mobile (375 px, sans défilement horizontal), accessibilité et performances — Lighthouse mobile : Performance 96 · Accessibilité 100 · Bonnes pratiques 100 · SEO 100
- [ ] Brancher le formulaire sur un service d'envoi (attribut `data-endpoint` dans `index.html`)
- [ ] Compléter les `[À COMPLÉTER]` (hébergeur, durée de conservation des données, validité RS6792)

## Structure des fichiers
- `index.html` : accueil (maquette + financement, avis, formulaire)
- `formations/ia-marketing.html` : RS7439, programme complet (source : PDF v2.0 du 08/10/2026)
- `formations/ia-conversationnelle-cycle-de-vente.html` : RS6792, programme complet (source : PDF v1.0 du 14/11/2025)
- `mentions-legales.html` : mentions légales et données personnelles
- `assets/css/style.css` (charte en variables CSS), `assets/js/main.js` (menu mobile, scroll, formulaire)
- `assets/docs/` : PDF des programmes · `assets/img/` : logo, favicons, image Open Graph

## Formulaire de contact
Sans `data-endpoint`, l'envoi ouvre la messagerie du visiteur avec un e-mail pré-rempli adressé à `data-mailto`.
Avec un `data-endpoint` (ex. `https://formspree.io/f/xxxx`), la demande est envoyée en POST JSON et un message de confirmation s'affiche sur la page.

## Points à vérifier (incohérences relevées dans les sources)
- **SIRET** : maquette et PDF RS7439 = 92030335100034 ; site actuel et PDF RS6792 = 92030335100018. Le site utilise …034.
- **RS6792** : enregistrement France Compétences « valable jusqu'au 01/10/2026 » d'après le site actuel et le PDF → à confirmer (renouvellement ?).
- **RS6702 Marketing Digital** (site actuel) : « valide jusqu'au 19/07/2026 » → non reprise sur le nouveau site.
- **Qualiopi** : le certificat en ligne (F3659-2) est daté « valable du 11/02/2026 au 12/04/2026 » et indique un NDA 84692368469 (≠ 84692050969). Logo Qualiopi non affiché tant que ce n'est pas confirmé.
- **PDF RS6792** : ancienne adresse (62 rue Christian Lacouture) et autre téléphone (07 56 93 34 75). À regénérer.
- Les 3 avis repris du site actuel ont des étiquettes incohérentes (« Formation Marketing » sur un avis parlant de la formation IA) : seuls le prénom et le texte sont affichés.
- Liens CGV, règlement intérieur et politique de confidentialité : pointent encore vers le WordPress actuel.

## Règles
- Ne rien inventer (chiffres, avis, taux de réussite) : mettre `[À COMPLÉTER]` si une info manque.
- Me montrer le plan avant toute modification importante.
- Textes en français.
