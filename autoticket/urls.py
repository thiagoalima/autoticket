from django.contrib import admin
from django.urls import path, include

from autoticketapp.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('autoticket/', include('autoticketapp.urls')),
    path('autoticket/users', include('users.urls')),
    path('admin/', admin.site.urls),
]
