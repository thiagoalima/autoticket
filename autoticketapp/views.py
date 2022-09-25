from django.views.generic import View
from django.shortcuts import  render, redirect
from django.urls import reverse

from users.utilities.view import TableView, CreateView, UpdateView, DeleteView, DetailView
from .models import Ticket
from .tables import TicketTable


class HomeView(View):
    template_name = 'base/home.html'

    def get(self, request):
        if  not request.user.is_authenticated:
            url = "{}?next={}".format(reverse('user:login'), request.path )
            return redirect(url)
        
        return render(request, self.template_name, {})

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