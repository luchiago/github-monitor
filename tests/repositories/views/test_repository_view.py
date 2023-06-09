import json
import os
from unittest.mock import Mock, patch

from django.urls import reverse
from faker import Faker
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APITestCase

from common.factories import UserSocialAuthFactory
from repositories.factories import RepositoryFactory
from repositories.models import Commit, Repository

fake = Faker()


class RepositoryViewTest(APITestCase):
    def setUp(self):
        self.user = UserSocialAuthFactory().user

        self.client.force_authenticate(user=self.user)
        self.url = reverse('repositories:repositories-list-create')

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

    @patch('repositories.repository_search.RepositorySearch.fetch_commits')
    @patch('repositories.repository_search.RepositorySearch.create_repository')
    @patch('repositories.repository_search.RepositorySearch.search', return_value=True)
    def test_create_repository_with_error_on_serializer(
        self,
        mock_search,
        mock_create_repository,
        mock_fetch_commits,
    ):
        """
        GIVEN: a invalid repository name
        THEN: return bad request status
        AND: do not create a Repository object
        """

        mock_create_repository.side_effect = ValidationError('Invalid name')

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
            ['Invalid name']
        )
        self.assertEqual(Repository.objects.count(), 0)

        mock_search.assert_called_once()
        mock_fetch_commits.assert_not_called()

    @patch('repositories.repository_search.RepositorySearch.fetch_commits')
    @patch('repositories.repository_search.RepositorySearch.create_repository')
    @patch('repositories.repository_search.RepositorySearch.search', return_value=True)
    def test_create_repository(
        self,
        mock_search,
        mock_create_repository,
        mock_fetch_commits,
    ):
        """
        GIVEN: a valid repository name
        THEN: return created status
        AND: create a Repository object
        """

        data = {
            'values': f'{self.user.username}/valid-repository-name',
            'name': 'valid-repository-name',
        }
        repository = RepositoryFactory(name=data.get('name'))
        mock_create_repository.return_value = repository

        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        mock_search.assert_called_once()
        mock_fetch_commits.assert_called_once_with(repository)

    def test_list_all_repositories_empty(self):
        """
        GIVEN: no repositories on the db
        THEN: return an empty list
        """

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('result'), [])

    def test_list_all_repositories(self):
        """
        GIVEN: repositories on the db
        THEN: return repositories names
        """
        RepositoryFactory.create_batch(5)
        expected_response = Repository.objects.only(
            'name'
        ).all().values_list('name', flat=True)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('result'), list(expected_response))


class RepositoryViewIntegrationTest(APITestCase):
    def setUp(self):
        self.user = UserSocialAuthFactory().user

        self.fake_data = {'data': 'fake'}

        self.client.force_authenticate(user=self.user)
        self.url = reverse('repositories:repositories-list-create')

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
            url='http://test.com',
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
        file_path = os.path.abspath("tests/fixtures/commit.json")
        with open(file_path, mode='r', encoding='utf-8') as file:
            commits_data = json.load(file)

        mock_get.side_effect = [
            Mock(
                ok=True,
                url='https://test.com',
                json=Mock(return_value=self.fake_data),
            ),
            Mock(
                ok=True,
                url='https://test.com',
                json=Mock(return_value=commits_data),
            ),
        ]

        data = {
            'values': f'{self.user.username}/valid-repository-name',
            'name': 'valid-repository-name',
        }

        response = self.client.post(self.url, data, format='json')

        created_repository = Repository.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(created_repository.name, data.get('name'))
        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(Commit.objects.count(), 1)
        self.assertEqual(Commit.objects.last().repository, created_repository)
