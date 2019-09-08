import json
import os
import textwrap
_all_products = None


class ProductData():
    """
    Our product records. In this case they come from a json file, but you could
    just as easily load them from a database, or anywhere else.
    """

    def __init__(self, id_, name, image, price):
        self.id = id_
        self.name = name
        self.image = image
        self.price = price

    def __str__(self):
        return textwrap.dedent("""\
            Id: {}
            Name: {}
            ImageUrl: {}
            Price: {} VND
        """).format(self.id, self.name, self.image, self.price)

    def asDict(self):
        return {"id": self.id, "name": self.name,
                "image": self.image, "price": self.price};


def all_products():
    """
    Returns a list of ProductData objects, loaded from
    searchapp/products.json
    """

    global _all_products

    if _all_products is None:
        _all_products = []

        # Load the product json from the same directory as this file.
        dir_path = os.path.dirname(os.path.realpath(__file__))
        products_path = os.path.join(dir_path, 'products.json')
        with open(products_path) as product_file:
            for idx, product in enumerate(json.load(product_file, strict=False)):
                id_ = idx + 1  # ES indexes must be positive integers, so add 1
                product_data = ProductData(id_, **product)
                _all_products.append(product_data)

    return _all_products
