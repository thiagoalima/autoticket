from django.db import models
from ansible.playbook import Playbook
from ansible.parsing.yaml.dumper import AnsibleDumper
from ansible.parsing.dataloader import DataLoader
from ansible.cli.galaxy import GalaxyCLI
from django.conf import settings
from git import Repo
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
            
            cli = GalaxyCLI(args=["ansible-galaxy", "init", self.nome,"--init-path", self.folderRepository()+'/roles',"--force"])
            cli.run()
        
        self.playbookRepository = self.getPlaybookRepository()

        self.playbookRepository.salvarPlaybooks()

        super(Repository, self).save(*args, **kwargs)
    
    def getPlaybookRepository(self):
        loader = DataLoader()
        loader.set_basedir(self.folderRepository())

        plays = []

        for playbookFile in os.listdir(self.folderRepository()): 
            if playbookFile.endswith(".yml") or playbookFile.endswith(".yaml") :
                plays.append(Playbook.load(self.folderRepository()+'/'+playbookFile, loader=loader))

        return PlaybookRepository(repository=self,playbooks=plays)
    
class PlaybookRepository():
    
    def __init__(self, repository:Repository,playbooks=None):
        self.repository = repository
        self.playbooks = playbooks
    
    def retirar_nulos(self, data):
        return {k: v for k, v in data.items() if v}
    
    def salvarYaml(self, data, folder = None, filename = None):
        if not filename:
            filename = 'main.yml'
        if not folder:
            folder = self.repository.folderRepository()

        with open(folder+'/'+filename, 'w') as file:
                documents = yaml.dump([data], file, Dumper=AnsibleDumper, explicit_start=True, explicit_end=True, sort_keys=False, default_flow_style=False, default_style='')

    def salvarRoles(self, data):
        for r in data:
            self.salvarDefaults(data['_default_vars'])
            self.salvarHandlers(data['_handler_blocks'])
            self.salvarTasks(data['_task_blocks'])
            self.salvarVars(data['_role_vars'])

    def salvarPlaybooks(self):
        for playbook in self.playbooks:
            for p in playbook._entries:
                validos = self.retirar_nulos(p.serialize())
                del validos['strategy'] 
                del validos['uuid']

                self.salvarRoles(validos['roles'])
        
                data = {'name':validos.pop('name')}
                data.update(validos)
                roles = []
                for r in data['roles']:
                    roles.append(r['_role_name'])

                data['roles'] = roles

                self.salvarYaml(data,filename='main2.yml')
            
            

    
    

    



