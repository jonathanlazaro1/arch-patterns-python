from datetime import datetime
from random import randint
from typing import Optional
from uuid import uuid4
from models.order_line import OrderLine
from models.product import Product
from models.stock import Stock
from tests.helpers import generate_products
from utils.datetime import make_timezone_aware_datetime


def test_if_create_batch_works_as_expected():
    products = generate_products(3)
    stock = Stock()
    expected = []

    for _ in range(0, 10):
        quantity = randint(1, 100)
        product = products[randint(0, len(products) - 1)]
        eta: Optional[datetime] = None
        if randint(0, 2) == 1:
            eta = datetime.utcnow()

        batch = stock.create_batch(product, quantity, eta)
        expected.append({
            "product": product,
            "quantity": quantity,
            "eta": eta,
            "batch_ref": batch.reference
        })

    assert len(stock.batches) == len(expected)

    for item in expected:
        batch = stock.find_batch_by_reference(item["batch_ref"])
        assert batch.product.id == item["product"].id
        assert batch.available_quantity == item["quantity"]
        if item["eta"]:
            assert batch.eta == make_timezone_aware_datetime(item["eta"])
        else:
            assert batch.eta is None


def test_if_allocate_order_line_works_as_expected():
    stock = Stock()
    product = Product("Test", "units")
    quantity = 100
    batch = stock.create_batch(product, quantity)
    batch_ref = batch.reference

    assert len(stock.batches) == 1
    assert stock.find_product_availability(product.id) == quantity

    order_line = OrderLine(uuid4(), product, quantity / 2)
    stock.allocate_order_line(order_line)
    assert stock.find_product_availability(product.id) == quantity / 2

    batch = stock.find_batch_by_reference(batch_ref)
    assert batch.available_quantity == quantity / 2
    assert batch.order_lines[0] == order_line
