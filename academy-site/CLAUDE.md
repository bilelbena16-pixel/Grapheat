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
- [x] Ajouter un formulaire de contact (nom, e-mail, téléphone, formation souhaitée, situation)
- [x] Reprendre **tout** le contenu du site actuel : logo, Qualiopi (logo + certificat), France Compétences, formateur, qui sommes-nous, pourquoi nous, 4 piliers, chiffres clés, déroulement, avis, financements, FAQ, formation Marketing digital RS6702, mentions légales, CGV, règlement intérieur, politique de confidentialité, WhatsApp, espace apprenant
- [x] SEO : title/meta, Open Graph, données structurées `Course` + `BreadcrumbList`, `sitemap.xml`, `robots.txt`
- [x] Vérifier mobile (375 px, sans défilement horizontal), accessibilité et performances — Lighthouse mobile : 100 / 100 / 100 / 100 sur l'accueil et les pages formation
- [ ] Brancher le formulaire sur un service d'envoi (attribut `data-endpoint` dans `index.html`)
- [ ] Trancher les incohérences listées ci-dessous

## Structure des fichiers
- `index.html` : accueil (formations, programme, qui sommes-nous, formateur, labels, inscription, financement, avis, contact)
- `formations/ia-marketing.html` : RS7439 (source : PDF v2.0 du 08/10/2026)
- `formations/ia-conversationnelle-cycle-de-vente.html` : RS6792 (source : PDF v1.0 du 14/11/2025 + page du site actuel)
- `formations/marketing-digital.html` : RS6702 (source : page du site actuel ; pas de PDF)
- `mentions-legales.html`, `cgv.html`, `reglement-interieur.html`, `politique-de-confidentialite.html` : repris du site actuel (version du 14/11/2025)
- `assets/css/style.css` (charte en variables CSS), `assets/js/main.js` (menu mobile, scroll, formulaire)
- `assets/docs/` : PDF des programmes + certificat Qualiopi · `assets/img/` : logos, favicons, image Open Graph
- `outils/synchro-gabarit.py` : **en-tête, menu, pied de page et bouton WhatsApp sont définis dans ce script**. Pour les modifier : éditer le script puis lancer `python3 outils/synchro-gabarit.py` (met à jour toutes les pages)

## Thème sombre / thème clair (fond blanc)
Le site existe en deux versions avec le même contenu :
- **clair** (**par défaut**, choisi le 08/10/2026) : fond blanc, mêmes boutons #4ADE80, textes et icônes en verts foncés (#052E16, #15803D, #16A34A) pour garder les contrastes AA ;
- **sombre** : fond vert foncé #06140D (charte d'origine de la maquette).
Pour basculer toutes les pages : `python3 outils/synchro-gabarit.py clair` (ou `sombre`). Le thème clair est défini en fin de `assets/css/style.css` (`:root[data-theme="light"]`).

## Formulaire de contact
Sans `data-endpoint`, l'envoi ouvre la messagerie du visiteur avec un e-mail pré-rempli adressé à `data-mailto`.
Avec un `data-endpoint` (ex. `https://formspree.io/f/xxxx`), la demande est envoyée en POST JSON et un message de confirmation s'affiche sur la page.

## Points à vérifier (incohérences relevées dans les sources)
- **SIRET** : maquette et PDF RS7439 = 92030335100034 ; site actuel, PDF RS6792 et anciennes mentions légales = 92030335100018. Le nouveau site utilise …034 partout (y compris mentions légales et politique de confidentialité).
- **Qualiopi** : le certificat F3659-2-I est « valable du 11/02/2026 au 12/04/2026 » et indique un NDA 84692368469 (≠ 84692050969). Affiché comme sur le site actuel ; à remplacer par le certificat en cours de validité.
- **Validité des certifications** (dates reprises du site actuel) : RS6792 « valide jusqu'au 01/10/2026 », RS6702 « valide jusqu'au 19/07/2026 ».
- **RS6702** : certificateur « Les Instapreneurs » ou « SCORE » (le site actuel indique les deux) → `[À COMPLÉTER]` sur la page. L'objectif « valider la certification RS 6792 » de l'ancien site a été corrigé en RS6702.
- **Délais et assistance contradictoires** : démarrage « 11 à 30 jours ouvrés » (PDF) vs « < 7 jours ouvrés » (ancien site) ; assistance « ≤ 2 h » (PDF) vs « réponse sous 24 h » (ancien site). Annulation : « sans frais ≥ 10 jours ouvrés » (pages formation) vs barème CGV (≥ 14 j : 0 %, 7–13 j : 50 %, < 7 j : 100 %). CGV « prix en EUR HT » vs « TVA non applicable » sur les formations.
- **Programme RS6792** : le site actuel présentait un programme en 10 étapes (dont « Automatisation & intégration » et une présentation finale de 20–30 pages) différent du PDF officiel. Le nouveau site suit le PDF.
- **PDF RS6792** : ancienne adresse (62 rue Christian Lacouture) et autre téléphone (07 56 93 34 75). À regénérer.
- **Non repris volontairement** : textes « chantier, sécurité » de « Qui sommes-nous » (ne correspondent pas aux formations proposées), « Taux de réussite supérieurs à la moyenne » (contredit « en attente de statistiques »), « Progressez à votre rythme, sans contrainte horaire » (contredit le 100 % synchrone), illustrations génériques (pas de photo réelle du formateur). La mention « chantier, sécurité, bureautique » reste dans « Objet du site » des mentions légales (texte juridique repris à l'identique).

## Règles
- Ne rien inventer (chiffres, avis, taux de réussite) : mettre `[À COMPLÉTER]` si une info manque.
- Me montrer le plan avant toute modification importante.
- Textes en français.
