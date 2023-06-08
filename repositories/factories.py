import factory
from faker import Faker

from repositories.models import Commit, Repository

fake = Faker()


class RepositoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Repository

    name = factory.LazyAttribute(lambda obj: fake.pystr(max_chars=99))


class CommitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Commit

    message = fake.sentence(nb_words=6)
    sha = fake.pystr(max_chars=99)
    author = fake.name()
    url = fake.url()
    date = fake.date_time_this_month()
    avatar = fake.url()
    repository = factory.SubFactory(RepositoryFactory)
