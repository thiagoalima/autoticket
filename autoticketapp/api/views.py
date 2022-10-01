from rest_framework.routers import APIRootView
from rest_framework.viewsets import ModelViewSet
from users.querysets import RestrictedQuerySet

from ..models import  Ticket
from . import serializers

class AutoTicketRootView(APIRootView):
    """
    Raiz do autoticket API
    """
    def get_view_name(self):
        return 'Autoticket'


#
# Ticket
#

class TicketViewSet(ModelViewSet):
    queryset = RestrictedQuerySet(model=Ticket).all()
    serializer_class = serializers.TicketSerializer
