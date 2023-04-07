from django.shortcuts import render
from users.utilities.view import TableView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from ansible.inventory.host import Host
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

"""
    Classes refering to the Playbook views
"""

class PlaybookDetailView (DetailView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        context = {'playbookRepository':playbookRepository}
        return self.render_to_response(context)

class AddHostView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()

        if request.POST['host']:
            #host = Host(request.POST['host'])
            playbookRepository.inventoryRepository.inventory.add_host(request.POST['host'],'all')
            playbookRepository.inventoryRepository.saveInventory()

        context = {'playbookRepository':playbookRepository}
        return self.render_to_response(context)

class JoinGroupHostView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()

        if request.POST['host'] and request.POST['groups']:
            host = playbookRepository.inventoryRepository.inventory.get_host(request.POST['host'])
            if host:
                for group in request.POST['groups']:
                    host.add_group(group)

                playbookRepository.inventoryRepository.saveInventory()

        context = {'playbookRepository':playbookRepository}
        return self.render_to_response(context)
