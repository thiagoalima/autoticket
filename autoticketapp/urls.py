from django.urls import path

from . import views

app_name = 'autoticket'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('ticket/',views.TicketListView.as_view(), name='ticket'),
    path('ticket/<pk>',views.TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/add/',views.TicketCreateView.as_view(), name='ticket_add'),
    path('ticket/edit/<pk>',views.TicketUpdateView.as_view(), name='ticket_edit'),
    path('ticket/del/<pk>',views.TicketDeleteView.as_view(), name='ticket_del'),
]