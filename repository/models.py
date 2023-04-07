from django.db import models
from ansible.inventory.manager import InventoryManager
from ansible.playbook import Playbook
from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.parsing.dataloader import DataLoader
from ansible.cli.galaxy import GalaxyCLI
from ansible.vars.manager import VariableManager
from ansible.vars.plugins import get_vars_from_path
from ansible.plugins.vars.host_group_vars import VarsModule
from django.conf import settings
from git import Repo
from .constants import ATTRIBUTES_TASK, ATTRIBUTES_PLAYBOOK
import configparser
import yaml
import os


# Class to handle Repository
class Repository(models.Model):

    def __init__(self, *args, **kwargs):
        self.playbookRepository = None
        super().__init__(*args, **kwargs)

    nome = models.CharField(
        max_length=100,
        verbose_name='Nome',
    )

    url = models.CharField(
        max_length=100,
        verbose_name='URL',
    )

    token = models.CharField(
        max_length=100,
        verbose_name='Token',
    )

    token_key = models.CharField(
        max_length=100,
        verbose_name='Token Key',
    )
    
    def folderRepository(self):
        return settings.FOLDER_REPOSITORY+'/'+self.nome
    
    def save(self, *args, **kwargs):
        isExist = os.path.exists(self.folderRepository())

        if not isExist:
            os.makedirs(self.folderRepository())
            Repo.clone_from(self.url, self.folderRepository())
            #TODO criar pastas group_vars e host_vars
            #criar um projeto em branco 
            cli = GalaxyCLI(args=["ansible-galaxy", "init", self.nome,"--init-path", self.folderRepository()+'/roles',"--force"])
            cli.run()
        
        #bloco de teste
        self.playbookRepository = self.getPlaybookRepository()

        self.playbookRepository.salvarPlaybooks()

        self.playbookRepository.inventoryRepository.saveInventory()

        super(Repository, self).save(*args, **kwargs)
    
    def getPlaybookRepository(self):
        loader = DataLoader()
        loader.set_basedir(self.folderRepository())

        plays = []

        for playbookFile in os.listdir(self.folderRepository()): 
            if playbookFile.endswith(".yml") or playbookFile.endswith(".yaml") :
                plays.append(Playbook.load(self.folderRepository()+'/'+playbookFile, loader=loader))

        return PlaybookRepository(repository=self,playbooks=plays)

class InventoryRepository():

    def __init__(self, repository:Repository, loader:DataLoader=None, inventory:InventoryManager=None) -> None:
        self.loader = loader
        self.repository = repository
        self.inventory = inventory
        self.host_vars = {}
        self.group_vars = {}
        if not inventory:
            self.load_inventory()
        if self.variable_manager:
            self.load_files_vars()

    def load_inventory(self):
        self.loader = DataLoader()
        self.loader.set_basedir(self.repository.folderRepository())
        self.inventory = InventoryManager(loader=self.loader,sources=[self.url_inventory_hosts()], parse=True)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
    
    def url_host_vars(self,host):
        return self.repository.folderRepository()+'/host_vars/'+host

    def url_group_vars(self,group):
        return self.repository.folderRepository()+'/group_vars/'+group
    
    def url_inventory_hosts(self):
        return self.repository.folderRepository()+'/hosts'
    
    def load_files_vars(self):
        for key,host in self.inventory.hosts.items():
            self.host_vars[key] = get_vars_from_path(self.loader, self.repository.folderRepository(), [host], 'all')

        for key,group in self.inventory.groups.items():
            if group.name not in ['all','ungrouped']:
                self.group_vars[key] = get_vars_from_path(self.loader, self.repository.folderRepository(), [group], 'all')
    
    def saveInventory(self):
        for host,vars in self.host_vars.items():
            if vars:
                with open(self.url_host_vars(host), 'w+') as fileHost:
                    documents = yaml.dump(vars, fileHost, Dumper=AnsibleDumper, explicit_start=True, explicit_end=True, sort_keys=False, default_flow_style=False,default_style='', allow_unicode=True)
        for group,vars in self.group_vars.items():
            if vars:
                with open(self.url_group_vars(group), 'w') as fileGroup:
                    documents = yaml.dump(vars, fileGroup, Dumper=AnsibleDumper, explicit_start=True, explicit_end=True, sort_keys=False, default_flow_style=False,default_style='', allow_unicode=True)

        with open(self.url_inventory_hosts(), 'w') as fileInventory:
            self.createConfigParser(self.inventory._inventory).write(fileInventory)
    
    def createConfigParser(self, data):
        result = configparser.ConfigParser(allow_no_value=True,delimiters=' ')
        for host in data.groups['all'].hosts:
            vars = ''
            result['all']={}
            for k,v in host.vars.items():
                if k not in ['inventory_file', 'inventory_dir']:
                    vars += k + "=" + v+" "
            result['all'].update({host.name:vars})
        
        for name, group in data.groups.items():
            if name not in ['ungrouped','all']:
                vars = ''
                result[name]={}
                for host in group.hosts:
                    for k,v in host.vars.items():
                        if k not in ['inventory_file', 'inventory_dir']:
                            vars += k + "=" + v+" "
                    result[name].update({host.name:vars})

        return result
    
    
class PlaybookRepository():
    
    def __init__(self, repository:Repository,playbooks=None, inventoryRepository:InventoryRepository=None):
        self.repository = repository
        self.playbooks = playbooks
        self.inventoryRepository = inventoryRepository
        if not inventoryRepository:
            self.inventoryRepository = InventoryRepository(repository=self.repository)
    
    
    def retirar_nulos(self, data,listAtrribute=None):
        if listAtrribute:
            return {k: v for k, v in data.items() if v and k in listAtrribute}
        return {k: v for k, v in data.items() if v}
    
    def salvarYaml(self, data, folder = None, filename = None):
        if not filename:
            filename = 'main.yml'
        if not folder:
            folder = self.repository.folderRepository()

        with open(folder+'/'+filename, 'w') as file:
                documents = yaml.dump(data, file, Dumper=AnsibleDumper, explicit_start=True, explicit_end=True, sort_keys=False, default_flow_style=False, default_style='', allow_unicode=True)

    def salvarDefaults(self, data):
        folder = data._role_path+'/defaults'
        self.salvarYaml(data._default_vars,folder=folder)
    
    def salvarHandlers(self, data):
        folder = data._role_path+'/handlers'
        handlers = []
        for b in data._handler_blocks:
            for h in b.block:
                handlers.append({'name': h.name,h.action: h.args})

        self.salvarYaml(handlers,folder=folder)
        
    def salvarTasks(self, data):
        folder = data._role_path+'/tasks'
        tasks= []
        for b in data._task_blocks:
            for t in b.block:
                tmp = self.retirar_nulos(t.serialize(),listAtrribute=ATTRIBUTES_TASK)

                args = tmp['args']
                #Atributo desatualizado no ansible
                if '_raw_params' in tmp['args']:
                    args['cmd'] = args['_raw_params']
                    del args['_raw_params']

                task = {'name': tmp.pop('name'),tmp.pop('action'): tmp.pop('args')}
                task.update(tmp)

                tasks.append(task)

        self.salvarYaml(tasks,folder=folder)
    
    def salvarVars(self, data):
        folder = data._role_path+'/vars'
        self.salvarYaml(data._role_vars,folder=folder)

    def salvarRoles(self, data):
        for role in data:
            self.salvarDefaults(role)
            self.salvarHandlers(role)
            self.salvarTasks(role)
            self.salvarVars(role)

    def salvarPlaybooks(self):
        for playbook in self.playbooks:
            for p in playbook._entries:
                validos = self.retirar_nulos(p.serialize(), ATTRIBUTES_PLAYBOOK)

                self.salvarRoles(p.roles)
        
                data = {'name':validos.pop('name')}
                data.update(validos)
                roles = []
                for r in p.roles:
                    roles.append(r._role_name)

                data['roles'] = roles

                filename = os.path.basename(playbook._file_name)

                self.salvarYaml([data],filename=filename)
            
            

    
    

    



