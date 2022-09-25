from django.views.generic import View
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django_tables2 import SingleTableView
from django.shortcuts import  render

from .models import Ticket
from .tables import TicketTable
from .forms import TicketForm


class HomeView(View):
    template_name = 'base/home.html'

    def get(self, request):
        #if settings.LOGIN_REQUIRED and not request.user.is_authenticated:
        #    return redirect("login")
        
        return render(request, self.template_name, {})

class TicketListView(SingleTableView):
    model = Ticket
    table_class = TicketTable
    template_name = 'autoticketapp/ticket_list.html'

class TicketCreateView(CreateView):
    model = Ticket
    fields = ["numero","titulo","descricao","prioridade"]
    template_name = "autoticketapp/ticket_form.html"
    success_url = "/autoticket/ticket/"

class TicketUpdateView(UpdateView):
    model = Ticket
    fields = ["numero","titulo","descricao","prioridade"]
    template_name = "autoticketapp/ticket_form.html"
    success_url = "/autoticket/ticket/"

class TicketDeleteView(DeleteView):
    model = Ticket
    success_url = "/autoticket/ticket/"
    template_name = "autoticketapp/confirm_delete.html"