# Consignes permanentes – Comptes rendus de TP

Ces règles s'appliquent à chaque nouveau TP demandé par l'utilisateur.

## Déroulé d'un TP
- Faire le TP en entier, de A à Z (commandes, configuration, vérifications).
- TP sur VM ou sur machine : tout exécuter soi-même et noter chaque commande et son résultat.
- Prendre une capture à chaque fois que le sujet en demande une (et aux étapes clés si rien n'est précisé).
- Si quelque chose n'est pas faisable depuis l'environnement (pas de VM, pas d'accès à l'ordi, logiciel graphique Windows…),
  le dire clairement à l'utilisateur au lieu d'inventer un résultat ou une capture.

## Rangement
- Un dossier par TP : `comptes-rendus/TPxx-sujet/`
  - `cr.md` : texte du compte rendu
  - `captures/` : captures numérotées (`01-...png`, `02-...png`)
  - `cr.docx` et `cr.pdf` : documents finaux générés

## Style du compte rendu
- Simple et sobre, pas un document « tape-à-l'œil ».
- Une seule police pour tout (Calibri), texte en noir, pas de couleurs.
- Pas de schéma ni d'image générés par IA : uniquement les vraies captures du TP.
- Plan type : Objectif / Réalisation (étapes avec commandes + captures) / Conclusion.
- Phrases courtes, ton d'étudiant, en français.

## Génération et métadonnées
- Capture d'une commande : `node comptes-rendus/outils/capture_terminal.js "commande" captures/01-nom.png`
  (préfixer par `NODE_PATH=$(npm root -g)` si besoin).
- Générer le document : `python3 comptes-rendus/outils/generer_cr.py comptes-rendus/TPxx-sujet/cr.md --pdf`
- Le script supprime automatiquement les métadonnées (auteur, dates, logiciel, EXIF des images, infos du PDF).
  Toujours générer par ce script, ne jamais livrer un fichier qui n'est pas passé par lui.
