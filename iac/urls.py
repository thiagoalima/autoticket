from django.urls import path
from .views import InventoryParameterHTML

app_name = 'iac'

urlpatterns = [
    path('inventoryParameter/<str:parametro>/', InventoryParameterHTML, name='InventoryParameter_detail_html'),
]