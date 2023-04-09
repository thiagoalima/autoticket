from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from .models import InventoryParameter

def InventoryParameterHTML(request, parametro):

    try:

        inventoryParameter = InventoryParameter.objects.get(id=int(parametro)) 
        html = None

        if inventoryParameter:
            if inventoryParameter.type.type in ['input','text','file','password']:
                html = '''<span class="input-group-text" >{name}</span> 
                        <input type="{type}" name="inventoryParameters" class="form-control" aria-describedby="{name}">
                    '''.format(name=inventoryParameter.name,type=inventoryParameter.type.type)
            elif inventoryParameter.type.type in ['radio','checkbox']:
                if inventoryParameter.value:
                    html = '<span class="input-group-text" >{name}</span> '.format(name=inventoryParameter.name)
                    for v in inventoryParameter.value.split(','):
                        html += '''<input type="{type}" name="inventoryParameters" value="{value}">
                                   <label>{value}</label><br>'''.format(value=inventoryParameter.value, type=inventoryParameter.type.type)
            elif inventoryParameter.type.type in ['select']:
                html = '<span class="input-group-text" >{name}</span> '.format(name=inventoryParameter.name)
                if inventoryParameter.value:
                    html += '<select class="form-select" name="inventoryParameters"> '
                    for v in inventoryParameter.value.split(','):
                        html += '<option value="{value}">{value}</option> '.format(value=v)
                    html += '</select> '   
        return HttpResponse(html)
    
    except ObjectDoesNotExist:
        return None
    


