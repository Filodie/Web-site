# filodie.ca

Site de Filodie : outils cliniques pour T.E.S. (français et anglais).

## Contenu du dépôt

| Élément | Rôle |
|---|---|
| `public/` | **Le site à mettre en ligne** : pages HTML, style, polices, images des produits. Rien à compiler. |
| `produits.json` | Le catalogue : titre, description, **prix** et **identifiant Payhip** de chaque produit. |
| `build_site.py` | Régénère le dossier `public/` à partir de `produits.json` (Python 3 et PyMuPDF). |

## Mettre le site en ligne (Cloudflare Pages, gratuit)

1. Publiez ce dépôt sur GitHub, avec GitHub Desktop : *File → Add local repository*, puis *Publish repository*. Un dépôt privé fonctionne.
2. Sur Cloudflare, ouvrez *Workers & Pages → Create → Pages → Connect to Git* et choisissez le dépôt.
3. Réglages de build : **Framework preset** = None, **Build command** = (vide), **Build output directory** = `public`.
4. Dans l'onglet *Custom domains*, ajoutez `filodie.ca` et `www.filodie.ca`.

À chaque *push* sur GitHub, Cloudflare remet le site à jour automatiquement.

> GitHub Pages est déconseillé : ses conditions d'utilisation excluent les sites servant principalement au commerce en ligne. Cloudflare Pages et Netlify le permettent.

## Activer un bouton « Acheter »

1. Dans Payhip, créez le produit. Son lien ressemble à `https://payhip.com/b/AbC12`.
2. Dans `produits.json`, écrivez `AbC12` dans `"payhip"` pour la version française, ou dans `"payhip_en"` pour la version anglaise.
3. Lancez `python3 build_site.py`, puis envoyez les changements sur GitHub (*commit* et *push*).

Pour changer un prix, modifiez `"prix"` dans `produits.json`, puis faites la même chose.

## Commandes

```bash
python3 build_site.py               # régénère les pages
python3 build_site.py --catalogue   # relit les PDF (nouveaux produits) en conservant prix et liens
python3 build_site.py --prix        # réapplique la grille de prix par défaut définie dans build_site.py
```

Les options `--catalogue` et `--prix` et la création des images ont besoin du dossier `Filodie – Outils T.E.S.` placé à côté de ce dépôt. Pour modifier seulement des prix ou des liens, `build_site.py` suffit.

© 2026 Filodie. Illustrations : Fluent Emoji © Microsoft (licence MIT). Polices : Fraunces, Nunito Sans (SIL Open Font License).
