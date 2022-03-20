from random import randint
from typing import List

import pytest
from models.order import Order
from models.product import Product


def test_if_add_order_line_works_as_expected():
    product = Product("Test", "units")
    order = Order()
    quantity = randint(1, 100)
    added_order_line = order.add_order_line(product, quantity)

    assert added_order_line.product == product
    assert added_order_line.quantity == quantity


def test_if_find_order_line_by_product_id_works_as_expected():
    product = Product("Test", "units")
    order = Order()
    quantity = randint(1, 100)
    order.add_order_line(product, quantity)

    assert len(order.order_lines) == 1

    order_line = order.find_by_product_id(product.id)

    assert order_line.product == product
    assert order_line.quantity == quantity


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


def test_if_multiple_order_lines_are_handled_correctly():
    order = Order()
    products: List[Product] = []

    for i in range(1, 10):
        p = Product(f"Test {i}", "units")
        order.add_order_line(p, i)
        products.append(p)

    assert len(order.order_lines) == len(products)

    for i in range(1, 10):
        p = products[i-1]
        order_line = order.find_by_product_id(p.id)
        assert order_line.product == p
        assert order_line.quantity == i


def test_if_remove_order_line_works_as_expected():
    product_1 = Product("Test 1", "units")
    product_2 = Product("Test 2", "units")
    quantity_1 = randint(1, 100)
    quantity_2 = randint(1, 100)

    order = Order()
    order.add_order_line(product_1, quantity_1)
    order.add_order_line(product_2, quantity_2)

    assert len(order.order_lines) == 2

    removed_order_line = order.remove_order_line(product_1.id)

    assert len(order.order_lines) == 1
    assert removed_order_line.product == product_1
    assert removed_order_line.quantity == quantity_1


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
