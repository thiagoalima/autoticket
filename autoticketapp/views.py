from django.views.generic import View
from django.shortcuts import  render, redirect
from django.urls import reverse

from users.utilities.view import TableView, CreateView, UpdateView, DeleteView, DetailView
from .models import Ticket
from .tables import TicketTable
from .models import Template

class HomeView(View):
    template_name = 'base/home.html'

    def get(self, request):
        if  not request.user.is_authenticated:
            url = "{}?next={}".format(reverse('user:login'), request.path )
            return redirect(url)
        
        return render(request, self.template_name, {})

"""
    Classes refering to the ticket views
"""
class TicketDetailView (DetailView):
    model = Ticket

class TicketListView(TableView):
    permission_required = 'autoticketapp.view_ticket'
    model = Ticket
    table_class = TicketTable
    template_name = 'autoticketapp/ticket_list.html'

class TicketCreateView(CreateView):
    permission_required = 'autoticketapp.add_ticket'
    model = Ticket
    fields = ["numero","titulo","descricao","prioridade"]
    template_name = "autoticketapp/ticket_form.html"

class TicketUpdateView(UpdateView):
    permission_required = 'autoticket.change_ticket'
    model = Ticket
    fields = ["numero","titulo","descricao","prioridade"]
    template_name = "autoticketapp/ticket_form.html"

class TicketDeleteView(DeleteView):
    permission_required = 'autoticket.delete_ticket'
    model = Ticket
    template_name = "autoticketapp/confirm_delete.html"
    
"""
    Classes refering to the Template views
"""

TEMPLATE_URL = '/autoticketapp/template/'

class TemplateDetailView (DetailView):
    model = Template

class TemplateListView(TableView):
    permission_required = 'autoticketapp.view_template'
    model = Template
    # table_class = TemplateTable
    template_name = 'autoticketapp/template_list.html'

class TemplateCreateView(CreateView):
    permission_required = 'autoticketapp.add_template'
    model = Template
    fields = ["nome", "codigo"]
    template_name = "autoticketapp/template_form.html"
    success_url = TEMPLATE_URL

class TemplateUpdateView(UpdateView):
    permission_required = 'autoticket.change_template'
    model = Template
    fields = ["nome", "codigo"]
    template_name = "autoticketapp/template_form.html"
    success_url = TEMPLATE_URL

class TemplateDeleteView(DeleteView):
    permission_required = 'autoticket.delete_template'
    model = Template
    template_name = "autoticketapp/confirm_delete.html"
    success_url = TEMPLATE_URL
