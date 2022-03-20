from random import randint

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

    fetched_order_line = order.find_by_product_id(product.id)

    assert fetched_order_line.product == product
    assert fetched_order_line.quantity == quantity


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
