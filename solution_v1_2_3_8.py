#importation des librairies
import math
import sys
sys.setrecursionlimit(10000) # pour éviter le dépassement de la limite de récursion


# =============================================================Définition des classes======================================================

# classe pour la simulation
class Simulation:
    def __init__(self, rows, columns, drones, turns, max_payload, product_types, warehouses, orders):
        self.rows = rows
        self.columns = columns
        self.drones = drones
        self.turns = turns
        self.max_payload = max_payload
        self.product_types = product_types
        self.warehouses = warehouses
        self.orders = orders
        self.score = 0

    def sort_orders(self):
        # trier par différents produits en ordre croissant
        self.orders.sort(key=lambda x: sum(x.inventory.values())) 
        # trier par poids en ordre croissant
        self.orders.sort(key=lambda x: sum([self.product_types[product_type].weight * quantity for product_type, quantity in x.inventory.items()])) 
        # trier par nombre d'articles en ordre croissant
        self.orders.sort(key=lambda x: len(x.inventory)) 
        
        return self.orders

# classe pour le drone
class Drone:
    def __init__(self, drone_id, location):
        self.drone_id = drone_id
        self.location = location
        self.payload = 0
        self.current_turn = 0
        self.inventory = {}
        self.is_free = True

    # méthode pour mettre à jour le statut du drone
    def update_is_free(self):
        self.is_free = all(value == 0 for value in self.inventory.values())

    # méthode pour charger le drone
    def load(self, Warehouse, product_type, quantity):
        # charger la quantié à priori positive
        if quantity > 0:
            if product_type in self.inventory:
                self.inventory[product_type] += quantity
            else:
                self.inventory[product_type] = quantity

            # mettre à jour le payload
            self.payload += quantity * simulation.product_types[product_type].weight

            # mettre à jour le warehouse
            Warehouse.inventory[product_type] -= quantity
            Warehouse.update_is_empty()

            # mettre à jour le statut du drone
            self.update_is_free()

    # méthode pour décharger le drone afin de livrer la commande
    def deliver(self, order, product_type, quantity):
        # décharger la quantity
        if quantity > 0:
            self.inventory[product_type] -= quantity

            # mettre à jour le payload
            self.payload -= quantity * simulation.product_types[product_type].weight

            # mettre à jour la commande
            order.inventory[product_type] -= quantity
            order.update_is_completed()

            # mettre à jour le statut du drone
            self.update_is_free()
        
# classe pour l'entrepôt
class Warehouse:
    def __init__(self, warehouse_id, location, inventory):
        self.warehouse_id = warehouse_id
        self.location = location
        self.inventory = inventory
        self.update_is_empty()

    # méthode pour mettre à jour le statut de l'entrepôt
    def update_is_empty(self):
        self.is_empty = all(value == 0 for value in self.inventory.values())

# classe pour la commande
class Order:
    def __init__(self, order_id, location, inventory):
        self.order_id = order_id
        self.location = location
        self.inventory = inventory
        self.order_turns = 0
        self.is_completed = False

    # méthode pour mettre à jour le statut de la commande
    def update_is_completed(self):
        self.is_completed = all(value == 0 for value in self.inventory.values())

# classe pour le type de produit
class ProductType:
    def __init__(self, product_type_id, weight):
        self.product_type_id = product_type_id
        self.weight = weight
        

# =============================================================Parser le fichier d'entrée ======================================================


def parse_input_file(file_path):
    
    # Lire le fichier d'entrée dans le repertoire /challenges
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # premier bloc de données : 1ère ligne
    rows, columns, drones_count, turns, max_payload = map(int, lines[0].split())
    
    # deuxième bloc de données : 2ème ligne
    product_types_count = int(lines[1])
    product_types = [ProductType(i, int(weight)) for i, weight in enumerate(lines[2].split())]

    # troisième bloc de données
    current_line = 3
    warehouses_count = int(lines[current_line])
    warehouses = []
    for i in range(warehouses_count):
        current_line += 1
        location = tuple(map(int, lines[current_line].split()))
        current_line += 1
        inventory = {j: int(quantity) for j, quantity in enumerate(lines[current_line].split())}
        
        warehouses.append(Warehouse(i, location, inventory))

    # quatrième bloc de données
    current_line += 1
    orders_count = int(lines[current_line])
    orders = []
    for i in range(orders_count):
        current_line += 1
        location = tuple(map(int, lines[current_line].split()))
        
        current_line += 1
        products_count = int(lines[current_line])
        products_data = list(map(int, lines[current_line + 1].split()))
        
        current_line += 1
        inventory = {productType: products_data.count(productType) for productType in set(products_data)}

        orders.append(Order(i, location, inventory))

    # créer une liste de drones
    drones = [Drone(i, warehouses[0].location) for i in range(drones_count)]


    # créer une instance de la classe Simulation
    simulation = Simulation(rows, columns, drones, turns, max_payload, product_types, warehouses, orders)

    return simulation

# ============================================================= implémentation de l'algorithme de livraison======================================================


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
    eligible_drones = [drone for drone in drones if drone.current_turn < simulation.turns]

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
        print('Simulation terminée {}'.format(drone.current_turn))
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
                    order.order_turns += 1
                    drone.load(warehouse, product_type, load_quantity)
                    delivery_plan.append((drone.drone_id, 'L', warehouse.warehouse_id, product_type, load_quantity))
                else:
                    print('Simulation terminée {}'.format(simulation.turns))
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
def deliver_order(drone, order, t_simulation, delivery_plan):
    # Liste des produits de la commande qui ont quantité supérieure à 0
    for product_type, quantity in order.inventory.items():
        # livrer la quantité qui se trouve dans le drone et qui est bien évidemment supérieure à 0
        if quantity > 0:
            deliver_quantity = min(quantity, drone.inventory.get(product_type, 0))
            deliver_remaining_quantity(drone, order, product_type, deliver_quantity, t_simulation, delivery_plan)




# fonction pour livrer les produits de la commande
def deliver_remaining_quantity(drone, order, product_type, deliver_quantity, t_simulation, delivery_plan):
    if deliver_quantity > 0:
        # vérifier si le drone peut livrer le produit
        if product_type in drone.inventory and drone.inventory[product_type] >= deliver_quantity:
            if drone.current_turn + 1 <= t_simulation.turns:
                drone.current_turn += 1
                order.order_turns += 1
                drone.deliver(order, product_type, deliver_quantity)
                delivery_plan.append((drone.drone_id, 'D', order.order_id, product_type, deliver_quantity))
            else:
                print('Simulation terminée {}'.format(simulation.turns))
                exit()
            deliver_remaining_quantity(drone, order, product_type, 0, t_simulation, delivery_plan)
        else:
            # Si le drone ne peut pas livrer le produit, passer au produit suivant
            deliver_remaining_quantity(drone, order, product_type, deliver_quantity - 1, t_simulation, delivery_plan)
    else:
        return



# fonction pour écrire le fichier de sortie
def write_output_file(file_path, delivery_plan):
    with open(file_path, 'w') as file:
        file.write(str(len(delivery_plan)) + '\n')
        for command in delivery_plan:
            file.write(' '.join(map(str, command)) + '\n')




# initialiser le plan de livraison            
delivery_plan = []

def main_algorithm(simulation):
    # tier les commandes par : nombre de différents produits, poids, nombre d'articles
    simulation.sort_orders()

    # proceder à la livraison des commandes une par une
    process_orders(simulation, simulation.orders, delivery_plan)


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
        return


simulation = parse_input_file('a_example.in')
# simulation = parse_input_file('b_busy_day.in')
# simulation = parse_input_file('c_redudancy.in')
# simulation = parse_input_file('d_mother_of_all_warehouses.in')
main_algorithm(simulation)
# print(simulation.score)

