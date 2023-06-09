from django.conf import settings
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from common.factories import UserSocialAuthFactory
from repositories.factories import CommitFactory, RepositoryFactory
from repositories.serializers import CommitSerializer

fake = Faker()


class CommitView(APITestCase):
    def setUp(self):
        self.user = UserSocialAuthFactory().user

        self.client.force_authenticate(user=self.user)
        self.url = reverse('repositories:commits-list')

    def test_retrieve_commits_empty(self):
        """
        GIVEN: no commits on the database
        THEN: retrieve an empty list
        """

        response = self.client.get(self.url)
        response_data = response.json()

        self.assertEqual(
            response_data,
            {'count': 0, 'next': None, 'previous': None, 'results': []}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_commits_one(self):
        """
        GIVEN: one commit on the database
        THEN: retrieve that commit
        """
        commit = CommitFactory()
        expected_data = CommitSerializer(commit).data

        response = self.client.get(self.url)
        response_data = response.json()

        self.assertEqual(
            response_data,
            {
                'count': 1,
                'next': None,
                'previous': None,
                'results': [expected_data],
            }
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_retrieve_commits_many(self):
        """
        GIVEN: many commits on the database
        THEN: retrieve those commits
        """
        batch_size = 5
        CommitFactory.create_batch(batch_size)

        response = self.client.get(self.url)
        response_data = response.json()

        self.assertEqual(response_data.get('count'), batch_size)
        self.assertIsNone(response_data.get('next'))
        self.assertIsNone(response_data.get('previous'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_pagination(self):
        """
        GIVEN: many commits on the database
        THEN: return response with pagination information
        """
        pagination_size = settings.REST_FRAMEWORK.get('PAGE_SIZE')

        batch_size = (pagination_size * 2) + pagination_size // 2
        CommitFactory.create_batch(batch_size)

        response = self.client.get(self.url)
        response_data = response.json()

        self.assertEqual(response_data.get('count'), batch_size)
        self.assertIsNotNone(response_data.get('next'))
        self.assertIsNone(response_data.get('previous'))
        self.assertEqual(len(response_data.get('results')), pagination_size)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Next page

        response = self.client.get(response_data.get('next'))
        response_data = response.json()

        self.assertEqual(response_data.get('count'), batch_size)
        self.assertIsNotNone(response_data.get('next'))
        self.assertIsNotNone(response_data.get('previous'))
        self.assertEqual(len(response_data.get('results')), pagination_size)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Last page

        response = self.client.get(response_data.get('next'))
        response_data = response.json()

        self.assertEqual(response_data.get('count'), batch_size)
        self.assertIsNone(response_data.get('next'))
        self.assertIsNotNone(response_data.get('previous'))
        self.assertLess(len(response_data.get('results')), pagination_size)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_commit_filter(self):
        """
        GIVEN: commits registered in the database
        THEN: we are able to filter commits by author
        AND: filter by repository name
        """

        commits = [
            CommitFactory(
                author='author1',
                repository=RepositoryFactory(name='repo1'),
            ),
            CommitFactory(
                author='author2',
                repository=RepositoryFactory(name='repo2'),
            )
        ]

        # Filter by author name
        response = self.client.get(self.url, {'author': commits[0].author})
        response_data = response.json()

        self.assertEqual(
            response_data.get('results')[0],
            CommitSerializer(commits[0]).data
        )
        self.assertEqual(len(response_data.get('results')), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Filter by repository name
        response = self.client.get(self.url, {'repository__name': commits[1].repository})
        response_data = response.json()

        self.assertEqual(
            response_data.get('results')[0],
            CommitSerializer(commits[1]).data
        )
        self.assertEqual(len(response_data.get('results')), 1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Filter by repository name
        response = self.client.get(self.url, {'author': 'inexistent'})
        response_data = response.json()

        self.assertEqual(response_data.get('results'), [])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
