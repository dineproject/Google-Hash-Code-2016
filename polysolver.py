from os import path, makedirs
from classes import Simulation
from polyparser import parse_challenge
import math


def solve(simulation, var_optimize):

    # fonction pour calculer la distance entre deux points et l'arrondir à l'entier supérieur
    def calculate_distance(location1, location2):
        return math.ceil(math.sqrt((location1[0] - location2[0]) ** 2 + (location1[1] - location2[1]) ** 2))



    # fonction pour trouver l'entrepôt qui contient au moins un produit de la commande et qui est le plus proche de la commande
    def get_closest_warehouse(warehouses, order):
        # Position de la commande
        order_location = order.location
        # Liste des entrepôts qui ont au moins un produit de la commande
        eligible_warehouses = [warehouse for warehouse in warehouses if any(warehouse.inventory.get(product_type, 0) > 0 for product_type in order.inventory if order.inventory[product_type] > 0)]

        if not eligible_warehouses:
            # Si aucun entrepôt n'a de produits de la commande
            raise Exception('Aucun entrepôt ne contient de produits de la commande')

        # Trier les entrepôts en fonction de la distance
        sorted_warehouses = sorted(eligible_warehouses, key=lambda warehouse: calculate_distance(warehouse.location, order_location))

        # Renvoyer le premier entrepôt trié
        return sorted_warehouses[0]



    # fonction pour trouver le drone qui est le plus proche de l'entrepôt
    def get_closest_drone(drones, warehouse):
        # Position de l'entrepôt
        warehouse_location = warehouse.location

        # trier les drones qui n'ont pas attein leur limite de tour
        eligible_drones = [drone for drone in drones if drone.current_turn < math.ceil((simulation.turns*var_optimize))]

        # Trier les drones en fonction de la distance
        sorted_drones = sorted(eligible_drones, key=lambda drone: calculate_distance(drone.location, warehouse_location))

        # Renvoyer le premier drone trié
        return sorted_drones[0]



    # fonction pour déplacer le drone vers la destination
    def move_drone(drone, destination, simulation, order):
        # Calculer la distance entre le drone et la destination
        distance = calculate_distance(drone.location, destination.location)

        # Vérifier si le drone peut atteindre la destination avant la fin de la simulation
        if drone.current_turn + distance <= simulation.turns:
            drone.current_turn += distance
            # mettre à jour le nombre de tours de la commande
            order.order_turns += distance
            drone.location = destination.location
        else:
            print('Simulation terminée précocement pour le drone {}'.format(drone.drone_id))
            exit()



    # fonction pour dérouler un cycle de chargement dans un entrepôt
    def load_drone(drone, warehouse, order, simulation, delivery_plan):

        # Liste des produits de la commande qui ont quantité supérieure à 0
        eligible_products = [product_type for product_type, quantity in order.inventory.items() if quantity > 0]

        # charger les produits de la commande
        load_remaining_products(drone, warehouse, order, eligible_products, simulation, delivery_plan)



    # fonction pour charger de manière optimale les produits de la commande
    def load_remaining_products(drone, warehouse, order, eligible_products, simulation, delivery_plan):
        if eligible_products:
            # charger le premier produit de la liste
            product_type = eligible_products[0]

            # vérifier si le produit est disponible dans l'entrepôt sinon passer au produit suivant
            if product_type in warehouse.inventory and warehouse.inventory[product_type] > 0:
                # vérifier si le drone peut charger le produit sinon passer au produit suivant
                min_quantity = min(warehouse.inventory[product_type], order.inventory[product_type])
                # charger la quantité optimale
                load_quantity = find_optimal_quantity(drone, warehouse, product_type, order, simulation, min_quantity)
                # vérifier si la quantité est supérieure à 0 à priori oui
                if load_quantity > 0:
                    if drone.current_turn + 1 <= simulation.turns:
                        drone.current_turn += 1
                        drone.load(warehouse, product_type, simulation.product_types[product_type].weight, load_quantity)
                        delivery_plan.append((drone.drone_id, 'L', warehouse.warehouse_id, product_type, load_quantity))
                        order.order_turns += 1
                    else:
                        print('Simulation terminée précocement pour le drone {}'.format(drone.drone_id))
                        exit()
                    # passer au produit suivant
            load_remaining_products(drone, warehouse, order, eligible_products[1:], simulation, delivery_plan)
        else:
            return



    # fonction pour trouver la quantité optimale à charger
    def find_optimal_quantity(drone, warehouse, product_type, order, simulation, quantity):
        if (drone.payload + quantity * simulation.product_types[product_type].weight) <= simulation.max_payload:
            return quantity
        else:
            # Si le drone ne peut pas charger le produit, diminuer la quantité demandée de 1 et réessayer
            return find_optimal_quantity(drone, warehouse, product_type, order, simulation, quantity - 1)
        


    # fonction pour dérouler un cycle de livraison
    def deliver_order(drone, order, simulation, delivery_plan):
        # Liste des produits de la commande qui ont quantité supérieure à 0
        for product_type, quantity in order.inventory.items():
            # livrer la quantité qui se trouve dans le drone et qui est bien évidemment supérieure à 0
            if quantity > 0:
                deliver_quantity = min(quantity, drone.inventory.get(product_type, 0))
                deliver_remaining_quantity(drone, order, product_type, deliver_quantity, simulation, delivery_plan)




    # fonction pour livrer les produits de la commande
    def deliver_remaining_quantity(drone, order, product_type, deliver_quantity, simulation, delivery_plan):
        if deliver_quantity > 0:
            # vérifier si le drone peut livrer le produit
            if product_type in drone.inventory and drone.inventory[product_type] >= deliver_quantity:
                if drone.current_turn + 1 <= simulation.turns:
                    drone.current_turn += 1
                    drone.deliver(order, product_type, simulation.product_types[product_type].weight, deliver_quantity)
                    delivery_plan.append((drone.drone_id, 'D', order.order_id, product_type, deliver_quantity))
                    order.order_turns += 1
                else:
                    print('Simulation terminée précocement pour le drone {}'.format(drone.drone_id))
                    exit()
                deliver_remaining_quantity(drone, order, product_type, 0, simulation, delivery_plan)
            else:
                # Si le drone ne peut pas livrer le produit, passer au produit suivant
                deliver_remaining_quantity(drone, order, product_type, deliver_quantity - 1, simulation, delivery_plan)
        else:
            return



    # fonction pour écrire le fichier de sortie

    # output_file_path = simulation.output_file

    def write_output_file(file_path, delivery_plan):
        # vérifier si le répertoire 'output' existe, sinon le créer
        output_directory = './output'
        if not path.exists(output_directory):
            makedirs(output_directory)

        with open(file_path, 'w') as file:
            file.write(str(len(delivery_plan)) + '\n')
            for command in delivery_plan:
                file.write(' '.join(map(str, command)) + '\n')

    # fonction pour traiter les commandes
    def process_orders(simulation, orders, delivery_plan):
        # vérifier si la liste des commandes n'est pas vide
        if orders:
            # prendre la première commande
            order = orders[0]

            # vérifier si la commande est complétée, si oui passer à la commande suivante
            if order.is_completed:

                write_output_file('./output/'+ simulation.output_file, delivery_plan)
                # je veux que le nom du fichier de sortie soit le même que celui du fichier d'entrée avec l'extension .txt

                # write_output_file('{}.txt'.format(output_file_path.split('.')[0]), delivery_plan)
                process_orders(simulation, orders[1:], delivery_plan)
            else:
                # trouver l'entrepôt le plus proche de la commande
                warehouse = get_closest_warehouse(simulation.warehouses, order)
                # trouver le drone le plus proche de l'entrepôt
                drone = get_closest_drone(simulation.drones, warehouse)
                # déplacer le drone vers l'entrepôt
                move_drone(drone, warehouse, simulation, order)
                # charger le drone
                load_drone(drone, warehouse, order, simulation, delivery_plan)
                # déplacer le drone vers la commande
                move_drone(drone, order, simulation, order)
                # livrer la commande
                deliver_order(drone, order, simulation, delivery_plan)
                # reprendre le traitement de la commande en cours
                process_orders(simulation, orders, delivery_plan)
                
        else:
            return

    # initialiser le plan de livraison            
    delivery_plan = []

    # tier les commandes par : nombre de différents produits, poids, nombre d'articles
    simulation.sort_orders()

    # proceder à la livraison des commandes une par une
    process_orders(simulation, simulation.orders, delivery_plan)
