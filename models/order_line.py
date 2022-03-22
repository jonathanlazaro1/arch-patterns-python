from uuid import UUID
from models.product import Product


class OrderLine:
    __order_ref: UUID
    __product: Product
    __quantity: int

    def __init__(self, order_ref: UUID, product: Product, quantity: int):
        self.__order_ref = order_ref
        self.__product = product
        self.__quantity = quantity

    @property
    def order_ref(self):
        return self.__order_ref

    @property
    def product(self):
        return self.__product

    @property
    def quantity(self):
        return self.__quantity

    @quantity.setter
    def quantity(self, qty: int):
        if (qty < 1):
            raise ValueError("Quantity must be greater than zero")

        self.__quantity = qty
