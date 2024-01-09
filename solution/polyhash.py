#================================CLASSES=============================================================

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


class Drone:
    def __init__(self, drone_id, max_payload, location=(0, 0)):
        self.drone_id = drone_id
        self.location = location
        self.max_payload = max_payload
        self.payload = 0
        self.inventory = {}
        self.is_free = True

    def update_is_free(self):
        self.is_free = all(value == 0 for value in self.inventory.values())

    def load(self, warehouse, product_type, quantity):
        product_weight = simulation.product_types[product_type].weight
        total_weight = quantity * product_weight
        if self.payload + total_weight <= self.max_payload:
            self.payload += total_weight
            if product_type in self.inventory:
                self.inventory[product_type] += quantity
            else:
                self.inventory[product_type] = quantity
            warehouse.inventory[product_type] -= quantity
            warehouse.update_is_empty()
            self.update_is_free()
        else:
            raise Exception('Drone {} en surcharge'.format(self.drone_id))

    def deliver(self, order, product_type, quantity):
            if product_type in self.inventory:
                self.inventory[product_type] -= quantity
                order.inventory[product_type] -= quantity
                order.update_is_completed()
                self.update_is_free()
            else:
                raise Exception('Drone {} n a pas ce type de produit {}'.format(self.drone_id, product_type))


class Warehouse:
    def __init__(self, warehouse_id, location, inventory):
        self.warehouse_id = warehouse_id
        self.location = location
        self.inventory = inventory
        self.update_is_empty()

    def update_is_empty(self):
        self.is_empty = all(value == 0 for value in self.inventory.values())


class Order:
    def __init__(self, order_id, location, inventory):
        self.order_id = order_id
        self.location = location
        self.inventory = inventory
        self.update_is_completed()

    def update_is_completed(self):
        self.is_completed = all(value == 0 for value in self.inventory.values())


class ProductType:
    def __init__(self, product_type_id, weight):
        self.product_type_id = product_type_id
        self.weight = weight

#=================================POLYPARSER==========================================================

def parse_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    rows, columns, drones_count, turns, max_payload = map(int, lines[0].split())
    

    product_types_count = int(lines[1])
    product_types = [ProductType(i, int(weight)) for i, weight in enumerate(lines[2].split())]


    current_line = 3
    warehouses_count = int(lines[current_line])
    warehouses = []
    for i in range(warehouses_count):
        current_line += 1
        location = tuple(map(int, lines[current_line].split()))
        current_line += 1
        inventory = {j: int(quantity) for j, quantity in enumerate(lines[current_line].split())}
        
        warehouses.append(Warehouse(i, location, inventory))


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


    drones = [Drone(i, max_payload) for i in range(drones_count)]

    # Create simulation object
    simulation = Simulation(rows, columns, drones, turns, max_payload, product_types, warehouses, orders)

    return simulation


#=================================POLYSOLVER==========================================================

import math

def get_distance(position1, position2):
    return math.ceil(math.sqrt((position2[0] - position1[0])**2 + (position2[1] - position1[1])**2))

# Fonction pour trouver l'entrepôt le plus proche non vide
def find_nearest_non_empty_warehouse(location, warehouses):
    eligible_warehouses = [warehouse for warehouse in warehouses if not warehouse.is_empty]
    return min(eligible_warehouses, key=lambda w: get_distance(location, w.location))
# Trouver la quantié optimale à charger
def find_optimal_quantity(simulation, drone, warehouse, product_type):

    product_weight = simulation.product_types[product_type].weight
    available_capacity = simulation.max_payload - drone.payload
    optimal_quantity = warehouse.inventory[product_type]

    # une fonction récursive par subdivision pour trouver la quantité optimale à charger

    def try_quantity(quantity):
        total_weight = quantity * product_weight
        if total_weight > available_capacity:
            return int(try_quantity(quantity // 2))
        else:
            return quantity
    
    return try_quantity(optimal_quantity)

def find_nearest_order(drone, orders):
    eligible_orders = [order for order in orders if not order.is_completed and any(product_type in drone.inventory for product_type in order.inventory)]
    if not eligible_orders:
        return None
    return min(eligible_orders, key=lambda o: get_distance(drone.location, o.location))

def generate_delivry_plan(simulation):
    delivery_plan = []

    # Pour chaque drone dont l'inventaire est vide
    for drone in [d for d in simulation.drones if not d.inventory]:
        
        # Recherche de l'entrepôt le plus proche non vide
        nearest_warehouse = find_nearest_non_empty_warehouse(drone.location, simulation.warehouses)

        # Se rendre à l'entrepôt
        distance_to_warehouse = get_distance(drone.location, nearest_warehouse.location)
        drone.location = nearest_warehouse.location
        
        print('drone {} se rend à l\'entrepôt {}'.format(drone.drone_id, nearest_warehouse.warehouse_id))

        if simulation.turns - distance_to_warehouse > 0:
            simulation.turns -= distance_to_warehouse
        else:
            # arrêt de la simulation si le nombre de tours est atteint
            break
        
        # Charger jusqu'à atteindre la capacité maximale
        for product_type in nearest_warehouse.inventory:
            quantity = find_optimal_quantity(simulation, drone, nearest_warehouse, product_type)
            if quantity > 0:
                drone.load(nearest_warehouse, product_type, quantity)
                delivery_plan.append((drone.drone_id, 'L', nearest_warehouse.warehouse_id, product_type, quantity))
                print('drone {} charge {} produits de type {}'.format(drone.drone_id, quantity, product_type))
                if simulation.turns - 1 > 0:
                    simulation.turns -= 1
                else:
                    # arrêt de la simulation si le nombre de tours est atteint
                    break
        print('drone {} a fini de charger'.format(drone.drone_id))

        # Recherche de la commande la plus proche qui n'est pas encore complétée qui contient au moins un produit que le drone transporte
        
        nearest_order = find_nearest_order(drone, simulation.orders)

        # Si aucune commande n'est éligible, passer au drone suivant
        if not nearest_order:
            print('drone {} n\'a pas trouvé de commande éligible'.format(drone.drone_id))
            continue
        
        distance_to_order = get_distance(drone.location, nearest_order.location)
        drone.location = nearest_order.location
        print('drone {} se rend à la commande {}'.format(drone.drone_id, nearest_order.order_id))

        if simulation.turns - distance_to_order > 0:
            simulation.turns -= distance_to_order
        else:
            # arrêt de la simulation si le nombre de tours est atteint
            break

        #TODO
        print('à implémenter')

    return delivery_plan

def write_output_file(file_path, delivery_plan):
    with open(file_path, 'w') as file:
        file.write('{}\n'.format(len(delivery_plan)))
        for command in delivery_plan:
            file.write('{}\n'.format(' '.join(map(str, command))))


input_file_path = 'a_example.in'
output_file_path = 'a_example.out'
simulation = parse_input_file(input_file_path)
delivery_plan = generate_delivry_plan(simulation)
write_output_file(output_file_path, delivery_plan)
