from uuid import UUID
from models.product import Product


class OrderLine:
    __order_ref: UUID
    __product: Product
    quantity: int

    def __init__(self, order_ref: UUID, product: Product, quantity: int):
        self.__order_ref = order_ref
        self.__product = product
        self.quantity = quantity

    @property
    def order_ref(self):
        return self.__order_ref

    @property
    def product(self):
        return self.__product
