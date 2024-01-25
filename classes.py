import math
import sys
sys.setrecursionlimit(10000) # pour éviter le dépassement de la limite de récursion

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
            self.payload += quantity * Simulation.product_types[product_type].weight

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
            self.payload -= quantity * Simulation.product_types[product_type].weight

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
