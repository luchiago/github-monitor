from datetime import timedelta
from logging import getLogger

from django.db import transaction
from django.utils.timezone import now

from common.github_client import GithubClient
from common.models import UserProfile
from repositories.models import Commit, Repository
from repositories.serializers import RepositorySerializer

REPO_PATH = 'repos/'
COMMITS_PATH = 'commits'
BATCH_SIZE = 100
SINCE_DAYS = 30

logger = getLogger('__name__')


class FetchRepositoryCommits:
    """
    Service class for fetching commits from a repository on Github
    """

    def __init__(
        self,
        repo_path: str,
        access_token: str,
        repository: Repository,
        client: GithubClient = GithubClient()
    ):
        self.repo_path = repo_path
        self.path = ('/'.join((repo_path, COMMITS_PATH)))
        self.access_token = access_token
        self.repository = repository
        self.client = client

    def _sanitize_commit_data(self, commits: list) -> dict:
        sanitized = []
        for commit in commits:
            commit_info = commit.get('commit', {})
            commit_author_info = commit_info.get('author', {})
            sanitized.append({
                'message': commit_info.get('message'),
                'sha': commit.get('sha'),
                'author': commit_author_info.get('name'),
                'url': commit_info.get('url'),
                'date': commit_author_info.get('date'),
                'avatar': commit.get('author', {}).get('avatar_url'),
                'repository_id': self.repository.id,
            })
        return sanitized

    @transaction.atomic
    def save_commits(self, commits_data: list) -> None:
        commits_data = self._sanitize_commit_data(commits_data)

        commits = [Commit(**commit_data) for commit_data in commits_data]

        while commits:
            chunk, commits = commits[:BATCH_SIZE], commits[BATCH_SIZE:]
            Commit.objects.bulk_create(chunk, BATCH_SIZE)

    def get_commits(self) -> None:
        logger.info("Fetching commits for repository %s", self.repository.name)

        params = {'since': (now() - timedelta(days=30)).isoformat()}

        success, commits_data = self.client.get(
            self.path,
            self.access_token,
            params=params
        )

        if not success:
            return

        self.save_commits(commits_data)


class RepositorySearch:
    """
    Service class for searching repositories on Github
    """

    def __init__(
        self,
        name: str,
        user: UserProfile,
        client: GithubClient = GithubClient(),
    ) -> None:
        self.name = name
        self.full_repo_name = ('/'.join((user.username, self.name)))
        self.path = ('/'.join((REPO_PATH, self.full_repo_name)))
        self.access_token = user.access_token
        self.client = client

    def fetch_commits(self, repository: Repository) -> None:
        fetch_service = FetchRepositoryCommits(
            repo_path=self.path,
            repository=repository,
            access_token=self.access_token,
            client=self.client,
        )
        fetch_service.get_commits()

    def create_repository(self) -> Repository:
        serializer = RepositorySerializer(data={'name': self.name})
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def search(self) -> bool:
        logger.info("Searching for repository %s", self.name)

        found, _ = self.client.get(self.path, self.access_token)

        return found
