# j'ai mis en place une fonction qui va prendre en entrée le fichier dans challenge puis va extraire les données pour les mettre dans la structure de données que j'ai choisie

def parse_input_file(file_path):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    simulation_params = list(map(int, lines[0].split()))
    simulation = {
        'rows': simulation_params[0],
        'columns': simulation_params[1],
        'drones': simulation_params[2],
        'turns': simulation_params[3],
        'max_payload': simulation_params[4],
    }

    product_types_count = int(lines[1])
    product_type_weights = list(map(int, lines[2].split()))
    product_types = [{'weight': weight} for weight in product_type_weights]

    warehouses_count = int(lines[3])
    warehouses_data = lines[4:4 + 2 * warehouses_count]
    warehouses = []
    for i in range(0, len(warehouses_data), 2):
        w_location = tuple(map(int, warehouses_data[i].split()))
        w_products = list(map(int, warehouses_data[i + 1].split()))
        warehouse = {'w_location': w_location, 'w_products': w_products}
        warehouses.append(warehouse)

    orders_count = int(lines[4 + 2 * warehouses_count])
    orders_data = lines[5 + 2 * warehouses_count:]
    orders = []
    for i in range(0, len(orders_data), 3):
        o_location = tuple(map(int, orders_data[i].split()))
        o_products_count = int(orders_data[i + 1])
        o_products_data = list(map(int, orders_data[i + 2].split()))
        o_products = {product_type: o_products_data.count(product_type) for product_type in set(o_products_data)}
        order = {'o_location': o_location, 'o_products': o_products}
        orders.append(order)

    drones = [{'d_location': warehouses[0]['w_location'], 'd_payload': 0} for _ in range(simulation['drones'])]

    return {'Simulation': simulation, 'ProductType': product_types, 'Warehouse': warehouses, 'Order': orders, 'Drone': drones}

file_path = "a_example.in"
parsed_data = parse_input_file(file_path)

print("Simulation:", parsed_data['Simulation'])
print("ProductType:", parsed_data['ProductType'])
print("Warehouse:", parsed_data['Warehouse'])
print("Order:", parsed_data['Order'])
print("Drone:", parsed_data['Drone'])


# La complexité de cette fonction est de l'ordre O(n).
