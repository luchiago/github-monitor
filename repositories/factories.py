import factory
from faker import Faker

from repositories.models import Repository

fake = Faker()


class RepositoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Repository

    name = factory.LazyAttribute(lambda obj: fake.pystr(max_chars=99))
