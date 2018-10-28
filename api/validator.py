import re


class ValidateSale(object):
    """Class to validate a sales record attributes"""

    def __init__(self, name, quantity):
        self.name = name
        self.quantity = quantity

    def validate(self):
        """
        Method validates the attributes of a sale.

        :returns:

        True - if the sale details are all valid.

        False - if one or all of the sale attributes  are invalid.
        """
        if not self.name or not self.quantity or self.name.isspace():
            return False
        else:
            return True


class ValidateProduct(ValidateSale):
    """Class to validate product attributes"""

    def __init__(self, name, quantity, unit_price):
        ValidateSale.__init__(self, name, quantity)
        self.unit_price = unit_price

    def validate(self):
        """
        Method validates the attributes of a product.

        :returns:

        True - if the product details are all valid.

        False - if one or all of the product details  are invalid.
        """
        if not self.name or not self.unit_price or not self.quantity or\
                self.name.isspace():
            return False
        else:
            return True


class ValidateUser:
    """Class to validate user attributes"""

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def validate_username(self):
        """
        Method validates a user's username

        :returns:

        True - if username is valid

        False - if username is not valid
        """

        if not self.username or self.username.isspace() or not isinstance(
                self.username, str):
            return False
        else:
            return True

    def validate_email(self):
        """
        Method validates a user's email

        :returns:

        True - if email is valid

        False - if email is not valid
        """

        if not self.email or not re.match(
                r"[^@.]+@[A-Za-z]+\.[a-z]+", self.email):
                # source: https://docs.python.org/2/howto/regex.html
            return False
        else:
            return True

    def validate_password(self):
        """
        Method validates a user's password

        :returns:

        True - if password is valid

        False - if password is not valid
        """

        lower_case = re.search(r"[a-z]", self.password)
        upper_case = re.search(r"[A-Z]", self.password)
        numbers = re.search(r"[0-9]", self.password)

        if not self.password or not all((lower_case, upper_case, numbers))\
                or not len(self.password) > 5:
            return False
        else:
            return True
