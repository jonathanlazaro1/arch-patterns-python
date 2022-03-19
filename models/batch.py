from datetime import datetime
from functools import reduce
from typing import List, Optional
from uuid import UUID, uuid4
from models.order_line import OrderLine
from models.product import Product
from utils.datetime import make_timezone_aware_datetime


class Batch:
    _reference: UUID
    _eta: Optional[datetime]
    _product: Product
    _order_lines: List[OrderLine]
    _quantity: int

    def __init__(self, product: Product, quantity: int, utc_eta: Optional[datetime]):
        self._reference = uuid4()
        self._order_lines = []
        self._product = product
        self._quantity = quantity
        if utc_eta:
            self._eta = make_timezone_aware_datetime(utc_eta)

    def _index_of_order_line(self, order_ref: UUID):
        try:
            return next(x[0] for x in enumerate(self._order_lines) if x[1].order_ref == order_ref)
        except StopIteration as ex:
            raise ValueError(
                f"No order line found to order reference {order_ref}") from ex

    def _upsert_order_line(self, order_line: OrderLine):
        try:
            idx = self._index_of_order_line(order_line.order_ref)
            self._order_lines[idx] = order_line
        except ValueError:
            self._order_lines.append(order_line)

    @property
    def reference(self):
        return self._reference

    @property
    def eta(self):
        return self._eta

    @property
    def is_in_stock(self):
        return self._eta is None

    @property
    def product(self):
        return self._product

    @property
    def order_lines(self):
        return self._order_lines

    @property
    def available_quantity(self):
        ols_allocation = reduce(
            lambda a, b: a + b.quantity, self._order_lines, 0)
        return self._quantity - ols_allocation

    def find_by_order_ref(self, order_ref: UUID):
        return self._order_lines[self._index_of_order_line(order_ref)]

    def available_quantity_for_order_line(self, order_ref: UUID):
        try:
            order_line = self.find_by_order_ref(order_ref)
            return self.available_quantity + order_line.quantity
        except ValueError:
            return self.available_quantity

    def mark_as_shipped(self):
        self._eta = None

    def allocate_order_line(self, order_line: OrderLine) -> OrderLine:
        if order_line.quantity < 1:
            raise ValueError("Order line quantity must be greater than 0")
        if self.available_quantity_for_order_line(order_line.order_ref) - order_line.quantity < 0:
            raise ValueError(
                "No available quantity in this batch to allocate this order line")
        if order_line.product.id != self._product.id:
            raise ValueError(
                "Order line must be from the same product as batch")

        self._upsert_order_line(order_line)

        return order_line

    def remove_order_line(self, order_ref: UUID) -> OrderLine:
        order_line = self.find_by_order_ref(order_ref)
        self._order_lines.remove(order_line)
        return order_line
