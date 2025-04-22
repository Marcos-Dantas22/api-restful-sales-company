import factory
from api_restful.models import Clients
from api_restful.tests.factories.system_user import SystemUserFactory 

class ClientsFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Clients
        sqlalchemy_session = None 
        sqlalchemy_session_persistence = "flush"

    user = factory.SubFactory(SystemUserFactory)
    full_name = factory.Faker("name")
    cpf = factory.Sequence(lambda n: f"{n:011d}") 
    gender = factory.Iterator(["male", "female", "other"])  
    email = factory.LazyAttribute(lambda obj: f"{obj.full_name.replace(' ', '.').lower()}@example.com")
    phone = factory.Faker("phone_number")
    birth_date = factory.Faker("date_of_birth")
    address = factory.Faker("street_address")
    city = factory.Faker("city")
    state = factory.Faker("state_abbr")
