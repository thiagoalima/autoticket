from rest_framework import serializers

from .nested_serializers import *

from ..views import Ticket


__all__ = (
    'TicketSerializer',
)


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = '__all__'
    
