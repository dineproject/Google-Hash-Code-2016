#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module principal pour la mise en oeuvre du projet Poly#.
"""

# Vous pouvez structurer votre code en modules pour améliorer la
# compréhension et faciliter le travail collaboratif
from polyparser import parse_challenge
from polysolver import solve, score_solution, save_solution

if __name__ == "__main__":
    # On fournit ici un exemple permettant de passer un simple
    # argument (le fichier du challenge) en paramètre. N'hésitez pas à
    # compléter avec d'autres paramètres/options.

    # Consultez la documentation du module argparse:
    # https://docs.python.org/3/library/argparse.html

    import argparse
    parser = argparse.ArgumentParser(description='Solve Poly# challenge.')
    parser.add_argument('challenge', type=str,
                        help='challenge definition filename',
                        metavar="challenge.txt")
    parser.add_argument('output', type=str, default=None,
                        help='output filename',
                        metavar="sortie.txt")
    args = parser.parse_args()

    challenge = parse_challenge(args.challenge)
    solution = solve(challenge)
    if args.output is not None:
        # Sauvegarder le fichier généré
        save_solution(args.output, solution)
        print(f"Solution saved in {args.output}")
    print(f"Score: {score_solution(solution)}")
