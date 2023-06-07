from logging import getLogger

from common.github_client import GithubClient
from common.models import UserProfile

REPO_PATH = 'repos/'

logger = getLogger('__name__')


class RepositorySearch:
    """
    Service class for searching repositories on Github
    """

    def __init__(self, name: str, user: UserProfile) -> None:
        self.name = name
        self.username = user.username
        self.access_token = user.access_token

    def search(self) -> bool:
        logger.info("Searching for repository %s", self.name)

        path = ('/'.join((REPO_PATH, self.username, self.name)))
        client = GithubClient(
            access_token=self.access_token,
            path=path,
        )

        found, _ = client.get()

        return found
