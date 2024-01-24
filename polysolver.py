import math
from classes import Drone, Warehouse, Order, ProductType
from polyparser import Simulation
from Fonction import write_output_file, get_closest_warehouse, get_closest_drone, move_drone, load_drone, deliver_order

# initialiser le plan de livraison            

delivery_plan = []

# fonction pour traiter les commandes
def process_orders(simulation, orders, delivery_plan):
    # vérifier si la liste des commandes n'est pas vide
    if orders:
        # prendre la première commande
        order = orders[0]

        # vérifier si la commande est complétée, si oui passer à la commande suivante
        if order.is_completed:
            #  mettre à jour le score
            simulation.score += math.ceil(((simulation.turns - order.order_turns)/simulation.turns)*100)
        
            print('Order {} is completed'.format(order.order_id))
            print(f'score actuel {simulation.score} ')
            write_output_file('challenge.out', delivery_plan)
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
        return delivery_plan