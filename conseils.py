# -*- coding: utf-8 -*-
"""Articles « Conseils » de filodie.ca (FR + EN), lus par build_site.py.
Chaque article : slug FR/EN, titre, description (balise meta, ≤ 160 car.), date, temps de lecture,
corps HTML et produits liés (id de produits.json, affichés en cartes avec bouton d'achat).
Rédaction inclusive : épicène d'abord, sinon doublet féminin-masculin, jamais de point médian.
Ressources : Info-Social 811 option 2 (pas le 988)."""

ARTICLES = [
    dict(
        fr="conseil-halloween-enfant-sensible.html",
        en="tip-halloween-sensitive-child.html",
        date="2026-10-06",
        minutes=5,
        produits=["gratuit-mois-2610", "cahier-vsoc-06", "cahier-vtsa-33"],
        titre_fr="Halloween avec un enfant autiste ou sensible : 8 idées pour une soirée plus calme",
        titre_en="Halloween with an autistic or sensitive child: 8 ideas for a calmer evening",
        desc_fr="Costumes, bruit, noirceur, bonbons : huit idées concrètes pour préparer un enfant autiste, "
                "anxieux ou sensible à l’Halloween et vivre une soirée plus douce.",
        desc_en="Costumes, noise, darkness, candy: eight practical ideas to prepare an autistic, anxious or "
                "sensitive child for Halloween and enjoy a gentler evening.",
        corps_fr="""
<p class="lead">Pour bien des enfants, l’Halloween est une fête attendue toute l’année. Pour d’autres, c’est une
soirée remplie de surprises : des visages masqués, des cris, des lumières qui clignotent, une routine bousculée
et beaucoup de sucre. Avec un peu de préparation, la fête peut redevenir un plaisir.</p>

<h2>Pourquoi l’Halloween peut être difficile</h2>
<p>Tout ce qui fait le charme de l’Halloween est aussi ce qui peut surcharger un enfant : la nouveauté,
l’imprévisibilité, les stimulations sensorielles et le changement d’horaire. Un enfant autiste, anxieux, qui a
un TDAH ou simplement très sensible peut vite se sentir dépassé. Ce n’est pas un caprice : son système nerveux
reçoit plus d’information qu’il ne peut en traiter.</p>

<h2>Avant la soirée</h2>
<ol>
<li><strong>Racontez la soirée à l’avance.</strong> Une courte histoire en images ou une routine visuelle
montre ce qui va se passer, dans l’ordre : se costumer, sortir, sonner, dire « Joyeuse Halloween », revenir.</li>
<li><strong>Essayez le costume plusieurs fois.</strong> Un costume qui gratte, serre ou cache la vue peut tout
faire basculer. Le confort passe avant l’effet. Un chandail thématique ou un simple accessoire suffit.</li>
<li><strong>Montrez des décorations et des costumes.</strong> Regarder des photos ou se promener de jour dans
le quartier décoré enlève une partie de la surprise.</li>
<li><strong>Décidez ensemble du parcours.</strong> Combien de maisons ? Quelle rue ? Un nombre précis rend la
fin prévisible : « On fait 10 maisons, puis on rentre. »</li>
</ol>

<h2>Pendant la soirée</h2>
<ol start="5">
<li><strong>Prévoyez une trousse sensorielle.</strong> Coquilles antibruit, lampe de poche, collation connue,
objet réconfortant : de petits outils qui aident l’enfant à rester bien.</li>
<li><strong>Convenez d’un signal « c’est trop ».</strong> Un mot, un geste ou une carte que l’enfant peut
montrer quand il ou elle a besoin d’une pause ou de rentrer. Respectez-le, même si la tournée n’est pas finie.</li>
<li><strong>Permettez de participer autrement.</strong> Distribuer les bonbons à la porte, observer de la
fenêtre ou faire une petite fête à la maison, c’est aussi célébrer l’Halloween.</li>
</ol>

<h2>Après la soirée</h2>
<ol start="8">
<li><strong>Gardez un retour au calme.</strong> Le bain, le pyjama, une histoire : retrouver la routine
habituelle aide à redescendre. Décidez à l’avance du nombre de bonbons permis ce soir-là pour éviter une
négociation à la fin d’une soirée déjà intense.</li>
</ol>

<div class="astuce"><strong>Repère pour l’adulte</strong><p>Le succès ne se mesure pas au nombre de maisons
visitées. Une soirée courte qui se termine bien vaut mieux qu’une longue tournée qui finit en crise. L’enfant
gardera surtout le souvenir d’avoir été compris.</p></div>
""",
        corps_en="""
<p class="lead">For many children, Halloween is the most anticipated night of the year. For others, it is an
evening full of surprises: masked faces, shrieks, flashing lights, a disrupted routine and a lot of sugar. With a
little preparation, the holiday can become fun again.</p>

<h2>Why Halloween can be hard</h2>
<p>Everything that makes Halloween exciting can also overwhelm a child: novelty, unpredictability, sensory
input and a change in schedule. An autistic child, an anxious child, a child with ADHD or simply a very
sensitive child can quickly feel overloaded. It is not a whim: their nervous system is receiving more
information than it can process.</p>

<h2>Before the evening</h2>
<ol>
<li><strong>Tell the story of the evening ahead of time.</strong> A short picture story or a visual routine
shows what will happen, in order: put on the costume, go out, ring the bell, say “Happy Halloween”, come home.</li>
<li><strong>Try the costume on several times.</strong> A costume that itches, squeezes or blocks vision can
tip everything over. Comfort comes before looks. A themed sweater or a single accessory is enough.</li>
<li><strong>Show decorations and costumes.</strong> Looking at photos or walking around the decorated
neighbourhood in daylight takes away part of the surprise.</li>
<li><strong>Plan the route together.</strong> How many houses? Which street? A precise number makes the end
predictable: “We’ll do 10 houses, then go home.”</li>
</ol>

<h2>During the evening</h2>
<ol start="5">
<li><strong>Pack a sensory kit.</strong> Ear defenders, a flashlight, a familiar snack, a comfort object:
small tools that help the child stay regulated.</li>
<li><strong>Agree on a “too much” signal.</strong> A word, a gesture or a card the child can show when they
need a break or want to go home. Respect it, even if the round isn’t finished.</li>
<li><strong>Allow other ways to take part.</strong> Handing out candy at the door, watching from the window or
having a small party at home is also celebrating Halloween.</li>
</ol>

<h2>After the evening</h2>
<ol start="8">
<li><strong>Keep a wind-down routine.</strong> Bath, pyjamas, a story: returning to the usual routine helps the
child come back down. Decide ahead of time how many candies are allowed that night to avoid negotiating at the
end of an already intense evening.</li>
</ol>

<div class="astuce"><strong>Tip for the adult</strong><p>Success isn’t measured by the number of houses
visited. A short evening that ends well is better than a long round that ends in a meltdown. What the child
will remember most is feeling understood.</p></div>
"""),
    dict(
        fr="conseil-transitions-difficiles.html",
        en="tip-difficult-transitions.html",
        date="2026-10-06",
        minutes=6,
        produits=["routines-rtn-e", "cahier-vtsa-27", "cahier-vsoc-08"],
        titre_fr="Transitions difficiles : aider l’enfant à passer d’une activité à l’autre",
        titre_en="Difficult transitions: helping a child move from one activity to the next",
        desc_fr="Arrêter un jeu, quitter le parc, changer de local : des stratégies simples pour réduire les "
                "crises lors des transitions, à la maison comme en classe.",
        desc_en="Stopping a game, leaving the park, changing rooms: simple strategies to reduce meltdowns during "
                "transitions, at home and in the classroom.",
        corps_fr="""
<p class="lead">« Encore cinq minutes ! » Éteindre la tablette, sortir du bain, ranger les blocs ou quitter le
parc : pour certains enfants, chaque changement d’activité devient une bataille. Les transitions sont l’un des
moments les plus fréquents de désorganisation, et aussi l’un des plus faciles à prévenir.</p>

<h2>Pourquoi les transitions coûtent autant</h2>
<p>Passer d’une activité à l’autre demande plusieurs efforts en même temps : arrêter quelque chose
d’agréable, accepter de ne pas savoir exactement ce qui vient, réorganiser son attention et parfois changer de
lieu. Pour un enfant autiste, un enfant qui a un TDAH ou un enfant anxieux, ces efforts sont plus grands. La
crise n’est pas de l’opposition : c’est souvent le signe que la transition est arrivée trop vite ou de façon
trop floue.</p>

<h2>Annoncer avant d’arrêter</h2>
<ul>
<li><strong>Donnez un avertissement concret.</strong> « Dans 5 minutes, on range » est plus clair si on
l’accompagne d’une minuterie visuelle que l’enfant peut regarder.</li>
<li><strong>Utilisez un repère de fin.</strong> « Encore deux glissades », « à la fin de la chanson » : une fin
que l’enfant peut voir ou compter est plus facile à accepter qu’une heure abstraite.</li>
<li><strong>Montrez ce qui vient après.</strong> Un horaire visuel ou une carte « d’abord… ensuite… »
répond à la question que l’enfant se pose : qu’est-ce qui m’attend ?</li>
</ul>

<h2>Rendre le passage plus doux</h2>
<ul>
<li><strong>Prévoyez un objet de transition.</strong> Apporter une petite figurine du jeu jusqu’à la table, ou
tenir l’horaire, donne quelque chose de concret à faire pendant le changement.</li>
<li><strong>Offrez un choix limité.</strong> « Tu veux marcher comme un pingouin ou comme un lapin jusqu’à la
salle de bain ? » Le changement n’est pas négociable, mais la façon de le vivre peut l’être.</li>
<li><strong>Gardez une séquence stable.</strong> Les transitions qui reviennent chaque jour (le départ pour
l’école, la fin de la récréation) gagnent à toujours se faire de la même façon.</li>
</ul>

<h2>Quand l’imprévu arrive</h2>
<p>Certains changements ne peuvent pas être annoncés. Pour s’y préparer, on peut enseigner l’idée de
l’imprévu à un moment calme : une carte « surprise » dans l’horaire, une courte histoire sociale, ou un
plan B déjà convenu. L’enfant apprend ainsi qu’un changement de programme n’est pas une catastrophe.</p>

<div class="astuce"><strong>Repère pour l’adulte</strong><p>Observez quelles transitions bloquent le plus et
à quel moment de la journée. Souvent, ce ne sont pas toutes les transitions qui posent problème, mais celles qui
arrivent quand l’enfant est déjà fatigué ou qui interrompent une activité très aimée.</p></div>
""",
        corps_en="""
<p class="lead">“Five more minutes!” Turning off the tablet, getting out of the bath, putting away the blocks
or leaving the park: for some children, every change of activity becomes a battle. Transitions are one of the
most common moments for a child to fall apart, and also one of the easiest to prevent.</p>

<h2>Why transitions are so hard</h2>
<p>Moving from one activity to another takes several efforts at once: stopping something enjoyable, accepting
not knowing exactly what comes next, shifting attention and sometimes changing places. For an autistic child,
a child with ADHD or an anxious child, these efforts are greater. The meltdown isn’t defiance: it is often a
sign that the transition came too fast or was too unclear.</p>

<h2>Announce before you stop</h2>
<ul>
<li><strong>Give a concrete warning.</strong> “In 5 minutes, we’ll tidy up” is clearer with a visual timer the
child can look at.</li>
<li><strong>Use a visible end point.</strong> “Two more slides”, “at the end of the song”: an ending the child
can see or count is easier to accept than an abstract time.</li>
<li><strong>Show what comes next.</strong> A visual schedule or a “first… then…” card answers the question
the child is asking: what’s waiting for me?</li>
</ul>

<h2>Make the change gentler</h2>
<ul>
<li><strong>Offer a transition object.</strong> Carrying a small figure from the game to the table, or holding
the schedule, gives the child something concrete to do during the change.</li>
<li><strong>Offer a limited choice.</strong> “Do you want to walk like a penguin or hop like a bunny to the
bathroom?” The change isn’t negotiable, but how to live it can be.</li>
<li><strong>Keep a stable sequence.</strong> Daily transitions (leaving for school, the end of recess) work
better when they always happen the same way.</li>
</ul>

<h2>When the unexpected happens</h2>
<p>Some changes can’t be announced. To prepare, you can teach the idea of the unexpected at a calm moment: a
“surprise” card in the schedule, a short social story, or a plan B agreed on ahead of time. The child learns
that a change of plan is not a disaster.</p>

<div class="astuce"><strong>Tip for the adult</strong><p>Notice which transitions are hardest and at what time
of day. Often it isn’t every transition that causes trouble, but the ones that happen when the child is already
tired or that interrupt a much-loved activity.</p></div>
"""),
    dict(
        fr="conseil-renforcement-positif.html",
        en="tip-positive-reinforcement.html",
        date="2026-10-06",
        minutes=6,
        produits=["trousse-renforcement_r610", "trousse-gestion_de_classe", "cahier-vtdah-19"],
        titre_fr="Renforcement positif : bien l’utiliser à la maison et en classe",
        titre_en="Positive reinforcement: using it well at home and in the classroom",
        desc_fr="Éloges précis, points, récompenses : utiliser le renforcement positif sans surenchère, avec des "
                "exemples concrets pour les 6 à 12 ans.",
        desc_en="Specific praise, point charts, rewards: how to use positive reinforcement without escalating, "
                "with concrete examples for children ages 6 to 12.",
        corps_fr="""
<p class="lead">On remarque vite ce qui ne va pas : le cri, le coup, la consigne ignorée. Ce qui va bien passe
souvent inaperçu. Le renforcement positif inverse cette tendance : il consiste à remarquer et à souligner les
comportements qu’on souhaite voir revenir. Bien utilisé, c’est l’un des outils les plus efficaces en
intervention.</p>

<h2>Ce que c’est, et ce que ce n’est pas</h2>
<p>Renforcer, c’est faire suivre un comportement de quelque chose d’agréable pour que ce comportement se
reproduise. Ce n’est pas acheter la paix, ni promettre un cadeau pour arrêter une crise. Le renforcement arrive
<em>après</em> le comportement souhaité, jamais pour mettre fin à un comportement difficile.</p>

<h2>Commencer par l’éloge précis</h2>
<p>« Bravo ! » fait plaisir, mais n’apprend pas grand-chose. Un éloge précis décrit ce que l’enfant a fait :
« Tu as rangé tes crayons sans que je te le demande. » « Tu as attendu ton tour même si c’était long. » L’enfant
sait exactement quoi refaire. C’est gratuit, rapide et souvent suffisant.</p>

<h2>Utiliser un système de points avec soin</h2>
<ul>
<li><strong>Visez un ou deux comportements à la fois,</strong> formulés de façon positive : « je lève la main »
plutôt que « je ne crie pas ».</li>
<li><strong>Rendez la réussite possible dès le départ.</strong> Si l’enfant n’obtient jamais de points, le
système devient une source de découragement.</li>
<li><strong>Choisissez les renforçateurs avec l’enfant.</strong> Du temps avec l’adulte, un privilège, une
responsabilité : ce qui motive un enfant n’en motive pas un autre.</li>
<li><strong>Ne retirez pas les points gagnés.</strong> Ce qui est acquis reste acquis. Retirer des points
transforme l’outil en punition.</li>
</ul>

<h2>Éviter la surenchère</h2>
<p>Un système de récompenses n’a pas à durer toujours. À mesure que le comportement s’installe, espacez les
récompenses matérielles et misez davantage sur l’éloge, la fierté et les privilèges naturels. L’objectif est que
l’enfant trouve peu à peu sa motivation en lui-même ou en elle-même.</p>

<div class="astuce"><strong>Repère pour l’adulte</strong><p>Essayez la règle de 4 pour 1 : quatre interactions
positives pour chaque correction. Ce simple équilibre change souvent le climat de la classe ou de la maison en
quelques jours.</p></div>
""",
        corps_en="""
<p class="lead">We quickly notice what goes wrong: the shout, the hit, the ignored instruction. What goes well
often goes unnoticed. Positive reinforcement flips that habit: it means noticing and highlighting the behaviours
we want to see again. Used well, it is one of the most effective tools in intervention.</p>

<h2>What it is, and what it isn’t</h2>
<p>To reinforce is to follow a behaviour with something pleasant so that the behaviour happens again. It is not
buying peace, or promising a gift to stop a meltdown. Reinforcement comes <em>after</em> the desired behaviour,
never to end a difficult one.</p>

<h2>Start with specific praise</h2>
<p>“Great job!” feels nice but doesn’t teach much. Specific praise describes what the child did: “You put away
your pencils without me asking.” “You waited for your turn even though it was long.” The child knows exactly what
to do again. It is free, quick and often enough.</p>

<h2>Use a point system with care</h2>
<ul>
<li><strong>Target one or two behaviours at a time,</strong> phrased positively: “I raise my hand” rather than
“I don’t shout”.</li>
<li><strong>Make success possible from the start.</strong> If the child never earns points, the system becomes
a source of discouragement.</li>
<li><strong>Choose reinforcers with the child.</strong> Time with the adult, a privilege, a responsibility:
what motivates one child doesn’t motivate another.</li>
<li><strong>Don’t take away points already earned.</strong> What is earned stays earned. Removing points turns
the tool into a punishment.</li>
</ul>

<h2>Avoid escalation</h2>
<p>A reward system doesn’t have to last forever. As the behaviour settles in, space out material rewards and
rely more on praise, pride and natural privileges. The goal is for the child to gradually find their own
motivation.</p>

<div class="astuce"><strong>Tip for the adult</strong><p>Try the 4-to-1 rule: four positive interactions for
every correction. This simple balance often changes the mood of a classroom or a home within a few days.</p></div>
"""),
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
