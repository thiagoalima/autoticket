import django_tables2 as tables
from django_tables2.utils import Accessor
from django_tables2.columns import TemplateColumn

from .models import Ticket

class BaseTable(tables.Table):
    template_name = "django_tables2/bootstrap.html"

class TicketTable(tables.Table):

    numero = tables.LinkColumn(
        viewname='autoticket:ticket_detail',
        args=[Accessor('id')]
    )

    controls = TemplateColumn(verbose_name=' ', template_name='autoticketapp/ticket_controls.html')

    class Meta:
        model = Ticket
        template_name = "django_tables2/bootstrap4.html"
        fields = ("numero","titulo","descricao","data_inicio","prioridade","controls" )