from random import randint
from typing import List
from uuid import UUID

import pytest
from models.order import Order
from models.product import Product


def test_if_add_order_line_works_as_expected():
    order = Order()
    product_ids: List[UUID] = []

    for r in range(1, 10):
        product_id = Product(f"Test {r}", "units")
        order.add_order_line(product_id, r)
        product_ids.append(product_id.id)

    assert len(order.order_lines) == len(product_ids)

    for r in range(1, len(order.order_lines)):
        product_id = product_ids[r-1]
        order_line = order.find_by_product_id(product_id)
        assert order_line.product.id == product_id
        assert order_line.quantity == r


@pytest.mark.parametrize("quantity", [-1, 0])
def test_if_add_order_line_with_invalid_quantity_throws(quantity: int):
    product = Product("Test", "units")
    order = Order()

    with pytest.raises(ValueError) as ex:
        order.add_order_line(product, quantity)

    assert str(ex.value) == "Order line quantity must be greater than 0"


def test_if_add_same_product_multiple_times_correctly_updates_it():
    product = Product("Test", "units")
    order = Order()

    for _ in range(1, 10):
        quantity = randint(1, 100)
        added_order_line = order.add_order_line(product, quantity)

        assert added_order_line.product == product
        assert added_order_line.quantity == quantity
        assert len(order.order_lines) == 1


def test_if_find_order_line_by_product_id_throws_when_not_found():
    product_1 = Product("Test 1", "units")
    product_2 = Product("Test 2", "units")

    order = Order()
    quantity = randint(1, 100)
    order.add_order_line(product_1, quantity)

    assert len(order.order_lines) == 1

    with pytest.raises(ValueError) as ex:
        order.find_by_product_id(product_2.id)

    assert str(ex.value) == f"No order line found to Product Id {product_2.id}"


def test_if_remove_order_line_works_as_expected():
    order = Order()
    product_ids: List[UUID] = []

    for i in range(1, 10):
        p = Product(f"Test {i}", "units")
        order.add_order_line(p, i)
        product_ids.append(p.id)

    for r in range(len(order.order_lines) - 1, 0):
        product_id = product_ids[r]
        order_line = order.remove_order_line(product_id)

        assert order_line.product.id == product_id
        assert order_line.quantity == r+1
        assert len(order.order_lines) == r


def test_if_remove_order_line_throws_when_not_found():
    product_1 = Product("Test 1", "units")
    product_2 = Product("Test 2", "units")

    order = Order()
    quantity = randint(1, 100)
    order.add_order_line(product_1, quantity)

    assert len(order.order_lines) == 1

    with pytest.raises(ValueError) as ex:
        order.remove_order_line(product_2.id)

    assert str(ex.value) == f"No order line found to Product Id {product_2.id}"
