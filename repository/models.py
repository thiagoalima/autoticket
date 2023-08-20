"""Model Repository"""
import os
import configparser
import yaml
from django.db import models
from ansible.inventory.manager import InventoryManager
from ansible.playbook import Playbook
from ansible.playbook.play import Play
from ansible.cli.galaxy import GalaxyCLI
from ansible.vars.manager import VariableManager
from ansible.vars.plugins import get_vars_from_path
from ansible.parsing.dataloader import DataLoader
from ansible.parsing.vault import VaultLib, VaultSecret,VaultEditor
from .dumper import AnsibleDumperRepository
from .constants import ATTRIBUTES_TASK, ATTRIBUTES_PLAYBOOK
from django.conf import settings
from git import Repo
from datetime import datetime

from ansible import constants as C

VAULT_SECRET = [(C.DEFAULT_VAULT_IDENTITY, VaultSecret(settings.VAULT_KEY.encode()))]

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
    
    def urlGit(self):
        return f'http://{self.token}:{self.token_key}@{self.url}'
    
    def commitAndPush(self):
        dataAtual= datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

        #TODO coloca o usuario que fez o commit
        commit_message = f'commit realizado em {dataAtual}'

        repo = Repo(self.folderRepository())

        #TODO fazer pull

        repo.git.add('--all')
        repo.index.commit(commit_message)

        origin = repo.remote(name='origin')
        origin.push()
    
    def save(self, *args, **kwargs):
        isExist = os.path.exists(self.folderRepository())

        if not isExist:
            os.makedirs(self.folderRepository())
            Repo.clone_from(self.urlGit(), self.folderRepository())

            if not os.path.exists(self.folderRepository()+'/group_vars'):
                os.makedirs(self.folderRepository()+'/group_vars')

            if not os.path.exists(self.folderRepository()+'/host_vars'):   
                os.makedirs(self.folderRepository()+'/host_vars')
                
            if not os.path.exists(self.folderRepository()+'/files'):   
                os.makedirs(self.folderRepository()+'/files')
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
            if (playbookFile.endswith(".yml") or playbookFile.endswith(".yaml")) and 'gitlab-ci' not in playbookFile  :
                plays.append(Playbook.load(self.folderRepository()+'/'+playbookFile, loader=loader))

        return PlaybookRepository(repository=self,playbooks=plays)

class InventoryRepository():

    def __init__(self, repository:Repository, loader:DataLoader=None, inventory:InventoryManager=None) -> None:
        self.loader = loader
        self.repository = repository
        self.inventory = inventory
        self.host_vars = {}
        self.group_vars = {}
        self.vault = VaultLib(VAULT_SECRET)
        if not inventory:
            self.load_inventory()
        if self.variable_manager:
            self.load_files_vars()

    def load_inventory(self):
        self.loader = DataLoader()
        self.loader.set_vault_secrets(VAULT_SECRET)
        self.loader.set_basedir(self.repository.folderRepository())
        self.inventory = InventoryManager(loader=self.loader,sources=[self.url_inventory_hosts()], parse=True)
        self.variable_manager = VariableManager(loader=self.loader, inventory=self.inventory)
    
    def url_host_vars(self,host):
        return self.repository.folderRepository()+'/host_vars/'+host

    def url_group_vars(self,group):
        return self.repository.folderRepository()+'/group_vars/'+group
    
    def url_inventory_hosts(self):
        return self.repository.folderRepository()+'/hosts'
    
    def remove_host_vars_file(self, host):
        if host in self.host_vars:
            del self.host_vars[host]

        if os.path.exists(self.url_host_vars(host)):
            os.remove(self.url_host_vars(host))
    
    def remove_group_vars_file(self, group):
        if group in self.group_vars:
            del self.group_vars[group]

        if os.path.exists(self.url_group_vars(group)):
            os.remove(self.url_group_vars(group))
    
    def load_files_vars(self):
        for key,host in self.inventory.hosts.items():
            self.host_vars[key] = get_vars_from_path(self.loader, self.repository.folderRepository(), [host], 'all')

        for key,group in self.inventory.groups.items():
            if group.name not in ['all','ungrouped']:
                self.group_vars[key] = get_vars_from_path(self.loader, self.repository.folderRepository(), [group], 'all')
    
    def addVarsHost(self,host,vars):
        self.host_vars[host] = vars

    def getHostVars(self,host):
        return self.host_vars[host]
    
    def addVarsGroup(self,group,vars):
        self.group_vars[group] = vars

    def getGroupVars(self,host):
        return self.group_vars[host]
    
    def _encrypt_files(self):
        vault_editor = VaultEditor(vault=self.vault)
        for host,vars_host in self.host_vars.items():
            if vars_host and os.path.exists(self.url_host_vars(host)):
                vault_editor.encrypt_file(self.url_host_vars(host),None,C.DEFAULT_VAULT_IDENTITY)
        for group,vars_group in self.group_vars.items():
            if vars_group and os.path.exists(self.url_group_vars(group)):
                vault_editor.encrypt_file(self.url_group_vars(group),None,C.DEFAULT_VAULT_IDENTITY)
        vault_editor.encrypt_file(self.url_inventory_hosts(),None,C.DEFAULT_VAULT_IDENTITY)
    
    def saveInventory(self):
        for host,vars in self.host_vars.items():
            if vars:
                with open(self.url_host_vars(host), 'w+') as fileHost:
                    documents = yaml.dump(vars, fileHost, Dumper=AnsibleDumperRepository, explicit_start=True, explicit_end=True, sort_keys=False, default_flow_style=False,default_style='', allow_unicode=True)
        for group,vars in self.group_vars.items():
            if vars:
                with open(self.url_group_vars(group), 'w') as fileGroup:
                    documents = yaml.dump(vars, fileGroup, Dumper=AnsibleDumperRepository, explicit_start=True, explicit_end=True, sort_keys=False, default_flow_style=False,default_style='', allow_unicode=True)

        with open(self.url_inventory_hosts(), 'w') as fileInventory:
            self.createConfigParser(self.inventory._inventory).write(fileInventory)
        
        self._encrypt_files()
        self.repository.commitAndPush()
    
    def createConfigParser(self, data):
        result = configparser.ConfigParser(allow_no_value=True,delimiters=' ')
        
        for host in data.groups['all'].hosts:
            vars = ''
            for k,v in host.vars.items():
                if k not in ['inventory_file', 'inventory_dir']:
                    vars += k + "=" + v+" "
            if 'all' in result:
                result['all'].update({host.name:vars})
            else:
                result['all']={host.name:vars}
        
        for name, group in data.groups.items():
            if name not in ['ungrouped','all']:
                vars = ''
                for host in group.hosts:
                    for k,v in host.vars.items():
                        if k not in ['inventory_file', 'inventory_dir']:
                            vars += k + "=" + v+" "
                    if name in result:
                        result[name].update({host.name:vars})
                    else:
                        result[name]={host.name:vars}

        return result
    
    
class PlaybookRepository():
    
    def __init__(self, repository:Repository,playbooks=None, inventoryRepository:InventoryRepository=None):
        self.repository = repository
        self.playbooks = playbooks
        self.inventoryRepository = inventoryRepository
        if not inventoryRepository:
            self.inventoryRepository = InventoryRepository(repository=self.repository)

    def addPlaybook(self,filename, data):
        loader = DataLoader()
        loader.set_basedir(self.repository.folderRepository())
        playbook = Playbook(loader=loader)
        playbook._file_name = filename

        for d in data:
            play = Play()
            play.deserialize({"name":d})
            playbook._entries.append(play)
        
        self.playbooks.append(playbook)
    
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
                documents = yaml.dump(data, file, Dumper=AnsibleDumperRepository, explicit_start=True, explicit_end=True, sort_keys=False, default_flow_style=False, default_style='', allow_unicode=True)

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
            filename = os.path.basename(playbook._file_name)
            dataPlaybook = []
            for p in playbook._entries:
                validos = self.retirar_nulos(p.serialize(), ATTRIBUTES_PLAYBOOK)

                self.salvarRoles(p.roles)
        
                data = {'name':validos.pop('name')}
                data.update(validos)
                roles = []
                for r in p.roles:
                    roles.append(r._role_name)

                if roles:
                    data['roles'] = roles

                dataPlaybook.append(data)
        

            self.salvarYaml(dataPlaybook,filename=filename)
        self.repository.commitAndPush()
            
            

    
    

    



