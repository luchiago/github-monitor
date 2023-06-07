from unittest.mock import Mock, patch

from django.test import TestCase
from requests.exceptions import HTTPError

from common.github_client import DEFAULT_TIMEOUT_SECONDS, GithubClient


class TestGithubClient(TestCase):
    def setUp(self):
        self.client = GithubClient(
            access_token='fake-token',
            path='path'
        )

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

        is_successful, data = self.client.get()

        self.assertFalse(is_successful)
        self.assertEqual(data, {})

        mock_get.assert_called_once_with(
            self.client.url,
            headers=self.client.headers,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )

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
            json=Mock(return_value=fake_data),
        )

        is_successful, data = self.client.get()

        self.assertTrue(is_successful)
        self.assertEqual(data, fake_data)

        mock_get.assert_called_once_with(
            self.client.url,
            headers=self.client.headers,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
