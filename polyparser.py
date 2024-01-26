from classes import Simulation, Drone, Warehouse, Order, ProductType

def parse_challenge(file_path):

    output_file = file_path.split('/')[-1] 
    output_file = output_file.split('.')[0] + '.out'
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

    parsed_simulation = Simulation(rows, columns, drones, turns, max_payload, product_types, warehouses, orders, output_file)

    return parsed_simulation
