from os import getcwd, path
from json import dump, load
from random import randint
from sys import stderr

global cwd
cwd = getcwd()

def write_file(data:dict):
    with open(f"{cwd}/database.json", "w") as file:
        dump(data, file, indent=3)

def read_file():
    with open(f"{cwd}/database.json", "r") as file:
        return load(file)

global database

if not path.exists(f"{cwd}/database.json"):
    write_file({})
    database = {}
else:
    database = read_file()
    
def create_id():
    while True:
        uuid = randint(1111111, 9999999)
        if uuid not in database.keys():
            return uuid

class product:
    def __init__(self, identifier=None):
        self._item = None

        self.productName = None
        self.productId = None
        self.exists = False
        
        if identifier is None:
            self._item = {}
        
        if type(identifier) is str:
            self.productName = identifier.lower()
        elif type(identifier) is int:
            self.productId = identifier

        

    @property
    def item(self):
        if self._item is None:
            if self.productName is not None:
                for item in database.keys():
                    if database[item]["name"] == self.productName:
                        self._item = database[item]
                        self.productId = item
                        break
            elif self.productId is not None:
                if self.productId in database.keys():
                    self._item = database[self.productId]
            if self._item is None:
                self._item = False
            else:
                self.exists = True
        return self._item

    @property
    def productQuantity(self):
        return self.item["quantity"]

    @productQuantity.setter
    def productQuantity(self, value):
        self.item["quantity"] = value
        database[self.productId] = self.item
        self.save()
        
    @property
    def productLocation(self):
        return self.item["location"]

    @productLocation.setter
    def productLocation(self, value):
        self.item["location"] = value
        database[self.productId] = self.item
        self.save()
        
    @property
    def productDepartment(self):
        return self.item["department"]

    @productDepartment.setter
    def productDepartment(self, value):
        self.item["department"] = value
        database[self.productId] = self.item
        self.save()
        
    @property
    def productPrice(self):
        return self.item["price"]

    @productPrice.setter
    def productPrice(self, value):
        self.item["price"] = value
        database[self.productId] = self.item
        self.save()

    def display(self):
        for key in self.item.keys():
            print(f"    {key}: {self.item[key]}")
    
    def create(self):
        global database
        
        if self.productId is None:
            self.productId = create_id()
            
        self._item = {
            "quantity": self.productQuantity,
            "name": self.productName,
            "location": self.productLocation,
            "price": self.productPrice,
            "department": self.productDepartment
        }

        database[self.productId] = self._item
        self.exists = True
        self.save()

        print(f"\nCreated product under ID: {self.productId}")
        self.display()

    def save(self):
        if self.exists:
            write_file(database)

    def __del__(self):
        del database[self.productId]
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

def create_product():
    item = product()
    item.productId = create_id()
    item.productName = input("\nPlease enter the products name:\n")
    item.productQuantity = require_int("\nPlease enter the products quantity:\n")
    item.productLocation = input("\nPlease enter the products location:\n")
    item.productPrice = require_float("\nPlease enter the price of the product:\n")
    item.productDepartment = input("\nPlease enter the department of the product:\n")
    item.create()

def remove_product():
    pass

def search_product():
    identifer = input("\nPlease enter the name or id of the product\n")

    try:
        identifier = int(identifier)
    except:
        pass

    item = product(identifier)
    if item.item is False:
        print("\nThat item does not exist!\n")
        return
    item.display()

while True:
    command = input("\nPlease enter a command:\n    1) Create a product\n    2) Remove a product\n    3) Search a product\n    4) Exit\n")

    try:
        command = int(command)
        if command not in range(1, 5): raise
    except:
        print("\nPlease enter a valid option!\n", file=stderr)
        continue

    if command == 1:
        create_product()
    elif command == 2:
        remove_product()
    elif command == 3:
        search_product()
    elif command == 4:
        break
        

