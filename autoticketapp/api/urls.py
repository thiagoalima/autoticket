from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'autoticket-api'

router = DefaultRouter()
router.APIRootView = views.AutoTicketRootView

# Ticket
router.register('ticket', views.TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
