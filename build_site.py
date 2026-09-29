# -*- coding: utf-8 -*-
"""Construit le site filodie.ca (français + anglais) dans le dossier « public ».

    python3 build_site.py            # pages + images manquantes
    python3 build_site.py --catalogue  # relit les PDF et met à jour produits.json (garde prix et liens Payhip)

Pour activer un bouton « Acheter » : collez l'identifiant Payhip (ex. « aB3dE ») dans produits.json,
champ "payhip" (français) ou "payhip_en" (anglais), puis relancez ce script."""
import html
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
CAT = os.path.join(HERE, "produits.json")
sys.path.insert(0, SRC)

EN = {}
for fn in sorted(os.listdir(os.path.join(SRC, "i18n"))) if os.path.isdir(os.path.join(SRC, "i18n")) else []:
    if fn.startswith("en_") and fn.endswith(".json"):
        EN.update(json.load(open(os.path.join(SRC, "i18n", fn), encoding="utf-8")))


def tr(s):
    return EN.get(s, s)


# Prix à l'unité (dollars canadiens). Les lots ont leur prix fixé plus bas, dans catalogue().
PRIX = {"trousse": 5.00, "edition": 2.00, "cahier": 2.00, "livre": 15.00, "bottin": 0.0,
        "lot_cahiers": 20.00, "lot_collection": 20.00, "lot_specialisees": 30.00, "lot_tout": 60.00, "mega": 99.00}


# --------------------------------------------------------------------------- catalogue
def catalogue():
    from contenu_ages import AGES
    from contenu_troubles import TROUBLES
    from contenu_nouveaux import NOUVEAUX
    import filodie_trousses as ft
    from filodie_editions import EDITIONS
    from filodie_visuel import load, SERIES, fname
    items = []

    def add(**k):
        k.setdefault("prix", PRIX[k["type"]])
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
        add(id="lot-" + re.sub(r"\W+", "-", v.lower()).strip("-"), type="lot_collection", groupe="Lots",
            titre=f"Collection Filodie : {v.split('– ')[-1]}", sous=f"{len(its)} trousses",
            desc="Toutes les trousses du volet « " + v.split("– ")[-1] + " ».", fichiers=[], contient=[i["id"] for i in its])
    sp = [i["id"] for i in items if i["groupe"] == "Trousses spécialisées"]
    add(id="lot-specialisees", type="lot_specialisees", groupe="Lots", titre="Les 16 trousses spécialisées",
        sous="Âges et troubles", desc="Petite enfance, secondaire, adultes, aînés, TSA, TDAH, DI, langage, comportement, "
                                      "crise, suicide, dépendances et plus.", fichiers=[], contient=sp)
    tous = [i["id"] for i in items if i["type"] == "cahier"]
    add(id="lot-tous-les-cahiers", type="lot_tout", groupe="Lots", titre="Tous les cahiers visuels",
        sous=f"{len(tous)} cahiers · 5 séries", prix=60.00,
        desc="Les cahiers TSA, TDAH, habiletés sociales, DI et comportement, en couleur et à colorier.",
        fichiers=[], contient=tous)
    tt = [i["id"] for i in items if i["type"] in ("trousse", "edition")]
    add(id="lot-toutes-les-trousses", type="lot_tout", groupe="Lots", titre="Toutes les trousses",
        sous=f"{len(tt)} trousses et éditions", prix=60.00,
        desc="La trousse principale, les 16 trousses spécialisées, les 78 trousses de la Collection et les 5 éditions.",
        fichiers=[], contient=tt)
    add(id="lot-mega", type="mega", groupe="Lots", titre="Tout Filodie", sous="Toute la collection",
        desc="Les 95 trousses, les éditions, les 179 cahiers visuels, le Grand livre clinique et le bottin régional.",
        fichiers=[], contient=[i["id"] for i in items if not i["type"].startswith("lot") and i["type"] != "mega"])
    # lots de collection : environ 2 $ par trousse, arrondi à 5 $
    for i in items:
        if i["type"] == "lot_collection":
            i["prix"] = float(max(10, 5 * round(len(i["contient"]) * 2 / 5)))
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
    json.dump(items, open(CAT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(len(items), "produits dans produits.json")


# --------------------------------------------------------------------------- images
def en_path(rel):
    import filodie_i18n as i
    return i.path_en(os.path.join(OUT_FR, rel))


def vignette(pdf, out, w=420):
    if os.path.exists(out) and os.path.getmtime(out) > os.path.getmtime(pdf):
        return
    d = fitz.open(pdf)
    pix = d[0].get_pixmap(matrix=fitz.Matrix(w / d[0].rect.width, w / d[0].rect.width))
    pix.save(out, jpg_quality=82) if out.endswith(".jpg") else pix.save(out)


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
    for i in items:
        if i.get("contient"):
            i["img"] = i["contient"][0]


# --------------------------------------------------------------------------- textes du site
L = {
    "fr": {
        "lang": "fr-CA", "other": "en", "other_label": "EN", "base": "",
        "tag": "Outils cliniques pour T.E.S.",
        "nav": [("index.html", "Accueil"), ("boutique.html", "Boutique"), ("bottin.html", "Bottin gratuit"),
                ("a-propos.html", "À propos"), ("faq.html", "FAQ"), ("contact.html", "Contact")],
        "hero_k": "Outils cliniques · éducation spécialisée",
        "hero_1": "Tenir le fil,", "hero_2": "de l’observation à l’intervention.",
        "hero_p": "Des trousses, des cahiers visuels et un grand livre clinique conçus au Québec pour les T.E.S., "
                  "les enseignantes, les éducatrices et les familles. Imprimables, remplissables à l’écran, "
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
        "shop_t": "Boutique", "shop_p": "Cahiers à 2 $, trousses à 5 $, et des lots jusqu’à 90 % moins chers. Prix en dollars canadiens, téléchargement immédiat après le paiement.",
        "search": "Rechercher un outil…", "all": "Tout",
        "types": {"trousse": "Trousses", "edition": "Éditions", "cahier": "Cahiers visuels", "livre": "Grand livre",
                  "bottin": "Bottin", "lot": "Lots"},
        "buy": "Acheter", "soon": "Bientôt disponible", "free": "Gratuit", "get": "Obtenir", "details": "Détails",
        "count": "produits", "value": "Valeur à l’unité", "save": "économie",
        "bottin_t": "Bottin régional gratuit",
        "bottin_p": "Les ressources des 17 régions du Québec, classées par problématique : signalement à la DPJ, centres de crise, "
                    "CLSC, associations en autisme et en TDAH, déficience intellectuelle, proches aidants, violence et dépendances. "
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
                ("about.html", "About"), ("faq.html", "FAQ"), ("contact.html", "Contact")],
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
        "shop_t": "Shop", "shop_p": "Workbooks at $2, toolkits at $5, and bundles up to 90% off. Prices in Canadian dollars, instant download after payment.",
        "search": "Search for a tool…", "all": "All",
        "types": {"trousse": "Toolkits", "edition": "Editions", "cahier": "Visual workbooks", "livre": "Handbook",
                  "bottin": "Directory", "lot": "Bundles"},
        "buy": "Buy", "soon": "Coming soon", "free": "Free", "get": "Get it", "details": "Details",
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
         "a-propos.html": "about.html", "faq.html": "faq.html", "contact.html": "contact.html",
         "licence.html": "licence.html", "conditions.html": "terms.html", "confidentialite.html": "privacy.html"}
PAIRS_EN = {v: k for k, v in PAIRS.items()}

THREAD = ('<svg class="thread" viewBox="0 0 600 90" preserveAspectRatio="none" aria-hidden="true"><path d="M-10 60 '
          'C 80 30, 160 80, 250 50 S 330 10, 300 35 S 330 70, 420 55 S 560 20, 610 30" fill="none" stroke="currentColor" '
          'stroke-width="2.4" stroke-linecap="round"/></svg>')


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
<title>{html.escape(title) + " · Filodie" if title != "Filodie" else "Filodie · " + t["tag"]}</title>
<meta name="description" content="{html.escape(desc or t['hero_p'])}">
<link rel="alternate" hreflang="{L[t['other']]['lang']}" href="{other_href}">
<link rel="icon" href="{b}favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{b}style.css">
</head>
<body>
<header class="top">
  <div class="wrap bar">
    <a class="logo" href="index.html">filodie<span class="knot" aria-hidden="true"></span></a>
    <button class="menu" aria-expanded="false" aria-controls="nav">☰</button>
    <nav id="nav">{nav}<a class="lang" href="{other_href}" hreflang="{L[t['other']]['lang']}">{t['other_label']}</a></nav>
  </div>
</header>
<main>
{body}
</main>
<footer class="foot">
  <div class="wrap">
    <p class="logo small">filodie</p>
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


def home(lang):
    t = L[lang]
    shop = "boutique.html" if lang == "fr" else "shop.html"
    bot = "bottin.html" if lang == "fr" else "directory.html"
    stats = "".join(f"<div><strong>{n}</strong><span>{l}</span></div>" for n, l in t["stats"])
    cols = "".join(f'<a class="card col" href="{h}"><img src="{t["base"]}img/{lang}/{img}.jpg" alt="" loading="lazy">'
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
<section class="wrap"><h2>{t['col_t']}</h2><div class="grid4">{cols}</div></section>
<section class="band"><div class="wrap"><h2>{t['why_t']}</h2><div class="grid4 why">{why}</div></div></section>
"""
    return page(lang, "index.html", "Filodie", body)


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
            "n": tr(i["titre"]) if lang == "en" else i["titre"],
            "s": tr(i["sous"]) if lang == "en" else i["sous"],
            "d": tr(i["desc"]) if lang == "en" else i["desc"],
            "p": i["prix"], "k": i["payhip_en"] if lang == "en" else i["payhip"],
            "img": f"{t['base']}img/{img_lang}/{img}.jpg", "c": i.get("code", ""), "v": i.get("valeur", 0),
        })
    chips = "".join(f'<button data-t="{k}">{v}</button>' for k, v in t["types"].items())
    labels = json.dumps({k: t[k] for k in ("buy", "soon", "free", "get", "details", "count", "value", "save")}, ensure_ascii=False)
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
</section>"""
    js = f"""<script>
const P={json.dumps(data, ensure_ascii=False)};
const T={labels};
const fmt=new Intl.NumberFormat('{t['lang']}',{{style:'currency',currency:'CAD'}});
let type=(location.hash||'').slice(1), grp='', q='';
const list=document.getElementById('list'), sel=document.getElementById('g');
function esc(s){{return s.replace(/[&<>"]/g,c=>({{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}}[c]))}}
function groups(){{const gs=[...new Set(P.filter(p=>!type||p.t===type).map(p=>p.g))];
 sel.innerHTML='<option value="">{t['all']}</option>'+gs.map(g=>'<option>'+esc(g)+'</option>').join('');sel.value=grp}}
function card(p){{
 const price=p.p?fmt.format(p.p):T.free;
 const btn=p.k?'<a class="btn payhip-buy-button" data-theme="none" data-product="'+p.k+'" href="https://payhip.com/b/'+p.k+'">'+(p.p?T.buy:T.get)+'</a>'
   :'<span class="btn off">'+T.soon+'</span>';
 return '<article class="card prod"><img src="'+p.img+'" alt="" loading="lazy"><div class="pb"><p class="grp">'+esc(p.g)+(p.c?' · '+p.c:'')+'</p><h3>'+esc(p.n)+'</h3><p class="sub">'+esc(p.s)+'</p>'
  +(p.v>p.p?'<p class="save">'+T.value+' : <s>'+fmt.format(p.v)+'</s> · '+T.save+' '+Math.round(100-100*p.p/p.v)+' %</p>':'')
  +'<details><summary>'+T.details+'</summary><p>'+esc(p.d)+'</p></details><div class="buy"><strong>'+price+'</strong>'+btn+'</div></div></article>'}}
function draw(){{const w=q.toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'');
 const r=P.filter(p=>(!type||p.t===type)&&(!grp||p.g===grp)&&(!w||(p.n+' '+p.s+' '+p.d+' '+p.g+' '+p.c).toLowerCase().normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').includes(w)));
 document.getElementById('n').textContent=r.length+' '+T.count;list.innerHTML=r.map(card).join('');
 if(window.Payhip&&Payhip.Buttons)try{{Payhip.Buttons.init()}}catch(e){{}}}}
document.querySelectorAll('.chips button').forEach(b=>{{if(b.dataset.t===type){{document.querySelector('.chips .on').classList.remove('on');b.classList.add('on')}}
 b.onclick=()=>{{document.querySelector('.chips .on').classList.remove('on');b.classList.add('on');type=b.dataset.t;grp='';history.replaceState(null,'',type?'#'+type:location.pathname);groups();draw()}}}});
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
<p>Je m’appelle Mélodie. Je suis étudiante en Techniques d’éducation spécialisée et je crée les outils dont j’avais besoin en stage : clairs, beaux, rigoureux et vraiment utilisables avec les personnes que l’on accompagne. <em>[À personnaliser : ton parcours, tes stages, ce qui t’anime.]</em></p>
<p>Chaque outil est conçu au Québec, avec le vocabulaire du réseau et des ressources vérifiées dans les 17 régions. Les versions anglaises s’adressent aux milieux anglophones et bilingues.</p>
<h2>Mes engagements</h2>
<ul><li>Des contenus originaux, révisés et datés.</li><li>Des ressources vérifiées à la source et mises à jour chaque année.</li>
<li>Des outils respectueux de la dignité et de l’autodétermination des personnes.</li></ul>"""),
    ("en", "about.html"): ("About", """
<p class="lead">Filodie is built on one idea: good intervention holds together like a thread, linking observation, understanding, planning, support and communication.</p>
<p>My name is Mélodie. I am a special care counselling student, and I create the tools I needed during my internships: clear, attractive, rigorous and truly usable with the people we support. <em>[To personalize: your background, internships, what drives you.]</em></p>
<p>Every tool is designed in Québec, with the vocabulary of the health and education networks and resources verified in all 17 regions. French versions of every tool are also available.</p>
<h2>My commitments</h2>
<ul><li>Original, reviewed and dated content.</li><li>Resources verified at the source and updated every year.</li>
<li>Tools that respect the dignity and self-determination of every person.</li></ul>"""),
    ("fr", "faq.html"): ("Questions fréquentes", """
<h2>Comment je reçois mes outils ?</h2><p>Dès le paiement, une page de téléchargement s’ouvre et un courriel contenant le lien vous est envoyé. Vous pouvez télécharger vos fichiers plusieurs fois.</p>
<h2>Les PDF sont-ils remplissables ?</h2><p>Oui : la plupart des fiches se remplissent à l’écran (Adobe Acrobat Reader, Aperçu sur Mac, navigateur) et s’impriment en format lettre.</p>
<h2>Puis-je imprimer plusieurs copies ?</h2><p>Oui, autant de copies que nécessaire pour vos propres interventions. Le partage des fichiers avec des collègues est interdit : une licence d’équipe est offerte pour les écoles et les organismes.</p>
<h2>Pourquoi mon courriel apparaît-il sur les pages ?</h2><p>Chaque PDF est personnalisé au nom de l’acheteuse ou de l’acheteur. Cela protège le travail de création et permet de garder les prix accessibles.</p>
<h2>Les ressources de ma région sont-elles incluses ?</h2><p>Chaque trousse contient une page des 17 régions (DPJ, crise, autisme). Le bottin régional complet est gratuit.</p>
<h2>Existe-t-il des versions en anglais ?</h2><p>Oui, chaque outil a une version anglaise (bouton EN en haut de la page).</p>
<h2>Puis-je être remboursée ?</h2><p>Si un fichier est défectueux ou ne correspond pas à sa description, écrivez-nous dans les 14 jours : nous le corrigeons ou nous vous remboursons. Voir les <a href="conditions.html">conditions de vente</a>.</p>
<h2>Mon école peut-elle payer par bon de commande ?</h2><p>Oui, écrivez-nous pour une soumission et une facture au nom de l’établissement.</p>"""),
    ("en", "faq.html"): ("Frequently asked questions", """
<h2>How do I receive my tools?</h2><p>Right after payment, a download page opens and an email with the link is sent to you. You can download your files several times.</p>
<h2>Are the PDFs fillable?</h2><p>Yes: most sheets can be filled in on screen (Adobe Acrobat Reader, Preview on Mac, browser) and printed on letter paper.</p>
<h2>Can I print several copies?</h2><p>Yes, as many copies as you need for your own interventions. Sharing the files with colleagues is not allowed: a team licence is available for schools and organizations.</p>
<h2>Why does my email appear on the pages?</h2><p>Each PDF is personalized with the buyer’s details. This protects the creative work and keeps prices affordable.</p>
<h2>Are resources for my region included?</h2><p>Every toolkit includes a page covering all 17 regions (youth protection, crisis, autism). The complete regional directory is free.</p>
<h2>Are the tools available in French?</h2><p>Yes, every tool has a French version (FR button at the top of the page).</p>
<h2>Can I get a refund?</h2><p>If a file is defective or does not match its description, write to us within 14 days: we will fix it or refund you. See the <a href="terms.html">terms of sale</a>.</p>
<h2>Can my school pay with a purchase order?</h2><p>Yes, write to us for a quote and an invoice in the organization’s name.</p>"""),
    ("fr", "contact.html"): ("Contact", """
<p class="lead">Une question, une licence d’équipe, une correction à signaler dans une ressource ?</p>
<p>Écrivez à <a href="mailto:bonjour@filodie.ca">bonjour@filodie.ca</a>. Réponse en 2 jours ouvrables.</p>
<p class="muted">Pour une situation urgente, composez le 9-1-1 ou le 811 option 2 (Info-Social). Filodie n’offre pas de service d’intervention.</p>"""),
    ("en", "contact.html"): ("Contact", """
<p class="lead">A question, a team licence, a resource that needs updating?</p>
<p>Write to <a href="mailto:bonjour@filodie.ca">bonjour@filodie.ca</a>. We reply within 2 business days.</p>
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
<h2>Licence d’équipe</h2><p>Pour une école, un CPE, un service de garde, un organisme ou une équipe : les fichiers peuvent être déposés sur le réseau interne de l’établissement. Tarif : 3 fois le prix individuel, jusqu’à 25 intervenantes et intervenants.</p>
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
<h2>Team licence</h2><p>For a school, daycare, organization or team: the files may be placed on the organization’s internal network. Price: 3 times the individual price, for up to 25 staff members.</p>
<p class="muted">Illustrations: Fluent Emoji © Microsoft, MIT licence. Fonts: Fraunces, Nunito Sans, Caveat (SIL Open Font License).</p>"""),
    ("fr", "conditions.html"): ("Conditions de vente", """
<p><strong>Entreprise :</strong> Filodie, entreprise individuelle immatriculée au Québec (NEQ : <em>[à compléter]</em>). Courriel : bonjour@filodie.ca.</p>
<h2>Produits et prix</h2><p>Les produits sont des fichiers numériques (PDF). Les prix sont affichés en dollars canadiens et correspondent au prix total à payer. <em>[Si vous êtes inscrite à la TPS et à la TVQ : les taxes applicables sont ajoutées et détaillées avant le paiement.]</em></p>
<h2>Paiement et livraison</h2><p>Le paiement est traité de façon sécurisée par Payhip, Stripe ou PayPal; Filodie n’a jamais accès à vos données de carte. La livraison est immédiate : une page de téléchargement s’ouvre après le paiement et un courriel de confirmation contenant le lien vous est envoyé.</p>
<h2>Remboursements</h2><p>Comme un fichier numérique ne peut pas être retourné, les achats ne sont pas remboursables pour un simple changement d’idée. Si un fichier est défectueux, illisible ou ne correspond pas à sa description, écrivez-nous dans les 14 jours : nous le corrigeons, le remplaçons ou vous remboursons. Ces conditions n’enlèvent aucun des droits prévus par la Loi sur la protection du consommateur.</p>
<h2>Utilisation</h2><p>L’achat donne droit à la <a href="licence.html">licence individuelle</a>. Les outils soutiennent l’intervention et ne remplacent ni l’évaluation d’une personne professionnelle qualifiée ni le jugement clinique. Les coordonnées des ressources sont vérifiées à la date indiquée et peuvent changer.</p>
<h2>Droit applicable</h2><p>Ces conditions sont régies par les lois du Québec et du Canada.</p>"""),
    ("en", "terms.html"): ("Terms of sale", """
<p><strong>Business:</strong> Filodie, sole proprietorship registered in Québec (NEQ: <em>[to complete]</em>). Email: bonjour@filodie.ca.</p>
<h2>Products and prices</h2><p>Products are digital files (PDF). Prices are shown in Canadian dollars and are the total amount payable. <em>[If registered for GST/QST: applicable taxes are added and itemized before payment.]</em></p>
<h2>Payment and delivery</h2><p>Payment is processed securely by Payhip, Stripe or PayPal; Filodie never has access to your card details. Delivery is instant: a download page opens after payment and a confirmation email with the link is sent to you.</p>
<h2>Refunds</h2><p>Because a digital file cannot be returned, purchases are not refundable for a simple change of mind. If a file is defective, unreadable or does not match its description, write to us within 14 days: we will fix it, replace it or refund you. These terms do not limit any rights under Québec’s Consumer Protection Act.</p>
<h2>Use</h2><p>Each purchase includes the <a href="licence.html">individual licence</a>. The tools support intervention and do not replace an assessment by a qualified professional or clinical judgment. Resource contact details are verified on the date shown and may change.</p>
<h2>Governing law</h2><p>These terms are governed by the laws of Québec and Canada.</p>"""),
    ("fr", "confidentialite.html"): ("Politique de confidentialité", """
<p>Dernière mise à jour : 28 septembre 2026.</p>
<h2>Responsable de la protection des renseignements personnels</h2><p>Mélodie <em>[nom de famille]</em>, propriétaire de Filodie · bonjour@filodie.ca</p>
<h2>Renseignements recueillis</h2><ul><li>Lors d’un achat : nom, adresse courriel, pays ou province (pour les taxes) et historique d’achat, recueillis par Payhip.</li>
<li>Si vous vous abonnez à l’infolettre : adresse courriel et prénom, avec votre consentement explicite.</li>
<li>Si vous nous écrivez : le contenu de votre message.</li></ul>
<h2>Pourquoi</h2><p>Pour livrer vos fichiers, émettre vos reçus, répondre à vos questions et, si vous y consentez, vous envoyer l’infolettre. Vos renseignements ne sont jamais vendus.</p>
<h2>Communication à des tiers</h2><p>Payhip (plateforme de vente), Stripe et PayPal (paiements) et, s’il y a lieu, le service d’infolettre traitent certains renseignements pour notre compte. Ces entreprises peuvent conserver des données à l’extérieur du Québec; nous les avons choisies pour leurs mesures de sécurité reconnues.</p>
<h2>Témoins (cookies)</h2><p>Le site filodie.ca ne dépose aucun témoin de suivi ni de publicité. Les pages de paiement Payhip utilisent des témoins nécessaires à la transaction.</p>
<h2>Conservation</h2><p>Les renseignements d’achat sont conservés 6 ans (obligations fiscales), puis détruits. Vous pouvez vous désabonner de l’infolettre en tout temps.</p>
<h2>Vos droits</h2><p>Vous pouvez demander l’accès à vos renseignements, leur rectification ou leur suppression en écrivant à bonjour@filodie.ca. Vous pouvez aussi porter plainte à la Commission d’accès à l’information du Québec.</p>"""),
    ("en", "privacy.html"): ("Privacy policy", """
<p>Last updated: September 28, 2026.</p>
<h2>Person in charge of personal information</h2><p>Mélodie <em>[last name]</em>, owner of Filodie · bonjour@filodie.ca</p>
<h2>Information collected</h2><ul><li>When you buy: name, email address, country or province (for taxes) and purchase history, collected by Payhip.</li>
<li>If you subscribe to the newsletter: email address and first name, with your express consent.</li>
<li>If you write to us: the content of your message.</li></ul>
<h2>Why</h2><p>To deliver your files, issue receipts, answer your questions and, if you consent, send the newsletter. Your information is never sold.</p>
<h2>Service providers</h2><p>Payhip (sales platform), Stripe and PayPal (payments) and, if applicable, the newsletter service process some information on our behalf. These companies may store data outside Québec; they were chosen for their recognized security measures.</p>
<h2>Cookies</h2><p>The filodie.ca website does not set any tracking or advertising cookies. Payhip checkout pages use cookies required for the transaction.</p>
<h2>Retention</h2><p>Purchase information is kept for 6 years (tax obligations), then destroyed. You may unsubscribe from the newsletter at any time.</p>
<h2>Your rights</h2><p>You may request access to, correction or deletion of your information by writing to bonjour@filodie.ca. You may also file a complaint with the Commission d’accès à l’information du Québec.</p>"""),
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
.top{position:sticky;top:0;z-index:10;background:var(--cream);border-bottom:1px solid var(--sand)}
.bar{display:flex;align-items:center;justify-content:space-between;height:64px}
.logo{font-family:Fraunces,serif;font-weight:800;font-size:1.7rem;color:var(--ink);text-decoration:none;position:relative}
.logo.small{font-size:1.3rem;margin:0}
.knot{display:inline-block;width:18px;height:12px;margin-left:3px;border-bottom:2px solid var(--terra);border-radius:0 0 12px 0}
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
.pb{padding:12px 14px;display:flex;flex-direction:column;flex:1}.grp{margin:0;color:var(--sage);font-weight:800;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em}
.prod h3{font-size:1.05rem}.sub{margin:0;color:var(--gray);font-size:.9rem}
.save{margin:6px 0 0;font-size:.82rem;font-weight:800;color:var(--sage)}
details{font-size:.9rem;margin:6px 0}summary{cursor:pointer;color:var(--terra);font-weight:700}
.buy{margin-top:auto;display:flex;justify-content:space-between;align-items:center;padding-top:10px}.buy strong{font-size:1.1rem}
.split{display:grid;grid-template-columns:1.2fr 1fr;gap:40px;align-items:center;padding:40px 20px 70px}
@media (max-width:760px){.split{grid-template-columns:1fr}}
.shadow{border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,.15)}
.prose{max-width:780px;padding-bottom:60px}.prose h2{font-size:1.4rem}
.foot{background:var(--cream);border-top:1px solid var(--sand);padding:30px 0;font-size:.9rem;color:var(--gray)}
.foot .legal a{color:var(--ink)}.note{font-size:.8rem}
"""

FAVICON = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#F8F2E9"/>'
           '<text x="14" y="46" font-family="Georgia,serif" font-weight="800" font-size="40" fill="#1F3B4D">f</text>'
           '<path d="M30 44 C40 46 44 40 46 32 S40 22 38 30 S48 44 58 40" fill="none" stroke="#D9734E" stroke-width="3.5" '
           'stroke-linecap="round"/></svg>')


def build():
    if "--catalogue" in sys.argv or "--prix" in sys.argv or not os.path.exists(CAT):
        catalogue()
    items = json.load(open(CAT, encoding="utf-8"))
    os.makedirs(os.path.join(PUB, "en"), exist_ok=True)
    fd = os.path.join(PUB, "fonts")
    os.makedirs(fd, exist_ok=True)
    for f in ("Fraunces-600.ttf", "Fraunces-800.ttf", "Fraunces-500i.ttf", "NunitoSans-400.ttf", "NunitoSans-700.ttf",
              "NunitoSans-800.ttf"):
        shutil.copy(os.path.join(SRC, "fonts", f), fd)
    open(os.path.join(PUB, "style.css"), "w").write(CSS)
    open(os.path.join(PUB, "favicon.svg"), "w").write(FAVICON)
    images(items)
    for lang, d in (("fr", PUB), ("en", os.path.join(PUB, "en"))):
        open(os.path.join(d, "index.html"), "w").write(home(lang))
        open(os.path.join(d, "boutique.html" if lang == "fr" else "shop.html"), "w").write(shop(lang, items))
        open(os.path.join(d, "bottin.html" if lang == "fr" else "directory.html"), "w").write(bottin(lang, items))
    open(os.path.join(PUB, "404.html"), "w").write(page("fr", "index.html", "Page introuvable",
        '<section class="wrap prose"><h1>Page introuvable</h1><p class="lead">Cette page n’existe pas ou a été déplacée. '
        '· This page does not exist.</p><p><a class="btn" href="/">Accueil · Home</a></p></section>').replace('href="index.html"', 'href="/index.html"'))
    for (lang, name), (title, content) in CONTENT.items():
        d = PUB if lang == "fr" else os.path.join(PUB, "en")
        open(os.path.join(d, name), "w").write(textpage(lang, name, title, content))
    print("Site prêt :", PUB)


if __name__ == "__main__":
    build()
