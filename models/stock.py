from datetime import datetime
from functools import reduce
from typing import List, Optional
from uuid import UUID

from models.batch import Batch
from models.order import OrderLine
from models.product import Product


class Stock:
    __batches: List[Batch]

    def __init__(self):
        self.__batches = []

    def __get_batches_by_availability_and_eta(self):
        return sorted(self.__batches, key=lambda b: (b.is_in_stock, b.eta), reverse=True)

    def __index_of_batch(self, reference: UUID):
        try:
            return next(x[0] for x in enumerate(self.__batches) if x[1].reference == reference)
        except StopIteration as ex:
            raise ValueError(
                f"No batch found to reference {reference}") from ex

    def __index_of_batch_by_product(self, product_id: UUID):
        try:
            return next(x[0] for x in enumerate(self.__batches) if x[1].product.id == product_id)
        except StopIteration as ex:
            raise ValueError(
                f"No batch found containing product Id {product_id}") from ex

    def __find_batch_by_order_line(self, order_ref: UUID):
        for batch in self.__batches:
            try:
                batch.find_by_order_ref(order_ref)
                return batch
            except ValueError:
                continue
        return None

    def __update_batch(self, batch: Batch):
        self.__batches[self.__index_of_batch(batch.reference)] = batch

    def find_batch_by_reference(self, reference: UUID):
        return self.__batches[self.__index_of_batch(reference)]

    def find_batch_by_product(self, product_id: UUID):
        return self.__batches[self.__index_of_batch_by_product(product_id)]

    def find_product_availability(self, product_id: UUID) -> int:
        batches = [x for x in self.__batches if x.product.id == product_id]
        return reduce(lambda a, b: a + b.available_quantity, batches, 0)

    def create_batch(self, product: Product, quantity: int, utc_eta: Optional[datetime] = None):
        batch = Batch(product, quantity, utc_eta)
        self.__batches.append(batch)
        return batch

    def mark_batch_as_shipped(self, batch_ref: UUID):
        batch = self.find_batch_by_reference(batch_ref)
        batch.mark_as_shipped()
        self.__update_batch(batch)

        return batch

    def allocate_order_line(self, order_line: OrderLine):
        batch = self.__find_batch_by_order_line(order_line.order_ref)
        if batch:
            batch.allocate_order_line(order_line)
            self.__update_batch(batch)
            return batch

        batches = self.__get_batches_by_availability_and_eta()
        batches = [b for b in batches if b.product.id == order_line.product.id]
        for batch in batches:
            if batch.available_quantity >= order_line.quantity:
                batch.allocate_order_line(order_line)
                return batch

        raise IndexError("No batch found to allocate order line")
