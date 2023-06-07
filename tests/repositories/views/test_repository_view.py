from unittest.mock import Mock, patch

from django.urls import reverse
from faker import Faker
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.test import APITestCase

from common.factories import UserSocialAuthFactory
from repositories.models import Repository

fake = Faker()


class RepositoryViewTest(APITestCase):
    def setUp(self):
        self.user = UserSocialAuthFactory().user

        self.client.force_authenticate(user=self.user)
        self.url = reverse('repositories:repositories-create')

    @patch('repositories.repository_search.RepositorySearch.search', return_value=False)
    def test_create_repository_fail(self, mock_search):
        """
        GIVEN: an invalid repository name
        THEN: return not found status with an error message
        AND: do not create a Repository object
        """

        data = {
            'values': f'{self.user.username}/invalid-repository-name',
            'name': 'invalid-repository-name',
        }

        response = self.client.post(self.url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response_data,
            {
                'message': 'The requested repository does not exist',
            }
        )
        self.assertEqual(Repository.objects.count(), 0)

        mock_search.assert_called_once()

    @patch('repositories.repository_search.RepositorySearch.search', return_value=True)
    def test_create_repository_with_error_on_serializer(self, mock_search):
        """
        GIVEN: a invalid repository name
        AND: serializer validation error
        THEN: return bad request status
        AND: do not create a Repository object
        """

        invalid_str_size = Repository._meta.get_field('name').max_length + 1
        longe_name = fake.pystr(
            min_chars=invalid_str_size,
            max_chars=(invalid_str_size + 10),
        )

        data = {
            'values': f'{self.user.username}/{longe_name}',
            'name': longe_name,
        }

        response = self.client.post(self.url, data, format='json')

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_data,
            {
                'name': [
                    'Ensure this field has no more than 100 characters.',
                ],
            }
        )
        self.assertEqual(Repository.objects.count(), 0)

        mock_search.assert_called_once()

    @patch('repositories.repository_search.RepositorySearch.search', return_value=True)
    def test_create_repository(self, mock_search):
        """
        GIVEN: a valid repository name
        THEN: return created status
        AND: create a Repository object
        """

        data = {
            'values': f'{self.user.username}/valid-repository-name',
            'name': 'valid-repository-name',
        }

        response = self.client.post(self.url, data, format='json')

        created_repository = Repository.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_repository.name, data.get('name'))
        self.assertEqual(Repository.objects.count(), 1)

        mock_search.assert_called_once()


class RepositoryViewIntegrationTest(APITestCase):
    def setUp(self):
        self.user = UserSocialAuthFactory().user

        self.fake_data = {'data': 'fake'}

        self.client.force_authenticate(user=self.user)
        self.url = reverse('repositories:repositories-create')

    @patch('requests.get')
    def test_create_repository_fail(self, mock_get):
        """
        GIVEN: an invalid repository name
        THEN: return not found status with an error message
        AND: do not create a Repository object
        """
        mock_get.return_value = Mock(
            ok=False,
            raise_for_status=Mock(side_effect=HTTPError),
        )

        data = {
            'values': f'{self.user.username}/invalid-repository-name',
            'name': 'invalid-repository-name',
        }

        response = self.client.post(self.url, data, format='json')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(
            response_data,
            {
                'message': 'The requested repository does not exist',
            }
        )
        self.assertEqual(Repository.objects.count(), 0)

    @patch('requests.get')
    def test_create_repository_with_error_on_serializer(self, mock_get):
        """
        GIVEN: a invalid repository name
        AND: serializer validation error
        THEN: return bad request status
        AND: do not create a Repository object
        """

        mock_get.return_value = Mock(
            ok=True,
            json=Mock(return_value=self.fake_data),
        )

        invalid_str_size = Repository._meta.get_field('name').max_length + 1
        longe_name = fake.pystr(
            min_chars=invalid_str_size,
            max_chars=(invalid_str_size + 10),
        )

        data = {
            'values': f'{self.user.username}/{longe_name}',
            'name': longe_name,
        }

        response = self.client.post(self.url, data, format='json')

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response_data,
            {
                'name': [
                    'Ensure this field has no more than 100 characters.',
                ],
            }
        )
        self.assertEqual(Repository.objects.count(), 0)

    @patch('requests.get')
    def test_create_repository(self, mock_get):
        """
        GIVEN: a valid repository name
        THEN: return created status
        AND: create a Repository object
        """
        mock_get.return_value = Mock(
            ok=True,
            json=Mock(return_value=self.fake_data),
        )

        data = {
            'values': f'{self.user.username}/valid-repository-name',
            'name': 'valid-repository-name',
        }

        response = self.client.post(self.url, data, format='json')

        created_repository = Repository.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_repository.name, data.get('name'))
        self.assertEqual(Repository.objects.count(), 1)
