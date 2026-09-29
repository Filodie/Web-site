# -*- coding: utf-8 -*-
"""Publier le site filodie.ca en une commande.

1. reconstruit le site (build_site.py) ;
2. enregistre les changements dans Git ;
3. les envoie sur GitHub. Cloudflare Pages voit l’envoi et met filodie.ca à jour tout seul (environ 1 minute).

    python3 publier.py                         → message automatique
    python3 publier.py "Nouvelles trousses"    → message choisi
    python3 publier.py --catalogue             → relit aussi les PDF (après l’ajout d’outils)
"""
import os
import subprocess
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))


def git(*a, check=True, capture=False):
    return subprocess.run(["git", *a], cwd=HERE, check=check, text=True,
                          stdout=subprocess.PIPE if capture else None, stderr=subprocess.STDOUT if capture else None)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    build = [sys.executable, os.path.join(HERE, "build_site.py")] + (["--catalogue"] if "--catalogue" in sys.argv else [])
    subprocess.run(build, cwd=HERE, check=True)

    git("add", "-A")
    if not git("status", "--porcelain", capture=True).stdout.strip():
        print("Aucun changement : le site en ligne est déjà à jour.")
        return
    msg = args[0] if args else f"Mise à jour du site – {datetime.now():%Y-%m-%d %H:%M}"
    git("commit", "-q", "-m", msg)
    print("Changements enregistrés :", msg)

    if not git("remote", capture=True).stdout.strip():
        print("\nPas encore relié à GitHub : les changements sont enregistrés sur l’ordinateur seulement.\n"
              "Dans VS Code, ouvrez « Contrôle de code source » et cliquez sur « Publier la branche ».")
        return
    r = git("push", "-q", "origin", "main", check=False, capture=True)
    if r.returncode:
        print("\nL’envoi vers GitHub a échoué :\n" + r.stdout +
              "\nLes changements restent enregistrés ; relancez la commande une fois le problème réglé.")
        sys.exit(1)
    print("Envoyé sur GitHub. filodie.ca sera à jour dans environ une minute.")


if __name__ == "__main__":
    main()
