# Ajouter un témoignage

Seulement des témoignages **réels**, avec un « oui » écrit à la publication (courriel conservé).

Ajoute un bloc dans `temoignages.json`, puis lance `python3 publier.py --catalogue "Nouveau témoignage"` :

```json
[
  {
    "prenom": "Julie",
    "role_fr": "T.E.S. au primaire",
    "role_en": "Special care counsellor, elementary school",
    "texte_fr": "Le texte tel qu'écrit par la personne.",
    "texte_en": "Traduction anglaise (facultative).",
    "outil": "Cahier de détective – Émotions",
    "date": "2026-10-15",
    "consentement": true
  }
]
```

- `consentement: true` est obligatoire, sinon le témoignage n'apparaît pas.
- Jamais de nom de famille, de milieu de travail ni de détail sur un enfant.
- Les 6 premiers s'affichent sur l'accueil (FR et EN).

# Ajouter une note Payhip (étoiles seulement)

Quand un avis Payhip n'a pas de texte, ajoute une ligne dans `avis_payhip.json` (jamais de nom ni de courriel) :

```json
{"outil_fr": "Nom de l'outil", "outil_en": "Tool name", "etoiles": 5, "date": "2026-10-05"}
```

La moyenne et le nombre d'avis s'affichent sur l'accueil (FR et EN). Puis `python3 publier.py --catalogue "Nouvel avis"`.
