# -*- coding: utf-8 -*-
"""Activer ou désactiver le code promo affiché sur filodie.ca.

Le code lui-même se crée dans Payhip (Marketing → Coupons) : c’est Payhip qui applique le rabais au paiement.
Ce script affiche seulement la bannière sur le site, puis reconstruit le site.

    python3 promo.py activer RENTREE15 15%                      → 15 % de rabais, sans date de fin
    python3 promo.py activer RENTREE15 15% --fin 2026-10-15     → la bannière disparaît seule après le 15 octobre
    python3 promo.py activer BIENVENUE 5$ --debut 2026-11-01 --fin 2026-11-30
    python3 promo.py activer NOEL 20% --message "Rabais des fêtes : 20 % avec le code" --message-en "Holiday sale: 20% off with code"
    python3 promo.py desactiver
    python3 promo.py statut
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
PROMO = os.path.join(HERE, "promo.json")
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre",
        "décembre"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",
          "December"]


def lire():
    if os.path.exists(PROMO):
        return json.load(open(PROMO, encoding="utf-8"))
    return {"actif": False}


def ecrire(p):
    json.dump(p, open(PROMO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def jour(s):
    try:
        return date.fromisoformat(s)
    except ValueError:
        sys.exit(f"Date invalide : {s} (format attendu : AAAA-MM-JJ, par exemple 2026-10-15)")


def rabais(s):
    """« 15% », « 15 », « 5$ » → (texte français, texte anglais)."""
    m = re.fullmatch(r"\s*(\d+(?:[.,]\d+)?)\s*(%|\$)?\s*", s)
    if not m:
        sys.exit(f"Rabais invalide : {s} (exemples : 15%  ou  5$)")
    n, u = m.group(1).replace(".", ","), m.group(2) or "%"
    return (f"{n} %", f"{n.replace(',', '.')}%") if u == "%" else (f"{n} $", f"${n.replace(',', '.')}")


def construire(msg="Code promo"):
    """Reconstruit le site et le met en ligne (publier.py), ou seulement localement si GitHub n’est pas relié."""
    subprocess.run([sys.executable, os.path.join(HERE, "publier.py"), msg], check=True)


def main():
    ap = argparse.ArgumentParser(description="Code promo de filodie.ca")
    sub = ap.add_subparsers(dest="action", required=True)
    a = sub.add_parser("activer")
    a.add_argument("code")
    a.add_argument("rabais", help="15%% ou 5$")
    a.add_argument("--debut", default="")
    a.add_argument("--fin", default="")
    a.add_argument("--message", default="", help="texte français affiché avant le code")
    a.add_argument("--message-en", default="", help="texte anglais affiché avant le code")
    sub.add_parser("desactiver")
    sub.add_parser("statut")
    o = ap.parse_args()

    if o.action == "statut":
        p = lire()
        if not p.get("actif"):
            print("Aucun code promo affiché sur le site.")
        else:
            print(f"Code affiché : {p['code']} ({p['rabais_fr']})",
                  f"du {p['debut']}" if p.get("debut") else "", f"jusqu’au {p['fin']}" if p.get("fin") else "sans date de fin")
            print("FR :", p["message_fr"], p["code"])
            print("EN :", p["message_en"], p["code"])
        return

    if o.action == "desactiver":
        p = lire()
        p["actif"] = False
        ecrire(p)
        construire("Code promo retiré")
        print("Bannière retirée du site. Pensez aussi à désactiver ou supprimer le coupon dans Payhip.")
        return

    code = o.code.strip().upper()
    if not re.fullmatch(r"[A-Z0-9_-]{3,30}", code):
        sys.exit("Le code doit contenir de 3 à 30 lettres, chiffres, tirets ou traits de soulignement, sans espace ni accent.")
    fr, en = rabais(o.rabais)
    fin = debut = ""
    if o.debut:
        debut = jour(o.debut).isoformat()
    if o.fin:
        d = jour(o.fin)
        if d < date.today():
            sys.exit("La date de fin est déjà passée.")
        fin = d.isoformat()
    jusqu_fr = f" jusqu’au {d.day}{'er' if d.day == 1 else ''} {MOIS[d.month - 1]}" if fin else ""
    until_en = f" until {MONTHS[d.month - 1]} {d.day}" if fin else ""
    p = {"actif": True, "code": code, "rabais_fr": fr, "rabais_en": en, "debut": debut, "fin": fin,
         "message_fr": o.message or f"{fr} de rabais sur toute la boutique{jusqu_fr} avec le code",
         "message_en": o.message_en or f"{en} off the whole shop{until_en} with code"}
    ecrire(p)
    construire(f"Code promo {code} activé")
    print(f"Bannière activée : {p['message_fr']} {code}")
    print("Important : le même code doit exister dans Payhip (Marketing → Coupons), sinon il sera refusé au paiement.")


if __name__ == "__main__":
    main()
