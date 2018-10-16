class Product:
    products = []

    def __init__(self, *args):
        self.name = args[0]
        self.unit_price = args[1]
        self.quantity = args[2]
        self._id = args[3]

    def validate_product(self):
        if not self.name or not self.unit_price or not self.quantity or\
                self.name.isspace() or self.quantity.isspace():
            return False
        else:
            return True


class Sale:
    sales = []

    def __init__(self, *args, total=0):
        self.item_name = args[0]
        self.unit_price = args[1]
        self.quantity = args[2]
        self.total = total

    def validate_sale(self):
        """
        Method validates a sale.

        :returns:

        True - if the sale is valid.

        False - if the sale is invalid.
        """
        if self.item_name == '' or not self.unit_price or not self.quantity or\
                self.item_name.isspace() or self.quantity.isspace():
            return False
        else:
            return True
