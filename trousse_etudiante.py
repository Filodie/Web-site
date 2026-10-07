# -*- coding: utf-8 -*-
"""Page de présentation détaillée de la « Trousse de l’étudiante et de l’étudiant en T.E.S. » (lot-etudes-tes),
lue par build_site.py : trousse-etudiante.html / en/student-kit.html.
Chaque entrée : (id du produit inclus, ce qu’il contient FR, ce qu’il contient EN), regroupées par thème."""

FR, EN = "trousse-etudiante.html", "student-kit.html"
LOT, ECH = "lot-etudes-tes", "trousse-decouverte_etudiant_tes"

TITRE = {"fr": "Ce que contient la trousse de l’étudiante et de l’étudiant en T.E.S.",
         "en": "What’s inside the SCC student kit"}
DESC = {"fr": "Les 16 outils de la trousse étudiante Filodie pour réussir ses stages et ses travaux en Techniques "
              "d’éducation spécialisée, en un coup d’œil.",
        "en": "The 16 tools in the Filodie student kit for succeeding in special care counselling internships and "
              "coursework, at a glance."}
LEAD = {"fr": "Seize outils pensés pour les personnes qui étudient en Techniques d’éducation spécialisée : pour "
              "arriver en stage préparée ou préparé, rédiger des travaux solides et faire le pont vers le premier emploi. "
              "Tout est en PDF à imprimer ou à remplir à l’écran, en français et en anglais.",
        "en": "Sixteen tools designed for special care counselling students: to arrive at your internship prepared, "
              "write solid assignments and bridge the gap to your first job. Everything comes as PDFs to print or fill "
              "in on screen, in French and English."}

GROUPES = [
    ("Pour les stages", "For internships", [
        ("trousse-debut_stage", "se préparer avant d’arriver, découvrir le milieu et la clientèle, s’entendre avec la "
         "personne superviseure, faire le bilan de la première semaine.",
         "prepare before you arrive, get to know the setting and the clientele, agree on expectations with your "
         "supervisor, review your first week."),
        ("trousse-journal_stage", "objectifs, situations marquantes, émotions et valeurs, rétroaction, bilans de "
         "mi-stage et final.", "goals, significant situations, emotions and values, feedback, mid-term and final reviews."),
        ("trousse-ethique_stage", "limites de la relation, confidentialité, réseaux sociaux, analyse d’un dilemme.",
         "boundaries in the relationship, confidentiality, social media, working through a dilemma."),
        ("trousse-activite_educative", "objectif, déroulement minuté, matériel, imprévus, évaluation.",
         "objective, timed plan, materials, the unexpected, evaluation."),
    ]),
    ("Pour les travaux et l’intervention", "For coursework and intervention", [
        ("trousse-plan_intervention", "forces et besoins, objectifs observables, moyens, révision.",
         "strengths and needs, observable goals, strategies, review."),
        ("trousse-note_evolutive", "faits ou interprétations, bons mots, structure, exemples.",
         "facts versus interpretations, the right words, structure, examples."),
        ("trousse-modele_pph", "facteurs personnels, environnement, habitudes de vie.",
         "personal factors, environment, life habits."),
        ("trousse-analyser_groupe", "structure, dynamique et rôles, mise en situation avec réponses.",
         "structure, dynamics and roles, a case scenario with answers."),
        ("trousse-etude_de_cas", "portrait, analyse des besoins, hypothèses, présentation.",
         "profile, needs analysis, hypotheses, presentation."),
        ("trousse-ecoute_active", "questions ouvertes, reflet, reformulation, autoévaluation d’un entretien.",
         "open questions, reflecting, paraphrasing, self-assessing an interview."),
    ]),
    ("Pour travailler avec les autres", "For working with others", [
        ("trousse-collaborer_familles", "premier contact, message difficile, rencontre de parents.",
         "first contact, delivering a difficult message, parent meetings."),
        ("trousse-equipe_interdisciplinaire", "rôles des professions, réunions, désaccords constructifs.",
         "professional roles, meetings, constructive disagreement."),
        ("trousse-diversite", "posture interculturelle, chocs culturels, adapter l’intervention.",
         "intercultural stance, culture shock, adapting your intervention."),
        ("trousse-reseau_ressources", "services publics, organismes, lignes d’écoute, diriger une personne.",
         "public services, community organizations, helplines, referring a person."),
    ]),
    ("Pour réussir ses études et la suite", "For succeeding in school and beyond", [
        ("trousse-etudier_efficacement", "planifier la session, pratique de rappel, étude espacée, préparer les examens.",
         "planning the semester, retrieval practice, spaced study, exam preparation."),
        ("trousse-premier_emploi", "portfolio, CV, entrevue, recherche d’emploi.",
         "portfolio, résumé, interview, job search."),
    ]),
]
