from os import path, makedirs
from sys import setrecursionlimit
from math import ceil, sqrt
from classes import Simulation
from polyparser import parse_challenge
from polysolver import solve
import argparse

setrecursionlimit(10000) # Augmentation de la limite de récursion pour éviter les débordements de pile

def main():
    # Création d'un analyseur d'arguments avec une description
    parser = argparse.ArgumentParser(description='Solve Polyhash 2016 challenge')

    # Définition d'un argument en ligne de commande 'file_path' de type string
    parser.add_argument('file_path', type=str, help='Path to the input file')

    args = parser.parse_args() # Analyse des arguments de ligne de commande
    file_path = args.file_path # Récupération du chemin du fichier à partir des arguments analysés

    var_optimize = 1 # Initialisation d'une variable pour le facteur d'optimisation

    file_path_optimize = file_path.split('/')[-1] # Extraction du nom de fichier à partir du chemin du fichier
    
    if file_path_optimize == "a_example.in":
        var_optimize = 0.1
    elif file_path_optimize == "b_busy_day.in":
        var_optimize = 0.4627
    elif file_path_optimize == "c_redudancy.in":
        var_optimize = 0.0889
    elif file_path_optimize == "d_mother_of_all_warehouses.in":
        var_optimize = 0.2147   

    challenge = parse_challenge(file_path) # Analyse du défi à partir du fichier d'entrée
    solve(challenge, var_optimize)# Résolution du défi avec le facteur d'optimisation

#Exécution de la fonction main
if __name__ == "__main__":
    main()
