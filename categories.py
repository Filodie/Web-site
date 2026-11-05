# -*- coding: utf-8 -*-
"""Catégories du menu Boutique (5 nov. 2026) : un produit peut être dans plusieurs catégories.

Chaque produit reçoit ses catégories selon son groupe (GROUPES), puis selon la liste de chaque catégorie (AJOUTS_CAT).
Au moment de construire le site, build_site.py affiche les produits sans catégorie pour qu’aucun ne soit oublié.
"""

# id, libellé français, libellé anglais, produit affiché en premier
CATEGORIES = [
    ("tsa", "TSA (autisme)", "Autism (ASD)", "trousse-tsa"),
    ("tdah", "TDAH", "ADHD", "trousse-tdah"),
    ("di", "Déficience intellectuelle", "Intellectual disability", "trousse-deficience_intellectuelle"),
    ("langage", "Langage et apprentissage", "Language and learning", "trousse-trouble_du_langage"),
    ("motricite", "Motricité et déficience physique", "Motor skills and physical disability", "trousse-deficience_physique"),
    ("comportement", "Comportement et crise", "Behaviour and crisis", "trousse-troubles_du_comportement"),
    ("sociales", "Habiletés sociales", "Social skills", "trousse-habiletes_sociales"),
    ("emotions", "Émotions et anxiété", "Emotions and anxiety", "trousse-emotions_et_empathie"),
    ("sante", "Santé mentale et dépendances", "Mental health and addictions", "trousse-sante_mentale"),
    ("deuil", "Deuil, trauma et violence", "Grief, trauma and violence", "trousse-soutenir_deuil"),
    ("petite", "Petite enfance", "Early childhood", "trousse-petite_enfance_0-5_ans"),
    ("ecole", "École et classe", "School and classroom", "trousse-enseignants_primaire"),
    ("ados", "Adolescence", "Teens", "trousse-adolescence"),
    ("adultes", "Adultes", "Adults", "trousse-adultes"),
    ("aines", "Personnes aînées", "Older adults", "trousse-aines"),
    ("pa", "Pour les parents", "For parents", "trousse-parents"),
    ("pro", "Professions et pratique", "Professions and practice", "trousse-principale"),
    ("etudes", "Études et stages en T.E.S.", "SCC studies and internships", "lot-etudes-tes"),
]

# Lots généraux : ils contiennent de tout, on les laisse dans le format « Lots » seulement.
SANS_CATEGORIE = {"lot-mega", "lot-toutes-les-trousses", "lot-tous-les-cahiers", "lot-specialisees"}

GROUPES = {
    "Cahiers TSA": ["tsa"], "Cahiers TDAH": ["tdah"], "Cahiers Déficience intellectuelle": ["di"],
    "Cahiers Comportement": ["comportement"], "Cahiers Habiletés sociales": ["sociales"],
    "Études et stages en T.E.S.": ["etudes"], "Accompagner le grand âge": ["aines"], "Vieillir avec dignité": ["aines"],
    "Scolaire": ["ecole"], "Équipe-école et réseau": ["ecole"], "Professions": ["pro"], "Professions et pratique": ["pro"],
    "Boîte à outils en psychoéducation": ["pro"], "Pour enseignantes et enseignants en T.E.S.": ["pro", "etudes"],
    "Enseignement aux adultes": ["adultes"], "Outils d’intervention": ["adultes"], "Traverser l’épreuve": ["adultes"],
    "Albums pour enfants": ["petite"], "Cahiers thématiques": ["petite"], "Après le diagnostic": ["pa"],
}


def _ids(prefixe, *noms):
    return [f"{prefixe}{n}" for n in noms]


def _num(serie, *nums):
    return [f"cahier-{serie}-{n:02d}" for n in nums]


def _t(*noms):
    return _ids("trousse-", *noms)


_HISTOIRES = _num("vsoc", *range(11, 28))
_ROUTINES = _ids("routines-rtn-", *"abcdef") + ["lot-routines"]

AJOUTS_CAT = {
    "tsa": _t("tsa", "diagnostic_tsa", "adultes_autistes", "cerveau_tsa", "formation_tsa", "sexualite_adaptee", "pictogrammes", "histoires_sociales")
           + ["lot-cahiers-tsa", "affiches-aff-e"] + _ROUTINES + _HISTOIRES + _num("vsoc", 4, 6, 7, 8),
    "tdah": _t("tdah", "diagnostic_tdah", "cerveau_tdah", "impulsivite", "routines_et_organisation_scolaire", "procrastination")
            + ["lot-cahiers-tdah", "routines-rtn-d", "affiches-aff-e"] + _num("vsoc", 2, 19),
    "di": _t("deficience_intellectuelle", "diagnostic_di", "dims", "cerveau_di", "sexualite_adaptee", "integration_socioprofessionnelle",
             "readaptation_foyer", "pictogrammes", "budget")
          + ["lot-cahiers-déficience-intellectuelle"] + _ROUTINES,
    "langage": _t("trouble_du_langage", "diagnostic_tdl", "cerveau_tdl", "soutien_langagier_primaire", "soutien_langagier_secondaire",
                  "troubles_apprentissage", "apprentissage-langage", "orthopedagogie", "orthophonie", "hpi", "dyspraxie_tdc",
                  "francais_1re_annee", "francais_2e_annee", "francais_3e_annee", "francais_4e_annee", "francais_5e_annee",
                  "francais_6e_annee", "mathematiques_5e_annee")
               + ["lot-7-scolaire"] + _num("vtsa", 22, 26),
    "motricite": _t("deficience_physique", "dyspraxie_tdc", "motricite_fine", "parcours_moteur", "ergotherapie",
                    "education_physique_inclusive", "chutes_aines") + _num("vtsa", 23) + _num("vtdah", 33),
    "comportement": _t("troubles_du_comportement", "gestion_de_crise", "observation_des_comportements", "renforcement_r05",
                       "renforcement_r610", "renforcement_r1115", "formation_comportements_defis", "syndrome_gilles_de_la_tourette",
                       "impulsivite", "gestion_de_classe", "readaptation_foyer")
                    + ["lot-cahiers-comportement", "lot-1-habiletés-et-comportement", "lot-2-clientèles-et-interventions",
                       "affiches-aff-a", "jeux-jeu-d"]
                    + _num("vtdah", 2, 6, 12, 16, 28) + _num("vsoc", 18, 19, 25) + _num("vtsa", 3, 5, 28),
    "sociales": _t("habiletes_sociales", "communication_et_cooperation", "histoires_sociales", "conflit")
                + ["lot-cahiers-habiletés-sociales", "lot-1-habiletés-et-comportement", "jeux-jeu-b", "jeux-jeu-d", "jeux-jeu-f",
                   "affiches-aff-c", "detective-dam", "edition-edition_intimidation"]
                + _num("vtsa", 8, 12, 19) + _num("vtdah", 3, 7, 13, 26, 31)
                + _num("vcomp", 6, 9, 11, 14, 16, 18, 19, 20, 21, 22, 25, 28, 29) + _num("vdi", 18, 36),
    "emotions": _t("emotions_et_empathie", "ateliers_emotions", "cerveau_anxiete", "estime_de_soi", "tcc_quotidien")
                + ["edition-edition_anxiete", "jeux-jeu-a", "jeux-jeu-c", "jeux-jeu-e", "affiches-aff-a", "affiches-aff-b", "affiches-aff-f",
                   "detective-dem", "detective-din", "detective-dco", "detective-dfo", "detective-dcb", "detective-dde", "detective-dre",
                   "lot-detective", "lot-jeux", "album-nuage-teo", "album-marmite-lina", "gratuit-mois-2709", "gratuit-mois-2702"]
                + _num("vsoc", 1, 17, 18, 25) + _num("vcomp", 5, 8, 24, 30, 31, 32) + _num("vtdah", 6, 16, 20, 23, 28)
                + _num("vtsa", 10, 17, 28, 34),
    "sante": _t("sante_mentale", "prevention_du_suicide", "dependances", "reduction_mefaits", "alcool_faire_le_point",
                "drogues_reduire_les_mefaits", "jeu_excessif", "troubles_alimentaires", "entretien_motivationnel", "tcc_quotidien",
                "refus_traitement", "demander_aide", "cerveau_anxiete", "ecrans_et_cyberdependance")
             + ["lot-sante-mentale-dependances"] + _num("vcomp", 33, 41),
    "deuil": _t("soutenir_deuil", "deuil_et_separation", "deuil_aines", "fin_de_vie", "approche_sensible_au_trauma", "cerveau_trauma",
                "violence_conjugale", "violence_conjugale_victimes", "auteurs_de_violence", "violence_sexuelle",
                "agression_sexuelle_victimes", "auteurs_infractions_sexuelles", "protection_de_la_jeunesse", "maltraitance_aines")
             + ["lot-12-traverser-l-épreuve", "album-caillou-nilou", "album-pont-zelie", "edition-edition_intimidation"]
             + _num("vtsa", 16),
    "petite": _t("petite_enfance_0-5_ans", "educatrices_cpe", "direction_garderie", "renforcement_r05", "attachement", "motricite_fine",
                 "parcours_moteur", "cahier_a_colorier", "jeux_a_imprimer")
              + ["lot-albums", "lot-6-cahiers-thématiques"] + _num("vcomp", 37),
    "ecole": _t("gestion_de_classe", "routines_et_organisation_scolaire", "soutien_langagier_primaire", "soutien_langagier_secondaire",
                "pack_rentree_tes_primaire", "peh", "service_de_garde_scolaire", "nouveaux_arrivants", "troubles_apprentissage",
                "secondaire_12-17_ans", "orthopedagogie")
             + ["lot-7-scolaire", "lot-9-équipe-école-et-réseau", "affiches-aff-d", "lot-affiches", "edition-edition_transitions",
                "edition-edition_intimidation", "gratuit-mois-2708", "gratuit-mois-2706"]
             + _num("vcomp", 5, 38) + _num("vsoc", 16, 21, 22, 26, 29, 31) + _num("vtdah", 5, 11, 15, 21, 27) + _num("vtsa", 29),
    "ados": _t("secondaire_12-17_ans", "adolescence", "renforcement_r1115", "grossesse_adolescence", "ecrans_et_cyberdependance",
               "enseignants_secondaire", "soutien_langagier_secondaire", "orientation", "troubles_alimentaires")
            + ["edition-edition_ados", "detective-dnu"] + _num("vtsa", 31) + _num("vsoc", 32),
    "adultes": _t("adultes", "adultes_autistes", "sante_mentale", "integration_socioprofessionnelle", "dependances", "violence_conjugale",
                  "autosoins_intervenants", "proches_aidants", "fga_fp_reussite")
               + ["lot-11-enseignement-aux-adultes"],
    "aines": _t("aines", "chsld_tes_pab", "cerveau_tnc", "proches_aidants")
             + ["lot-13-vieillir-avec-dignité", "lot-15-accompagner-le-grand-âge"],
    "pro": _t("fondements_theoriques", "cadre_legal", "entretien_motivationnel", "animer_groupe", "systemique_famille", "pouvoir_agir",
              "securite_travail", "autosoins_intervenants", "supervision_stagiaires", "principale", "guide_accompagnement_tes",
              "cahier_videos", "trousse_decouverte", "evaluation_globale_du_jeune", "cerveau_developpement")
           + ["grand-livre", "livre-glossaire-clinique", "bottin-regional", "lot-3-professions", "lot-4-professions-et-pratique",
              "lot-10-boîte-à-outils-du-psychoéducateur", "lot-14-le-cerveau-expliqué", "lot-5-jeux-et-activités",
              "lot-8-thèmes-complémentaires"] + _num("vcomp", 35, 36),
    "pa": ["lot-16-après-le-diagnostic"],
    "etudes": _t("modele_pph") + ["grand-livre", "livre-glossaire-clinique", "lot-etudes-tes"],
}

_PAR_ID = {}
for _c, _liste in AJOUTS_CAT.items():
    for _i in _liste:
        _PAR_ID.setdefault(_i, []).append(_c)


def categories_de(item, parents=False):
    """Liste des catégories d’un produit, dans l’ordre du menu."""
    trouve = set(GROUPES.get(item["groupe"], [])) | set(_PAR_ID.get(item["id"], []))
    if parents:
        trouve.add("pa")
    return [c[0] for c in CATEGORIES if c[0] in trouve]


def verifier(items, parents_de):
    """Signale les produits oubliés et les identifiants mal écrits (les outils gratuits à venir ne sont pas encore au catalogue)."""
    ids = {i["id"] for i in items}
    inconnus = sorted(i for i in _PAR_ID if i not in ids and not i.startswith("gratuit-mois-")) + sorted(c[3] for c in CATEGORIES if c[3] not in ids)
    oublies = [i["id"] for i in items if i["id"] not in SANS_CATEGORIE and not categories_de(i, parents_de(i))]
    if inconnus:
        print("⚠️  Catégories : identifiants inconnus :", ", ".join(inconnus))
    if oublies:
        print("⚠️  Catégories : produits sans catégorie :", ", ".join(oublies))
