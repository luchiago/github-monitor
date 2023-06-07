import factory
from faker import Faker
from social_django.models import UserSocialAuth

from common.models import UserProfile

fake = Faker()


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile

    username = factory.LazyAttribute(lambda obj: fake.user_name())
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class UserSocialAuthFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserSocialAuth

    user = factory.SubFactory(UserProfileFactory)
    provider = 'github'
    uid = factory.LazyAttribute(lambda obj: fake.unique.uuid4())
    extra_data = factory.Dict(
        {
            'auth_time': fake.date_time_this_month().timestamp(),
            'id': fake.random_number(digits=6),
            'expires': fake.future_datetime().isoformat(),
            'login': factory.SelfAttribute('..user.username'),
            # Doesn't need to be a unique UUID/Token string like UserSocialAuthFactory.uid
            'access_token': fake.uuid4(),
            'token_type': 'bearer',
        }
    )
