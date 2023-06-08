import json
import os
from unittest.mock import patch

from django.db import IntegrityError
from django.test import TestCase
from faker import Faker
from rest_framework.exceptions import ValidationError

from common.factories import UserProfileFactory
from repositories.factories import RepositoryFactory
from repositories.models import Commit, Repository
from repositories.repository_search import (REPO_PATH, FetchRepositoryCommits,
                                            RepositorySearch)

fake = Faker()


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

    def test_create_repository(self):
        """
        GIVEN: a repository data
        THEN: create a valid repository
        """

        self.assertEqual(Repository.objects.count(), 0)

        repository = self.search_service.create_repository()

        self.assertEqual(Repository.objects.count(), 1)
        self.assertEqual(Repository.objects.last(), repository)

    def test_create_repository_fail(self):
        """
        GIVEN: a repository invalid data
        THEN: do not create a valid repository
        """
        invalid_str_size = Repository._meta.get_field('name').max_length + 1

        self.assertEqual(Repository.objects.count(), 0)

        with self.assertRaises(ValidationError):
            self.search_service.name = fake.pystr(
                min_chars=invalid_str_size,
                max_chars=(invalid_str_size + 10),
            )
            self.search_service.create_repository()

        self.assertEqual(Repository.objects.count(), 0)

    @patch('repositories.repository_search.FetchRepositoryCommits.get_commits')
    def test_fetch_commits(self, mock_commits):
        """
        GIVEN: a created repository
        THEN: fetch it's commits
        """

        repository = RepositoryFactory()

        self.search_service.fetch_commits(repository)

        mock_commits.assert_called_once()


class FetchRepositoryCommitsTest(TestCase):
    def setUp(self) -> None:
        self.repository = RepositoryFactory(name='test')
        self.full_repo_name = f'test/{self.repository.name}'
        self.repo_path = ('/'.join((REPO_PATH, self.full_repo_name)))
        self.access_token = 'token'
        file_path = os.path.abspath("tests/fixtures/commit.json")
        with open(file_path, mode='r', encoding='utf-8') as file:
            self.valid_data = json.load(file)

        self.fetch_service = FetchRepositoryCommits(
            repo_path=self.repo_path,
            access_token=self.access_token,
            repository=self.repository
        )

    @patch('repositories.repository_search.FetchRepositoryCommits.save_commits')
    @patch('common.github_client.GithubClient.get')
    def test_get_commits(self, mock_get, mock_save):
        """
        GIVEN: a created repository
        THEN: fetch it's commits from the Github API
        AND: save those commits
        """
        fake_data = {'repo': 'data'}
        mock_get.return_value = (True, fake_data)

        self.fetch_service.get_commits()

        mock_save.assert_called_once_with(fake_data)

    @patch('repositories.repository_search.FetchRepositoryCommits.save_commits')
    @patch('common.github_client.GithubClient.get')
    def test_get_commits_fail(self, mock_get, mock_save):
        """
        GIVEN: a created repository
        THEN: fetch it's commits from the Github API
        AND: do not create commits objects on failure
        """
        fake_data = {}
        mock_get.return_value = (False, fake_data)

        self.fetch_service.get_commits()

        mock_save.assert_not_called()

    def test_save_commits(self):
        """
        GIVEN: a commit data from Github API
        THEN: save commit data
        """

        self.assertEqual(Commit.objects.count(), 0)

        self.fetch_service.save_commits(self.valid_data)

        self.assertEqual(Commit.objects.count(), len(self.valid_data))

    def test_save_commits_fail(self):
        """
        GIVEN: a commit data from Github API
        THEN: save commit data
        AND: do not create commits objects with wrong data
        """
        invalid_data = self.valid_data
        invalid_data[0].pop('commit')

        self.assertEqual(Commit.objects.count(), 0)

        with self.assertRaises(IntegrityError):
            self.fetch_service.save_commits(invalid_data)

        self.assertEqual(Commit.objects.count(), 0)
