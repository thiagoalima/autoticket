from django.db import models


class Host():

    def __init__(self,value,variables={}):
        self.value = value
        self.variables = variables


class Group():

    def __init__(self,name,hosts=[], variables={},groups=[]):
        self.name = name
        self.hosts = hosts
        self.variables = variables
        self.groups = groups
    
class Inventory():

    def __init__(self,name, hosts=[], groups=[]):
        self.name = name
        self.hosts = hosts
        self.groups = groups

class Module():

    def __init__(self,name, attributes=[]):
        self.name = name
        self.attributes = attributes

class Task():

    def __init__(self,name, module, variables=[], handler=None, when=None):
        self.name = name
        self.module = module
        self.variables = variables
        self.notify = handler
        self.when = when

class Template():

    def __init__(self,name=None, attributes=[]):
        self.name = name
        self.attributes = attributes
    
    def deserialize(self, data):
        self.name = data['name']
        self.attributes = data['template']

class Handler():

    def __init__(self,name=None, module=None):
        self.name = name
        self.module = module

    def deserialize(self, data):
        for key, value in data.items():
            if key in 'name':
                self.name = value
            else:
                self.module = Module(name=key,attributes=value)
        

class Role():

    def __init__(self,name=None, variables=[], tasks=[], defaults=[], files=[], handlers = [], templates=[]):
        self.name = name
        self.variables = variables
        self.tasks = tasks
        self.defaults = defaults
        self.files = files
        self.handlers = handlers
        self.templates = templates
    
    def deserialize(self, data):
        self.name = data

class Playbook():

    def __init__(self,name=None, hosts=None, attributes=[],roles=[], variables = [], handlers=[],tasks=[]):
        self.name = name
        self.hosts = hosts
        self.attributes = attributes
        self.roles = roles
        self.variables = variables
        self.handlers = handlers
        self.tasks = tasks

    def deserialize(self, data):
        for item in data:
            self.name = item['name']
            self.hosts = item['hosts']
            for r in item.get('roles'):
                role = Role(name=r)
                self.roles.append(role)
    


