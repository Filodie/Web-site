"""Page « Pour les écoles » (ecoles.html / en/schools.html), 26 nov. 2026.

Regroupe ce qui existait déjà ailleurs pour une équipe-école : outils de départ, licence d’équipe,
bon de commande et soumission pour plusieurs écoles. Appelée depuis build_site.build().
Règle Filodie : rester dans le rôle de la T.E.S., rien de hautain, aucune taxe inventée.
"""

FR, EN = "ecoles.html", "schools.html"

DEBUT = ["trousse-pack_rentree_tes_primaire", "trousse-routines_et_organisation_scolaire", "trousse-secondaire_12-17_ans",
         "lot-pictos-porte-cles", "lot-affiches", "trousse-histoires_sociales"]

TXT = {
    "fr": dict(
        titre="Pour les écoles",
        desc="Outils d’intervention pour l’école conçus par une T.E.S. : routines, transitions, pictogrammes et affiches. "
             "Licence d’équipe pour tout le personnel, facture au nom de l’école et bon de commande.",
        lead="Des outils conçus par une T.E.S. pour le quotidien à l’école : routines, transitions, pictogrammes et soutien "
             "aux élèves qui ont besoin d’un peu plus. Toute l’équipe peut les utiliser, avec une seule facture au nom de l’école.",
        recu_t="Ce que votre équipe reçoit",
        recu=["Des PDF prêts à imprimer et à remplir à l’écran, en français et en anglais.",
              "Une version Word modifiable pour la plupart des trousses, pour adapter chaque outil à l’élève et à votre milieu.",
              "Des pictogrammes porte-clés et des affiches pensés pour l’école québécoise.",
              "Des outils qui soutiennent l’intervention, sans remplacer l’évaluation ni le travail des autres "
              "professionnelles et professionnels de l’école."],
        debut_t="Par où commencer",
        equipe_t="Acheter pour toute l’équipe",
        equipe=("Un achat dans la boutique donne une licence individuelle. Pour que plusieurs membres du personnel utilisent "
                "les mêmes outils, choisissez la licence d’équipe : 3 fois le prix individuel, pour jusqu’à 25 personnes "
                "d’un même établissement. Les fichiers peuvent alors être déposés sur le réseau interne de l’école."),
        th=("Produit", "Licence individuelle", "Licence d’équipe"),
        lignes=(("Une trousse", "trousse"), ("Toutes les trousses", "trousses"), ("Tout Filodie", "tout")),
        etapes_t="Comment commander",
        etapes=["Écrivez-moi en indiquant les produits voulus, le nom et l’adresse de l’école, ainsi que la personne-ressource.",
                "Vous recevez une facture en PDF au nom de l’école, payable par virement Interac ou par chèque.",
                "Dès la réception du paiement, vous recevez les fichiers par courriel."],
        bon="Votre service des achats demande un bon de commande ? Remplissez celui-ci à l’écran et joignez-le à votre courriel.",
        b_bon="Télécharger le bon de commande", pdf="/pdf/Filodie_bon_de_commande.pdf",
        b_mail="Demander une facture",
        mail="mailto:melodie@filodie.ca?subject=Licence%20d%E2%80%99%C3%A9quipe%20%C3%A9cole",
        b_det="Détails de la licence d’équipe", det="services.html#licence-equipe",
        plusieurs="Plusieurs écoles ou un centre de services scolaire ? Écrivez-moi pour une soumission.",
        voir_t="Voir aussi",
        voir=[("ecole", "Tous les outils pour l’école et la classe"), ("pictos", "Pictogrammes à imprimer"),
              ("bottin.html", "Bottin gratuit des ressources des 17 régions"), ("coloriage.html", "Cahiers à colorier gratuits")],
    ),
    "en": dict(
        titre="For schools",
        desc="Intervention tools for schools designed by a special care counsellor: routines, transitions, pictograms and "
             "posters. Team licence for all staff, invoice in the school’s name and purchase order.",
        lead="Tools designed by a special care counsellor (SCC) for everyday school life: routines, transitions, pictograms "
             "and support for students who need a little more. Your whole team can use them, with a single invoice in the "
             "school’s name.",
        recu_t="What your team gets",
        recu=["Ready-to-print PDFs, fillable on screen, in English and French.",
              "An editable Word version for most toolkits, to adapt each tool to the student and your setting.",
              "Keychain pictograms and posters designed for Québec schools.",
              "Tools that support intervention, without replacing assessment or the work of the school’s other professionals."],
        debut_t="Where to start",
        equipe_t="Buying for the whole team",
        equipe=("A purchase in the shop gives an individual licence. For several staff members to use the same tools, choose "
                "the team licence: 3 times the individual price, for up to 25 people in the same organization. The files "
                "may then be placed on the school’s internal network."),
        th=("Product", "Individual licence", "Team licence"),
        lignes=(("One toolkit", "trousse"), ("All Toolkits", "trousses"), ("All of Filodie", "tout")),
        etapes_t="How to order",
        etapes=["Email me with the products you want, the school’s name and address, and a contact person.",
                "You receive a PDF invoice in the school’s name, payable by Interac e-Transfer or cheque.",
                "As soon as payment is received, you receive the files by email."],
        bon="Does your purchasing department need a purchase order? Fill this one in on screen and attach it to your email.",
        b_bon="Download the purchase order", pdf="/pdf/Filodie_purchase_order.pdf",
        b_mail="Request an invoice",
        mail="mailto:melodie@filodie.ca?subject=School%20team%20licence",
        b_det="Team licence details", det="services.html#team-licence",
        plusieurs="Several schools or a school service centre? Email me for a quote.",
        voir_t="See also",
        voir=[("ecole", "All school and classroom tools"), ("pictos", "Printable pictograms"),
              ("directory.html", "Free directory of resources in all 17 regions"), ("colouring.html", "Free colouring books")],
    ),
}


def corps(lang, tous, carte, eq, prix, sujets):
    """HTML de la page. carte = build_site.carte_produit, eq = build_site._eq, prix = PRIX_EQ, sujets = SUJETS."""
    t, fr = TXT[lang], lang == "fr"
    recu = "".join(f"<li>{x}</li>" for x in t["recu"])
    cartes = "".join(carte(lang, tous[k]) for k in DEBUT if k in tous)
    lignes = "".join(f"<tr><td>{n}</td><td>{eq(prix[k], fr)}</td><td>{eq(prix[k] * 3, fr)}</td></tr>" for n, k in t["lignes"])
    etapes = "".join(f"<li>{x}</li>" for x in t["etapes"])
    voir = " · ".join(f'<a href="{sujets[k][lang] if k in sujets else k}">{l}</a>' for k, l in t["voir"])
    return (f'<section class="wrap prose"><h1>{t["titre"]}</h1><p class="lead">{t["lead"]}</p>'
            f'<h2>{t["recu_t"]}</h2><ul>{recu}</ul></section>'
            f'<section class="band"><div class="wrap"><h2>{t["debut_t"]}</h2><div class="grid3">{cartes}</div></div></section>'
            f'<section class="wrap prose"><h2>{t["equipe_t"]}</h2><p>{t["equipe"]}</p>'
            f'<table class="tbl"><thead><tr>{"".join(f"<th>{h}</th>" for h in t["th"])}</tr></thead><tbody>{lignes}</tbody></table>'
            f'<h3>{t["etapes_t"]}</h3><ol>{etapes}</ol><p>{t["bon"]}</p>'
            f'<p class="ctas"><a class="btn" href="{t["mail"]}">{t["b_mail"]}</a> '
            f'<a class="btn ghost" href="{t["pdf"]}" download>{t["b_bon"]}</a> '
            f'<a class="btn ghost" href="{t["det"]}">{t["b_det"]}</a></p>'
            f'<p class="muted">{t["plusieurs"]}</p>'
            f'<h2>{t["voir_t"]}</h2><p>{voir}</p></section>')
