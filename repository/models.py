from django.db import models
from ansible.cli.galaxy import GalaxyCLI
from django.conf import settings
from os.path import abspath
from git import Repo
import os
import yaml

from iac.models import Playbook,Inventory, Handler, Template

# Class to handle Repository
class Repository(models.Model):

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

            cli = GalaxyCLI(args=["ansible-galaxy", "init", self.nome,"--init-path", self.folderRepository()+'/roles',"--force"])
            cli.run()
        
        playbookRepository = self.getPlaybookRepository()
        print(playbookRepository) 

        super(Repository, self).save(*args, **kwargs)
    
    def getPlaybookRepository(self):
        return PlaybookRepository(repository=self)
    
class PlaybookRepository():
    
    def __init__(self, repository:Repository,inventory:Inventory=None,playbooks:Playbook=[]) -> None:
        self.repository = repository
        self.playbooks = playbooks
        self.inventory = inventory
        self.loadPlaybook()
    
    def loadPlaybook(self):
        for play in os.listdir(self.repository.folderRepository()): 
            if play.endswith(".yml") or play.endswith(".yaml") :
                playbook = Playbook()
                
                with open(self.repository.folderRepository()+'/'+play) as file:
                    filePlaybook = yaml.full_load(file)
                    playbook.deserialize(filePlaybook)

                    for role in playbook.roles:
                        role.defaults = self.loadDefaults(role)
                        role.files = self.loadFiles(role)
                        role.handlers = self.loadHandlers(role)
                        role.templates = self.loadTemplates(role)

                    self.playbooks.append(playbook)

    def loadTemplates(self,role):
        templates = []
        with open(self.repository.folderRepository()+'/roles/'+role.name+'/templates/main.yml') as file:
            for t in yaml.full_load(file):
                template = Template()
                template.deserialize(t)
                templates.append(template)
        return templates
    
    def loadHandlers(self,role):
        handlers = []
        with open(self.repository.folderRepository()+'/roles/'+role.name+'/handlers/main.yml') as file:
            for h in yaml.full_load(file):
                handler = Handler()
                handler.deserialize(h)
                handlers.append(handler)
        return handlers

    def loadDefaults(self,role):
        with open(self.repository.folderRepository()+'/roles/'+role.name+'/defaults/main.yml') as file:
            return yaml.full_load(file)

    def loadFiles(self,role):
        return os.listdir(self.repository.folderRepository()+'/roles/'+role.name+'/files')

    def loadInventory(self):
        print(self.repository.folderRepository())
        print(os.listdir(self.repository.folderRepository()))
        print(filter(os.path.isfile, os.listdir(self.repository.folderRepository())))

    def deserialize(self, data):
        pass
        #self._groups_dict_cache = {}
        #self.hosts = data.get('hosts')
        #self.groups = data.get('groups')
        #self.localhost = data.get('local')
        #self.current_source = data.get('source')
        #self.processed_sources = data.get('processed_sources')

