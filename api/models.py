class Product:
    products = []

    def __init__(self, *args):
        self.name = args[0]
        self.unit_price = args[1]
        self.quantity = args[2]

    def validate_product(self):
        if not self.name or not self.unit_price or not self.quantity or\
                self.name.isspace() or self.quantity.isspace():
            return False
        else:
            return True
