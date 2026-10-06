# -*- coding: utf-8 -*-
"""Articles « Conseils » de filodie.ca (FR + EN), lus par build_site.py.
Chaque article : slug FR/EN, titre, description (balise meta, ≤ 160 car.), date, temps de lecture,
corps HTML et produits liés (id de produits.json, affichés en cartes avec bouton d'achat).
Rédaction inclusive : épicène d'abord, sinon doublet féminin-masculin, jamais de point médian.
Ressources : Info-Social 811 option 2 (pas le 988)."""

ARTICLES = [
    dict(
        fr="conseil-routine-visuelle-matin.html",
        en="tip-morning-visual-routine.html",
        date="2026-10-06",
        minutes=5,
        produits=["routines-rtn-a", "lot-routines", "routines-rtn-b"],
        titre_fr="Routine visuelle du matin : la créer et l’utiliser avec un enfant",
        titre_en="Morning visual routine: how to create one and use it with a child",
        desc_fr="Comment créer une routine visuelle du matin qui fonctionne vraiment : étapes, nombre d’images, "
                "erreurs fréquentes et façon de l’introduire avec l’enfant.",
        desc_en="How to build a morning visual routine that actually works: steps, how many pictures, common "
                "mistakes and how to introduce it to the child.",
        corps_fr="""
<p class="lead">Les matins sont souvent le moment le plus tendu de la journée : peu de temps, beaucoup d’étapes
et des consignes répétées dix fois. Une routine visuelle transforme ces consignes orales en repères que l’enfant
peut consulter seul, à son rythme.</p>

<h2>Pourquoi une routine en images aide autant</h2>
<p>Une consigne orale disparaît dès qu’elle est dite. Une image, elle, reste là. Pour un enfant qui a de la
difficulté à retenir une suite d’étapes, à gérer les transitions ou à traiter l’information entendue, cette
permanence change tout. C’est particulièrement vrai chez les enfants autistes, chez ceux qui ont un TDAH et
chez les tout-petits, mais la plupart des enfants en profitent.</p>
<p>La routine visuelle rend aussi la journée prévisible. Savoir ce qui vient ensuite diminue l’anxiété et les
négociations. L’adulte n’a plus à répéter : il ou elle peut simplement pointer l’image.</p>

<h2>Créer la routine en 5 étapes</h2>
<ol>
<li><strong>Observez un vrai matin.</strong> Notez les étapes telles qu’elles se passent réellement, dans
l’ordre, et repérez celles qui bloquent.</li>
<li><strong>Gardez de 4 à 7 étapes.</strong> Au-delà, la routine devient difficile à suivre. Regroupez si
nécessaire : « s’habiller » peut devenir une seule image au début.</li>
<li><strong>Une image, une action.</strong> Choisissez des images claires, toujours les mêmes, accompagnées
d’un mot court. Évitez les images qui montrent plusieurs choses à la fois.</li>
<li><strong>Placez-la au bon endroit.</strong> À la hauteur des yeux de l’enfant, là où les étapes se
passent : la salle de bain, la chambre ou près de la porte.</li>
<li><strong>Ajoutez une façon de cocher.</strong> Retourner l’image, la déplacer dans une enveloppe « fini »
ou la cocher donne un sentiment d’accomplissement concret.</li>
</ol>

<h2>L’introduire avec l’enfant</h2>
<p>Présentez la routine à un moment calme, pas en pleine course du matin. Faites-la ensemble les premiers
jours : l’adulte montre l’image, l’enfant fait l’étape, puis on passe à la suivante. Diminuez ensuite
graduellement votre aide jusqu’à ce que l’enfant consulte la routine seul. Soulignez les réussites, même
partielles : « Tu as regardé ta routine sans que je te le dise ! »</p>

<h2>Les erreurs fréquentes</h2>
<ul>
<li><strong>Trop d’étapes dès le départ.</strong> Mieux vaut commencer petit et ajouter ensuite.</li>
<li><strong>Changer les images souvent.</strong> La stabilité fait la force de l’outil.</li>
<li><strong>L’utiliser comme punition.</strong> La routine est un soutien, pas une liste de reproches.</li>
<li><strong>L’abandonner trop vite.</strong> Comptez deux à trois semaines avant de juger de son efficacité.</li>
</ul>

<div class="astuce"><strong>Repère pour l’adulte</strong><p>Si un matin se passe mal, ce n’est pas un échec de
la routine. Notez l’étape qui a bloqué : c’est souvent elle qu’il faut découper en plus petites actions.</p></div>
""",
        corps_en="""
<p class="lead">Mornings are often the most stressful part of the day: little time, lots of steps and
instructions repeated ten times over. A visual routine turns those spoken instructions into cues the child
can check on their own, at their own pace.</p>

<h2>Why a picture routine helps so much</h2>
<p>A spoken instruction is gone the moment it is said. A picture stays. For a child who struggles to remember
a sequence of steps, to handle transitions or to process what they hear, that permanence changes everything.
This is especially true for autistic children, children with ADHD and young children, but most children
benefit.</p>
<p>A visual routine also makes the day predictable. Knowing what comes next reduces anxiety and negotiation.
The adult no longer has to repeat themselves: they can simply point to the picture.</p>

<h2>Building the routine in 5 steps</h2>
<ol>
<li><strong>Observe a real morning.</strong> Write down the steps as they actually happen, in order, and
spot the ones where things get stuck.</li>
<li><strong>Keep it to 4 to 7 steps.</strong> More than that becomes hard to follow. Group steps if needed:
“get dressed” can be a single picture at first.</li>
<li><strong>One picture, one action.</strong> Use clear pictures, always the same ones, with a short word.
Avoid pictures that show several things at once.</li>
<li><strong>Put it in the right place.</strong> At the child’s eye level, where the steps happen: the
bathroom, the bedroom or near the door.</li>
<li><strong>Add a way to check off.</strong> Flipping the picture, moving it to a “done” envelope or ticking
it off gives a concrete sense of accomplishment.</li>
</ol>

<h2>Introducing it to the child</h2>
<p>Present the routine at a calm moment, not in the middle of the morning rush. Do it together for the first
few days: the adult shows the picture, the child does the step, then you move on. Then gradually reduce your
help until the child checks the routine on their own. Celebrate successes, even partial ones: “You looked at
your routine without me reminding you!”</p>

<h2>Common mistakes</h2>
<ul>
<li><strong>Too many steps at the start.</strong> Start small and add later.</li>
<li><strong>Changing the pictures often.</strong> Consistency is what makes the tool work.</li>
<li><strong>Using it as a punishment.</strong> The routine is a support, not a list of reproaches.</li>
<li><strong>Giving up too soon.</strong> Allow two to three weeks before judging whether it works.</li>
</ul>

<div class="astuce"><strong>Tip for the adult</strong><p>If a morning goes badly, the routine has not failed.
Note the step where things got stuck: that is often the one to break down into smaller actions.</p></div>
"""),
    dict(
        fr="conseil-enfant-anxieux.html",
        en="tip-anxious-child.html",
        date="2026-10-06",
        minutes=6,
        produits=["detective-din", "affiches-aff-a", "detective-dde"],
        titre_fr="Aider un enfant anxieux : 7 gestes simples au quotidien",
        titre_en="Helping an anxious child: 7 simple everyday steps",
        desc_fr="Sept gestes concrets pour aider un enfant anxieux à la maison, en classe ou en service de garde, "
                "et les signes qui indiquent qu’il est temps de demander de l’aide.",
        desc_en="Seven concrete steps to help an anxious child at home, in class or in daycare, and the signs that "
                "it is time to ask for help.",
        corps_fr="""
<p class="lead">Mal de ventre avant l’école, questions répétées, refus de nouvelles activités : l’anxiété
de l’enfant prend plusieurs formes. On ne peut pas la faire disparaître d’un coup, mais on peut aider l’enfant
à l’apprivoiser, un petit geste à la fois.</p>

<h2>1. Accueillir l’émotion avant de rassurer</h2>
<p>« Il n’y a rien là » part d’une bonne intention, mais l’enfant peut comprendre que ce qu’il ou elle ressent
n’est pas valable. Commencez plutôt par nommer : « Je vois que ça t’inquiète beaucoup. » Une émotion reconnue
redescend plus facilement.</p>

<h2>2. Mettre des mots, et des images, sur l’inquiétude</h2>
<p>Beaucoup d’enfants ne savent pas expliquer ce qui se passe en eux. Un thermomètre de 1 à 5, des images
d’émotions ou un dessin de « l’inquiétude » rendent la chose plus concrète. Plus l’inquiétude est nommée,
moins elle prend de place.</p>

<h2>3. Repérer les signaux du corps</h2>
<p>Ventre noué, cœur qui bat vite, mains moites : aider l’enfant à reconnaître ces signaux lui permet d’agir
plus tôt, avant que l’anxiété monte trop haut.</p>

<h2>4. Pratiquer le calme quand tout va bien</h2>
<p>La respiration lente ou la pause dans le coin calme s’apprennent mieux quand l’enfant est calme. En pleine
crise, on utilise ce qui a été pratiqué. Quelques minutes par jour suffisent.</p>

<h2>5. Rendre la journée prévisible</h2>
<p>Annoncer les changements à l’avance, utiliser un horaire visuel et préparer les nouvelles situations
(une visite, une sortie) réduit l’incertitude, qui nourrit l’anxiété.</p>

<h2>6. Éviter d’éviter</h2>
<p>Éviter tout ce qui fait peur soulage sur le moment, mais l’anxiété grandit ensuite. Mieux vaut avancer
par petites étapes : d’abord regarder la piscine, puis y tremper les pieds, puis entrer dans l’eau, en
soulignant chaque réussite.</p>

<h2>7. Laisser l’enfant devenir l’enquêteur ou l’enquêteuse</h2>
<p>Plutôt que de donner toutes les réponses, posez des questions : « Qu’est-ce qui t’a aidé la dernière
fois ? » L’enfant reste la personne experte de sa propre vie, et ses propres stratégies sont souvent celles
qui fonctionnent le mieux.</p>

<h2>Quand demander de l’aide</h2>
<p>Consultez un ou une professionnelle si l’anxiété dure plusieurs semaines, empêche l’enfant d’aller à
l’école ou de dormir, ou prend beaucoup de place dans la vie familiale. Au Québec, <strong>Info-Social 811,
option 2</strong>, offre une consultation psychosociale 24 heures sur 24, et les jeunes peuvent joindre
<strong>Tel-jeunes</strong> au 1 800 263-2266.</p>
""",
        corps_en="""
<p class="lead">A stomach ache before school, repeated questions, refusing new activities: anxiety in children
takes many forms. It can’t be made to vanish all at once, but we can help the child tame it, one small step at
a time.</p>

<h2>1. Acknowledge the feeling before reassuring</h2>
<p>“It’s no big deal” comes from a good place, but the child may hear that what they feel doesn’t count.
Start by naming it instead: “I can see you’re really worried about this.” A feeling that is acknowledged
settles more easily.</p>

<h2>2. Put words, and pictures, to the worry</h2>
<p>Many children can’t explain what is going on inside them. A 1-to-5 thermometer, feelings pictures or a
drawing of “the worry” make it more concrete. The more the worry is named, the less room it takes up.</p>

<h2>3. Notice the body’s signals</h2>
<p>A knotted stomach, a racing heart, sweaty hands: helping the child recognize these signals lets them act
earlier, before the anxiety climbs too high.</p>

<h2>4. Practise calm when things are going well</h2>
<p>Slow breathing or a break in the calm corner are best learned when the child is calm. In the middle of a
crisis, we use what we have practised. A few minutes a day is enough.</p>

<h2>5. Make the day predictable</h2>
<p>Announcing changes ahead of time, using a visual schedule and preparing for new situations (a visit, an
outing) reduces uncertainty, which feeds anxiety.</p>

<h2>6. Avoid avoiding</h2>
<p>Avoiding everything scary brings relief in the moment, but the anxiety grows afterwards. It’s better to
move forward in small steps: first look at the pool, then dip a toe in, then get into the water, celebrating
each success.</p>

<h2>7. Let the child be the detective</h2>
<p>Instead of giving all the answers, ask questions: “What helped you last time?” The child remains the expert
on their own life, and their own strategies are often the ones that work best.</p>

<h2>When to ask for help</h2>
<p>Consult a professional if the anxiety lasts several weeks, keeps the child from going to school or
sleeping, or takes up a lot of room in family life. In Québec, <strong>Info-Social 811, option 2</strong>,
offers psychosocial support 24 hours a day, and young people can reach <strong>Tel-jeunes</strong> at
1 800 263-2266.</p>
"""),
    dict(
        fr="conseil-colere-enfant.html",
        en="tip-child-anger.html",
        date="2026-10-06",
        minutes=6,
        produits=["detective-dco", "jeux-jeu-c", "affiches-aff-b"],
        titre_fr="Quand la colère déborde : accompagner l’enfant avant, pendant et après",
        titre_en="When anger boils over: supporting a child before, during and after",
        desc_fr="Comment accompagner un enfant en colère avant, pendant et après la crise : prévenir, rester "
                "calme, assurer la sécurité et revenir sur l’événement pour apprendre.",
        desc_en="How to support an angry child before, during and after an outburst: prevent, stay calm, keep "
                "everyone safe and talk it through afterwards to learn.",
        corps_fr="""
<p class="lead">La colère n’est pas un problème en soi : elle signale qu’un besoin n’est pas comblé ou qu’une
limite a été dépassée. Ce qui pose problème, c’est la façon dont elle sort. L’accompagnement se fait en trois
temps, et le plus important se passe… quand tout est calme.</p>

<h2>Avant : prévenir et outiller</h2>
<ul>
<li><strong>Repérer les déclencheurs.</strong> Faim, fatigue, transitions, injustice perçue, bruit : notez
ce qui précède les crises pendant une ou deux semaines. Des tendances apparaissent souvent.</li>
<li><strong>Connaître les signaux d’alerte.</strong> Poings serrés, voix qui monte, agitation : plus on les
repère tôt, plus il est facile d’intervenir.</li>
<li><strong>Bâtir un plan de calme avec l’enfant.</strong> Ce qui l’aide à redescendre (bouger, s’isoler,
respirer, serrer un coussin) se décide à froid, ensemble.</li>
</ul>

<h2>Pendant : sécurité et peu de mots</h2>
<ul>
<li><strong>La sécurité d’abord.</strong> Éloignez les objets dangereux et, au besoin, les autres enfants.</li>
<li><strong>Restez calme, ou faites semblant.</strong> Le ton bas et la posture détendue de l’adulte aident
le système nerveux de l’enfant à se réguler.</li>
<li><strong>Parlez peu.</strong> En pleine crise, le raisonnement ne passe pas. Quelques mots suffisent :
« Je suis là. Tu es en sécurité. On en reparle quand tu seras calme. »</li>
<li><strong>Proposez le plan de calme</strong> sans l’imposer, et attendez.</li>
</ul>

<h2>Après : revenir sur l’événement</h2>
<p>Une fois l’enfant calme, parfois seulement plusieurs heures plus tard, revenez sur ce qui s’est passé, sans
blâme : qu’est-ce qui s’est passé juste avant ? Qu’est-ce que tu ressentais dans ton corps ? Qu’est-ce qui
t’aurait aidé ? Que pourrions-nous essayer la prochaine fois ? C’est dans ce retour que l’enfant apprend
vraiment. Si un geste a blessé quelqu’un, la réparation (un dessin, une aide, un mot) a plus de sens qu’une
punition éloignée du geste.</p>

<div class="astuce"><strong>Repère pour l’adulte</strong><p>Prenez aussi soin de vous. Accompagner la colère
d’un enfant demande beaucoup. Il est normal d’avoir besoin d’une pause avant de revenir sur l’événement.</p></div>

<h2>Quand demander de l’aide</h2>
<p>Si les crises sont fréquentes, intenses ou dangereuses, ou si elles s’accompagnent d’autres difficultés,
parlez-en à un ou une professionnelle. Au Québec, <strong>Info-Social 811, option 2</strong>, peut vous
orienter, 24 heures sur 24.</p>
""",
        corps_en="""
<p class="lead">Anger isn’t a problem in itself: it signals that a need isn’t being met or that a limit has
been crossed. What causes problems is the way it comes out. Support happens in three stages, and the most
important part happens… when everything is calm.</p>

<h2>Before: prevent and equip</h2>
<ul>
<li><strong>Spot the triggers.</strong> Hunger, fatigue, transitions, perceived unfairness, noise: note what
comes before outbursts for a week or two. Patterns often emerge.</li>
<li><strong>Know the warning signs.</strong> Clenched fists, a rising voice, restlessness: the earlier you
spot them, the easier it is to step in.</li>
<li><strong>Build a calm-down plan with the child.</strong> What helps them come back down (moving, being
alone, breathing, squeezing a cushion) is decided together, when things are calm.</li>
</ul>

<h2>During: safety and few words</h2>
<ul>
<li><strong>Safety first.</strong> Move dangerous objects away and, if needed, other children.</li>
<li><strong>Stay calm, or act like it.</strong> The adult’s low voice and relaxed posture help the child’s
nervous system settle.</li>
<li><strong>Say little.</strong> In the middle of an outburst, reasoning doesn’t get through. A few words are
enough: “I’m here. You’re safe. We’ll talk about it when you’re calm.”</li>
<li><strong>Offer the calm-down plan</strong> without forcing it, and wait.</li>
</ul>

<h2>After: talk it through</h2>
<p>Once the child is calm, sometimes only hours later, go back over what happened, without blame: What
happened just before? What did you feel in your body? What would have helped? What could we try next time?
This is where the child really learns. If someone was hurt, making amends (a drawing, a helping hand, a few
words) means more than a punishment far removed from the act.</p>

<div class="astuce"><strong>Tip for the adult</strong><p>Take care of yourself too. Supporting a child’s
anger takes a lot. It’s normal to need a break before talking it through.</p></div>

<h2>When to ask for help</h2>
<p>If outbursts are frequent, intense or dangerous, or come with other difficulties, talk to a professional.
In Québec, <strong>Info-Social 811, option 2</strong>, can point you in the right direction, 24 hours a day.</p>
"""),
]
