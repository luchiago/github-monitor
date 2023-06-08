from unittest.mock import Mock, patch

from django.test import TestCase
from requests.exceptions import HTTPError

from common.github_client import GithubClient


class TestGithubClient(TestCase):
    def setUp(self):
        self.token = 'token'
        self.path = 'path/'
        self.client = GithubClient()

    @patch('requests.get')
    def test_get_failure(self, mock_get):
        """
        GIVEN: an invalid request
        THEN: return a bool indicating failure
        AND: return an empty response data
        """

        mock_get.return_value = Mock(
            ok=False,
            raise_for_status=Mock(side_effect=HTTPError),
        )

        is_successful, data = self.client.get(self.path, self.token)

        self.assertFalse(is_successful)
        self.assertEqual(data, {})

        mock_get.assert_called_once()

    @patch('requests.get')
    def test_get_success(self, mock_get):
        """
        GIVEN: an valid request
        THEN: return a bool indicating success
        AND: return the requested data
        """
        fake_data = {'data': 'fake'}

        mock_get.return_value = Mock(
            ok=True,
            url='http://test.com',
            json=Mock(return_value=fake_data),
        )

        is_successful, data = self.client.get(self.path, self.token)

        self.assertTrue(is_successful)
        self.assertEqual(data, fake_data)

        mock_get.assert_called_once()
