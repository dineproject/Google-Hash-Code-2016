from polyparser import parse_input_file, Simulation
from polysolver import process_orders

def main_algorithm(simulation):
    # Trier les commandes par : nombre de différents produits, poids, nombre d'articles
    simulation.sort_orders()

    # Procéder à la livraison des commandes une par une
    delivery_plan = []
    process_orders(simulation, simulation.orders, delivery_plan)
    return delivery_plan

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Solve Poly# challenge.')
    parser.add_argument('challenge', type=str, help='challenge definition filename', metavar="challenge.txt")
    parser.add_argument('output', type=str, default=None, help='output filename', metavar="sortie.txt")
    args = parser.parse_args()

    challenge = parse_input_file(args.challenge)
    solution = main_algorithm(challenge)

    # Écrire la solution dans le fichier de sortie
    with open(args.output, 'w') as file:
        file.write(str(len(solution)) + '\n')
        for command in solution:
            file.write(' '.join(map(str, command)) + '\n')