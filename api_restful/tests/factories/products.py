# api_restful/tests/factories/products.py

import factory
from api_restful.models import Products, ProductHistory
from api_restful.tests.factories.system_user import SystemUserFactory
from datetime import datetime

class ProductsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Products
        sqlalchemy_session = None 
        sqlalchemy_session_persistence = "flush"

    description = factory.Faker("sentence", nb_words=3)
    price = factory.Faker("pydecimal", left_digits=4, right_digits=2, positive=True)
    barcode = factory.Sequence(lambda n: f"BRCD{n:09d}")
    section = factory.Faker("word")
    initial_stock = factory.Faker("random_int", min=10, max=100)
    expiration_date = factory.Faker("date_between", start_date="+30d", end_date="+365d")


class ProductHistoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ProductHistory
        sqlalchemy_session = None 
        sqlalchemy_session_persistence = "flush"

    product = factory.SubFactory(ProductsFactory)
    user = factory.SubFactory(SystemUserFactory)
    action = factory.Iterator(["created", "updated", "deleted"])
    changed_fields = factory.Faker("sentence", nb_words=6)
    timestamp = factory.LazyFunction(datetime.utcnow)