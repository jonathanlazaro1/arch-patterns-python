from typing import List
from uuid import UUID, uuid4
from models.order_line import OrderLine
from models.product import Product


class Order:
    __reference: UUID
    __order_lines: List[OrderLine]

    def __init__(self):
        self.__reference = uuid4()
        self.__order_lines = []

    def __index_of_order_line(self, product_id: UUID):
        try:
            return next(x[0] for x in enumerate(self._order_lines) if x[1].product.id == product_id)
        except StopIteration as ex:
            raise ValueError(
                f"No order line found to Product Id {product_id}") from ex

    def __upsert_order_line(self, order_line: OrderLine):
        try:
            idx = self._index_of_order_line(order_line.product.id)
            self._order_lines[idx] = order_line
        except ValueError:
            self._order_lines.append(order_line)

    @property
    def reference(self):
        return self.__reference

    @property
    def order_lines(self):
        return self.__order_lines

    def find_by_product_id(self, product_id: UUID):
        return self.__order_lines[self.__index_of_order_line(product_id)]

    def upsert_line(self, product: Product, quantity: int) -> OrderLine:
        if quantity < 1:
            raise ValueError("Order line quantity must be greater than 0")
        order_line = OrderLine(self.__reference, product, quantity)
        self.__upsert_order_line(order_line)

        return order_line

    def remove_line(self, product_id: UUID) -> OrderLine:
        order_line = self.__order_lines[self.__index_of_order_line(product_id)]
        self.__order_lines.remove(order_line)
        return order_line
