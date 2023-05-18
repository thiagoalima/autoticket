from django.shortcuts import render
from users.utilities.view import TableView, CreateView, UpdateView, DeleteView, DetailView
from django.views import View
from ansible.inventory.host import Host
from ansible.playbook.task import Task
from ansible.playbook.handler import Handler
from .tables import RepositoryTable
from django.http import HttpResponse
from iac.views import getHtmlInventoryParameter
from .models import (
    Repository
)

from iac.models import InventoryParameter, PlaybookParameter, AnsibleModule, AnsibleModuleVariable

from ansible.playbook.block import Block
from django.http import JsonResponse

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
        inventoryParameters = InventoryParameter.objects.all()
        playbookParameters = PlaybookParameter.objects.all()
        ansibleModules = AnsibleModule.objects.all()

        context = {'ansibleModules':ansibleModules,'playbookParameters': playbookParameters, 
                   'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)

class HandlerDetailView (DetailView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()

        playbookHost = request.GET['playbook']
        filename = request.GET['filename']

        handlers = []
        jsonHandlers = []
        for playbook in playbookRepository.playbooks:
            if filename in playbook._file_name:
                for play in playbook.get_plays():
                    if playbookHost == play.get_name():
                        handlers = getattr(play,'handlers')

        for b in handlers:
            for h in b.block:
                jsonHandlers.append({'name':h.name,'action':h.action, h.action:h.args})

        return JsonResponse(jsonHandlers, safe=False)    

class TaskDetailView (DetailView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()

        playbookHost = request.GET['playbook']
        filename = request.GET['filename']

        tasks = []
        jsonTask = []
        for playbook in playbookRepository.playbooks:
            if filename in playbook._file_name:
                for play in playbook.get_plays():
                    if playbookHost == play.get_name():
                        tasks = getattr(play,'tasks')
        for b in tasks:
            for t in b.block:
                jsonTask.append({'name':t.name,'action':t.action, t.action:t.args})

        return JsonResponse(jsonTask, safe=False)
    
class AddHandlerPlaybookView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()
        

        playbookHost = request.POST['playbook']
        filename = request.POST['filename']
        name = request.POST['name']
        idModule = request.POST['actionSelect']

        ansibleModule = AnsibleModule.objects.get(id=idModule)
        
        params_data = {}    
        all_post_data = request.POST.dict()
        for line in all_post_data:
            if line.startswith('param__'):
                params_key = line.replace('param__','')
                if all_post_data[line]:
                    params_data[params_key]=all_post_data[line]

        for playbook in playbookRepository.playbooks:
            if filename in playbook._file_name:
                for play in playbook.get_plays():
                    if playbookHost == play.get_name():
                        handler = Handler()
                        setattr(handler,'name',name)
                        setattr(handler,'action',ansibleModule.name)
                        setattr(handler,'args',params_data)
                        handlers = getattr(play,'handlers')
                        handlers.append(handler)
                        setattr(play,'handlers',handlers)
    
        playbookRepository.salvarPlaybooks();

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)

class TaskDeleteView(DeleteView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()

        playbookName = request.GET['playbook']
        filename = request.GET['filename']
        name = request.GET['name']
        
        for playbook in playbookRepository.playbooks:
            if filename in playbook._file_name:
                for play in playbook.get_plays():
                    if playbookName == play.get_name():
                        blocks = getattr(play,'tasks')
                        remover = None;
                        for block in blocks:
                            for task in block.get_tasks():
                                if name in task.name:
                                    remover = block
                        blocks.remove(remover)
                        setattr(play,'tasks',blocks)
    
        playbookRepository.salvarPlaybooks();

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)
       

class AddTaskPlaybookView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()
        

        playbookHost = request.POST['playbook']
        filename = request.POST['filename']
        name = request.POST['name']
        idModule = request.POST['actionSelect']

        notifications = []
        if 'notify[]' in request.POST:
            for notify in request.POST.getlist('notify[]'):
                notifications.append(notify)

        ansibleModule = AnsibleModule.objects.get(id=idModule)
        
        params_data = {}    
        all_post_data = request.POST.dict()
        for line in all_post_data:
            if line.startswith('param__'):
                params_key = line.replace('param__','')
                if all_post_data[line]:
                    params_data[params_key]=all_post_data[line]

        tasks = []
        for playbook in playbookRepository.playbooks:
            if filename in playbook._file_name:
                for play in playbook.get_plays():
                    if playbookHost == play.get_name():
                        task = Task()
                        setattr(task,'name',name)
                        setattr(task,'action',ansibleModule.name)
                        setattr(task,'args',params_data)
                        setattr(task,'notify',notifications)
                        tasks = getattr(play,'tasks')
                        tasks.append(task)
                        setattr(play,'tasks',tasks)
    
        playbookRepository.salvarPlaybooks();

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)

class AddVarsPlaybookView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()

        playbookHost = request.POST['playbook']
        filename = request.POST['filename']
        
        params_data = {}    
        all_post_data = request.POST.dict()
        for line in all_post_data:
            if line.startswith('param__'):
                params_key = line.replace('param__','')
                params_data[params_key]=all_post_data[line]

        for playbook in playbookRepository.playbooks:
            if filename in playbook._file_name:
                for play in playbook.get_plays():
                    if playbookHost == play.get_name():
                        for k,v in params_data.items():
                            if v in ('true','false'):
                                v = bool(v)
                            setattr(play,k,v)
    
        playbookRepository.salvarPlaybooks();

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)
    
class AddHostPlaybookView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()

        playbookHost = request.POST['playbook']
        filename = request.POST['filename']
        hosts = request.POST.getlist('hosts[]')
        groups = request.POST.getlist('groups[]')

        for playbook in playbookRepository.playbooks:
            if filename in playbook._file_name:
                for play in playbook.get_plays():
                    if playbookHost == play.get_name():
                        if hosts:
                            setattr(play,'hosts', ','.join(hosts))
                        else:
                            setattr(play,'hosts',','.join(groups))
    
        playbookRepository.salvarPlaybooks();

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)

class AddFileView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()

        if request.POST['file'] and request.POST['playbook[]']:
            playbooks =  request.POST.getlist('playbook[]')
            file = request.POST['file']
            playbookRepository.addPlaybook(file+'.yaml',playbooks)
            playbookRepository.salvarPlaybooks();

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)
    
class HostDeleteView(DeleteView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()

        delHost = playbookRepository.inventoryRepository.inventory.get_host(request.GET['del'])

        if delHost:
            playbookRepository.inventoryRepository.inventory._inventory.remove_host(delHost)
            playbookRepository.inventoryRepository.remove_host_vars_file(delHost.name)
            playbookRepository.inventoryRepository.saveInventory()
        
        request.GET = None

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)

class GroupDeleteView(DeleteView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()

        delGroup = playbookRepository.inventoryRepository.inventory.groups[request.GET['del']]

        if delGroup:
            playbookRepository.inventoryRepository.inventory._inventory.remove_group(delGroup.name)
            playbookRepository.inventoryRepository.remove_group_vars_file(delGroup.name)
            playbookRepository.inventoryRepository.saveInventory()
        
        request.GET = None

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)

    
class HostVarsDetailView (DetailView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        host = request.GET['host']
        vars = playbookRepository.inventoryRepository.getHostVars(host)

        html = ''
        for var in vars:
            inventoryParameter = InventoryParameter.objects.get(name=var)
            html += '''<div id="{id}_div_parameter" class="input-group">
                        {html}
                      <button class="btn btn-outline-secondary" type="button" onclick="removeInventoryParameter('{id}_div_parameter')"><span class="bi-trash"></span></button>
                      </div>'''.format(id=inventoryParameter.id, html=getHtmlInventoryParameter(inventoryParameter,vars[var]) )

        return HttpResponse(html)
    
class GroupVarsDetailView (DetailView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        group = request.GET['group']
        vars = playbookRepository.inventoryRepository.getGroupVars(group)

        html = ''
        for var in vars:
            inventoryParameter = InventoryParameter.objects.get(name=var)
            html += '''<div id="{id}_div_parameter" class="input-group">
                        {html}
                      <button class="btn btn-outline-secondary" type="button" onclick="removeInventoryParameter('{id}_div_parameter')"><span class="bi-trash"></span></button>
                      </div>'''.format(id=inventoryParameter.id, html=getHtmlInventoryParameter(inventoryParameter,vars[var]) )

        return HttpResponse(html)
    
    
class AddGroupView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()

        params_data = {}    
        all_post_data = request.POST.dict()
        for line in all_post_data:
            if line.startswith('param__'):
                params_key = line.replace('param__','')
                params_data[params_key]=all_post_data[line]
        
        groupObject = None
        if request.POST['group'] in playbookRepository.inventoryRepository.inventory.groups:
            groupObject = playbookRepository.inventoryRepository.inventory.groups[request.POST['group']]

        if request.POST['group'] and not groupObject:
            group = request.POST['group']
            playbookRepository.inventoryRepository.inventory.add_group(group)
            playbookRepository.inventoryRepository.addVarsGroup(group,params_data)
            playbookRepository.inventoryRepository.saveInventory()
        else:
            playbookRepository.inventoryRepository.addVarsGroup(groupObject.name,params_data)
            playbookRepository.inventoryRepository.saveInventory()

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)

class AddHostView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()

        params_data = {}    
        all_post_data = request.POST.dict()
        for line in all_post_data:
            if line.startswith('param__'):
                params_key = line.replace('param__','')
                params_data[params_key]=all_post_data[line]

        hostObject = playbookRepository.inventoryRepository.inventory.get_host(request.POST['host'])

        if request.POST['host'] and not hostObject:
            host = request.POST['host']
            playbookRepository.inventoryRepository.inventory.add_host(host,'all')
            playbookRepository.inventoryRepository.addVarsHost(host,params_data)
            playbookRepository.inventoryRepository.saveInventory()
        else:
            playbookRepository.inventoryRepository.addVarsHost(hostObject.name,params_data)
            playbookRepository.inventoryRepository.saveInventory()

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)

class JoinGroupHostView(CreateView):
    model = Repository
    template_name = "repository/playbook_form.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        playbookRepository = self.object.getPlaybookRepository()
        inventoryParameters = InventoryParameter.objects.all()

        groupPost = request.POST.getlist('groups[]')

        if request.POST['hostJoinGroup'] and groupPost:
            host = playbookRepository.inventoryRepository.inventory.get_host(request.POST['hostJoinGroup'])
            
            if host:

                #zerando os grupos
                for g in host.groups:
                    g.remove_host(host)

                host.groups = []

                for group in groupPost:
                    g = playbookRepository.inventoryRepository.inventory.groups[group];
                    g.add_host(host)
                    host.add_group(g)

                playbookRepository.inventoryRepository.saveInventory()

        context = {'inventoryParameters':inventoryParameters, 'playbookRepository':playbookRepository}
        return self.render_to_response(context)
