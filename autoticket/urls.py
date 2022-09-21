from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('autoticket/', include('autoticketapp.urls')),
    path('autoticket/users', include('users.urls')),
    path('admin/', admin.site.urls),
]
