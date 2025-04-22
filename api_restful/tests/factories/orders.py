# api_restful/tests/factories/orders.py

import factory
from datetime import datetime, timezone

from api_restful.models import Orders, OrdersProducts
from api_restful.tests.factories.clients import ClientsFactory
from api_restful.tests.factories.products import ProductsFactory


class OrdersFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Orders
        sqlalchemy_session = None 
        sqlalchemy_session_persistence = "flush"

    client = factory.SubFactory(ClientsFactory)
    status = factory.Iterator(["created", "processing", "completed", "cancelled"])


class OrdersProductsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = OrdersProducts
        sqlalchemy_session = None  
        sqlalchemy_session_persistence = "flush"

    order = factory.SubFactory(OrdersFactory)
    product = factory.SubFactory(ProductsFactory)

    product_description = factory.LazyAttribute(lambda o: o.product.description)
    product_price = factory.LazyAttribute(lambda o: o.product.price)
    product_barcode = factory.LazyAttribute(lambda o: o.product.barcode)
    section = factory.LazyAttribute(lambda o: o.product.section)
    product_actual_stock = factory.LazyAttribute(lambda o: o.product.initial_stock)
    order_quantity = factory.Faker("random_int", min=1, max=5)

    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    updated_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
