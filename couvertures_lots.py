# -*- coding: utf-8 -*-
"""Couvertures des lots Filodie (FR et EN), toutes dans le même style.

Pour chaque lot de produits.json : logo, « LOT FILODIE », titre, sous-titre, grille de miniatures des produits
inclus (échantillon réparti si le lot est grand) et pastille bilingue.
Sortie : couvertures_lots/{id}_{fr,en}.jpg — build_site.py les reprend pour le site ; sur Payhip, elles servent de
vignette du lot.  Relancer : python3 couvertures_lots.py [id…]   (après build_site.py, qui crée les miniatures)"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "Filodie – Outils T.E.S.", "_source"))
from filodie_logo import logo, police, ENCRE, TERRA, SAUGE, MOUTARDE, ROSE, CREME  # noqa: E402
import build_site as B  # noqa: E402

SORTIE = os.path.join(HERE, "couvertures_lots")
IMG = os.path.join(HERE, "public", "img")
W, H = 1200, 1553
MARGE = 80

TXT = {"fr": dict(kicker="LOT FILODIE", badge=("FR", "+ EN"), pied="PDF imprimables et remplissables · filodie.ca"),
       "en": dict(kicker="FILODIE BUNDLE", badge=("EN", "+ FR"), pied="Printable, fillable PDFs · filodie.ca")}


def lignes(txt, fichier, taille, largeur):
    f = police(fichier, taille)
    out, cur = [], ""
    for mot in txt.split():
        essai = (cur + " " + mot).strip()
        if f.getlength(essai) <= largeur or not cur:
            cur = essai
        else:
            out.append(cur)
            cur = mot
    return out + [cur]


def echantillon(ids, k):
    """k produits répartis dans tout le lot (pour montrer sa variété)."""
    if len(ids) <= k:
        return ids
    return [ids[round(j * (len(ids) - 1) / (k - 1))] for j in range(k)]


def miniature(pid, lang):
    for l in (lang, "fr"):
        p = os.path.join(IMG, l, pid + ".jpg")
        if os.path.exists(p):
            return Image.open(p).convert("RGB")
    return None


def couverture(lot, lang):
    tx = TXT[lang]
    titre = lot["titre"] if lang == "fr" else B.en(lot, "titre")
    sous = (lot.get("sous") or "") if lang == "fr" else B.en(lot, "sous") if lot.get("sous") else ""
    im = Image.new("RGB", (W, H), CREME)
    d = ImageDraw.Draw(im)

    lg = logo(1.45)
    im.paste(lg, ((W - lg.width) // 2, 60), lg)
    y = 60 + lg.height + 64
    d.text((W / 2, y), tx["kicker"], font=police("NunitoSans-800.ttf", 26), fill=TERRA, anchor="ms")
    taille = 62
    tl = lignes(titre, "Fraunces-600.ttf", taille, W - 2 * MARGE)
    if len(tl) > 2:
        taille = 52
        tl = lignes(titre, "Fraunces-600.ttf", taille, W - 2 * MARGE)
    y += 80
    for l in tl:
        d.text((W / 2, y), l, font=police("Fraunces-600.ttf", taille), fill=ENCRE, anchor="ms")
        y += int(taille * 1.19)
    if sous:
        d.text((W / 2, y + 6), sous, font=police("Fraunces-500i.ttf", 34), fill=SAUGE, anchor="ms")
        y += 40

    # grille : jusqu’à 11 miniatures + la pastille bilingue
    ids = echantillon(lot["contient"], 11)
    thumbs = [m for m in (miniature(p, lang) for p in ids) if m]
    cases = len(thumbs) + 1
    cols = 2 if cases <= 4 else 3 if cases <= 9 else 4
    rows = math.ceil(cases / cols)
    top, bas, gap = y + 50, H - 150, 30
    ratio = 1.294
    mw = min((W - 2 * MARGE - (cols - 1) * gap) / cols, ((bas - top) - (rows - 1) * gap) / rows / ratio, 300)
    mw, mh = int(mw), int(mw * ratio)
    x0 = (W - (cols * mw + (cols - 1) * gap)) // 2
    y0 = top + ((bas - top) - (rows * mh + (rows - 1) * gap)) // 2
    for k in range(cases):
        r, c = divmod(k, cols)
        if r == rows - 1:                                  # dernière rangée centrée
            n_der = cases - (rows - 1) * cols
            xs = (W - (n_der * mw + (n_der - 1) * gap)) // 2
        else:
            xs = x0
        cx, cy = xs + c * (mw + gap), y0 + r * (mh + gap)
        if k < len(thumbs):
            t = thumbs[k]
            t.thumbnail((mw, mh), Image.LANCZOS)
            ox, oy = cx + (mw - t.width) // 2, cy + (mh - t.height) // 2
            ombre = Image.new("RGBA", (t.width + 30, t.height + 30), (0, 0, 0, 0))
            ImageDraw.Draw(ombre).rectangle([15, 15, t.width + 15, t.height + 15], fill=(31, 59, 77, 70))
            ombre = ombre.filter(ImageFilter.GaussianBlur(8))
            im.paste(ombre, (ox - 9, oy - 5), ombre)
            im.paste(t, (ox, oy))
        else:
            rr = min(mw, mh) // 2 - 10
            mx, my = cx + mw // 2, cy + mh // 2
            d.ellipse([mx - rr, my - rr, mx + rr, my + rr], fill=TERRA)
            d.text((mx, my - rr * 0.08), tx["badge"][0], font=police("NunitoSans-800.ttf", int(rr * 0.72)),
                   fill=CREME, anchor="ms")
            d.text((mx, my + rr * 0.55), tx["badge"][1], font=police("NunitoSans-800.ttf", int(rr * 0.5)),
                   fill=CREME, anchor="ms")

    yb = H - 70
    for i, c in enumerate([ENCRE, TERRA, SAUGE, MOUTARDE, ROSE]):
        x = W / 2 - 88 + i * 44
        d.ellipse([x - 9, yb - 56, x + 9, yb - 38], fill=c)
    d.text((W / 2, yb), tx["pied"], font=police("NunitoSans-700.ttf", 28), fill=ENCRE, anchor="ms")
    out = os.path.join(SORTIE, f"{lot['id']}_{lang}.jpg")
    im.save(out, quality=90, optimize=True)
    return out


if __name__ == "__main__":
    os.makedirs(SORTIE, exist_ok=True)
    items = json.load(open(os.path.join(HERE, "produits.json"), encoding="utf-8"))
    for lot in items:
        if lot.get("contient") and (not sys.argv[1:] or lot["id"] in sys.argv[1:]):
            for lang in ("fr", "en"):
                couverture(lot, lang)
            print("✓", lot["id"])
