# Produits retirés de la vente le 20 novembre 2026 (recentrage de Filodie sur le rôle de T.E.S.).
# Rien n'est supprimé : les PDF et les codes Payhip restent dans produits.json et dans les dossiers.
# Les personnes qui ont déjà acheté gardent leur lien de téléchargement.
# Pour remettre un produit en vente, il suffit de retirer son identifiant de cette liste.

RETIRES = {
    # Suicide et automutilation : formation reconnue exigée, règles de communication à respecter
    "trousse-prevention_du_suicide",
    "cahier-vcomp-33",                          # Quand j'ai envie de me faire mal
    # Évaluation : activité réservée à certains ordres professionnels
    "trousse-psychoeducation_evaluation",
    "trousse-evaluation_globale_du_jeune",
    # Outils destinés à d'autres professions
    "trousse-psychoeducation_planification",
    "trousse-psychoeducation_accompagnement",
    "trousse-psychoeducation_pratique",
    "trousse-psychoeducation",
    "trousse-psychoeducation_scolaire",
    "trousse-orthopedagogie",
    "trousse-orthophonie",
    "trousse-travail_social",
    "trousse-travail_social_scolaire",
    "trousse-tts",
    "trousse-criminologie",
    "trousse-soins_infirmiers",
    "trousse-psychologie_scolaire",
    "trousse-ergotherapie",
    "trousse-orientation",
    "trousse-education_physique_inclusive",
    "trousse-zootherapie",
    "trousse-direction_garderie",
    "trousse-equipe_ecole",
    "trousse-supervision_stagiaires",
    "trousse-service_de_garde_scolaire",        # personnel éducateur en service de garde
    "trousse-educatrices_cpe",                  # personnel éducateur en CPE
    "trousse-chsld_tes_pab",                    # vise aussi les PAB
    "trousse-travail_de_rue",
    "trousse-peh",                              # préposées et préposés aux élèves handicapés
    "trousse-gestion_de_classe",                # rôle du personnel enseignant
    "trousse-tcc_quotidien",                    # TCC : relève de la psychothérapie
    # Personnel enseignant et matières scolaires
    "trousse-enseignants_primaire",
    "trousse-enseignants_secondaire",
    "trousse-adaptation_scolaire",
    "trousse-suppleance",
    "trousse-enseigner_aux_adultes",
    "trousse-fga_fp_reussite",
    "trousse-francais_1re_annee",
    "trousse-francais_2e_annee",
    "trousse-francais_3e_annee",
    "trousse-francais_4e_annee",
    "trousse-francais_5e_annee",
    "trousse-francais_6e_annee",
    "trousse-mathematiques_5e_annee",
    # Trousses pour le personnel enseignant du cégep
    "trousse-enseignants-tes",
    "trousse-apprentissage-langage",
    # Outils limites retirés par prudence (20 nov. 2026)
    "trousse-pratique_privee",
    "trousse-formation_tsa",
    "trousse-formation_comportements_defis",
    "trousse-auteurs_de_violence",              # Hommes ayant des comportements violents
    "trousse-auteurs_infractions_sexuelles",
    "lot-4-professions-et-pratique",           # ne contiendrait plus que 2 trousses
    # Lots dont il ne resterait presque rien
    "lot-9-équipe-école-et-réseau",
    "lot-3-professions",
    # 21 nov. 2026 : retrait par prudence de tout ce qui pourrait dépasser le cadre de la T.E.S.
    # (travail d'une autre profession, évaluation ou dépistage, médical, juridique, thérapie)
    "trousse-troubles_apprentissage",          # Troubles d’apprentissage
    "trousse-trouble_du_langage",              # Trouble développemental du langage
    "trousse-dyspraxie_tdc",                   # Dyspraxie – TDC
    "trousse-soutien_langagier_primaire",      # Soutien langagier au primaire
    "trousse-soutien_langagier_secondaire",    # Soutien langagier au secondaire
    "trousse-motricite_fine",                  # Motricité fine
    "trousse-parcours_moteur",                 # Parcours moteur
    "trousse-stimulation_aines",               # Stimuler la cognition avec plaisir
    "trousse-chutes_aines",                    # Prévenir les chutes et garder confiance
    "trousse-sante_mentale",                   # Santé mentale : troubles courants chez l’adulte
    "trousse-perinatalite",                    # Santé mentale périnatale : prendre soin des parents
    "trousse-troubles_alimentaires",           # Troubles alimentaires : repérer et soutenir
    "trousse-troubles_neurocognitifs",         # Troubles neurocognitifs : accompagner la personne
    "trousse-cerveau_developpement",           # Le cerveau, de la naissance à la vieillesse
    "trousse-cerveau_tsa",                     # Le cerveau et l’autisme
    "trousse-cerveau_tdah",                    # Le cerveau et le TDAH
    "trousse-cerveau_di",                      # Le cerveau et la déficience intellectuelle
    "trousse-cerveau_tdl",                     # Le cerveau et le trouble développemental du langage
    "trousse-cerveau_trauma",                  # Le cerveau et le trauma
    "trousse-cerveau_anxiete",                 # Le cerveau et l’anxiété
    "trousse-cerveau_tnc",                     # Le cerveau et les troubles neurocognitifs
    "lot-14-le-cerveau-expliqué",              # Collection Filodie : Le cerveau expliqué
    "trousse-diagnostic_tsa",                  # Après le diagnostic de TSA
    "trousse-diagnostic_tdah",                 # Après le diagnostic de TDAH
    "trousse-diagnostic_di",                   # Après le diagnostic de déficience intellectuelle
    "trousse-diagnostic_tdl",                  # Après le diagnostic de TDL
    "lot-16-après-le-diagnostic",              # Collection Filodie : Après le diagnostic
    "trousse-refus_traitement",                # Quand la personne refuse un traitement
    "trousse-grossesse_adolescence",           # Grossesse à l’adolescence : mes options
    "trousse-fin_de_vie",                      # Accompagner la fin de vie
    "trousse-cadre_legal",                     # Cadre légal en intervention
    "trousse-protection_de_la_jeunesse",       # Protection de la jeunesse (DPJ)
    "trousse-maltraitance_aines",              # Maltraitance envers les personnes aînées
    "trousse-conduite_aines",                  # Conduire en vieillissant
    "trousse-alcool_faire_le_point",           # Alcool : faire le point
    "trousse-jeu_excessif",                    # Jeu excessif : reprendre le contrôle
    "trousse-drogues_reduire_les_mefaits",     # Drogues : s’informer, réduire les méfaits
    "trousse-violence_conjugale",              # Violence conjugale
    "trousse-violence_conjugale_victimes",     # Violence conjugale : reprendre le pouvoir
    "trousse-agression_sexuelle_victimes",     # Agression sexuelle : se reconstruire
    "trousse-violence_sexuelle",               # Violence sexuelle
    "trousse-sexualite_adaptee",               # Sexualité et relations saines (DI et TSA)
    "trousse-intimite_aines",                  # Intimité et sexualité des personnes aînées
    "lot-12-traverser-l-épreuve",              # Collection Filodie : Traverser l’épreuve
    "lot-15-accompagner-le-grand-âge",         # Collection Filodie : Accompagner le grand âge
}


def retirer(items):
    """Enlève les produits retirés du catalogue et de tous les lots.
    Un lot qui ne contient plus aucun produit en vente est retiré lui aussi."""
    garde = [i for i in items if i["id"] not in RETIRES]
    for i in garde:
        if i.get("contient"):
            i["contient"] = [c for c in i["contient"] if c not in RETIRES]
    return [i for i in garde if not (i["type"].startswith("lot") or i["type"] == "mega") or i.get("contient")]
