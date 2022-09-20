from django.views.generic import View
from django.conf import settings
from django.shortcuts import redirect, render


class HomeView(View):
    template_name = 'base/home.html'

    def get(self, request):
        #if settings.LOGIN_REQUIRED and not request.user.is_authenticated:
        #    return redirect("login")
        
        return render(request, self.template_name, {})