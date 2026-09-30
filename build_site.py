# -*- coding: utf-8 -*-
"""Construit le site filodie.ca (français + anglais) dans le dossier « public ».

    python3 build_site.py            # pages + images manquantes
    python3 build_site.py --catalogue  # relit les PDF et met à jour produits.json (garde prix et liens Payhip)

Pour activer un bouton « Acheter » : collez l'identifiant Payhip (ex. « aB3dE ») dans produits.json,
champ "payhip" (français) ou "payhip_en" (anglais), puis relancez ce script."""
import html
import hashlib
import json
import os
import re
import shutil
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT_FR = os.path.join(ROOT, "Filodie – Outils T.E.S.")
OUT_EN = os.path.join(ROOT, "Filodie – Tools for Special Education (English)")
SRC = os.path.join(OUT_FR, "_source")
PUB = os.path.join(HERE, "public")
LOGO = os.path.join(ROOT, "Logo Filodie")
# Fil à 5 perles du logo (mêmes unités que _source/filodie_logo.py), affiché sous le mot « filodie »
BEADS = ('<svg viewBox="33 106 236 48" aria-hidden="true"><path d="M40 130C67 110 67 110 95 130S122 150 150 130'
         'S177 110 205 130S232 150 260 130" fill="none" stroke="#D9734E" stroke-width="3.2" stroke-linecap="round"/>'
         + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="{c}"/>' for x, y, c in [
             (67, 115, "#1F3B4D"), (123, 145, "#D9734E"), (178, 115, "#6F9A81"), (233, 145, "#E3B04B"),
             (260, 130, "#D98FA0")]) + "</svg>")
CAT = os.path.join(HERE, "produits.json")
sys.path.insert(0, SRC)

EN = {}
for fn in sorted(os.listdir(os.path.join(SRC, "i18n"))) if os.path.isdir(os.path.join(SRC, "i18n")) else []:
    if fn.startswith("en_") and fn.endswith(".json"):
        EN.update(json.load(open(os.path.join(SRC, "i18n", fn), encoding="utf-8")))


# Identifiants conservés quand un volet est renommé (le code Payhip est rattaché à l’identifiant).
ID_STABLE = {"lot-10-boîte-à-outils-en-psychoéducation": "lot-10-boîte-à-outils-du-psychoéducateur"}


def tr(s):
    return EN.get(s, s)


def en(i, k):
    """Texte anglais d'un produit : champ <k>_en s'il existe (textes calculés), sinon le dictionnaire."""
    return i.get(k + "_en") or tr(i[k])


# Prix à l'unité (dollars canadiens). Les lots ont leur prix fixé plus bas, dans catalogue().
# Chaque produit est bilingue (PDF français + anglais dans le même achat).
PRIX = {"trousse": 7.00, "edition": 3.00, "cahier": 3.00, "livre": 19.00, "bottin": 0.0,
        "lot_cahiers": 25.00, "lot_collection": 25.00, "lot_specialisees": 39.00, "lot_tout": 75.00, "mega": 129.00,
        "affiches": 5.00, "lot_affiches": 19.00, "jeux": 7.00, "lot_jeux": 29.00,
        "routines": 5.00, "lot_routines": 19.00, "gratuit": 0.00}


# --------------------------------------------------------------------------- catalogue
def catalogue():
    from contenu_ages import AGES
    from contenu_troubles import TROUBLES
    from contenu_nouveaux import NOUVEAUX
    import filodie_trousses as ft
    from filodie_editions import EDITIONS
    from filodie_visuel import load, SERIES, fname
    from filodie_affiches import load as load_affiches, fichier as fichier_affiches
    from filodie_jeux import load as load_jeux, fichier as fichier_jeux
    from filodie_routines import load as load_routines, fichier as fichier_routines
    from outil_du_mois import load as load_gratuit, fichier as fichier_gratuit
    items = []

    def add(**k):
        k.setdefault("prix", 0.0 if "decouverte" in k["id"] else PRIX[k["type"]])   # trousse découverte : gratuite
        k.setdefault("payhip", "")
        k.setdefault("payhip_en", "")
        items.append(k)

    add(id="trousse-principale", type="trousse", groupe="Trousses essentielles", titre="Trousse Filodie : Tenir le fil",
        sous="12 outils de l’observation à l’intervention",
        desc="Douze outils sobres, précis et reliés entre eux. Chaque fiche indique son étape du fil, renvoie à la suivante "
             "et se termine par un repère clinique. Imprimables ou remplissables à l’écran.",
        fichiers=["Trousse_Filodie_Outils_TES_2026.pdf"])
    for t in AGES + TROUBLES + NOUVEAUX:
        add(id="trousse-" + t["fichier"].lower(), type="trousse", groupe="Trousses spécialisées", titre=t["nom"],
            sous=f"{len(t['fiches'])} outils", desc=t["desc"],
            fichiers=[f"Trousses spécialisées/Trousse_Filodie_{t['fichier']}_2026.pdf"])
    from outil_choix_eclaire import CHOIX                 # outils d’intervention vendus à l’unité, hors collection
    from outils_3dollars import OUTILS
    for t in [CHOIX] + OUTILS:
        add(id="trousse-" + t["fichier"].lower(), type="trousse", groupe="Outils d’intervention", titre=t["nom"],
            sous=f"{len(t['fiches'])} outils", desc=t["desc"], prix=3.0,
            fichiers=[f"{t['dossier']}/Trousse_Filodie_{t['fichier']}_2026.pdf"])
    for t in ft.LOTS:
        add(id="trousse-" + t["fichier"].lower(), type="trousse", groupe=t["dossier"].split("/")[-1].split("– ")[-1],
            titre=t["nom"], sous=f"{len(t['fiches'])} outils", desc=t["desc"],
            fichiers=[f"{t['dossier']}/Trousse_Filodie_{t['fichier']}_2026.pdf"])
    for name, folder, tools, kicker, l1, l2, desc, groups in EDITIONS:
        add(id="edition-" + folder.lower(), type="edition", groupe="Éditions complémentaires",
            titre=f"Édition {name}", sous=f"{len(tools)} fiches", desc=desc,
            fichiers=[f"Éditions complémentaires/Filodie_{folder}_2026.pdf"])
    for c in load():
        s = SERIES[c.serie]
        add(id="cahier-" + c.code.lower(), type="cahier", groupe="Cahiers " + s["nom"], titre=c.titre,
            sous=c.public, desc=c.sous, code=c.code,
            fichiers=[f"Cahiers visuels Filodie/{s['dossier']}/Couleur/{fname(c)}.pdf",
                      f"Cahiers visuels Filodie/{s['dossier']}/À colorier (noir et blanc)/{fname(c)}_NB.pdf"])
    for pq in load_affiches():
        f = fichier_affiches(pq)
        add(id="affiches-" + pq.code.lower(), type="affiches", groupe="Affiches murales", titre="Affiches : " + pq.titre,
            titre_en="Posters: " + tr(pq.titre), sous=pq.sous, desc=pq.desc, code=pq.code,
            fichiers=[f"Affiches murales Filodie/Couleur/{f}.pdf", f"Affiches murales Filodie/Noir et blanc/{f}_NB.pdf"])
    for pq in load_jeux():
        f = fichier_jeux(pq)
        add(id="jeux-" + pq.code.lower(), type="jeux", groupe="Jeux et cartes", titre=pq.titre,
            sous=pq.sous, desc=pq.desc, code=pq.code,
            fichiers=[f"Jeux et cartes Filodie/Couleur/{f}.pdf", f"Jeux et cartes Filodie/Noir et blanc/{f}_NB.pdf"])
    for pq in load_routines():
        f = fichier_routines(pq)
        add(id="routines-" + pq.code.lower(), type="routines", groupe="Routines visuelles maison", titre=pq.titre,
            sous=pq.sous, desc=pq.desc, code=pq.code,
            fichiers=[f"Routines visuelles Filodie/Couleur/{f}.pdf", f"Routines visuelles Filodie/Noir et blanc/{f}_NB.pdf"])
    from datetime import date as _d
    _t = _d.today()
    _nxt = (_d(_t.year + 1, 1, 1) if _t.month == 12 else _d(_t.year, _t.month + 1, 1)).strftime("%y%m")
    for pq in load_gratuit():
        f = fichier_gratuit(pq)                        # outils des mois futurs : cachés sur le site (futur=True)
        add(id="gratuit-" + pq.code.lower(), type="gratuit", groupe="Outil gratuit du mois", titre=pq.titre,
            sous=pq.sous, desc=pq.desc, code=pq.code, futur=pq.code[-4:] > _nxt,
            fichiers=[f"Outils gratuits Filodie/Couleur/{f}.pdf", f"Outils gratuits Filodie/Noir et blanc/{f}_NB.pdf"])
    add(id="grand-livre", type="livre", groupe="Grand livre clinique", titre="Grand livre clinique T.E.S.",
        sous="143 fiches · 9 parties",
        desc="Les connaissances essentielles de la pratique en éducation spécialisée, en fiches visuelles avec une zone "
             "« Mon application clinique ». Version couleur et version noir et blanc.",
        fichiers=["Grand livre clinique Filodie/Grand_livre_clinique_TES_Filodie.pdf",
                  "Grand livre clinique Filodie/Grand_livre_clinique_TES_Filodie_NB_impression.pdf"])
    add(id="bottin-regional", type="bottin", groupe="Bottin régional", titre="Bottin régional : 17 régions du Québec",
        sous="Gratuit", desc="DPJ, centres de crise, CLSC, autisme, TDAH, déficience intellectuelle, proches, violence et "
                              "dépendances, région par région, avec les lignes provinciales classées par problématique.",
        fichiers=["Bottin régional Filodie/Bottin_regional_Filodie_17_regions.pdf"])
    # lots
    for s in SERIES.values():
        n = sum(1 for i in items if i["groupe"] == "Cahiers " + s["nom"])
        if n:
            add(id="lot-cahiers-" + s["nom"].lower().replace(" ", "-"), type="lot_cahiers", groupe="Lots",
                titre=f"Série complète : cahiers {s['nom']}", sous=f"{n} cahiers visuels",
                desc=f"Les {n} cahiers visuels de la série {s['nom']}, en couleur et à colorier.", fichiers=[],
                contient=[i["id"] for i in items if i["groupe"] == "Cahiers " + s["nom"]])
    for g in sorted({t["dossier"] for t in ft.LOTS}):
        its = [i for i in items if i["type"] == "trousse" and i["fichiers"][0].startswith(g + "/")]
        v = g.split("/")[-1]
        lid = "lot-" + re.sub(r"\W+", "-", v.lower()).strip("-")
        lid = ID_STABLE.get(lid, lid)          # volet renommé : on garde l’identifiant (et le code Payhip)
        add(id=lid, type="lot_collection", groupe="Lots",
            titre=f"Collection Filodie : {v.split('– ')[-1]}", sous=f"{len(its)} trousses",
            desc="Toutes les trousses du volet « " + v.split("– ")[-1] + " ».", fichiers=[], contient=[i["id"] for i in its],
            titre_en=f"Filodie Collection: {tr(v).split('– ')[-1]}", sous_en=f"{len(its)} toolkits",
            desc_en=f"All the toolkits in the “{tr(v).split('– ')[-1]}” section.")
    aff = [i["id"] for i in items if i["type"] == "affiches"]
    if aff:
        naff = sum(len(pq.affiches) for pq in load_affiches())
        add(id="lot-affiches", type="lot_affiches", groupe="Lots", titre="Toutes les affiches murales", titre_en="All the Wall Posters",
            sous=f"{naff} affiches · {len(aff)} paquets", sous_en=f"{naff} posters · {len(aff)} packs",
            desc="Régulation, émotions, habiletés sociales, vie de classe, routines et messages-repères, en couleur et en noir et blanc.",
            desc_en="Regulation, feelings, social skills, classroom life, routines and anchor messages, in colour and black and white.",
            fichiers=[], contient=aff)
    jx = [i["id"] for i in items if i["type"] == "jeux"]
    if jx:
        njx = sum(len(pq.jeux) for pq in load_jeux())
        add(id="lot-jeux", type="lot_jeux", groupe="Lots", titre="Tous les jeux et cartes", titre_en="All the Games and Cards",
            sous=f"{njx} jeux · {len(jx)} paquets", sous_en=f"{njx} games · {len(jx)} packs",
            desc="Émotions, amitié, calme, résolution de problèmes, forces et connaissance de soi : cartes, bingos, "
                 "mémoires, dominos et jeux de parcours, en couleur et en noir et blanc.",
            desc_en="Feelings, friendship, calm, problem solving, strengths and self-knowledge: cards, bingos, memory "
                    "games, dominoes and board games, in colour and black and white.",
            fichiers=[], contient=jx)
    rt = [i["id"] for i in items if i["type"] == "routines"]
    if rt:
        nrt = sum(len(pq.routines) for pq in load_routines())
        add(id="lot-routines", type="lot_routines", groupe="Lots", titre="Toutes les routines visuelles maison",
            titre_en="All the Home Visual Routines",
            sous=f"{nrt} routines · {len(rt)} paquets", sous_en=f"{nrt} routines · {len(rt)} packs",
            desc="Matin, soir et dodo, repas et hygiène, devoirs, sorties et autonomie : chaque routine en séquence "
                 "illustrée et en tableau de motivation, avec un guide pour les parents, en couleur et en noir et blanc.",
            desc_en="Morning, evening and bedtime, meals and hygiene, homework, outings and independence: each routine as an "
                    "illustrated sequence and a motivation chart, with a parent guide, in colour and black and white.",
            fichiers=[], contient=rt)
    sp = [i["id"] for i in items if i["groupe"] == "Trousses spécialisées"]
    add(id="lot-specialisees", type="lot_specialisees", groupe="Lots", titre="Les 16 trousses spécialisées",
        sous="Âges et troubles", desc="Petite enfance, secondaire, adultes, aînés, TSA, TDAH, DI, langage, comportement, "
                                      "crise, suicide, dépendances et plus.", fichiers=[], contient=sp)
    tous = [i["id"] for i in items if i["type"] == "cahier"]
    add(id="lot-tous-les-cahiers", type="lot_tout", groupe="Lots", titre="Tous les cahiers visuels",
        sous=f"{len(tous)} cahiers · 5 séries", prix=75.00, sous_en=f"{len(tous)} workbooks · 5 series",
        desc="Les cahiers TSA, TDAH, habiletés sociales, DI et comportement, en couleur et à colorier.",
        fichiers=[], contient=tous)
    tt = [i["id"] for i in items if i["type"] in ("trousse", "edition")]
    ntr = sum(1 for i in items if i["type"] == "trousse")
    ncol = sum(1 for i in items if i["type"] == "trousse" and i["fichiers"][0].startswith("Collection Filodie/"))
    ned = sum(1 for i in items if i["type"] == "edition")
    add(id="lot-toutes-les-trousses", type="lot_tout", groupe="Lots", titre="Toutes les trousses",
        sous=f"{len(tt)} trousses et éditions", prix=75.00, sous_en=f"{len(tt)} toolkits and editions",
        desc=f"La trousse principale, les {len(sp)} trousses spécialisées, les {ncol} trousses de la Collection et les {ned} éditions.",
        desc_en=f"The main toolkit, the {len(sp)} specialized toolkits, the {ncol} Collection toolkits and the {ned} editions.",
        fichiers=[], contient=tt)
    add(id="lot-mega", type="mega", groupe="Lots", titre="Tout Filodie", sous="Toute la collection",
        desc=f"Les {ntr} trousses, les éditions, les {len(tous)} cahiers visuels, les affiches murales, les jeux, les routines visuelles, le Grand livre clinique "
             "et le bottin régional.",
        desc_en=f"All {ntr} toolkits, the editions, the {len(tous)} visual workbooks, the wall posters, the games, the visual routines, the Clinical Handbook "
                "and the regional directory.",
        fichiers=[], contient=[i["id"] for i in items if not i["type"].startswith("lot") and i["type"] not in ("mega", "gratuit")])
    # lots de collection : environ 2,50 $ par trousse, arrondi à 5 $, entre 25 $ et 30 $
    # (petites collections de moins de 6 trousses : environ 30 % de rabais sur le prix à l'unité)
    for i in items:
        if i["type"] == "lot_collection":
            n = len(i["contient"])
            i["prix"] = float(min(30, max(25, 5 * round(n * 2.5 / 5)))) if n >= 6 else \
                float(max(10, round(n * PRIX["trousse"] * 0.7)))
    # valeur à l'unité, pour afficher l'économie
    px = {i["id"]: i["prix"] for i in items}
    for i in items:
        if i.get("contient"):
            i["valeur"] = round(sum(px[c] for c in i["contient"]), 2)
    # conserver prix / liens déjà saisis
    if os.path.exists(CAT):
        old = {i["id"]: i for i in json.load(open(CAT, encoding="utf-8"))}
        for i in items:
            o = old.get(i["id"])
            if o:
                for k in (("payhip", "payhip_en") if "--prix" in sys.argv else ("prix", "payhip", "payhip_en")):
                    i[k] = o.get(k, i[k])
    fiches = os.path.join(os.path.dirname(HERE), "Payhip – fiches", "fiches.csv")   # filet : codes notés dans fiches.csv
    if os.path.exists(fiches):
        import csv
        codes = {r["id"]: r["code_payhip"] for r in csv.DictReader(open(fiches, encoding="utf-8-sig")) if r.get("code_payhip")}
        for i in items:
            if not i["payhip"] and codes.get(i["id"]):
                i["payhip"] = i["payhip_en"] = codes[i["id"]]
    json.dump(items, open(CAT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(items), "produits dans produits.json")


# --------------------------------------------------------------------------- images
def en_path(rel):
    import filodie_i18n as i
    parts = rel.split("/")
    out = [tr(p) for p in parts[:-1]] + [tr(os.path.splitext(parts[-1])[0]) + os.path.splitext(parts[-1])[1]]
    return os.path.join(i.EN_ROOT, *out)


def vignette(pdf, out, w=420):
    if os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(pdf):
        return
    d = fitz.open(pdf)
    pix = d[0].get_pixmap(matrix=fitz.Matrix(w / d[0].rect.width, w / d[0].rect.width))
    pix.save(out, jpg_quality=82) if out.endswith(".jpg") else pix.save(out)


def apercu(pdf, out, n, marque, w=640):
    """Page n du PDF en image, avec un filigrane « APERÇU » en diagonale (le produit vendu n’en a pas)."""
    if os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(pdf):
        return
    from PIL import Image, ImageDraw, ImageFont
    pg = fitz.open(pdf)[n]
    pix = pg.get_pixmap(matrix=fitz.Matrix(w / pg.rect.width, w / pg.rect.width))
    im = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
    font = ImageFont.truetype(os.path.join(SRC, "fonts", "NunitoSans-800.ttf"), w // 11)
    txt = f"{marque} · filodie.ca"
    x0, y0, x1, y1 = font.getbbox(txt)
    calque = Image.new("RGBA", (x1 + 40, y1 + 40), (0, 0, 0, 0))
    ImageDraw.Draw(calque).text((20, 20 - y0), txt, font=font, fill=(217, 115, 78, 70))
    calque = calque.rotate(32, expand=True)
    for fy in (0.22, 0.62):
        im.paste(calque, ((im.width - calque.width) // 2, int(im.height * fy) - calque.height // 2), calque)
    im.save(out, quality=72, optimize=True)


def images(items):
    for lang in ("fr", "en"):
        os.makedirs(os.path.join(PUB, "img", lang), exist_ok=True)
    for i in items:
        if not i["fichiers"]:
            continue
        rel = i["fichiers"][0]
        fr = os.path.join(OUT_FR, rel)
        if os.path.exists(fr):
            vignette(fr, os.path.join(PUB, "img", "fr", i["id"] + ".jpg"))
        en = en_path(rel)
        if os.path.exists(en):
            vignette(en, os.path.join(PUB, "img", "en", i["id"] + ".jpg"))
    for lang in ("fr", "en"):                         # aperçus : 2 pages de chaque outil
        os.makedirs(os.path.join(PUB, "img", lang, "apercu"), exist_ok=True)
    for i in items:
        if not i["fichiers"]:
            continue
        rel = i["fichiers"][0]
        for lang, pdf in (("fr", os.path.join(OUT_FR, rel)), ("en", en_path(rel))):
            if not os.path.exists(pdf):
                continue
            nb = fitz.open(pdf).page_count
            pages = [k for k in (1, 2) if k < nb] or [0]
            noms = []
            for k in pages:
                nom = f"{i['id']}-{k + 1}"
                apercu(pdf, os.path.join(PUB, "img", lang, "apercu", nom + ".jpg"), k,
                       "APERÇU" if lang == "fr" else "PREVIEW")
                noms.append(nom)
            i["pv_" + lang] = noms
    par_id = {i["id"]: i for i in items}
    for i in items:
        if i.get("contient"):
            i["img"] = i["contient"][0]
            for lang in ("fr", "en"):                 # lots : première page d’aperçu des premiers produits
                i["pv_" + lang] = [par_id[c]["pv_" + lang][0] for c in i["contient"][:3] if par_id[c].get("pv_" + lang)]


# --------------------------------------------------------------------------- textes du site
L = {
    "fr": {
        "lang": "fr-CA", "other": "en", "other_label": "EN", "base": "",
        "tag": "Outils cliniques pour T.E.S.",
        "nav": [("index.html", "Accueil"), ("boutique.html", "Boutique"), ("bottin.html", "Bottin gratuit"),
                ("services.html", "Services"), ("a-propos.html", "À propos"), ("faq.html", "FAQ"), ("contact.html", "Contact")],
        "hero_k": "Outils cliniques · éducation spécialisée",
        "hero_1": "Tenir le fil,", "hero_2": "de l’observation à l’intervention.",
        "hero_p": "Des trousses, des cahiers visuels et un grand livre clinique conçus au Québec pour les T.E.S., "
                  "le personnel enseignant, le personnel éducateur et les familles. Imprimables, remplissables à l’écran, "
                  "avec les ressources de votre région.",
        "cta1": "Voir la boutique", "cta2": "Télécharger le bottin gratuit",
        "stats": [("95", "trousses thématiques"), ("179", "cahiers visuels"), ("143", "fiches du Grand livre"), ("17", "régions couvertes")],
        "col_t": "La collection",
        "cols": [("Trousses", "Des outils d’observation, de planification et de suivi, du CPE au CHSLD.", "boutique.html#trousse"),
                 ("Cahiers visuels", "Imagés et ludiques, pour travailler directement avec l’enfant : TSA, TDAH, habiletés sociales, DI, comportement.", "boutique.html#cahier"),
                 ("Grand livre clinique", "143 fiches de connaissances pour la pratique, en couleur et en noir et blanc.", "boutique.html#livre"),
                 ("Bottin régional", "Les ressources des 17 régions, classées par problématique. Gratuit.", "bottin.html")],
        "why_t": "Pourquoi Filodie ?",
        "why": [("Pensé pour le terrain", "Chaque outil suit le même fil : observer, comprendre, planifier, soutenir, communiquer."),
                ("Ancré au Québec", "Vocabulaire du réseau (PI, PPH, DPJ, LIP), ressources vérifiées dans chaque région."),
                ("Prêt à utiliser", "PDF remplissables à l’écran ou imprimables, versions à colorier en noir et blanc."),
                ("Livraison immédiate", "Vos fichiers sont téléchargeables dès le paiement, et le lien vous est aussi envoyé par courriel.")],
        "shop_t": "Boutique", "shop_p": "Chaque achat inclut la version française et la version anglaise. Cahiers à 3 $, trousses à 7 $, et des lots jusqu’à 90 % moins chers. Prix en dollars canadiens, téléchargement immédiat après le paiement.",
        "search": "Rechercher un outil…", "all": "Tout",
        "types": {"trousse": "Trousses", "edition": "Éditions", "cahier": "Cahiers visuels", "affiches": "Affiches", "jeux": "Jeux", "routines": "Routines", "gratuit": "Gratuit", "livre": "Grand livre",
                  "bottin": "Bottin", "lot": "Lots"},
        "buy": "Acheter", "soon": "Bientôt disponible", "free": "Gratuit", "get": "Obtenir", "details": "Détails", "cahier_nb": " · Couleur + version noir et blanc à colorier",
        "aff_nb": " · Couleur + noir et blanc · lettre et 11 × 17",
        "jeux_nb": " · Règles, cartes et plateaux · couleur + noir et blanc",
        "rtn_nb": " · Séquences, tableaux et guide parent · couleur + noir et blanc", "preview": "Aperçu", "close": "Fermer",
        "pvnote": "Quelques pages du produit. Le filigrane « aperçu » n’apparaît pas dans les fichiers achetés.",
        "count": "produits", "value": "Valeur à l’unité", "save": "économie",
        "bottin_t": "Bottin régional gratuit",
        "bottin_p": "Les ressources des 17 régions du Québec, classées par problématique : signalement à la DPJ, centres de crise, "
                    "CLSC, associations en autisme et en TDAH, déficience intellectuelle, personnes proches aidantes, violence et dépendances. "
                    "Coordonnées vérifiées sur les sites officiels.",
        "bottin_btn": "Recevoir le bottin gratuitement",
        "footer_legal": [("licence.html", "Licence d’utilisation"), ("conditions.html", "Conditions de vente"),
                         ("confidentialite.html", "Confidentialité")],
        "footer_note": "Les outils Filodie soutiennent l’intervention; ils ne remplacent ni l’évaluation d’une personne "
                       "professionnelle qualifiée ni le jugement clinique.",
        "rights": "© 2026 Filodie. Tous droits réservés.",
    },
    "en": {
        "lang": "en-CA", "other": "fr", "other_label": "FR", "base": "../",
        "tag": "Clinical tools for special care counsellors",
        "nav": [("index.html", "Home"), ("shop.html", "Shop"), ("directory.html", "Free directory"),
                ("services.html", "Services"), ("about.html", "About"), ("faq.html", "FAQ"), ("contact.html", "Contact")],
        "hero_k": "Clinical tools · special care counselling",
        "hero_1": "Hold the thread,", "hero_2": "from observation to intervention.",
        "hero_p": "Toolkits, visual workbooks and a clinical handbook made in Québec for special care counsellors, "
                  "teachers, educators and families. Printable or fillable on screen, with resources for your region.",
        "cta1": "Visit the shop", "cta2": "Get the free directory",
        "stats": [("95", "themed toolkits"), ("179", "visual workbooks"), ("143", "handbook sheets"), ("17", "regions covered")],
        "col_t": "The collection",
        "cols": [("Toolkits", "Observation, planning and follow-up tools, from daycare to long-term care.", "shop.html#trousse"),
                 ("Visual workbooks", "Colourful and playful, to work directly with the child: autism, ADHD, social skills, ID, behaviour.", "shop.html#cahier"),
                 ("Clinical handbook", "143 knowledge sheets for practice, in colour and in black and white.", "shop.html#livre"),
                 ("Regional directory", "Resources for all 17 regions, sorted by issue. Free.", "directory.html")],
        "why_t": "Why Filodie?",
        "why": [("Built for the field", "Every tool follows the same thread: observe, understand, plan, support, communicate."),
                ("Rooted in Québec", "Network vocabulary (IEP, HDM-DCP, DYP, Education Act) and verified resources in every region."),
                ("Ready to use", "PDFs fillable on screen or printable, with black-and-white colouring versions."),
                ("Instant delivery", "Your files can be downloaded right after payment, and the link is also emailed to you.")],
        "shop_t": "Shop", "shop_p": "Every purchase includes both the English and French versions. Workbooks at $3, toolkits at $7, and bundles up to 90% off. Prices in Canadian dollars, instant download after payment.",
        "search": "Search for a tool…", "all": "All",
        "types": {"trousse": "Toolkits", "edition": "Editions", "cahier": "Visual workbooks", "affiches": "Posters", "jeux": "Games", "routines": "Routines", "gratuit": "Free", "livre": "Handbook",
                  "bottin": "Directory", "lot": "Bundles"},
        "buy": "Buy", "soon": "Coming soon", "free": "Free", "get": "Get it", "details": "Details", "cahier_nb": " · Colour + black-and-white colouring version",
        "aff_nb": " · Colour + black and white · letter and 11 × 17",
        "jeux_nb": " · Rules, cards and boards · colour + black and white",
        "rtn_nb": " · Sequences, charts and parent guide · colour + black and white", "preview": "Preview", "close": "Close",
        "pvnote": "A few pages from the product. The “preview” watermark does not appear in the files you buy.",
        "count": "products", "value": "Value if bought separately", "save": "savings",
        "bottin_t": "Free regional directory",
        "bottin_p": "Resources for all 17 regions of Québec, sorted by issue: youth protection (DYP) reporting, crisis centres, "
                    "CLSCs, autism and ADHD associations, intellectual disability, caregivers, violence and addictions. "
                    "Contact details verified on official websites.",
        "bottin_btn": "Get the directory for free",
        "footer_legal": [("licence.html", "Licence"), ("terms.html", "Terms of sale"), ("privacy.html", "Privacy")],
        "footer_note": "Filodie tools support intervention; they do not replace an assessment by a qualified professional "
                       "or clinical judgment.",
        "rights": "© 2026 Filodie. All rights reserved.",
    },
}

# pages équivalentes (bouton de langue)
PAIRS = {"index.html": "index.html", "boutique.html": "shop.html", "bottin.html": "directory.html",
         "a-propos.html": "about.html", "faq.html": "faq.html", "contact.html": "contact.html", "services.html": "services.html",
         "licence.html": "licence.html", "conditions.html": "terms.html", "confidentialite.html": "privacy.html",
         "coloriage.html": "colouring.html"}
PAIRS_EN = {v: k for k, v in PAIRS.items()}

THREAD = ('<svg class="thread" viewBox="0 0 600 90" preserveAspectRatio="none" aria-hidden="true"><path d="M-10 60 '
          'C 80 30, 160 80, 250 50 S 330 10, 300 35 S 330 70, 420 55 S 560 20, 610 30" fill="none" stroke="currentColor" '
          'stroke-width="2.4" stroke-linecap="round"/></svg>')


PROMO = os.path.join(HERE, "promo.json")


def promo_html(lang):
    """Bannière du code promo (promo.json). Elle se cache seule avant « debut » et après « fin »."""
    if not os.path.exists(PROMO):
        return ""
    p = json.load(open(PROMO, encoding="utf-8"))
    if not p.get("actif") or not p.get("code"):
        return ""
    msg = html.escape(p.get("message_" + lang) or "")
    code = html.escape(p["code"])
    copier, copie = ("Copier", "Copié !") if lang == "fr" else ("Copy", "Copied!")
    return (f'<div class="promo" id="promo" data-debut="{p.get("debut", "")}" data-fin="{p.get("fin", "")}">'
            f'<span>{msg}</span> <code>{code}</code> '
            f'<button type="button" onclick="navigator.clipboard.writeText(\'{code}\');this.textContent=\'{copie}\'">{copier}</button></div>'
            '<script>(function(){var b=document.getElementById("promo"),d=new Date(),'
            'j=d.getFullYear()+"-"+String(d.getMonth()+1).padStart(2,"0")+"-"+String(d.getDate()).padStart(2,"0");'
            'if((b.dataset.debut&&j<b.dataset.debut)||(b.dataset.fin&&j>b.dataset.fin))b.remove();})();</script>\n')


def page(lang, name, title, body, desc="", scripts=""):
    t = L[lang]
    b = t["base"]
    other = (PAIRS if lang == "fr" else PAIRS_EN)[name]
    other_href = ("en/" if lang == "fr" else "../") + other
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == name else ""}>{l}</a>' for h, l in t["nav"])
    legal = " · ".join(f'<a href="{h}">{l}</a>' for h, l in t["footer_legal"])
    return f"""<!doctype html>
<html lang="{t['lang']}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<script>(function(w,d,e,u,f,l,n){{w[f]=w[f]||function(){{(w[f].q=w[f].q||[]).push(arguments);}},l=d.createElement(e),l.async=1,l.src=u,
n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);}})(window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');
ml('account', '2673065');</script>
<title>{html.escape(title) + " · Filodie" if title != "Filodie" else "Filodie · " + t["tag"]}</title>
<meta name="description" content="{html.escape(desc or t['hero_p'])}">
<link rel="alternate" hreflang="{L[t['other']]['lang']}" href="{other_href}">
<link rel="icon" href="{b}favicon.svg" type="image/svg+xml">
<meta property="og:type" content="website">
<meta property="og:title" content="Filodie · {t['tag']}">
<meta property="og:image" content="https://filodie.ca/og-image.png">
<link rel="stylesheet" href="{b}style.css">
</head>
<body>
{promo_html(lang)}<header class="top">
  <div class="wrap bar">
    <a class="logo" href="index.html" aria-label="Filodie">filodie{BEADS}</a>
    <button class="menu" aria-expanded="false" aria-controls="nav">☰</button>
    <nav id="nav">{nav}<a class="lang" href="{other_href}" hreflang="{L[t['other']]['lang']}">{t['other_label']}</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <p class="logo small">filodie{BEADS}</p>
    <p>{t['tag']}</p>
    <p class="legal">{legal}</p>
    <p class="note">{t['footer_note']}</p>
    <p class="note">{t['rights']} · Illustrations : Fluent Emoji © Microsoft (MIT).</p>
  </div>
</footer>
<script>
document.querySelector('.menu').addEventListener('click',e=>{{const n=document.getElementById('nav');
const o=n.classList.toggle('open');e.currentTarget.setAttribute('aria-expanded',o)}});
</script>
{scripts}
</body>
</html>
"""


def iv(lang, img):
    """« ?v=… » : empreinte de la vignette, pour que les navigateurs rechargent l’image quand elle change."""
    f = os.path.join(PUB, "img", lang, img + ".jpg")
    return "?v=" + hashlib.md5(open(f, "rb").read()).hexdigest()[:8] if os.path.exists(f) else ""


def home(lang):
    t = L[lang]
    shop = "boutique.html" if lang == "fr" else "shop.html"
    bot = "bottin.html" if lang == "fr" else "directory.html"
    stats = "".join(f"<div><strong>{n}</strong><span>{l}</span></div>" for n, l in t["stats"])
    cols = "".join(f'<a class="card col" href="{h}"><img src="{t["base"]}img/{lang}/{img}.jpg{iv(lang, img)}" alt="" loading="lazy">'
                   f'<h3>{a}</h3><p>{d}</p></a>'
                   for (a, d, h), img in zip(t["cols"], ["trousse-principale", "cahier-vtsa-01", "grand-livre", "bottin-regional"]))
    why = "".join(f"<div><h3>{a}</h3><p>{d}</p></div>" for a, d in t["why"])
    body = f"""
<section class="hero">
  <div class="wrap">
    {THREAD}
    <p class="kicker">{t['hero_k']}</p>
    <h1>{t['hero_1']}<br><em>{t['hero_2']}</em></h1>
    <p class="lead">{t['hero_p']}</p>
    <p class="ctas"><a class="btn" href="{shop}">{t['cta1']}</a> <a class="btn ghost" href="{bot}">{t['cta2']}</a></p>
    <div class="stats">{stats}</div>
  </div>
</section>
{gratuits(lang)}
<section class="wrap"><h2>{t['col_t']}</h2><div class="grid4">{cols}</div></section>
<section class="band"><div class="wrap"><h2>{t['why_t']}</h2><div class="grid4 why">{why}</div></div></section>
"""
    return page(lang, "index.html", "Filodie", body, scripts='<script src="https://payhip.com/payhip.js"></script>')


def gratuits(lang):
    """Section « Commencer gratuitement » : trousse découverte, outil du mois, bottin (aimant à courriels)."""
    items = {i["id"]: i for i in json.load(open(CAT, encoding="utf-8"))}
    from datetime import date as _d
    t = _d.today()                                     # MOIS-AAMM : l’outil du mois courant, sinon celui du mois
    now = t.strftime("%y%m")                           # suivant, sinon le plus récent déjà passé
    nxt = (_d(t.year + 1, 1, 1) if t.month == 12 else _d(t.year, t.month + 1, 1)).strftime("%y%m")
    tous = [i for i in items.values() if i["type"] == "gratuit"]
    mois = ([i for i in tous if i.get("code", "")[-4:] == now] or [i for i in tous if i.get("code", "")[-4:] == nxt]
            or sorted((i for i in tous if i.get("code", "")[-4:] < now), key=lambda i: i["id"]))
    ids = ["trousse-trousse_decouverte"] + ([mois[-1]["id"]] if mois else []) + ["bottin-regional"]
    fr = lang == "fr"
    etiq = {"trousse-trousse_decouverte": "Trousse découverte" if fr else "Starter toolkit",
            "bottin-regional": "Bottin des 17 régions" if fr else "17-region directory"}
    cards = ""
    for k in ids:
        i = items.get(k)
        if not i:
            continue
        code = i["payhip_en"] if not fr else i["payhip"]
        titre = i["titre"] if fr else en(i, "titre")
        lab = etiq.get(k) or ("Outil gratuit du mois" if fr else "Free tool of the month")
        btn = (f'<a class="btn payhip-buy-button" data-theme="none" data-product="{code}" href="https://payhip.com/b/{code}">'
               f'{"Recevoir gratuitement" if fr else "Get it free"}</a>') if code else ""
        cards += (f'<div class="card col"><img src="{L[lang]["base"]}img/{lang}/{k}.jpg{iv(lang, k)}" alt="" loading="lazy">'
                  f'<p class="kicker" style="padding:0 16px;margin:12px 0 0">{lab}</p><h3>{html.escape(titre)}</h3>'
                  f'<p style="padding-bottom:16px">{btn}</p></div>')
    h2 = "Commencer gratuitement" if fr else "Start for free"
    sous = ("Trois outils offerts, en français et en anglais. Cochez la case au paiement pour recevoir l’outil gratuit "
            "de chaque mois et les nouveautés." if fr else
            "Three free tools, in French and English. Tick the box at checkout to get each month’s free tool and "
            "what’s new.")
    abo_t = "Recevez l’outil gratuit chaque mois" if fr else "Get the free tool every month"
    abo_p = ("Inscrivez-vous à l’infolettre : un outil Filodie gratuit et les nouveautés, une fois par mois. Désabonnement "
             "en un clic." if fr else "Join the newsletter: a free Filodie tool and what’s new, once a month. Unsubscribe "
             "in one click.")
    colo = ("Nouveau : 4 cahiers à colorier gratuits, à télécharger sans inscription" if fr else
            "New: 4 free colouring books, download with no sign-up")
    lien = "coloriage.html" if fr else "colouring.html"
    return (f'<section class="wrap"><h2>{h2}</h2><p class="lead">{sous}</p><div class="grid4">{cards}</div>'
            f'<p style="margin-top:18px"><a class="btn" href="{lien}">🖍 {colo}</a></p></section>'
            f'<section class="band"><div class="wrap abo"><div><h2>{abo_t}</h2><p class="lead">{abo_p}</p></div>'
            f'<div class="ml-embedded" data-form="C80x4w"></div></div></section>')


def shop(lang, items):
    t = L[lang]
    data = []
    for i in items:
        typ = "lot" if i["type"].startswith("lot") or i["type"] == "mega" else i["type"]
        img = i.get("img") or i["id"]
        if not os.path.exists(os.path.join(PUB, "img", lang, img + ".jpg")):
            img_lang = "fr"
        else:
            img_lang = lang
        g = i["groupe"]
        data.append({
            "id": i["id"], "t": typ, "g": tr(g) if lang == "en" else g,
            "n": en(i, "titre") if lang == "en" else i["titre"],
            "s": (en(i, "sous") if lang == "en" else i["sous"])
                 + (t["cahier_nb"] if i["type"] == "cahier" else t["aff_nb"] if i["type"] == "affiches"
                    else t["jeux_nb"] if i["type"] == "jeux" else t["rtn_nb"] if i["type"] in ("routines", "gratuit") else ""),
            "d": en(i, "desc") if lang == "en" else i["desc"],
            "p": i["prix"], "k": i["payhip_en"] if lang == "en" else i["payhip"],
            "img": f"{t['base']}img/{img_lang}/{img}.jpg{iv(img_lang, img)}",
            "a": [f"{t['base']}img/{pl}/apercu/{a}.jpg{iv(pl, 'apercu/' + a)}"
                  for pl in ([lang] if i.get("pv_" + lang) else ["fr"]) for a in i.get("pv_" + pl, [])], "c": i.get("code", ""), "v": i.get("valeur", 0),
        })
    chips = "".join(f'<button data-t="{k}">{v}</button>' for k, v in t["types"].items())
    labels = json.dumps({k: t[k] for k in ("buy", "soon", "free", "get", "details", "count", "value", "save", "preview", "close", "pvnote")}, ensure_ascii=False)
    body = f"""
<section class="wrap shop">
  <h1>{t['shop_t']}</h1>
  <p class="lead">{t['shop_p']}</p>
  <div class="filters">
    <input id="q" type="search" placeholder="{t['search']}" aria-label="{t['search']}">
    <div class="chips"><button data-t="" class="on">{t['all']}</button>{chips}</div>
    <select id="g" aria-label="Groupe"></select>
  </div>
  <p id="n" class="muted"></p>
  <div id="list" class="products"></div>
</section>
<dialog id="pv" class="pv"><div class="pvh"><h3 id="pvt"></h3><button class="pvx" aria-label="{t['close']}">×</button></div>
<p class="note" id="pvn"></p><div id="pvi" class="pvi"></div><div class="buy" id="pvb"></div></dialog>"""
    js = f"""<script>
const P={json.dumps(data, ensure_ascii=False)};
const T={labels};
const fmt=new Intl.NumberFormat('{t['lang']}',{{style:'currency',currency:'CAD'}});
let type=(location.hash||'').slice(1), grp='', q='';
const list=document.getElementById('list'), sel=document.getElementById('g');
function esc(s){{return s.replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]))}}
function groups(){{const gs=[...new Set(P.filter(p=>!type||p.t===type).map(p=>p.g))];
 sel.innerHTML='<option value="">{t['all']}</option>'+gs.map(g=>'<option>'+esc(g)+'</option>').join('');sel.value=grp}}
function buybtn(p){{return p.k?'<a class="btn payhip-buy-button" data-theme="none" data-product="'+p.k+'" href="https://payhip.com/b/'+p.k+'">'+(p.p?T.buy:T.get)+'</a>'
   :'<span class="btn off">'+T.soon+'</span>'}}
function card(p){{
 const price=p.p?fmt.format(p.p):T.free, btn=buybtn(p);
 const im='<img src="'+p.img+'" alt="" loading="lazy">';
 return '<article class="card prod">'+(p.a.length?'<button class="pvb" data-pv="'+P.indexOf(p)+'" aria-label="'+T.preview+' : '+esc(p.n)+'">'+im+'<span class="pvl">'+T.preview+'</span></button>':im)+'<div class="pb"><p class="grp">'+esc(p.g)+(p.c?' · '+p.c:'')+'</p><h3>'+esc(p.n)+'</h3><p class="sub">'+esc(p.s)+'</p>'
  +(p.v>p.p?'<p class="save">'+T.value+' : <s>'+fmt.format(p.v)+'</s> · '+T.save+' '+Math.round(100-100*p.p/p.v)+' %</p>':'')
  +'<details><summary>'+T.details+'</summary><p>'+esc(p.d)+'</p></details><div class="buy"><strong>'+price+'</strong>'+btn+'</div></div></article>'}}
function draw(){{const w=q.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
 const r=P.filter(p=>(!type||p.t===type)&&(!grp||p.g===grp)&&(!w||(p.n+' '+p.s+' '+p.d+' '+p.g+' '+p.c).toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').includes(w)));
 document.getElementById('n').textContent=r.length+' '+T.count;list.innerHTML=r.map(card).join('');
 if(window.Payhip&&Payhip.Buttons)try{{Payhip.Buttons.init()}}catch(e){{}}}}
document.querySelectorAll('.chips button').forEach(b=>{{if(b.dataset.t===type){{document.querySelector('.chips .on').classList.remove('on');b.classList.add('on')}}
 b.onclick=()=>{{document.querySelector('.chips .on').classList.remove('on');b.classList.add('on');type=b.dataset.t;grp='';history.replaceState(null,'',type?'#'+type:location.pathname);groups();draw()}}}});
const dlg=document.getElementById('pv');
list.addEventListener('click',e=>{{const b=e.target.closest('[data-pv]');if(!b)return;const p=P[+b.dataset.pv];
 document.getElementById('pvt').textContent=p.n;document.getElementById('pvn').textContent=T.pvnote;
 document.getElementById('pvi').innerHTML=p.a.map(u=>'<img src="'+u+'" alt="">').join('');
 document.getElementById('pvb').innerHTML='<strong>'+(p.p?fmt.format(p.p):T.free)+'</strong>'+buybtn(p);
 dlg.showModal();if(window.Payhip&&Payhip.Buttons)try{{Payhip.Buttons.init()}}catch(e){{}}}});
dlg.querySelector('.pvx').onclick=()=>dlg.close();dlg.addEventListener('click',e=>{{if(e.target===dlg)dlg.close()}});
sel.onchange=()=>{{grp=sel.value;draw()}};document.getElementById('q').oninput=e=>{{q=e.target.value;draw()}};
groups();draw();
</script>"""
    if any(d["k"] for d in data):
        js = '<script src="https://payhip.com/payhip.js"></script>\n' + js
    name = "boutique.html" if lang == "fr" else "shop.html"
    return page(lang, name, t["shop_t"], body, scripts=js)


def bottin(lang, items):
    t = L[lang]
    b = next(i for i in items if i["id"] == "bottin-regional")
    k = b["payhip_en"] if lang == "en" else b["payhip"]
    btn = (f'<a class="btn payhip-buy-button" data-theme="none" data-product="{k}" href="https://payhip.com/b/{k}">{t["bottin_btn"]}</a>'
           if k else f'<span class="btn off">{t["soon"]}</span>')
    img = f'{t["base"]}img/{lang if os.path.exists(os.path.join(PUB, "img", lang, "bottin-regional.jpg")) else "fr"}/bottin-regional.jpg'
    img += iv(img.split("/")[-2], "bottin-regional")
    body = f"""
<section class="wrap split">
  <div><h1>{t['bottin_t']}</h1><p class="lead">{t['bottin_p']}</p><p>{btn}</p></div>
  <img class="shadow" src="{img}" alt="">
</section>"""
    js = '<script src="https://payhip.com/payhip.js"></script>' if k else ""
    return page(lang, "bottin.html" if lang == "fr" else "directory.html", t["bottin_t"], body, scripts=js)


def textpage(lang, name, title, content):
    return page(lang, name, title, f'<section class="wrap prose"><h1>{title}</h1>{content}</section>')


CONTENT = {
    ("fr", "a-propos.html"): ("À propos", """
<p class="lead">Filodie, c’est l’idée qu’une bonne intervention tient à un fil : celui qui relie l’observation, la compréhension, le plan, le soutien et la communication.</p>
<p>Je m’appelle Mélodie. Je suis maman de quatre filles, et c’est d’abord à la maison que j’ai appris qu’un enfant avance mieux quand on lui montre le chemin, une étape à la fois.</p>
<p>Je suis étudiante en Techniques d’éducation spécialisée, je détiens un certificat en travail social et je poursuis un baccalauréat multidisciplinaire, avec un certificat en psychologie du développement humain et un certificat en dépendances. Ce parcours me permet de regarder chaque situation sous plusieurs angles : le développement, la famille, le réseau et l’intervention au quotidien.</p>
<p>J’ai créé Filodie pour offrir aux intervenantes et intervenants, au personnel enseignant et aux parents les outils que j’aurais voulu avoir sous la main : clairs, beaux, rigoureux et vraiment utilisables avec les personnes que l’on accompagne.</p>
<h2>Mon parcours</h2>
<ul><li>Maman de quatre filles</li><li>Étudiante en Techniques d’éducation spécialisée</li><li>Certificat en travail social</li>
<li>Baccalauréat multidisciplinaire en cours : certificat en psychologie du développement humain et certificat en dépendances</li></ul>
<p>Chaque outil est conçu au Québec, avec le vocabulaire du réseau et des ressources vérifiées dans les 17 régions. Les versions anglaises s’adressent aux milieux anglophones et bilingues.</p>
<h2>Mes engagements</h2>
<ul><li>Des contenus originaux, révisés et datés.</li><li>Des ressources vérifiées à la source et mises à jour chaque année.</li>
<li>Des outils respectueux de la dignité et de l’autodétermination des personnes.</li></ul>"""),
    ("en", "about.html"): ("About", """
<p class="lead">Filodie is built on one idea: good intervention holds together like a thread, linking observation, understanding, planning, support and communication.</p>
<p>My name is Mélodie. I am the mother of four daughters, and it was at home that I first learned that children move forward best when you show them the way, one step at a time.</p>
<p>I am a special care counselling student, I hold a certificate in social work, and I am completing a multidisciplinary bachelor’s degree with a certificate in human developmental psychology and a certificate in addictions. This path lets me look at every situation from several angles: development, family, services and day-to-day intervention.</p>
<p>I created Filodie to give counsellors, teachers and parents the tools I wished I had on hand: clear, attractive, rigorous and truly usable with the people we support.</p>
<h2>My background</h2>
<ul><li>Mother of four daughters</li><li>Special care counselling student</li><li>Certificate in social work</li>
<li>Multidisciplinary bachelor’s degree in progress: certificates in human developmental psychology and in addictions</li></ul>
<p>Every tool is designed in Québec, with the vocabulary of the health and education networks and resources verified in all 17 regions. French versions of every tool are also available.</p>
<h2>My commitments</h2>
<ul><li>Original, reviewed and dated content.</li><li>Resources verified at the source and updated every year.</li>
<li>Tools that respect the dignity and self-determination of every person.</li></ul>"""),
    ("fr", "services.html"): ("Services", """
<p class="lead">Au-delà de la boutique, Filodie crée des outils conçus pour votre équipe ou votre famille, entièrement par courriel.</p>
<h2>Outils sur mesure</h2>
<p>Un enfant, une classe ou un milieu a besoin d’un outil qui n’existe pas encore ? Je le crée pour vous : routine visuelle avec les photos de votre milieu, plan de crise, histoire sociale, tableau de motivation, grille d’observation adaptée à votre clientèle. Chaque outil est livré en PDF remplissable, avec la signature Filodie et les sources qui l’appuient.</p>
<ul><li>Vous décrivez le besoin par courriel (aucune information nominative sur la personne n’est nécessaire).</li><li>Je vous envoie une proposition et un prix avant de commencer.</li><li>Une ronde de corrections est incluse.</li></ul>
<h2 id="licence-equipe">Licence d’équipe</h2>
<p>Un achat sur la boutique donne une <a href="licence.html">licence individuelle</a> : les fichiers sont réservés à la personne qui les achète. Si plusieurs membres d’un même milieu veulent utiliser le même outil, la licence d’équipe évite que chaque personne l’achète séparément.</p>
<h3>Ce que la licence d’équipe permet</h3>
<ul><li>Déposer les fichiers sur le réseau interne de l’établissement (disque partagé, intranet, Teams ou Google Drive réservés au personnel).</li>
<li>Les utiliser, les imprimer et les photocopier pour jusqu’à 25 membres du personnel d’un même établissement : intervenantes et intervenants, T.E.S., personnel enseignant, personnel éducateur, direction.</li>
<li>Recevoir une facture au nom de l’établissement, pratique pour un bon de commande ou un remboursement de dépenses.</li></ul>
<p>Comme pour la licence individuelle, il est interdit de revendre les fichiers ou de les rendre accessibles à l’extérieur de l’établissement (site Web public, réseaux sociaux, autres écoles ou organismes).</p>
<h3>Pourquoi 3 fois le prix individuel ?</h3>
<p>Le prix d’une licence d’équipe correspond à 3 licences individuelles, même si jusqu’à 25 personnes peuvent utiliser les fichiers. Ce choix repose sur trois raisons :</p>
<ul><li><strong>Une économie importante pour votre milieu.</strong> Acheter l’outil pour 25 personnes coûterait 25 fois le prix. Avec la licence d’équipe, vous payez 3 fois le prix, soit une économie de 88 %.</li>
<li><strong>Un prix juste pour le travail de création.</strong> Un fichier partagé dans toute une équipe remplace plusieurs ventes. Le multiplicateur de 3 reconnaît cette utilisation élargie tout en restant abordable pour les budgets des écoles, des CPE et des organismes.</li>
<li><strong>Un calcul simple et transparent.</strong> Pas de grille compliquée : vous connaissez le prix à l’avance, peu importe le nombre de personnes, jusqu’à 25.</li></ul>
<h3>Exemples de prix</h3>
<table class="tbl"><thead><tr><th>Produit</th><th>Licence individuelle</th><th>Licence d’équipe (× 3)</th></tr></thead><tbody>
<tr><td>Une trousse</td><td>7 $</td><td>21 $</td></tr>
<tr><td>Un cahier visuel</td><td>3 $</td><td>9 $</td></tr>
<tr><td>Une collection de trousses</td><td>25 $</td><td>75 $</td></tr>
<tr><td>Toutes les trousses</td><td>75 $</td><td>225 $</td></tr>
<tr><td>Tout Filodie</td><td>129 $</td><td>387 $</td></tr></tbody></table>
<p class="muted">Le prix de référence est le prix courant affiché dans la boutique. Pour plus de 25 personnes ou pour plusieurs établissements (par exemple un centre de services scolaire), écrivez-moi pour une soumission.</p>
<h3>Comment commander</h3>
<ol><li>Écrivez à <a href="mailto:melodie@filodie.ca?subject=Licence%20d%E2%80%99%C3%A9quipe">melodie@filodie.ca</a> en indiquant les produits voulus, le nom et l’adresse de l’établissement, ainsi que la personne-ressource.</li>
<li>Vous recevez une facture en PDF, payable par virement Interac ou par chèque.</li>
<li>Dès la réception du paiement, vous recevez les fichiers par courriel, avec la facture marquée « payée ».</li></ol>
<p><a class="btn" href="mailto:melodie@filodie.ca?subject=Demande%20de%20service%20Filodie">Écrire à Mélodie</a></p>
"""),
    ("en", "services.html"): ("Services", """
<p class="lead">Beyond the shop, Filodie creates tools designed for your team or family, entirely by email.</p>
<h2>Custom tools</h2>
<p>Does a child, a class or a setting need a tool that does not exist yet? I will create it for you: a visual routine with photos of your setting, a crisis plan, a social story, a motivation chart, an observation grid adapted to your clients. Every tool comes as a fillable PDF, with the Filodie signature and the sources behind it.</p>
<ul><li>Describe the need by email (no identifying information about the person is needed).</li><li>I send you a proposal and a price before starting.</li><li>One round of revisions is included.</li></ul>
<h2 id="team-licence">Team licence</h2>
<p>A purchase in the shop comes with an <a href="licence.html">individual licence</a>: the files are for the buyer only. When several people in the same setting want to use the same tool, the team licence saves each of them from buying it separately.</p>
<h3>What the team licence allows</h3>
<ul><li>Placing the files on the organization’s internal network (shared drive, intranet, Teams or Google Drive restricted to staff).</li>
<li>Using, printing and photocopying them for up to 25 staff members of the same organization: counsellors, teachers, educators, management.</li>
<li>Receiving an invoice in the organization’s name, handy for a purchase order or an expense claim.</li></ul>
<p>As with the individual licence, the files may not be resold or made available outside the organization (public website, social media, other schools or organizations).</p>
<h3>Why 3 times the individual price?</h3>
<p>A team licence costs the same as 3 individual licences, even though up to 25 people may use the files. There are three reasons for this:</p>
<ul><li><strong>Big savings for your setting.</strong> Buying the tool for 25 people would cost 25 times the price. With the team licence you pay 3 times the price, an 88% saving.</li>
<li><strong>A fair price for the creative work.</strong> A file shared across a team replaces several sales. The ×3 multiplier reflects this wider use while staying affordable for school, daycare and community budgets.</li>
<li><strong>A simple, transparent calculation.</strong> No complicated grid: you know the price in advance, whatever the number of people, up to 25.</li></ul>
<h3>Price examples</h3>
<table class="tbl"><thead><tr><th>Product</th><th>Individual licence</th><th>Team licence (× 3)</th></tr></thead><tbody>
<tr><td>One toolkit</td><td>$7</td><td>$21</td></tr>
<tr><td>One visual workbook</td><td>$3</td><td>$9</td></tr>
<tr><td>A toolkit collection</td><td>$25</td><td>$75</td></tr>
<tr><td>All toolkits</td><td>$75</td><td>$225</td></tr>
<tr><td>All of Filodie</td><td>$129</td><td>$387</td></tr></tbody></table>
<p class="muted">The reference price is the current price shown in the shop. For more than 25 people or several organizations (for example a school service centre), email me for a quote.</p>
<h3>How to order</h3>
<ol><li>Email <a href="mailto:melodie@filodie.ca?subject=Team%20licence">melodie@filodie.ca</a> with the products you want, the organization’s name and address, and a contact person.</li>
<li>You receive a PDF invoice, payable by Interac e-Transfer or cheque.</li>
<li>As soon as payment is received, you get the files by email, along with the invoice marked “paid”.</li></ol>
<p><a class="btn" href="mailto:melodie@filodie.ca?subject=Filodie%20service%20request">Email Mélodie</a></p>
"""),
    ("fr", "faq.html"): ("Questions fréquentes", """
<h2>Comment je reçois mes outils ?</h2><p>Dès le paiement, une page de téléchargement s’ouvre et un courriel contenant le lien vous est envoyé. Vous pouvez télécharger vos fichiers plusieurs fois.</p>
<h2>Les PDF sont-ils remplissables ?</h2><p>Oui : la plupart des fiches se remplissent à l’écran (Adobe Acrobat Reader, Aperçu sur Mac, navigateur) et s’impriment en format lettre.</p>
<h2>Puis-je imprimer plusieurs copies ?</h2><p>Oui, autant de copies que nécessaire pour vos propres interventions. Le partage des fichiers avec des collègues est interdit : une <a href="services.html#licence-equipe">licence d’équipe</a> est offerte pour les écoles, les CPE et les organismes.</p>
<h2>Pourquoi mon courriel apparaît-il sur les pages ?</h2><p>Chaque PDF est personnalisé au nom de l’acheteuse ou de l’acheteur. Cela protège le travail de création et permet de garder les prix accessibles.</p>
<h2>Les ressources de ma région sont-elles incluses ?</h2><p>Chaque trousse contient une page des 17 régions (DPJ, crise, autisme). Le bottin régional complet est gratuit.</p>
<h2>Existe-t-il des versions en anglais ?</h2><p>Oui, chaque outil a une version anglaise (bouton EN en haut de la page).</p>
<h2>Et si un fichier pose problème ?</h2><p>Les produits numériques ne sont pas remboursables. Si un fichier est défectueux ou ne correspond pas à sa description, écrivez-nous : nous le corrigeons ou le remplaçons rapidement. Voir les <a href="conditions.html">conditions de vente</a>.</p>
<h2>Mon école peut-elle payer par bon de commande ?</h2><p>Oui, écrivez-nous pour une soumission et une facture au nom de l’établissement.</p>"""),
    ("en", "faq.html"): ("Frequently asked questions", """
<h2>How do I receive my tools?</h2><p>Right after payment, a download page opens and an email with the link is sent to you. You can download your files several times.</p>
<h2>Are the PDFs fillable?</h2><p>Yes: most sheets can be filled in on screen (Adobe Acrobat Reader, Preview on Mac, browser) and printed on letter paper.</p>
<h2>Can I print several copies?</h2><p>Yes, as many copies as you need for your own interventions. Sharing the files with colleagues is not allowed: a <a href="services.html#team-licence">team licence</a> is available for schools, daycares and organizations.</p>
<h2>Why does my email appear on the pages?</h2><p>Each PDF is personalized with the buyer’s details. This protects the creative work and keeps prices affordable.</p>
<h2>Are resources for my region included?</h2><p>Every toolkit includes a page covering all 17 regions (youth protection, crisis, autism). The complete regional directory is free.</p>
<h2>Are the tools available in French?</h2><p>Yes, every tool has a French version (FR button at the top of the page).</p>
<h2>What if a file has a problem?</h2><p>Digital products are non-refundable. If a file is defective or does not match its description, write to us: we will quickly fix or replace it. See the <a href="terms.html">terms of sale</a>.</p>
<h2>Can my school pay with a purchase order?</h2><p>Yes, write to us for a quote and an invoice in the organization’s name.</p>"""),
    ("fr", "contact.html"): ("Contact", """
<p class="lead">Une question, une licence d’équipe, une correction à signaler dans une ressource ?</p>
<p>Écrivez à <a href="mailto:melodie@filodie.ca">melodie@filodie.ca</a>. Réponse en 2 jours ouvrables.</p>
<p class="muted">Pour une situation urgente, composez le 9-1-1 ou le 811 option 2 (Info-Social). Filodie n’offre pas de service d’intervention.</p>"""),
    ("en", "contact.html"): ("Contact", """
<p class="lead">A question, a team licence, a resource that needs updating?</p>
<p>Write to <a href="mailto:melodie@filodie.ca">melodie@filodie.ca</a>. We reply within 2 business days.</p>
<p class="muted">In an emergency, call 9-1-1 or 811 option 2 (Info-Social). Filodie does not provide intervention services.</p>"""),
    ("fr", "licence.html"): ("Licence d’utilisation", """
<h2>Licence individuelle (incluse avec chaque achat)</h2>
<ul><li>Utiliser les outils dans votre pratique professionnelle ou familiale.</li>
<li>Imprimer et photocopier autant de copies que nécessaire pour les personnes que <strong>vous</strong> accompagnez.</li>
<li>Remplir les fiches à l’écran et les conserver dans vos dossiers.</li></ul>
<h2>Ce qui est interdit</h2>
<ul><li>Partager, transférer ou envoyer les fichiers à d’autres personnes, y compris des collègues.</li>
<li>Déposer les fichiers sur un site, un réseau social, un disque partagé ou une plateforme accessible à d’autres.</li>
<li>Revendre, modifier pour revendre ou intégrer les outils à un produit commercial.</li>
<li>Retirer les mentions de droits d’auteur ou le tatouage de l’acheteuse ou de l’acheteur.</li></ul>
<h2>Licence d’équipe</h2><p>Pour une école, un CPE, un service de garde, un organisme ou une équipe : les fichiers peuvent être déposés sur le réseau interne de l’établissement. Tarif : 3 fois le prix individuel, pour jusqu’à 25 membres du personnel. <a href="services.html#licence-equipe">Détails, exemples de prix et commande</a>.</p>
<p class="muted">Illustrations : Fluent Emoji © Microsoft, sous licence MIT. Polices : Fraunces, Nunito Sans, Caveat (SIL Open Font License).</p>"""),
    ("en", "licence.html"): ("Licence", """
<h2>Individual licence (included with every purchase)</h2>
<ul><li>Use the tools in your professional or family practice.</li>
<li>Print and photocopy as many copies as needed for the people <strong>you</strong> support.</li>
<li>Fill in the sheets on screen and keep them in your files.</li></ul>
<h2>What is not allowed</h2>
<ul><li>Sharing, forwarding or sending the files to others, including colleagues.</li>
<li>Uploading the files to a website, social network, shared drive or any platform others can access.</li>
<li>Reselling, modifying for resale or including the tools in a commercial product.</li>
<li>Removing copyright notices or the buyer’s watermark.</li></ul>
<h2>Team licence</h2><p>For a school, daycare, organization or team: the files may be placed on the organization’s internal network. Price: 3 times the individual price, for up to 25 staff members. <a href="services.html#team-licence">Details, price examples and ordering</a>.</p>
<p class="muted">Illustrations: Fluent Emoji © Microsoft, MIT licence. Fonts: Fraunces, Nunito Sans, Caveat (SIL Open Font License).</p>"""),
    ("fr", "conditions.html"): ("Conditions de vente", """
<p><strong>Entreprise :</strong> Filodie, entreprise individuelle immatriculée au Québec (NEQ : 2282614819). Courriel : melodie@filodie.ca.</p>
<h2>Produits et prix</h2><p>Les produits sont des fichiers numériques (PDF). Les prix sont affichés en dollars canadiens et correspondent au prix total à payer. Filodie n’est pas inscrite aux fichiers de la TPS et de la TVQ (petit fournisseur). Toutefois, Payhip agit comme plateforme de vente et peut percevoir lui-même la taxe de vente applicable selon votre lieu de résidence (par exemple la TPS/TVH au Canada ou la TVA en Europe) ; le cas échéant, elle est affichée clairement avant le paiement.</p>
<h2>Paiement et livraison</h2><p>Le paiement est traité de façon sécurisée par Payhip, Stripe ou PayPal; Filodie n’a jamais accès à vos données de carte. La livraison est immédiate : une page de téléchargement s’ouvre après le paiement et un courriel de confirmation contenant le lien vous est envoyé.</p>
<h2>Aucun remboursement</h2><p>Comme un fichier numérique ne peut pas être retourné, les achats ne sont pas remboursables. Si un fichier est défectueux, illisible ou ne correspond pas à sa description, écrivez-nous à melodie@filodie.ca : nous le corrigeons ou le remplaçons sans frais. Ces conditions n’enlèvent aucun des droits prévus par la Loi sur la protection du consommateur.</p>
<h2>Utilisation</h2><p>L’achat donne droit à la <a href="licence.html">licence individuelle</a>. Les outils soutiennent l’intervention et ne remplacent ni l’évaluation d’une personne professionnelle qualifiée ni le jugement clinique. Les coordonnées des ressources sont vérifiées à la date indiquée et peuvent changer.</p>
<h2>Droit applicable</h2><p>Ces conditions sont régies par les lois du Québec et du Canada.</p>"""),
    ("en", "terms.html"): ("Terms of sale", """
<p><strong>Business:</strong> Filodie, sole proprietorship registered in Québec (NEQ: 2282614819). Email: melodie@filodie.ca.</p>
<h2>Products and prices</h2><p>Products are digital files (PDF). Prices are shown in Canadian dollars and are the total amount payable. Filodie is not registered for GST/QST (small supplier). However, Payhip acts as a marketplace facilitator and may itself collect the applicable sales tax based on where you live (for example GST/HST in Canada or VAT in Europe); if so, it is clearly shown before payment.</p>
<h2>Payment and delivery</h2><p>Payment is processed securely by Payhip, Stripe or PayPal; Filodie never has access to your card details. Delivery is instant: a download page opens after payment and a confirmation email with the link is sent to you.</p>
<h2>No refunds</h2><p>Because a digital file cannot be returned, purchases are non-refundable. If a file is defective, unreadable or does not match its description, write to us at melodie@filodie.ca: we will fix or replace it at no charge. These terms do not limit any rights under Québec’s Consumer Protection Act.</p>
<h2>Use</h2><p>Each purchase includes the <a href="licence.html">individual licence</a>. The tools support intervention and do not replace an assessment by a qualified professional or clinical judgment. Resource contact details are verified on the date shown and may change.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of Québec and Canada.</p>"""),
    ("fr", "confidentialite.html"): ("Politique de confidentialité", """
<p>Dernière mise à jour : 28 septembre 2026.</p>
<h2>Responsable de la protection des renseignements personnels</h2><p>Mélodie, propriétaire de Filodie · melodie@filodie.ca</p>
<h2>Renseignements recueillis</h2><ul><li>Lors d’un achat : nom, adresse courriel, pays ou province (pour les taxes) et historique d’achat, recueillis par Payhip.</li>
<li>Si vous vous abonnez à l’infolettre : adresse courriel et prénom, avec votre consentement explicite.</li>
<li>Si vous nous écrivez : le contenu de votre message.</li></ul>
<h2>Pourquoi</h2><p>Pour livrer vos fichiers, émettre vos reçus, répondre à vos questions et, si vous y consentez, vous envoyer l’infolettre. Vos renseignements ne sont jamais vendus.</p>
<h2>Communication à des tiers</h2><p>Payhip (plateforme de vente), Stripe et PayPal (paiements) et MailerLite (infolettre) traitent certains renseignements pour notre compte. Ces entreprises peuvent conserver des données à l’extérieur du Québec; nous les avons choisies pour leurs mesures de sécurité reconnues.</p>
<h2>Témoins (cookies)</h2><p>Le site filodie.ca ne dépose aucun témoin de suivi ni de publicité. Les pages de paiement Payhip utilisent des témoins nécessaires à la transaction.</p>
<h2>Conservation</h2><p>Les renseignements d’achat sont conservés 6 ans (obligations fiscales), puis détruits. Vous pouvez vous désabonner de l’infolettre en tout temps.</p>
<h2>Vos droits</h2><p>Vous pouvez demander l’accès à vos renseignements, leur rectification ou leur suppression en écrivant à melodie@filodie.ca. Vous pouvez aussi porter plainte à la Commission d’accès à l’information du Québec.</p>"""),
    ("en", "privacy.html"): ("Privacy policy", """
<p>Last updated: September 28, 2026.</p>
<h2>Person in charge of personal information</h2><p>Mélodie, owner of Filodie · melodie@filodie.ca</p>
<h2>Information collected</h2><ul><li>When you buy: name, email address, country or province (for taxes) and purchase history, collected by Payhip.</li>
<li>If you subscribe to the newsletter: email address and first name, with your express consent.</li>
<li>If you write to us: the content of your message.</li></ul>
<h2>Why</h2><p>To deliver your files, issue receipts, answer your questions and, if you consent, send the newsletter. Your information is never sold.</p>
<h2>Service providers</h2><p>Payhip (sales platform), Stripe and PayPal (payments) and MailerLite (newsletter) process some information on our behalf. These companies may store data outside Québec; they were chosen for their recognized security measures.</p>
<h2>Cookies</h2><p>The filodie.ca website does not set any tracking or advertising cookies. Payhip checkout pages use cookies required for the transaction.</p>
<h2>Retention</h2><p>Purchase information is kept for 6 years (tax obligations), then destroyed. You may unsubscribe from the newsletter at any time.</p>
<h2>Your rights</h2><p>You may request access to, correction or deletion of your information by writing to melodie@filodie.ca. You may also file a complaint with the Commission d’accès à l’information du Québec.</p>"""),
}

CSS = """@font-face{font-family:Fraunces;src:url(fonts/Fraunces-600.ttf);font-weight:600;font-display:swap}
@font-face{font-family:Fraunces;src:url(fonts/Fraunces-800.ttf);font-weight:800;font-display:swap}
@font-face{font-family:Fraunces;src:url(fonts/Fraunces-500i.ttf);font-style:italic;font-display:swap}
@font-face{font-family:Nunito;src:url(fonts/NunitoSans-400.ttf);font-weight:400;font-display:swap}
@font-face{font-family:Nunito;src:url(fonts/NunitoSans-700.ttf);font-weight:700;font-display:swap}
@font-face{font-family:Nunito;src:url(fonts/NunitoSans-800.ttf);font-weight:800;font-display:swap}
:root{--ink:#1F3B4D;--terra:#D9734E;--sage:#6F9A81;--cream:#F8F2E9;--sand:#E6DDCF;--gray:#6B7178;--bg:#FFFDF9;--card:#fff}
@media (prefers-color-scheme:dark){:root{--ink:#EDE6DA;--cream:#1E2A33;--sand:#34434E;--gray:#A9B1B8;--bg:#15202A;--card:#1B2833}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.6 Nunito,system-ui,sans-serif}
a{color:var(--terra)}img{max-width:100%;display:block}
.wrap{max-width:1140px;margin:0 auto;padding:0 20px}
h1,h2,h3{font-family:Fraunces,Georgia,serif;font-weight:600;line-height:1.15}
h1{font-size:clamp(2rem,5vw,3.4rem);margin:.2em 0}h2{font-size:1.9rem;margin:1.6em 0 .6em}h3{font-size:1.15rem;margin:.6em 0 .3em}
em{font-family:Fraunces,Georgia,serif;font-style:italic;color:var(--terra)}
.lead{font-size:1.15rem;color:var(--gray);max-width:720px}.muted{color:var(--gray)}
.promo{background:var(--terra);color:#fff;text-align:center;padding:9px 16px;font-weight:700;font-size:.95rem;line-height:1.5}
.promo code{background:#fff;color:#1F3B4D;padding:2px 9px;border-radius:6px;font:800 .95rem/1.4 ui-monospace,monospace;letter-spacing:.04em}
.promo button{margin-left:6px;background:transparent;color:#fff;border:1.5px solid #fff;border-radius:20px;padding:1px 11px;font:700 .85rem Nunito,sans-serif;cursor:pointer}
.top{position:sticky;top:0;z-index:10;background:var(--cream);border-bottom:1px solid var(--sand)}
.bar{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{display:inline-flex;flex-direction:column;align-items:center;font-family:Fraunces,serif;font-weight:600;font-size:1.7rem;line-height:1;color:var(--ink);text-decoration:none}
.logo svg{display:block;width:4em;height:.82em;margin:.1em -.3em 0}
.logo.small{font-size:1.3rem;margin:0 0 6px}
nav{display:flex;gap:18px;align-items:center}nav a{color:var(--ink);text-decoration:none;font-weight:700;font-size:.95rem}
nav a[aria-current]{color:var(--terra)}nav .lang{border:1.5px solid var(--ink);border-radius:20px;padding:2px 10px}
.menu{display:none;background:none;border:0;font-size:1.6rem;color:var(--ink)}
@media (max-width:820px){.menu{display:block}nav{display:none;position:absolute;top:64px;left:0;right:0;background:var(--cream);flex-direction:column;padding:16px;border-bottom:1px solid var(--sand)}nav.open{display:flex}}
.hero{background:var(--cream);padding:40px 0 56px;position:relative;overflow:hidden}
.thread{position:absolute;left:0;right:0;top:0;width:100%;height:90px;color:var(--terra);opacity:.9}
.kicker{margin-top:60px;color:var(--sage);font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:.85rem}
.btn{display:inline-block;background:var(--terra);color:#fff!important;text-decoration:none;font-weight:800;padding:11px 20px;border-radius:30px;border:2px solid var(--terra)}
.btn.ghost{background:transparent;color:var(--terra)!important}.btn.off{background:var(--sand);border-color:var(--sand);color:var(--gray)!important;font-size:.85rem}
.ctas{display:flex;gap:10px;flex-wrap:wrap}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:34px}
.stats div{background:var(--card);border-radius:14px;padding:14px}.stats strong{display:block;font-family:Fraunces,serif;font-size:2rem;color:var(--terra)}
@media (max-width:640px){.stats{grid-template-columns:repeat(2,1fr)}}
.grid4{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px}
.abo{display:grid;grid-template-columns:1fr 1fr;gap:32px;align-items:center}@media(max-width:760px){.abo{grid-template-columns:1fr}}
.card{background:var(--card);border:1px solid var(--sand);border-radius:16px;overflow:hidden;color:var(--ink);text-decoration:none}
.card.col img{aspect-ratio:17/13;object-fit:cover;object-position:top}.card.col h3,.card.col p{padding:0 16px}.card.col p{color:var(--gray);font-size:.95rem}
.band{background:var(--cream);padding:10px 0 40px;margin-top:40px}.why div{background:var(--card);border-radius:14px;padding:6px 18px}
.shop .filters{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:14px 0}
.filters input,.filters select{font:inherit;padding:9px 14px;border-radius:24px;border:1.5px solid var(--sand);background:var(--card);color:var(--ink)}
.filters input{flex:1 1 260px}.chips{display:flex;gap:6px;flex-wrap:wrap}
.chips button{font:inherit;font-weight:700;font-size:.9rem;padding:7px 14px;border-radius:20px;border:1.5px solid var(--sand);background:var(--card);color:var(--ink);cursor:pointer}
.chips button.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}
.products{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px;margin-bottom:60px}
@media (max-width:560px){.products{grid-template-columns:1fr 1fr;gap:10px}.pb{padding:8px 9px}.prod h3{font-size:.95rem}.buy{flex-direction:column;align-items:flex-start;gap:6px}}
.prod{display:flex;flex-direction:column}.prod img{aspect-ratio:612/792;object-fit:cover;border-bottom:1px solid var(--sand)}
.pvb{position:relative;display:block;padding:0;border:0;background:none;cursor:zoom-in;width:100%}.pvb img{display:block;width:100%}
.pvl{position:absolute;right:10px;bottom:12px;background:var(--ink);color:#fff;font-weight:800;font-size:.8rem;padding:4px 12px;border-radius:20px;opacity:.9}
.pvb:hover .pvl,.pvb:focus-visible .pvl{background:var(--terra);opacity:1}
.pv{border:0;border-radius:18px;padding:18px 20px;max-width:min(760px,94vw);width:100%;max-height:92vh;background:var(--card);color:var(--ink)}
.pv::backdrop{background:rgba(20,30,40,.6)}.pvh{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}.pvh h3{margin:0}
.pvx{font-size:1.8rem;line-height:1;background:none;border:0;cursor:pointer;color:var(--ink)}
.pvi{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin:10px 0}.pvi img{width:100%;border:1px solid var(--sand);border-radius:8px}
.pb{padding:12px 14px;display:flex;flex-direction:column;flex:1}.grp{margin:0;color:var(--sage);font-weight:800;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em}
.prod h3{font-size:1.05rem}.sub{margin:0;color:var(--gray);font-size:.9rem}
.save{margin:6px 0 0;font-size:.82rem;font-weight:800;color:var(--sage)}
details{font-size:.9rem;margin:6px 0}summary{cursor:pointer;color:var(--terra);font-weight:700}
.buy{margin-top:auto;display:flex;justify-content:space-between;align-items:center;padding-top:10px}.buy strong{font-size:1.1rem}
.split{display:grid;grid-template-columns:1.2fr 1fr;gap:40px;align-items:center;padding:40px 20px 70px}
@media (max-width:760px){.split{grid-template-columns:1fr}}
.shadow{border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,.15)}
.prose{max-width:780px;padding-bottom:60px}.prose h2{font-size:1.4rem}
.prose h3{font-size:1.1rem;margin-top:1.4em}.tbl{width:100%;border-collapse:collapse;margin:1em 0;font-size:.95rem}.tbl th,.tbl td{padding:8px 10px;text-align:left;border-bottom:1px solid rgba(127,127,127,.25)}.tbl th{font-weight:800}.tbl td:not(:first-child),.tbl th:not(:first-child){text-align:right;white-space:nowrap}
.foot{background:var(--cream);border-top:1px solid var(--sand);padding:30px 0;font-size:.9rem;color:var(--gray)}
.foot .legal a{color:var(--ink)}.note{font-size:.8rem}
"""

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#F8F2E9"/>'
           '<text x="32" y="36" text-anchor="middle" font-family="Georgia,serif" font-weight="700" font-size="36" fill="#1F3B4D">f</text>'
           '<path d="M6 50C12 44 12 44 18 50S24 56 30 50S36 44 42 50S48 56 56 50" fill="none" stroke="#D9734E" stroke-width="2.5" '
           'stroke-linecap="round"/>' + "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="{c}"/>' for x, y, c in [
               (12, 46, "#1F3B4D"), (24, 54, "#D9734E"), (36, 46, "#6F9A81"), (48, 54, "#E3B04B"), (56, 50, "#D98FA0")])
           + '</svg>')


COLO = os.path.join(SRC, "..", "Cahiers à colorier gratuits Filodie")


def coloriage(lang):
    """Page des cahiers à colorier gratuits : téléchargement direct (FR et EN), sans inscription."""
    import glob as _g
    import fitz
    fr = lang == "fr"
    od = os.path.join(PUB, "pdf", "colorier"); os.makedirs(od, exist_ok=True)
    idir = os.path.join(PUB, "img", "colorier"); os.makedirs(idir, exist_ok=True)
    cartes = ""
    for pf in sorted(_g.glob(os.path.join(COLO, "Français", "*.pdf"))):
        code = os.path.basename(pf).split("_")[1]
        pe = (_g.glob(os.path.join(COLO, "English", f"Filodie_{code}_*.pdf")) or [None])[0]
        for p in (pf, pe):
            if p: shutil.copy(p, od)
        src = pf if fr else (pe or pf)
        d = fitz.open(src)
        img = os.path.join(idir, f"{code}_{lang}.jpg")
        d[0].get_pixmap(dpi=60).save(img)
        titre = d.metadata.get("title", "").replace("Filodie – ", "")
        dl = lambda p, t: f'<a class="btn" href="{L[lang]["base"]}pdf/colorier/{os.path.basename(p)}" download>{t}</a>' if p else ""
        b1 = dl(pf, "Télécharger (français)" if fr else "Download (French)")
        b2 = dl(pe, "Télécharger (anglais)" if fr else "Download (English)")
        cartes += (f'<div class="card col"><img src="{L[lang]["base"]}img/colorier/{code}_{lang}.jpg" alt="" loading="lazy">'
                   f'<h3>{html.escape(titre)}</h3><p class="muted" style="padding:0 16px">'
                   f'{"6 pages · PDF à imprimer" if fr else "6 pages · printable PDF"}</p>'
                   f'<p style="padding:0 16px 16px;display:flex;gap:8px;flex-wrap:wrap">{(b1 + b2) if fr else (b2 + b1)}</p></div>')
    h1 = "Cahiers à colorier gratuits" if fr else "Free colouring books"
    lead = ("Des cahiers de 6 pages pour parler des émotions, du calme, de la gentillesse et des forces, en coloriant. "
            "Chaque page propose une question pour en discuter ensemble et un repère pour l’adulte. Téléchargement "
            "direct, sans inscription, à imprimer pour la maison ou la classe." if fr else
            "Six-page books to talk about feelings, calm, kindness and strengths while colouring. Each page has a "
            "question to discuss together and a tip for the adult. Direct download, no sign-up, free to print for "
            "home or classroom.")
    abo_t = "Recevez l’outil gratuit chaque mois" if fr else "Get the free tool every month"
    abo_p = ("Un outil Filodie gratuit et les nouveautés, une fois par mois." if fr else
             "A free Filodie tool and what’s new, once a month.")
    body = (f'<section class="wrap"><h1>{h1}</h1><p class="lead">{lead}</p><div class="grid4">{cartes}</div>'
            f'<p class="muted">{"Illustrations : Fluent Emoji © Microsoft, licence MIT, redessinées en traits à colorier." if fr else "Illustrations: Fluent Emoji © Microsoft, MIT licence, redrawn as colouring outlines."}</p></section>'
            f'<section class="band"><div class="wrap abo"><div><h2>{abo_t}</h2><p class="lead">{abo_p}</p></div>'
            f'<div class="ml-embedded" data-form="C80x4w"></div></div></section>')
    return page(lang, "coloriage.html" if fr else "colouring.html", h1, body)


def build():
    if "--catalogue" in sys.argv or "--prix" in sys.argv or not os.path.exists(CAT):
        catalogue()
    items = [i for i in json.load(open(CAT, encoding="utf-8")) if not i.get("futur")]
    for lang in ("fr", "en"):                         # chiffres de la page d’accueil, toujours à jour
        st = L[lang]["stats"]
        st[0] = (str(sum(1 for i in items if i["type"] == "trousse")), st[0][1])
        st[1] = (str(sum(1 for i in items if i["type"] == "cahier")), st[1][1])
    os.makedirs(os.path.join(PUB, "en"), exist_ok=True)
    fd = os.path.join(PUB, "fonts")
    os.makedirs(fd, exist_ok=True)
    for f in ("Fraunces-600.ttf", "Fraunces-800.ttf", "Fraunces-500i.ttf", "NunitoSans-400.ttf", "NunitoSans-700.ttf",
              "NunitoSans-800.ttf"):
        shutil.copy(os.path.join(SRC, "fonts", f), fd)
    open(os.path.join(PUB, "style.css"), "w").write(CSS)
    open(os.path.join(PUB, "favicon.svg"), "w").write(FAVICON)
    og = os.path.join(LOGO, "Filodie_couverture_facebook_1640x624.png")   # aperçu des partages Facebook
    if os.path.exists(og):
        shutil.copy(og, os.path.join(PUB, "og-image.png"))
    images(items)
    lg = os.path.join(LOGO, "Filodie_logo_couleur_fond_creme.png")      # logo des infolettres (MailerLite)
    if os.path.exists(lg):
        from PIL import Image
        im = Image.open(lg).convert("RGB")
        im.resize((480, int(im.height * 480 / im.width)), Image.LANCZOS).save(os.path.join(PUB, "img", "courriel-logo.png"),
                                                                              optimize=True)
    for lang, d in (("fr", PUB), ("en", os.path.join(PUB, "en"))):
        open(os.path.join(d, "index.html"), "w").write(home(lang))
        open(os.path.join(d, "boutique.html" if lang == "fr" else "shop.html"), "w").write(shop(lang, items))
        open(os.path.join(d, "bottin.html" if lang == "fr" else "directory.html"), "w").write(bottin(lang, items))
        open(os.path.join(d, "coloriage.html" if lang == "fr" else "colouring.html"), "w").write(coloriage(lang))
    open(os.path.join(PUB, "404.html"), "w").write(page("fr", "index.html", "Page introuvable",
        '<section class="wrap prose"><h1>Page introuvable</h1><p class="lead">Cette page n’existe pas ou a été déplacée. '
        '· This page does not exist.</p><p><a class="btn" href="/">Accueil · Home</a></p></section>').replace('href="index.html"', 'href="/index.html"'))
    for (lang, name), (title, content) in CONTENT.items():
        d = PUB if lang == "fr" else os.path.join(PUB, "en")
        open(os.path.join(d, name), "w").write(textpage(lang, name, title, content))
    print("Site prêt :", PUB)


if __name__ == "__main__":
    build()
