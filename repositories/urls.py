from django.urls import path

from .views import RepositoryView, commit_list_view

app_name = 'repositories'

urlpatterns = [
    path('api/commits/', commit_list_view, name='commits-list'),
    path('api/repositories/', RepositoryView.as_view(), name='repositories-create'),
]
