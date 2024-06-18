class Product:
    def __init__(self, name, price, category):
        # Initialize product attributes
        self._name = name
        self._price = price
        self._category = category

    # Define how products are classified
    def __eq__(self, other):
        if isinstance(other, Product):
            if (self._name == other._name and self._price == other._price) and (self._category == other._category):
                return True
            else:
                return False
        else:
            return False

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_category(self):
        return self._category

    # Implement string representation
    def __repr__(self):
        rep = 'Product(' + self._name + ',' + str(self._price) + ',' + self._category + ')'
        return rep


class Inventory:
    def __init__(self):
        # initialize inventory list
        self.inventory_list = []

    def add_to_productInventory(self, productName, productPrice, productQuantity):

        # dictionary for the product and its price and quantity and appending it to the inventory list
        inventory_dict = {
            "product name": productName,
            "product price": productPrice,
            "product quantity": productQuantity
        }

        self.inventory_list.append(inventory_dict)

    def add_productQuantity(self, nameProduct, addQuantity):

        # adding quantity to a product in the inventory list
        for product in self.inventory_list:
            if product["product name"] == nameProduct:
                product["product quantity"] += addQuantity

    def remove_productQuantity(self, nameProduct, removeQuantity):

        # removing quantity from a product in the inventory list
        for product in self.inventory_list:
            if product["product name"] == nameProduct:
                product["product quantity"] -= removeQuantity

    def get_productPrice(self, nameProduct):

        # getting the price of a product in the inventory
        for product in self.inventory_list:
            if product["product name"] == nameProduct:
                return product["product price"]

    def get_productQuantity(self, nameProduct):

        # getting the quantity of a product in the inventory
        for product in self.inventory_list:
            if product["product name"] == nameProduct:
                return product["product quantity"]

    def display_Inventory(self):

        # displaying the inventory
        for product in self.inventory_list:
            product_name = product["product name"]
            product_price = product["product price"]
            product_quantity = product["product quantity"]
            print("{}, {}, {}".format(product_name, product_price, product_quantity))


# populating inventory form a file
def populate_inventory(filename):

    # creating an inventory object
    inventory = Inventory()

    try:
        # trying to open the file
        read_file = open(filename, "r")
        read_file_lines = read_file.readlines()

        # looping through each line of the file and adding the products to the inventory
        for lines in read_file_lines:
            lines = lines.strip().split(",")
            productName = lines[0]
            productPrice = int(lines[1])
            productQuantity = int(lines[2])

            inventory.add_to_productInventory(productName, productPrice, productQuantity)

    # exception if error opening file
    except IOError:
        print("Could not read file")

    return inventory


class ShoppingCart:

    def __init__(self, buyerName, inventory):

        # Initializing the shoppingcart with buyer name and inventory
        self._buyerName = buyerName
        self.inventory = inventory
        self.shopping_cart_list = []

    def add_to_cart(self, nameProduct, requestedQuantity):

        # adding a product to the shopping cart with the name and requested quantity of the product and appending it
        # to the list
        shopping_cart_dict = {
            "product name": nameProduct,
            "requested quantity": requestedQuantity,
        }

        product_available_quantity = self.inventory.get_productQuantity(nameProduct)

        # checking if there is more quantity of the product in the inventory than the requested quantity
        if product_available_quantity >= requestedQuantity:

            # reducing the available quantity in the inventory and adding the requesting quantity in shopping cart
            product_available_quantity -= requestedQuantity
            self.inventory.remove_productQuantity(nameProduct, requestedQuantity)
            self.shopping_cart_list.append(shopping_cart_dict)
            return "Filled the order"

        else:
            return "Can not fill the order"

    def remove_from_cart(self, nameProduct, requestedQuantity):

        # removing a product from the shopping cart with the specific product name and quantity
        for items in self.shopping_cart_list:
            if items["product name"] == nameProduct:
                if items["requested quantity"] <= requestedQuantity:

                    # removing products from cart and adjusting the quantities
                    requestedQuantity -= items["requested quantity"]
                    self.shopping_cart_list.remove(items)
                    self.inventory.add_productQuantity(nameProduct, items["requested quantity"])
                    return "Successful"

                else:
                    return "The requested quantity to be removed from cart exceeds what is in the cart"
            else:
                return "Product not found in cart"

    def view_cart(self):
        # Viewing the contents of the shopping cart and calculating the total

        total = 0
        product_track = {}

        for product in self.shopping_cart_list:
            product_name = product["product name"]
            product_price = self.inventory.get_productPrice(product_name)
            product_quantity = product["requested quantity"]

            total += (product_price * product_quantity)

            # tracking the product quantities and adding the quantities that are the same product
            if product_name in product_track:
                product_track[product_name] += product_quantity
            else:
                product_track[product_name] = product_quantity

        # displaying the product total, quantities, product name, and buyer name
        for product_name, quantity in product_track.items():
            print("{} {}".format(product_name, quantity))

        print("Total: {} ".format(total))
        print("Buyer Name: {}".format(self._buyerName))


class ProductCatalog:
    def __init__(self):

        # initializing a product catalog list
        self.product_catalog_list = []

    def addProduct(self, product):

        # adding a product to the product catalog
        product_catalog_dict = {
            "product": product

        }
        self.product_catalog_list.append(product_catalog_dict)

    def price_category(self):

        # categorizing products based on their prices
        low_prices = set()
        medium_prices = set()
        highPrices = set()

        for items in self.product_catalog_list:
            product = items["product"]
            price_of_item = product.get_price()

            if 0 <= price_of_item <= 99:
                low_prices.add(product.get_name())

            elif 100 <= price_of_item <= 499:
                medium_prices.add(product.get_name())

            elif price_of_item >= 500:
                highPrices.add(product.get_name())

        print("Number of low price items: {}\nNumber of medium price items: {}\n"
              "Number of high price items: {}".format(len(low_prices), len(medium_prices), len(highPrices)))

    def display_catalog(self):

        # displaying the catalog
        for items in self.product_catalog_list:
            product = items["product"]
            name_of_product = product.get_name()
            price_of_item = product.get_price()
            category_of_item = product.get_category()
            print("Product: {} Price: {} Category: {}".format(name_of_product, price_of_item, category_of_item))


def populate_catalog(filename):
    # Creating a populate catalog object and populating it with data from a file
    product_catalog = ProductCatalog()

    # opening file
    read_file = open(filename, "r")
    read_file_lines = read_file.readlines()

    # looping through each line in the file and adding the products to the catalog
    for lines in read_file_lines:
        lines = lines.strip().split(",")
        productName = lines[0]
        productPrice = int(lines[1])
        productCategory = lines[3]

        # creating a product object and adding it to the product catalog by invoking the add product method
        product = Product(productName, productPrice, productCategory)
        product_catalog.addProduct(product)

    return product_catalog
