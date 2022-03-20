from typing import List, Optional
from uuid import uuid4
from faker import Faker
from models.order_line import OrderLine

from models.product import Product


def __generate_product(fake: Faker):
    return Product(name=fake.first_name(), sku=fake.bank_country())


def __generate_order_line(product: Product, quantity: int = 1):
    return OrderLine(uuid4(), product, quantity)


def generate_products(quantity: int = 1):
    if quantity < 1:
        raise ValueError("Quantity must be greater than zero")

    fake = Faker(['pt-BR'])
    products: List[Product] = []

    for _ in range(0, quantity):
        products.append(__generate_product(fake))

    return products


def generate_order_lines(quantity: int = 1, product: Optional[Product] = None):
    if quantity < 1:
        raise ValueError("Quantity must be greater than zero")

    products = None if product else generate_products(quantity)
    order_lines: List[OrderLine] = []

    for r in range(0, quantity):
        p = product if product else products[r]
        order_lines.append(__generate_order_line(p))

    return order_lines
