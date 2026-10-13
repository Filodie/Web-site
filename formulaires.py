# -*- coding: utf-8 -*-
"""Formulaires du site : boîte à suggestions et demande d’édition personnalisée (logo d’établissement).

Les réponses partent vers un script Google (Apps Script) qui :
  · les ajoute dans la feuille Google « Filodie – Formulaires du site » (un onglet par formulaire) ;
  · envoie un courriel à melodie@filodie.ca ;
  · range le logo reçu dans Google Drive.
Code du script et mode d’emploi : Conceptions Filodie/Formulaires du site/.

L’adresse du script se met dans formulaires.json : {"url": "https://script.google.com/macros/s/…/exec"}.
Tant qu’elle est vide, les formulaires ouvrent un courriel prérempli (rien ne se perd).
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CONF = os.path.join(HERE, "formulaires.json")


def url():
    try:
        return json.load(open(CONF, encoding="utf-8")).get("url", "").strip()
    except (OSError, ValueError):
        return ""


CSS = """
.fform{display:grid;gap:14px;background:var(--card);border:1px solid var(--sand);border-radius:14px;padding:22px;margin:1.4em 0}
.fform label{display:grid;gap:5px;font-weight:700;font-size:.95rem}
.fform .opt{font-weight:400;color:var(--gray);font-size:.85rem}
.fform input,.fform select,.fform textarea{font:inherit;font-weight:400;padding:10px 12px;border-radius:10px;border:1.5px solid var(--sand);background:var(--bg);color:var(--ink);width:100%;box-sizing:border-box}
.fform textarea{min-height:130px;resize:vertical}
.fform input:focus,.fform select:focus,.fform textarea:focus{outline:2px solid var(--terra);outline-offset:1px}
.fform .deux{display:grid;grid-template-columns:1fr 1fr;gap:14px}
@media (max-width:640px){.fform .deux{grid-template-columns:1fr}}
.fform .pot{position:absolute;left:-9999px;width:1px;height:1px;overflow:hidden}
.fform .check{display:flex;gap:8px;align-items:flex-start;font-weight:400}.fform .check input{width:auto;margin-top:4px}
.fform button{justify-self:start;cursor:pointer;font:inherit;font-weight:800}
.fform .etat{margin:0;font-weight:700}.fform .etat.ok{color:var(--sage)}.fform .etat.err{color:var(--terra)}
"""

T = {
    "fr": {
        "envoyer": "Envoyer", "envoi": "Envoi…",
        "merci": "Merci ! Votre message est bien reçu.",
        "erreur": "L’envoi n’a pas fonctionné. Votre logiciel de courriel va s’ouvrir avec le message prérempli.",
        "opt": "(facultatif)",
        "s_type": "Votre suggestion porte sur…",
        "s_types": ["Un nouvel outil à créer", "Une amélioration d’un outil existant", "Une erreur à corriger",
                    "Le site Web ou la boutique", "Autre chose"],
        "s_outil": "Outil ou produit concerné", "s_msg": "Votre suggestion",
        "s_msg_ph": "Décrivez votre idée : pour quel milieu, quel âge, quel besoin…",
        "s_role": "Vous êtes…", "s_roles": ["", "Intervenante ou intervenant (T.E.S. ou autre)", "Enseignante ou enseignant",
                                              "Personnel éducateur (CPE ou service de garde)", "Parent",
                                              "Personne étudiante ou stagiaire", "Gestionnaire", "Autre"],
        "s_nom": "Prénom", "s_courriel": "Courriel, si vous voulez une réponse",
        "s_conf": "Pour protéger la confidentialité, ne nommez aucun enfant ni aucune personne que vous accompagnez.",
        "p_etab": "Nom de l’établissement ou de l’entreprise",
        "p_lignes": "Nomenclature à afficher sur les fichiers",
        "p_lignes_ph": "Ex. : Direction des programmes DI-TSA-DP\nService d’adaptation et de réadaptation",
        "p_contact": "Personne-ressource", "p_courriel": "Courriel", "p_tel": "Téléphone",
        "p_nb": "Nombre de membres du personnel visés",
        "p_produits": "Outils voulus", "p_produits_ph": "Ex. : Trousse TSA, Trousse gestion de crise, toutes les trousses…",
        "p_logo": "Votre logo", "p_logo_aide": "PNG, JPG, SVG ou PDF, 3 Mo maximum. Idéalement sur fond transparent.",
        "p_logo_tard": "Vous pourrez aussi l’envoyer plus tard par courriel.",
        "p_msg": "Précisions",
        "p_ok": "Je confirme que l’établissement est autorisé à utiliser ce logo sur ses documents internes.",
        "trop_gros": "Le logo dépasse 3 Mo : envoyez-le plutôt par courriel après la demande.",
        "sujet_s": "Suggestion pour Filodie", "sujet_p": "Demande d’édition personnalisée Filodie",
    },
    "en": {
        "envoyer": "Send", "envoi": "Sending…",
        "merci": "Thank you! Your message has been received.",
        "erreur": "Sending did not work. Your email app will open with the message filled in.",
        "opt": "(optional)",
        "s_type": "Your suggestion is about…",
        "s_types": ["A new tool to create", "Improving an existing tool", "An error to fix", "The website or shop", "Something else"],
        "s_outil": "Tool or product concerned", "s_msg": "Your suggestion",
        "s_msg_ph": "Describe your idea: for which setting, age, need…",
        "s_role": "You are…", "s_roles": ["", "Special care counsellor or worker", "Teacher", "Daycare educator", "Parent",
                                           "Student or intern", "Manager", "Other"],
        "s_nom": "First name", "s_courriel": "Email, if you would like a reply",
        "s_conf": "To protect confidentiality, do not name any child or person you support.",
        "p_etab": "Name of the organization or company",
        "p_lignes": "Names to display on the files",
        "p_lignes_ph": "E.g. Intellectual disability and autism program\nRehabilitation services",
        "p_contact": "Contact person", "p_courriel": "Email", "p_tel": "Phone",
        "p_nb": "Number of staff members covered",
        "p_produits": "Tools wanted", "p_produits_ph": "E.g. Autism toolkit, Crisis management toolkit, all toolkits…",
        "p_logo": "Your logo", "p_logo_aide": "PNG, JPG, SVG or PDF, 3 MB maximum. Ideally on a transparent background.",
        "p_logo_tard": "You can also email it later.",
        "p_msg": "Details",
        "p_ok": "I confirm that the organization is authorized to use this logo on its internal documents.",
        "trop_gros": "The logo is larger than 3 MB: please email it after sending the request.",
        "sujet_s": "Suggestion for Filodie", "sujet_p": "Filodie custom edition request",
    },
}


def _e(s):
    return html.escape(s, quote=True)


def _champ(lab, name, t, typ="text", req=False, ph="", opt=False, attrs=""):
    o = f' <span class="opt">{t["opt"]}</span>' if opt else ""
    r = " required" if req else ""
    p = f' placeholder="{_e(ph)}"' if ph else ""
    if typ == "textarea":
        ctl = f'<textarea name="{name}"{r}{p} maxlength="5000"{attrs}></textarea>'
    else:
        ctl = f'<input type="{typ}" name="{name}"{r}{p} maxlength="300"{attrs}>'
    return f'<label><span>{_e(lab)}{o}</span>{ctl}</label>'


def _select(lab, name, options, t, req=False, opt=False):
    o = f' <span class="opt">{t["opt"]}</span>' if opt else ""
    ops = "".join(f'<option value="{_e(v)}">{_e(v)}</option>' for v in options)
    return f'<label><span>{_e(lab)}{o}</span><select name="{name}"{" required" if req else ""}>{ops}</select></label>'


def _fin(t, sujet, nom):
    """Champs cachés communs + anti-pourriel (champ piège et délai minimal) + bouton."""
    return (f'<div class="pot" aria-hidden="true"><label>Site web<input type="text" name="site_web" tabindex="-1" autocomplete="off"></label></div>'
            f'<input type="hidden" name="formulaire" value="{nom}"><input type="hidden" name="sujet" value="{_e(sujet)}">'
            f'<button class="btn" type="submit">{t["envoyer"]}</button><p class="etat" role="status" aria-live="polite"></p>')


def suggestion(lang):
    t = T[lang]
    return ('<form class="fform" data-filodie-form>'
            + _select(t["s_type"], "type", t["s_types"], t, req=True)
            + _champ(t["s_outil"], "outil", t, opt=True)
            + _champ(t["s_msg"], "message", t, "textarea", req=True, ph=t["s_msg_ph"])
            + f'<p class="opt">{t["s_conf"]}</p>'
            + '<div class="deux">' + _select(t["s_role"], "role", t["s_roles"], t, opt=True)
            + _champ(t["s_nom"], "prenom", t, opt=True) + '</div>'
            + _champ(t["s_courriel"], "courriel", t, "email", opt=True, attrs=' autocomplete="email"')
            + _fin(t, t["sujet_s"], "suggestion") + '</form>')


def personnalisation(lang):
    t = T[lang]
    return ('<form class="fform" data-filodie-form>'
            + _champ(t["p_etab"], "etablissement", t, req=True, attrs=' autocomplete="organization"')
            + _champ(t["p_lignes"], "nomenclature", t, "textarea", opt=True, ph=t["p_lignes_ph"], attrs=' style="min-height:80px"')
            + '<div class="deux">' + _champ(t["p_contact"], "contact", t, req=True, attrs=' autocomplete="name"')
            + _champ(t["p_courriel"], "courriel", t, "email", req=True, attrs=' autocomplete="email"') + '</div>'
            + '<div class="deux">' + _champ(t["p_tel"], "telephone", t, "tel", opt=True, attrs=' autocomplete="tel"')
            + _champ(t["p_nb"], "personnes", t, "number", opt=True, attrs=' min="1" max="100000"') + '</div>'
            + _champ(t["p_produits"], "produits", t, "textarea", req=True, ph=t["p_produits_ph"], attrs=' style="min-height:80px"')
            + f'<label><span>{t["p_logo"]} <span class="opt">{t["opt"]}</span></span>'
              f'<input type="file" name="logo" accept=".png,.jpg,.jpeg,.svg,.pdf,image/png,image/jpeg,image/svg+xml,application/pdf">'
              f'<span class="opt">{t["p_logo_aide"]} {t["p_logo_tard"]}</span></label>'
            + _champ(t["p_msg"], "message", t, "textarea", opt=True, attrs=' style="min-height:80px"')
            + f'<label class="check"><input type="checkbox" name="autorisation" value="oui" required><span>{t["p_ok"]}</span></label>'
            + _fin(t, t["sujet_p"], "personnalisation") + '</form>')


def script(lang):
    """Envoi des formulaires : vers le script Google si l’adresse est configurée, sinon courriel prérempli."""
    t = T[lang]
    cfg = json.dumps({"url": url(), "envoi": t["envoi"], "envoyer": t["envoyer"], "merci": t["merci"],
                      "erreur": t["erreur"], "gros": t["trop_gros"], "lang": lang}, ensure_ascii=False)
    return """<script>
(function(){const C=%s;const t0=Date.now();
function mailto(f,d){const lignes=[];for(const[k,v]of d){if(['site_web','formulaire','sujet','logo_b64','logo_type'].includes(k)||!v)continue;lignes.push(k+' : '+v)}
location.href='mailto:melodie@filodie.ca?subject='+encodeURIComponent(d.get('sujet'))+'&body='+encodeURIComponent(lignes.join('\\n'))}
function lire(file){return new Promise((ok,ko)=>{const r=new FileReader();r.onload=()=>ok(String(r.result).split(',')[1]);r.onerror=ko;r.readAsDataURL(file)})}
document.querySelectorAll('form[data-filodie-form]').forEach(f=>f.addEventListener('submit',async e=>{e.preventDefault();
const etat=f.querySelector('.etat'),b=f.querySelector('button');etat.className='etat';etat.textContent='';
const fd=new FormData(f);if(fd.get('site_web')||Date.now()-t0<3000){etat.className='etat ok';etat.textContent=C.merci;return}
const d=new URLSearchParams();for(const[k,v]of fd){if(!(v instanceof File))d.append(k,v)}
d.append('langue',C.lang);d.append('page',location.pathname);
const file=fd.get('logo');
if(file&&file.size){if(file.size>3e6){etat.className='etat err';etat.textContent=C.gros;return}
if(C.url){d.append('logo_nom',file.name);d.append('logo_type',file.type);d.append('logo_b64',await lire(file))}else{d.append('logo','(à joindre au courriel : '+file.name+')')}}
if(!C.url){mailto(f,d);return}
b.disabled=true;b.textContent=C.envoi;
try{await fetch(C.url,{method:'POST',mode:'no-cors',body:d});f.reset();etat.className='etat ok';etat.textContent=C.merci}
catch(err){etat.className='etat err';etat.textContent=C.erreur;setTimeout(()=>mailto(f,d),1500)}
finally{b.disabled=false;b.textContent=C.envoyer}}))})();
</script>""" % cfg


# ------------------------------------------------------------------ pages et sections
PAGE = {
    "fr": ("Boîte à suggestions", """
<p class="lead">Un outil qui vous manque ? Une idée pour en améliorer un ? Une coquille repérée ? Écrivez-la ici : chaque suggestion est lue.</p>
<p>Les idées reçues guident les prochains outils Filodie. Si vous laissez votre courriel, je vous préviens quand votre suggestion devient un outil.</p>
{form}
<p class="muted">Vos renseignements servent seulement à traiter votre suggestion. Voir la <a href="confidentialite.html">politique de confidentialité</a>. Pour une situation urgente, composez le 9-1-1 ou le 811 option 2.</p>"""),
    "en": ("Suggestion box", """
<p class="lead">Missing a tool? An idea to improve one? Spotted a typo? Write it here: every suggestion is read.</p>
<p>Your ideas guide the next Filodie tools. If you leave your email, I will let you know when your suggestion becomes a tool.</p>
{form}
<p class="muted">Your information is only used to handle your suggestion. See the <a href="privacy.html">privacy policy</a>. In an emergency, call 9-1-1 or 811 option 2.</p>"""),
}

SECTION_PERSO = {
    "fr": """
<h2 id="personnalisation">Édition personnalisée à l’image de votre établissement</h2>
<p>Pour un CIUSSS, un CISSS, un centre de services scolaire, un CPE, un organisme ou une entreprise : les outils Filodie peuvent porter <strong>votre logo et votre nomenclature</strong> (direction, programme, service), pour s’intégrer à vos documents internes.</p>
<ul><li>Votre logo, le nom de l’établissement et jusqu’à deux lignes de nomenclature en haut des pages et sur les couvertures.</li>
<li>Une page de garde à votre nom, avec la licence d’établissement.</li>
<li>La mention « © Filodie » reste en bas de chaque page.</li>
<li>Les PDF restent remplissables à l’écran et imprimables.</li>
<li>Version française, anglaise ou les deux.</li></ul>
<h3>Prix</h3>
<p>Le prix de la <a href="#licence-equipe">licence d’équipe</a> (3 fois le prix individuel, jusqu’à 25 membres du personnel), plus des frais de personnalisation de 49 $ par commande, peu importe le nombre de fichiers. Vous recevez le prix exact avant de payer. Pour plus de 25 personnes ou plusieurs installations, je vous envoie une soumission.</p>
<h3>Faire une demande</h3>
<p>Remplissez le formulaire : je vous réponds par courriel avec un aperçu et une facture. Aucun appel ni rencontre n’est nécessaire.</p>
{form}
""",
    "en": """
<h2 id="custom-edition">Custom edition with your organization’s branding</h2>
<p>For a health and social services centre, a school service centre, a daycare, a community organization or a company: Filodie tools can carry <strong>your logo and your names</strong> (department, program, service), to fit in with your internal documents.</p>
<ul><li>Your logo, the organization’s name and up to two lines of department names at the top of the pages and on the covers.</li>
<li>A title page in your name, with the organization licence.</li>
<li>The “© Filodie” notice remains at the bottom of every page.</li>
<li>The PDFs stay fillable on screen and printable.</li>
<li>English, French or both.</li></ul>
<h3>Price</h3>
<p>The price of the <a href="#team-licence">team licence</a> (3 times the individual price, up to 25 staff members), plus a $49 customization fee per order, whatever the number of files. You receive the exact price before paying. For more than 25 people or several sites, I will send you a quote.</p>
<h3>Request a custom edition</h3>
<p>Fill in the form: I will reply by email with a preview and an invoice. No call or meeting is needed.</p>
{form}
""",
}
