from typing import List
from faker import Faker

from models.product import Product


def __generate_product(fake: Faker):
    return Product(name=fake.first_name(), sku=fake.bank_country())


def generate_products(quantity: int = 1):
    if quantity < 1:
        raise ValueError("Quantity must be greater than zero")

    fake = Faker(['pt-BR'])
    products: List[Product] = []

    for _ in range(0, quantity):
        products.append(__generate_product(fake))

    return products
