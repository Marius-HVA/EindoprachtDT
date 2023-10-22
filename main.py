# As a supermarket employee,
# Want a system that can calculate how many colo I need to order basted on sales and inventory,
# so that I can save time to help customers.

import json
import math


class StoreItem:
    def __init__(self, name, stock, min_stock, colo_count):
        self.name = name
        self.stock = stock
        self.min_stock = min_stock
        self.colo_count = colo_count

    def calculate_order(self):
        if self.stock >= self.min_stock: return 0

        items_to_order = self.min_stock - self.stock
        return math.ceil(items_to_order / self.colo_count)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)


def get_items_from_db():
    items = []
    with open("db.txt", 'r') as file:
        json_data = json.load(file)
        for value in json_data:
            items.append(StoreItem(**json.loads(value)))
    return items


def store_items_in_db(items):
    with open("db.txt", 'w') as file:
        item_list = []
        for item in items:
            item_list.append(item.to_json())

        file.write(json.dumps(item_list))


def calculate_orders():
    store_items = get_items_from_db()
    for item in store_items:
        item_sold = int(input("How many {0}'s have sold: ".format(item.name)))
        old_stock = item.stock
        item.stock -= item_sold
        colo_to_order = item.calculate_order()
        print("The old stock was {0}, the new stock {1}. You need to order {2} colo".format(old_stock, item.stock,
                                                                                            colo_to_order))

        if colo_to_order > 0:
            add_order_to_stock = input('Do you want to add the order to the stock? (y/n): ').lower().strip() == 'y'
            if add_order_to_stock:
                item.stock += colo_to_order * item.colo_count
    store_items_in_db(store_items)


def add_item():
    store_item = StoreItem(
        input("Name of item: "),
        int(input("Current stock: ")),
        int(input("Minimum stock: ")),
        int(input("Items in colo: "))
    )
    current_items = get_items_from_db()

    for item in current_items:
        if item.name == store_item.name:
            print("Name already exists")
            return
    current_items.append(store_item)
    store_items_in_db(current_items)


def remove_item():
    name_of_item_to_remove = input("Name of item to remove:")
    current_items = get_items_from_db()
    for item in current_items:
        if item.name == name_of_item_to_remove:
            current_items.remove(item)
    store_items_in_db(current_items)


if __name__ == '__main__':
    while True:
        print("(1) Calculate order")
        print("(2) Add item")
        print("(3) Remove item")
        print("(4) Exit")
        user_requested_option = int(input("Choose a option? (1/4): "))

        match user_requested_option:
            case 1:
                calculate_orders()
            case 2:
                add_item()
            case 3:
                remove_item()
            case 4:
                break
