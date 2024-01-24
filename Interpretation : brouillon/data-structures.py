    '''
    Soit le fichier d'entrée suivant:

    Pour le fichier d'entree suivant:
    100 100 3 50 500
    3
    100 5 450
    2
    0 0
    5 1 0
    5 5
    0 10 2
    3
    1 1
    2
    2 0
    3 3
    1
    0
    5 6
    1
    2
'''
# On utilise cette structure pour stocker nos données en entrée

    Simulation = {
        rows: 100,
        columns: 100,
        drones: 3,
        turns: 50,
        max_payload: 500,
        productType: 3
    }

    Drone = [
        {
            'd_location': (0, 0),
            'd_payload': 0,
        },
        {
            'd_location': (0, 0),
            'd_payload': 0,
        },
        {
            'd_location': (0, 0),
            'd_payload': 0,
        }
    ]

    ProductType = [
        {
            'weight': 100
        },
        {
            'weight': 5
        },
        {
            'weight': 450
        }
        
    ]

    Warehouse = [
        {
            'w_location': (0, 0),
            'w_products': [5, 1, 0]
        },
        {
            'w_location': (5, 5),
            'w_products': [10, 0, 2]
        }
    ]

    Order = [
        {
            'o_location': (1, 1),
            'o_products': {2: 1, 0: 1}
        },
        {
            'o_location': (3, 3),
            'o_products': {0: 1}
        },
        {
            'o_location': (5, 6),
            'o_products': {2: 1}
        }
    ]
