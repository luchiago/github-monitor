from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Commit, Repository
from .repository_search import RepositorySearch
from .serializers import CommitSerializer


class CommitView(ListAPIView):
    serializer_class = CommitSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ('author', 'repository__name')
    queryset = Commit.objects.all()


class RepositoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        repositories_names = Repository.objects.only(
            'name'
        ).all().values_list('name', flat=True)

        return Response(data={'result': repositories_names}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        repository_name = request.data.get('name')
        search_service = RepositorySearch(name=repository_name, user=request.user)
        found = search_service.search()
        if found:
            repository = search_service.create_repository()
            search_service.fetch_commits(repository)
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            data={
                'message': 'The requested repository does not exist',
            },
            status=status.HTTP_404_NOT_FOUND,
        )
