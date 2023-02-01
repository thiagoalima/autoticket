from django.shortcuts import render
from users.utilities.view import TableView, CreateView, UpdateView, DeleteView, DetailView
from .tables import RepositoryTable
from .models import (
    Repository
)


"""
    Classes refering to the Repo views
"""
class RepoDetailView (DetailView):
    model = Repository

class RepoListView(TableView):
    permission_required = 'repository.view_repo'
    model = Repository
    table_class = RepositoryTable
    template_name = 'repository/repo_list.html'
    ordering = ['-id']

class RepoCreateView(CreateView):
    permission_required = 'repository.add_repo'
    model = Repository
    fields = ["nome","url","token","token_key"]
    template_name = "repository/repo_form.html"
    success_url = "/repository/repo/"

class RepoUpdateView(UpdateView):
    permission_required = 'repository.change_repo'
    model = Repository
    fields = ["nome","url","token","token_key"]
    template_name = "repository/repo_form.html"
    success_url = "/repository/repo/"

class RepoDeleteView(DeleteView):
    permission_required = 'repository.delete_repo'
    model = Repository
    template_name = "users/confirm_delete.html"

