from functools import reduce
from uuid import uuid4

import pytest
from models.batch import Batch
from models.order_line import OrderLine
from models.product import Product
from tests.helpers import generate_order_lines


def test_if_allocate_order_line_works_as_expected():
    product = Product("Test", "units")
    batch_quantity = 100
    batch = Batch(product, batch_quantity)

    assert batch.product == product

    order_lines = generate_order_lines(10, product)
    order_refs = [ol.order_ref for ol in order_lines]
    [batch.allocate_order_line(ol) for ol in order_lines]

    assert len(batch.order_lines) == len(order_refs)
    allocated_quantity = reduce(lambda a, b: a + b.quantity, order_lines, 0)
    assert batch.available_quantity == batch_quantity - allocated_quantity

    for r in range(0, len(batch.order_lines)):
        order_ref = order_refs[r]
        order_line = batch.find_by_order_ref(order_ref)

        assert order_line.order_ref == order_ref
        assert order_line.product.id == product.id
        assert order_line.quantity == 1


@pytest.mark.parametrize("quantity", [-1, 0])
def test_if_allocate_order_line_with_invalid_quantity_throws(quantity: int):
    product = Product("Test", "units")
    batch = Batch(product, 1)
    order_line = OrderLine(uuid4(), product, quantity)

    with pytest.raises(ValueError) as ex:
        batch.allocate_order_line(order_line)

    assert str(ex.value) == "Order line quantity must be greater than 0"
