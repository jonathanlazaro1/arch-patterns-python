from typing import List
from uuid import UUID, uuid4
from models.order_line import OrderLine
from models.product import Product


class Order:
    _reference: UUID
    _order_lines: List[OrderLine]

    def __init__(self):
        self._reference = uuid4()
        self._order_lines = []

    @property
    def reference(self):
        return self._reference

    @property
    def order_lines(self):
        return self._order_lines

    def upsert_line(self, product: Product, quantity: int) -> OrderLine:
        if quantity < 1:
            raise ValueError("Order line quantity must be greater than 0")
        (idx, ol) = next((x for x in enumerate(self._order_lines)
                          if x[1].product.id == product.id), None)
        if ol is None:
            ol = OrderLine(self._reference, product, quantity)
            self._order_lines.append(ol)
        else:
            ol.quantity += quantity
            self._order_lines[idx] = ol

        return ol

    def remove_line(self, product_id: UUID) -> OrderLine:
        try:
            order_line = next(
                x for x in self._order_lines if x.product.id == product_id)
            self._order_lines.remove(order_line)
            return order_line
        except StopIteration as ex:
            raise IndexError(
                f"No product in this Order with Id {product_id}") from ex
