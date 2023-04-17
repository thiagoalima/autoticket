from django.urls import path
from .views import InventoryParameterHTML, playbookParameterHTML

app_name = 'iac'

urlpatterns = [
    path('inventoryParameter/<str:parametro>/', InventoryParameterHTML, name='InventoryParameter_detail_html'),
    path('playbookParameter/<str:parametro>/', playbookParameterHTML, name='PlaybookParameter_detail_html'),
]