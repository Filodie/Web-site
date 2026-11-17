# -*- coding: utf-8 -*-
"""Bon de commande à remplir (PDF avec champs) pour la licence d’équipe et les achats d’établissement (17 nov. 2026).
Appelé par build_site.py : faire(dossier, prix) écrit Filodie_bon_de_commande.pdf et Filodie_purchase_order.pdf.
prix = {"trousse": 7, "cahier": 3, "collection": 25, "trousses": 75, "tout": 149} (prix courants de la boutique).
Aucun renseignement de paiement ni numéro de taxe : ils figurent sur la facture."""
import os
import sys

import fitz

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "Filodie – Outils T.E.S.", "_source")
sys.path.insert(0, SRC)
from filodie import FONTFILES, FONTS, INK, TERRA, SAGE, CREAM, SAND, RULE, GRAY, W, H  # noqa: E402

M = 40
T = {
    "fr": dict(
        fichier="Filodie_bon_de_commande.pdf", titre="Bon de commande",
        sous="Licence d’équipe et achats d’établissement",
        intro=("Remplissez ce bon à l’écran ou à la main, puis envoyez-le à melodie@filodie.ca. Vous recevez une facture "
               "en PDF au nom de l’établissement. Dès la réception du paiement, les fichiers vous sont envoyés par courriel, "
               "avec la facture marquée « payée »."),
        s1="1. Établissement", s2="2. Produits", s3="3. Paiement et autorisation",
        champs=[("Nom de l’établissement", 1), ("Adresse", 1), ("Ville", .5), ("Code postal", .5),
                ("Personne-ressource", .5), ("Fonction", .5), ("Courriel", .5), ("Téléphone", .5),
                ("N° de bon de commande interne (facultatif)", .5), ("Date", .5)],
        cols=["Produit (titre ou lien filodie.ca)", "Licence", "Prix", "Qté", "Total"],
        aide_licence="Licence : I = individuelle (1 personne), É = équipe (jusqu’à 25 membres du personnel, 3 fois le prix).",
        total="Total", paiement="Mode de paiement souhaité :", modes=["Virement Interac", "Chèque"],
        modes_note="Les coordonnées de paiement figurent sur la facture.",
        autorise="Nom de la personne qui autorise l’achat", signature="Signature",
        prix_t="Prix courants", prix_cols=["Produit", "Individuelle", "Équipe (× 3)"],
        prix_l=[("Une trousse", "trousse"), ("Un cahier visuel", "cahier"), ("Une collection de trousses", "collection"),
                ("Toutes les trousses", "trousses"), ("Tout Filodie", "tout")],
        prix_note=("Les prix de la boutique filodie.ca font foi. Plus de 25 personnes ou plusieurs établissements "
                   "(par exemple un centre de services scolaire) : demandez une soumission."),
        argent=lambda v: f"{v:g} $".replace(".", ","),
        pied="Filodie  |  filodie.ca  |  melodie@filodie.ca  |  Licence d’équipe : filodie.ca/services.html",
        meta="Filodie – Bon de commande"),
    "en": dict(
        fichier="Filodie_purchase_order.pdf", titre="Purchase order",
        sous="Team licence and organization purchases",
        intro=("Fill out this form on screen or by hand, then send it to melodie@filodie.ca. You will receive a PDF invoice "
               "in the organization’s name. As soon as payment is received, the files are sent to you by email, with the "
               "invoice marked “paid”."),
        s1="1. Organization", s2="2. Products", s3="3. Payment and authorization",
        champs=[("Organization name", 1), ("Address", 1), ("City", .5), ("Postal code", .5),
                ("Contact person", .5), ("Position", .5), ("Email", .5), ("Phone", .5),
                ("Internal purchase order no. (optional)", .5), ("Date", .5)],
        cols=["Product (title or filodie.ca link)", "Licence", "Price", "Qty", "Total"],
        aide_licence="Licence: I = individual (1 person), T = team (up to 25 staff members, 3 times the price).",
        total="Total", paiement="Preferred payment method:", modes=["Interac e-Transfer", "Cheque"],
        modes_note="Payment details are shown on the invoice.",
        autorise="Name of the person authorizing the purchase", signature="Signature",
        prix_t="Current prices", prix_cols=["Product", "Individual", "Team (× 3)"],
        prix_l=[("A toolkit", "trousse"), ("A visual workbook", "cahier"), ("A toolkit collection", "collection"),
                ("All the toolkits", "trousses"), ("All of Filodie", "tout")],
        prix_note=("Prices in the filodie.ca shop prevail. More than 25 people or several organizations "
                   "(for example a school service centre): ask for a quote."),
        argent=lambda v: f"${v:g}",
        pied="Filodie  |  filodie.ca  |  melodie@filodie.ca  |  Team licence: filodie.ca/en/services.html",
        meta="Filodie – Purchase Order"),
}


def _polices(p):
    for k in ("F8", "FI", "N4", "N7", "N8"):
        p.insert_font(fontname=k, fontfile=os.path.join(FONTS, FONTFILES[k]))


_F = {k: fitz.Font(fontfile=os.path.join(FONTS, FONTFILES[k])) for k in ("N4", "N7", "N8")}


def _ecrire(p, x, y, txt, police, taille, larg, coul=INK, lh=1.3):
    mots, ligne = txt.split(" "), ""
    for m in mots:
        e = (ligne + " " + m).strip()
        if _F[police].text_length(e, fontsize=taille) > larg and ligne:
            p.insert_text((x, y), ligne, fontname=police, fontsize=taille, color=coul)
            y += taille * lh
            ligne = m
        else:
            ligne = e
    p.insert_text((x, y), ligne, fontname=police, fontsize=taille, color=coul)
    return y + taille * lh


def _champ(p, nom, r, mult=False):
    w = fitz.Widget()
    w.field_type = fitz.PDF_WIDGET_TYPE_TEXT
    w.field_name = nom
    w.rect = r
    w.text_font = "Helv"
    w.text_fontsize = 0 if mult else 9.5
    w.border_width = 0
    w.fill_color = (1, 1, 1)
    if mult:
        w.field_flags = fitz.PDF_TX_FIELD_IS_MULTILINE
    p.add_widget(w)


def _case(p, nom, r):
    w = fitz.Widget()
    w.field_type = fitz.PDF_WIDGET_TYPE_CHECKBOX
    w.field_name = nom
    w.rect = r
    w.border_color = INK
    w.border_width = 0.8
    w.fill_color = (1, 1, 1)
    p.add_widget(w)


def _section(p, y, titre):
    p.insert_text((M, y), titre, fontname="N8", fontsize=12, color=TERRA)
    p.draw_line((M, y + 5), (W - M, y + 5), color=RULE, width=0.8)
    return y + 20


def faire(dossier, prix, langues=("fr", "en")):
    out = []
    for lang in langues:
        t = T[lang]
        doc = fitz.open()
        p = doc.new_page(width=W, height=H)
        _polices(p)
        p.draw_rect(fitz.Rect(0, 0, W, 76), color=None, fill=CREAM)
        p.insert_text((W - M - 78, 44), "filodie", fontname="F8", fontsize=22, color=INK)
        p.insert_text((M, 44), t["titre"], fontname="F8", fontsize=22, color=INK)
        p.insert_text((M, 62), t["sous"], fontname="FI", fontsize=10.5, color=TERRA)
        y = _ecrire(p, M, 96, t["intro"], "N4", 9.2, W - 2 * M)

        # 1. Établissement
        y = _section(p, y + 8, t["s1"])
        larg = W - 2 * M
        col = 0
        for i, (lab, frac) in enumerate(t["champs"]):
            w = larg if frac == 1 else (larg - 12) / 2
            xx = M + col * (w + 12)
            p.insert_text((xx, y + 7), lab, fontname="N7", fontsize=7.6, color=GRAY)
            r = fitz.Rect(xx, y + 10, xx + w, y + 26)
            p.draw_rect(r, color=SAND, width=0.8)
            _champ(p, f"etab_{i}", r)
            if frac == 1 or col == 1:
                y += 28
                col = 0
            else:
                col = 1
        # 2. Produits
        y = _section(p, y + 18, t["s2"])
        cw = [larg - 52 - 60 - 36 - 64, 52, 60, 36, 64]
        xs = [M]
        for c in cw[:-1]:
            xs.append(xs[-1] + c)
        p.draw_rect(fitz.Rect(M, y - 10, W - M, y + 5), color=None, fill=CREAM)
        for xi, c in zip(xs, t["cols"]):
            p.insert_text((xi + 4, y), c, fontname="N8", fontsize=8, color=INK)
        y += 5
        for row in range(7):
            for k, (xi, c) in enumerate(zip(xs, cw)):
                r = fitz.Rect(xi, y, xi + c, y + 19)
                p.draw_rect(r, color=SAND, width=0.7)
                _champ(p, f"prod_{row}_{k}", fitz.Rect(r.x0 + 1, r.y0 + 1, r.x1 - 1, r.y1 - 1))
            y += 19
        r = fitz.Rect(xs[-1], y, W - M, y + 19)
        p.draw_rect(r, color=INK, width=1)
        _champ(p, "total", fitz.Rect(r.x0 + 1, r.y0 + 1, r.x1 - 1, r.y1 - 1))
        tt = t["total"]
        p.insert_text((xs[-1] - 8 - _F["N8"].text_length(tt, fontsize=9.5), y + 13), tt, fontname="N8", fontsize=9.5, color=INK)
        _ecrire(p, M, y + 13, t["aide_licence"], "N4", 7.6, xs[-1] - M - 60, GRAY)
        y += 36

        # 3. Paiement
        y = _section(p, y + 2, t["s3"])
        p.insert_text((M, y + 2), t["paiement"], fontname="N7", fontsize=9, color=INK)
        xx = M + _F["N7"].text_length(t["paiement"], fontsize=9) + 14
        for i, mode in enumerate(t["modes"]):
            _case(p, f"paiement_{i}", fitz.Rect(xx, y - 7, xx + 10, y + 3))
            p.insert_text((xx + 15, y + 2), mode, fontname="N4", fontsize=9, color=INK)
            xx += 15 + _F["N4"].text_length(mode, fontsize=9) + 22
        p.insert_text((M, y + 16), t["modes_note"], fontname="N4", fontsize=7.6, color=GRAY)
        y += 32
        w2 = (larg - 12) / 2
        for i, lab in enumerate((t["autorise"], t["signature"])):
            xx = M + i * (w2 + 12)
            p.insert_text((xx, y), lab, fontname="N7", fontsize=7.6, color=GRAY)
            r = fitz.Rect(xx, y + 3, xx + w2, y + 25)
            p.draw_rect(r, color=SAND, width=0.8)
            _champ(p, f"autorisation_{i}", r)
        y += 40

        # rappel des prix
        r = fitz.Rect(M, y, W - M, y + 112)
        p.draw_rect(r, color=None, fill=CREAM)
        p.draw_rect(fitz.Rect(r.x0, r.y0, r.x0 + 4, r.y1), color=None, fill=SAGE)
        p.insert_text((r.x0 + 16, r.y0 + 18), t["prix_t"].upper(), fontname="N8", fontsize=7.6, color=SAGE)
        yy = r.y0 + 34
        cx = [r.x0 + 16, r.x0 + 250, r.x0 + 360]
        for xi, c in zip(cx, t["prix_cols"]):
            p.insert_text((xi, yy), c, fontname="N8", fontsize=8.6, color=INK)
        for lab, k in t["prix_l"]:
            yy += 12.5
            for xi, v in zip(cx, (lab, t["argent"](prix[k]), t["argent"](prix[k] * 3))):
                p.insert_text((xi, yy), v, fontname="N4", fontsize=8.6, color=INK)
        _ecrire(p, r.x0 + 16, yy + 15, t["prix_note"], "N4", 7.8, r.width - 32, GRAY)
        if r.y1 > H - 40:
            print("  ! bon de commande trop long", lang, round(r.y1))
        p.insert_text((M, H - 24), t["pied"], fontname="N7", fontsize=7.6, color=GRAY)
        doc.set_metadata({"title": t["meta"], "author": "Filodie", "creator": "Filodie"})
        chemin = os.path.join(dossier, t["fichier"])
        os.makedirs(dossier, exist_ok=True)
        doc.save(chemin, garbage=4, deflate=True)
        out.append(chemin)
    return out


if __name__ == "__main__":
    sp = sys.argv[1] if len(sys.argv) > 1 else HERE
    print(faire(sp, {"trousse": 7, "cahier": 3, "collection": 25, "trousses": 75, "tout": 149}))
