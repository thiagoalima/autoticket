from django.db import models
from ansible.cli.galaxy import GalaxyCLI
from django.conf import settings
from os.path import abspath
from git import Repo
import os

from iac.models import PlaybookFile,Inventory, LoadPlaybook

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

            cli = GalaxyCLI(args=["ansible-galaxy", "init", self.nome,"--init-path", self.folderRepository()+'/roles',"--force"])
            cli.run()
        
        self.playbookRepository = self.getPlaybookRepository()

        print(self.playbookRepository) 

        super(Repository, self).save(*args, **kwargs)
    
    def getPlaybookRepository(self):
        loadPlaybook = LoadPlaybook(folder=self.folderRepository())
        playbookFiles = loadPlaybook.loadPlaybookFiles()
        return PlaybookRepository(repository=self,playbookFiles=playbookFiles)
    
class PlaybookRepository():
    
    def __init__(self, repository:Repository,inventory:Inventory=None,playbookFiles:PlaybookFile=None) -> None:
        self.repository = repository
        self.playbookFiles = playbookFiles
        self.inventory = inventory
    
    

    



