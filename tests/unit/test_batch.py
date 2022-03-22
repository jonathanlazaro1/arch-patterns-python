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
def test_if_allocate_order_line_with_invalid_quantity_raises(quantity: int):
    product = Product("Test", "units")
    batch = Batch(product, 1)
    order_line = OrderLine(uuid4(), product, quantity)

    with pytest.raises(ValueError) as ex:
        batch.allocate_order_line(order_line)

    assert str(ex.value) == "Order line quantity must be greater than 0"


def test_if_allocate_same_order_line_multiple_times_correctly_updates_it_while_preserving_quantities():
    product = Product("Test", "units")
    batch = Batch(product, 10)
    order_line = OrderLine(uuid4(), product, 1)

    for r in range(0, 10):
        order_line.quantity = r+1
        batch.allocate_order_line(order_line)
        allocated_order_line = batch.find_by_order_ref(order_line.order_ref)

        assert order_line == allocated_order_line
        assert len(batch.order_lines) == 1
        assert batch.available_quantity == 10 - (r+1)


def test_if_allocate_new_order_line_above_available_quantity_raises():
    product = Product("Test", "units")
    order_line_1 = OrderLine(uuid4(), product, 2)
    order_line_2 = OrderLine(uuid4(), product, 1)

    batch = Batch(product, order_line_1.quantity)

    batch.allocate_order_line(order_line_1)
    assert len(batch.order_lines) == 1
    assert batch.available_quantity == 0

    with pytest.raises(ValueError) as ex:
        batch.allocate_order_line(order_line_2)

    assert str(
        ex.value) == "No available quantity in this batch to allocate this order line"


def test_if_already_allocated_order_line_raises_when_above_available_quantity():
    product = Product("Test", "units")
    order_line_1 = OrderLine(uuid4(), product, 2)

    batch = Batch(product, order_line_1.quantity)

    batch.allocate_order_line(order_line_1)
    assert len(batch.order_lines) == 1
    assert batch.available_quantity == 0

    order_line_1.quantity = 3
    with pytest.raises(ValueError) as ex:
        batch.allocate_order_line(order_line_1)

    assert str(
        ex.value) == "No available quantity in this batch to allocate this order line"


def test_if_allocate_order_line_with_different_product_from_batch_raises():
    product_1 = Product("Test 1", "units")
    product_2 = Product("Test 2", "units")

    batch = Batch(product_1, 10)
    order_line = OrderLine(uuid4(), product_2, 1)

    with pytest.raises(ValueError) as ex:
        batch.allocate_order_line(order_line)

    assert str(ex.value) == "Order line must be from the same product as batch"


def test_if_find_order_line_by_order_ref_raises_when_not_found():
    product = Product("Test", "units")
    order_line_1 = OrderLine(uuid4(), product, 1)
    order_line_2 = OrderLine(uuid4(), product, 1)

    batch = Batch(product, 10)
    batch.allocate_order_line(order_line_1)

    assert len(batch.order_lines) == 1

    with pytest.raises(ValueError) as ex:
        batch.find_by_order_ref(order_line_2.order_ref)

    assert str(
        ex.value) == f"No order line found to order reference {order_line_2.order_ref}"


def test_if_remove_order_line_works_as_expected():
    product = Product("Test", "units")
    batch = Batch(product, 10)

    assert batch.product == product

    order_lines = generate_order_lines(10, product)
    order_refs = [ol.order_ref for ol in order_lines]
    [batch.allocate_order_line(ol) for ol in order_lines]

    assert len(batch.order_lines) == len(order_refs)

    for r in range(0, len(batch.order_lines)):
        order_ref = order_refs[r]
        removed_order_line = batch.remove_order_line(order_ref)

        assert removed_order_line.order_ref == order_ref
        assert len(batch.order_lines) == 10 - (r+1)
        assert batch.available_quantity == 0 + (r+1)


def test_if_remove_order_line_raises_when_not_found():
    product = Product("Test", "units")
    order_line_1 = OrderLine(uuid4(), product, 1)
    order_line_2 = OrderLine(uuid4(), product, 1)

    batch = Batch(product, 10)
    batch.allocate_order_line(order_line_1)

    assert len(batch.order_lines) == 1

    with pytest.raises(ValueError) as ex:
        batch.remove_order_line(order_line_2.order_ref)

    assert str(
        ex.value) == f"No order line found to order reference {order_line_2.order_ref}"
