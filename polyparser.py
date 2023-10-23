#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module de parsing des fichiers d'entrée pour la mise en oeuvre du projet Poly#.
"""

def parse_challenge(filename: str) -> object:
    """Lit un fichier de challenge et extrait les informations nécessaires.

    Vous pouvez choisir la structure de données structurées qui va
    représenter votre challenge: dictionnaire, objet, etc
    """
    with open(filename, 'r') as f:
        # Lire la première ligne et la découper
        rows, columns, drone_count, deadline, max_load = [ int(v)
                                                           for v in f.readline().split() ]
        # ...

    return challenge
