from django.urls import path

from . import views

app_name = 'autoticket'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    # Ticket urls
    path('ticket/',views.TicketListView.as_view(), name='ticket'),
    path('ticket/<pk>',views.TicketDetailView.as_view(), name='ticket_detail'),
    path('ticket/add/',views.TicketCreateView.as_view(), name='ticket_add'),
    path('ticket/edit/<pk>',views.TicketUpdateView.as_view(), name='ticket_edit'),
    path('ticket/del/<pk>',views.TicketDeleteView.as_view(), name='ticket_del'),
    
    # Template urls
    path('template/', views.TemplateListView.as_view(), name='template'),                   # All templates
    path('template/<pk>', views.TemplateDetailView.as_view(), name='template_detail'),      # Selected template
    path('template/add/', views.TemplateCreateView.as_view(), name='template_add'),         # Add new template
    path('template/edit/<pk>', views.TemplateUpdateView.as_view(), name='template_edit'),   # Edit selected template
    path('template/del/<pk>', views.TemplateDeleteView.as_view(), name='template_del'),     # Delete selected template
    
    # Team urls
    path('team/', views.TeamListView.as_view(), name='team'),                   # All teams
    path('team/<pk>', views.TeamDetailView.as_view(), name='team_detail'),      # Selected team
    path('team/add/', views.TeamCreateView.as_view(), name='team_add'),         # Add new team
    path('team/edit/<pk>', views.TeamUpdateView.as_view(), name='team_edit'),   # Edit selected team
    path('team/del/<pk>', views.TeamDeleteView.as_view(), name='team_del'),     # Delete selected team
]