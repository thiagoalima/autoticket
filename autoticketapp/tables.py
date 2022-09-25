import django_tables2 as tables
from django_tables2.columns import TemplateColumn

from .models import Ticket

class BaseTable(tables.Table):
    template_name = "django_tables2/bootstrap.html"

class TicketTable(tables.Table): 

    controls = TemplateColumn(template_name='autoticketapp/ticket_controls.html')

    class Meta:
        model = Ticket
        template_name = "django_tables2/bootstrap4.html"
        fields = ("numero","titulo","descricao","data_inicio","prioridade","controls" )