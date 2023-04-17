from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.http import HttpResponse
from .models import InventoryParameter, PlaybookParameter

def getHtmlInventoryParameter(inventoryParameter,value=''):
    html = None

    if inventoryParameter:
        if inventoryParameter.type.type in ['input', 'text', 'file', 'password']:
                html = '''<span class="input-group-text" >{name}</span>
                        <input type="{type}" name="param__{name}" class="form-control" aria-describedby="{name}" value="{value}">
                    '''.format(name=inventoryParameter.name, type=inventoryParameter.type.type, value=value)
        elif inventoryParameter.type.type in ['radio', 'checkbox']:
                if inventoryParameter.value:
                    html = '<span class="input-group-text" >{name}</span> '.format(
                        name=inventoryParameter.name)
                    for v in inventoryParameter.value.split(','):
                        checked = 'checked' if v == value else None
                        html += '''<input type="{type}" name="param__{name}" value="{value}" {checked}>
                                   <label>{value}</label><br>'''.format(value=inventoryParameter.value, 
                                                                        type=inventoryParameter.type.type, 
                                                                        name=inventoryParameter.name,
                                                                        checked = checked)
        elif inventoryParameter.type.type in ['select']:
                html = '<span class="input-group-text" >{name}</span> '.format(
                    name=inventoryParameter.name)
                if inventoryParameter.value:
                    html += '<select class="form-select" name="param__{name}"> '.format(
                        name=inventoryParameter.name)
                    for v in inventoryParameter.value.split(','):
                        selected = 'selected' if v == value else None
                        html += '<option value="{value}" {selected}>{value}</option> '.format(
                            value=v, selected=selected)
                    html += '</select> '
    return html

def InventoryParameterHTML(request, parametro):

    try:

        inventoryParameter = InventoryParameter.objects.get(id=int(parametro)) 
        html = getHtmlInventoryParameter(inventoryParameter)

        return HttpResponse(html)
    
    except ObjectDoesNotExist:
        return None
    
def playbookParameterHTML(request, parametro):

    try:

        playbookParameter = PlaybookParameter.objects.get(id=int(parametro)) 
        html = getHtmlInventoryParameter(playbookParameter)

        return HttpResponse(html)
    
    except ObjectDoesNotExist:
        return None
    


