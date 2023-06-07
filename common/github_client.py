from logging import getLogger
from typing import Tuple
from urllib.parse import urljoin

import requests
from django.conf import settings
from requests.exceptions import HTTPError

logger = getLogger('__name__')

DEFAULT_TIMEOUT_SECONDS = 30


def log_request(func) -> Tuple[bool, dict]:
    """
    Decorator to log a request

    It will return a boolean indicating
    whether the request was successful
    or not and return the response data
    """

    def wrap(*args, **kwargs):
        try:
            url = [arg.url for arg in args][0]
            logger.info("Requesting with %s", url)

            response = func(*args, **kwargs)

            if not response.ok:
                response.raise_for_status()
        except HTTPError as e:
            logger.info("Request failed. Error message: %s", e)
            return False, {}
        return True, response.json()
    return wrap


class GithubClient:
    """
    Service class for creating requests to Github API
    """

    def __init__(self, access_token: str, path: str) -> None:
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'Authorization': f'Bearer {access_token}',
        }
        self.url = urljoin(settings.GITHUB_API_URL, path)

    @log_request
    def get(self) -> bool:
        return requests.get(
            self.url,
            headers=self.headers,
            timeout=DEFAULT_TIMEOUT_SECONDS,
        )
