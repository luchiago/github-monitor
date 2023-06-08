from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from common.factories import UserSocialAuthFactory
from repositories.factories import CommitFactory
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
        self.assertIsNone(response_data.get('next'), batch_size)
        self.assertIsNone(response_data.get('previous'), batch_size)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
