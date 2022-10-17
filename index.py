from os import getcwd, path
from json import dump, load
from random import randint
from sys import stderr

def create_id(database):
    while True:
        uuid = randint(1111111, 9999999)
        if uuid not in database.json.keys():
            return uuid

class database:
    def __init__(self):
        self.json = {}
        self.cwd = getcwd()

        if not path.exists(f"{self.cwd}/database.json"):
            self.write(self.json)
        else:
            try:
                self.json = self.load()
            except:
                self.json = {}
                self.save()

    def load(self):
        with open(f"{self.cwd}/database.json", "r") as file:
            return load(file)

    def save(self):
        with open(f"{self.cwd}/database.json", "w") as file:
            dump(self.json, file, indent=3)

class product:
    def __init__(self, database, identifier=None):
        self._item = None
        self.database = database

        self.productName = None
        self.productId = None

        if identifier is None:
            self._item = {}
            self.exists = False
            return

        if type(identifier) is str:
            self.productName = identifier.lower() #Search by name
        elif type(identifier) is int:
            self.productId = identifier #Search by id
        
        self.load_item()

        """
        self._item is None if unloaded, {} if doesnt exist
        """

    def load_item(self):
        if self.productName is not None:
            for item in self.database.json.keys():
                if self.database.json[item]["name"] == self.productName.lower():
                    self._item = self.database.json[item]
                    self.productId = item
                    break
        elif self.productId is not None:
            if str(self.productId) in self.database.json.keys():
                self._item = self.database.json[str(self.productId)]
                self.productName = self._item["name"]

        if self._item != {}:
            self.exists = True

    @property
    def item(self):
        if self._item is None:
            self.load_item()
        return self._item

    @property
    def productQuantity(self):
        return self.item["quantity"]

    @productQuantity.setter
    def productQuantity(self, value):
        self.item["quantity"] = value
        self.database.json[str(self.productId)] = self.item
        self.save()
        
    @property
    def productLocation(self):
        return self.item["location"]

    @productLocation.setter
    def productLocation(self, value):
        value = value.upper()
        self.item["location"] = value
        self.database.json[str(self.productId)] = self.item
        self.save()
        
    @property
    def productDepartment(self):
        return self.item["department"]

    @productDepartment.setter
    def productDepartment(self, value):
        value = value.lower()
        self.item["department"] = value
        self.database.json[str(self.productId)] = self.item
        self.save()
        
    @property
    def productPrice(self):
        return self.item["price"]

    @productPrice.setter
    def productPrice(self, value):
        self.item["price"] = value
        self.database.json[str(self.productId)] = self.item
        self.save()

    def display(self):
        if self.item is False or self.item is None:
            print("This item does not exist!")
        else:
            for key in self.item.keys():
                print(f"    {key}: {self.item[key]}")
            print(f"    id: {self.productId}")
    
    def create(self):        
        if self.productId is None:
            self.productId = create_id(self.database)
            
        self._item = {
            "quantity": self.productQuantity,
            "name": self.productName.lower(),
            "location": self.productLocation,
            "price": self.productPrice,
            "department": self.productDepartment
        }

        self.database.json[str(self.productId)] = self._item
        self.exists = True
        self.save()

        print(f"\nCreated product under ID: {self.productId}")
        self.display()

    def save(self):
        if self.exists:
            self.database.save()

    def delete(self):
        if self.productId in self.database.json:
            del self.database.json[self.productId]
        self.save()

def require_int(prompt):
    while True:
        val = input(prompt)
        
        try:
            val = int(val)
        except:
            print("Please enter a integer!")
        else:
            return val

def require_float(prompt):
    while True:
        val = input(prompt)
        
        try:
            val = float(val)
        except:
            print("Please enter a decimal integer!")
        else:
            return val

def get_product(db, valid):
    while True:
        item = input("Please enter the name or Id of the product or type 'exit' to exit:\n")

        if item.lower() == "exit":
            return
        
        try:
            item = int(item)
        except:
            pass

        item = product(db, item)
        
        if not valid or item.exists:
            return item
        else:
            print("\nThat isnt a valid item!\n")

def create_product(db):
    item = product(db)
    item.productId = create_id(db)
    item.productName = input("\nPlease enter the products name:\n")
    item.productQuantity = require_int("\nPlease enter the products quantity:\n")
    item.productLocation = input("\nPlease enter the products location:\n")
    item.productPrice = require_float("\nPlease enter the price of the product:\n")
    item.productDepartment = input("\nPlease enter the department of the product:\n")
    item.create()

def remove_product(db):
    item = get_product(db, valid=True)
    if item is None: return
    item.delete()
    print("\nItem deleted\n")

def search_product(db):
    item = get_product(db, valid=True)
    if item is None: return
    item.display()

def display_all_products(db):
    print()

    departments = {}

    for key in db.json.keys():
        if db.json[key]["department"] in departments.keys():
            departments[db.json[key]["department"]].append(product(db, int(key)))
        else:
            departments[db.json[key]["department"]] = [product(db, int(key))]
    
    for department in departments.keys():
        print(f"{department[0].upper()}{department[1:]}: ")
        for item in departments[department]:
            print(f"    {item.productName}")

def reduce_stock(db):
    item = get_product(db, valid=True)
    if item is None: return
    quantity = require_int("How much would you like to reduce the stock by?\n")

    if quantity > item.productQuantity:
        print("\nThat number is more than the current stock!")
        return

    item.productQuantity -= quantity

    print(f"\nThe quantity for {item.productName} has been corrected and is now {item.productQuantity}!\n")
    

db = database()

while True:
    command = input("\nPlease enter a command:\n    1) Create a product\n    2) Delete a product\n    3) Search a product\n    4) List all products\n    5) Reduce the stock on a product\n    6) Exit\n")

    try:
        command = int(command)
        if command not in range(1, 7): raise
    except:
        print("\nPlease enter a valid option!\n", file=stderr)
        continue

    if command == 1:
        create_product(db) #Done
    elif command == 2:
        remove_product(db)
    elif command == 3:
        search_product(db) #Done
    elif command == 4:
        display_all_products(db) #Done
    elif command == 5:
        reduce_stock(db)
    elif command == 6:
        break
        

