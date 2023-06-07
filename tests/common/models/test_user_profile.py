from django.test import TestCase
from faker import Faker

from common.factories import UserSocialAuthFactory
from common.models import UserProfile

fake = Faker()


class UserProfileTestCase(TestCase):
    def setUp(self):
        self.user = UserProfile.objects.create(
            username=fake.user_name(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email()
        )

    def test_user_profile_without_social_auth(self):
        """
        GIVEN: a user profile without social auth instance
        THEN: return an empty access_token
        """

        self.assertEqual(self.user.social_auth.count(), 0)
        self.assertEqual(self.user.access_token, '')

    def test_user_profile_with_social_auth(self):
        """
        GIVEN: a user profile with social auth instance
        THEN: return an empty access_token
        """

        extra_data = {'access_token': 'token'}
        UserSocialAuthFactory(user=self.user, extra_data=extra_data)
        self.user.refresh_from_db()

        self.assertEqual(self.user.social_auth.count(), 1)
        self.assertEqual(self.user.access_token, extra_data.get('access_token'))
