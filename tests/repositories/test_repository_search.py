from unittest.mock import patch

from django.test import TestCase

from common.factories import UserProfileFactory
from repositories.repository_search import RepositorySearch


class TestRepositorySearch(TestCase):
    def setUp(self):
        self.repository_name = 'repo'
        self.user = UserProfileFactory()

        self.search_service = RepositorySearch(
            name=self.repository_name,
            user=self.user,
        )

    @patch('common.github_client.GithubClient.get', return_value=(False, {}))
    def test_not_found_repository(self, mock_get):
        """
        GIVEN: an inexistent repository
        THEN: return a bool indicating not found
        """

        found = self.search_service.search()

        self.assertFalse(found)

        mock_get.assert_called_once()

    @patch('common.github_client.GithubClient.get', return_value=(True, {'repo': 'data'}))
    def test_found_repository(self, mock_get):
        """
        GIVEN: an existent repository
        THEN: return a bool indicating found
        """

        found = self.search_service.search()

        self.assertTrue(found)

        mock_get.assert_called_once()
