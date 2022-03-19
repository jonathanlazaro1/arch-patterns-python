from uuid import UUID
from models.product import Product


class OrderLine:
    _order_ref: UUID
    _product: Product
    quantity: int

    def __init__(self, order_ref: UUID, product: Product, quantity: int):
        self._order_ref = order_ref
        self._product = product
        self.quantity = quantity

    @property
    def order_ref(self):
        return self._order_ref

    @property
    def product(self):
        return self._product
