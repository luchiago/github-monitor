from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    def __str__(self):
        return self.username

    @property
    def access_token(self) -> str:
        social_auth_profile = self.social_auth.first()  # pylint: disable=no-member
        if social_auth_profile is not None:
            return social_auth_profile.access_token
        return ''
