from logging import getLogger
from typing import Optional, Tuple
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
            response = func(*args, **kwargs)

            logger.info("Requesting with %s", response.url)

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

    def _prepare_request(
        self,
        path: str,
        access_token: Optional[str] = ''
    ) -> Tuple[str, dict]:
        headers = {'Accept': 'application/vnd.github+json'}
        if access_token:
            headers.update({'Authorization': f'Bearer {access_token}'})

        url = urljoin(settings.GITHUB_API_URL, path)
        return url, headers

    @log_request
    def get(
        self,
        path: str,
        access_token: Optional[str] = '',
        params: Optional[dict] = None,
    ) -> bool:
        url, headers = self._prepare_request(path, access_token)
        return requests.get(
            url,
            headers=headers,
            timeout=DEFAULT_TIMEOUT_SECONDS,
            params=params
        )
