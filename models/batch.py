from datetime import datetime
from functools import reduce
from typing import List, Optional
from uuid import UUID, uuid4
from models.order_line import OrderLine
from models.product import Product
from utils.datetime import make_timezone_aware_datetime


class Batch:
    __reference: UUID
    __eta: Optional[datetime]
    __product: Product
    __order_lines: List[OrderLine]
    __quantity: int

    def __init__(self, product: Product, quantity: int, utc_eta: Optional[datetime] = None):
        self.__reference = uuid4()
        self.__order_lines = []
        self.__product = product
        self.__quantity = quantity
        self.__eta = None if not utc_eta else make_timezone_aware_datetime(
            utc_eta)

    def __index_of_order_line(self, order_ref: UUID):
        try:
            return next(x[0] for x in enumerate(self.__order_lines) if x[1].order_ref == order_ref)
        except StopIteration as ex:
            raise ValueError(
                f"No order line found to order reference {order_ref}") from ex

    def __upsert_order_line(self, order_line: OrderLine):
        try:
            idx = self.__index_of_order_line(order_line.order_ref)
            self.__order_lines[idx] = order_line
        except ValueError:
            self.__order_lines.append(order_line)

    @property
    def reference(self):
        return self.__reference

    @property
    def eta(self):
        return self.__eta

    @property
    def is_in_stock(self):
        return self.__eta is None

    @property
    def product(self):
        return self.__product

    @property
    def order_lines(self):
        return self.__order_lines

    @property
    def available_quantity(self):
        ols_allocation = reduce(
            lambda a, b: a + b.quantity, self.__order_lines, 0)
        return self.__quantity - ols_allocation

    def find_by_order_ref(self, order_ref: UUID):
        return self.__order_lines[self.__index_of_order_line(order_ref)]

    def available_quantity_for_order_line(self, order_ref: UUID):
        try:
            order_line = self.find_by_order_ref(order_ref)
            return self.available_quantity + order_line.quantity
        except ValueError:
            return self.available_quantity

    def mark_as_shipped(self):
        self.__eta = None

    def allocate_order_line(self, order_line: OrderLine) -> OrderLine:
        if order_line.quantity < 1:
            raise ValueError("Order line quantity must be greater than 0")
        if self.available_quantity_for_order_line(order_line.order_ref) - order_line.quantity < 0:
            raise ValueError(
                "No available quantity in this batch to allocate this order line")
        if order_line.product.id != self.__product.id:
            raise ValueError(
                "Order line must be from the same product as batch")

        self.__upsert_order_line(order_line)

        return order_line

    def remove_order_line(self, order_ref: UUID) -> OrderLine:
        order_line = self.find_by_order_ref(order_ref)
        self.__order_lines.remove(order_line)
        return order_line
