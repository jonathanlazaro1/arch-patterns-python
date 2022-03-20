from random import randint
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
