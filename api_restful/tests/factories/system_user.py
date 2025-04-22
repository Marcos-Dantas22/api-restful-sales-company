import factory
from api_restful.models import SystemUser
from api_restful.utils.security import hash_password
class SystemUserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = SystemUser
        sqlalchemy_session = None 
        sqlalchemy_session_persistence = "flush"

    username = factory.Sequence(lambda n: f"user{n}")
    password = factory.LazyFunction(
       lambda: hash_password('password12345')
    )
    is_admin = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        if "password" in kwargs:
            kwargs["password"] = hash_password(kwargs.pop("password"))
        return super()._create(model_class, *args, **kwargs)