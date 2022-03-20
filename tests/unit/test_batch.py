from random import randint
from typing import List
from uuid import UUID, uuid4
from models.batch import Batch
from models.order_line import OrderLine
from tests.helpers import generate_products


def test_if_allocate_order_line_works_as_expected():
    product = generate_products()[0]
    batch = Batch(product, 1000)

    assert batch.product == product

    order_refs: List[UUID] = []
    for r in range(0, 10):
        order_ref = uuid4()
        order_line = OrderLine(order_ref, product, r+1)
        batch.allocate_order_line(order_line)
        order_refs.append(order_ref)

    assert len(batch.order_lines) == len(order_refs)

    for r in range(0, len(batch.order_lines)):
        order_ref = order_refs[r]
        order_line = batch.find_by_order_ref(order_ref)

        assert order_line.order_ref == order_ref
        assert order_line.product.id == product.id
        assert order_line.quantity == r+1
