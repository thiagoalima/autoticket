import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm as DjangoPasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import View

from .forms import ConfirmationForm, TokenForm

from .models import Token


#
# Login/logout
#

class LoginView(View):

    template_name = 'users/login.html'


    def get(self, request):
        form = AuthenticationForm(request)

        if request.user.is_authenticated:
            logger = logging.getLogger('users.auth.login')
            return self.redirect_to_next(request, logger)


        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request):

        form = AuthenticationForm(request, data=request.POST)
        logger = logging.getLogger('users.auth.login')

        if form.is_valid():

            # Authenticate user
            auth_login(request, form.get_user())
            messages.info(request, f"Logado como {request.user}.")

            return self.redirect_to_next(request,logger)

        else:
            messages.info(request,"Login ou Senha invalido")

        return render(request, self.template_name, {
            'form': form,
        })

    def redirect_to_next(self, request, logger):
        data = request.POST if request.method == "POST" else request.GET
        redirect_url = data.get('next', settings.LOGIN_REDIRECT_URL)

        if redirect_url and url_has_allowed_host_and_scheme(redirect_url, allowed_hosts=None):
            logger.debug(f"Redirecionando o usuario para {redirect_url}")
        else:
            if redirect_url:
                logger.warning(f"Ignorando 'next' URL passado para o form login: {redirect_url}")
            redirect_url = reverse('home')

        return HttpResponseRedirect(redirect_url)


class LogoutView(View):

    def get(self, request):

        # Log out the user
        username = request.user
        auth_logout(request)
  
        messages.info(request, "Você foi deslogado.")

        # Delete session key cookie (if set) upon logout
        response = HttpResponseRedirect(reverse('home'))
        response.delete_cookie('session_key')

        return response


#
# User profiles
#

class ChangePasswordView(LoginRequiredMixin, View):
    template_name = 'users/password.html'

    def get(self, request):

        form = DjangoPasswordChangeForm(user=request.user)

        return render(request, self.template_name, {
            'form': form,
        })

    def post(self, request):
        form = DjangoPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Seu password foi alterado com sucesso.")
            return redirect('home')

        return render(request, self.template_name, {
            'form': form,
        })


#
# API tokens
#

class TokenListView(LoginRequiredMixin, View):

    def get(self, request):

        tokens = Token.objects.filter(user=request.user)

        return render(request, 'users/api_tokens.html', {
            'tokens': tokens,
            'active_tab': 'api-tokens',
        })


class TokenEditView(LoginRequiredMixin, View):

    def get(self, request, pk=None):

        if pk:
            token = get_object_or_404(Token.objects.filter(user=request.user), pk=pk)
        else:
            token = Token(user=request.user)

        form = TokenForm(instance=token)

        return render(request, 'generic/object_edit.html', {
            'object': token,
            'form': form,
            'return_url': reverse('user:token_list'),
        })

    def post(self, request, pk=None):

        if pk:
            token = get_object_or_404(Token.objects.filter(user=request.user), pk=pk)
            form = TokenForm(request.POST, instance=token)
        else:
            token = Token(user=request.user)
            form = TokenForm(request.POST)

        if form.is_valid():
            token = form.save(commit=False)
            token.user = request.user
            token.save()

            msg = f"Modified token {token}" if pk else f"Token criado {token}"
            messages.success(request, msg)

            if '_addanother' in request.POST:
                return redirect(request.path)
            else:
                return redirect('user:token_list')

        return render(request, 'generic/object_edit.html', {
            'object': token,
            'form': form,
            'return_url': reverse('user:token_list'),
        })


class TokenDeleteView(LoginRequiredMixin, View):

    def get(self, request, pk):

        token = get_object_or_404(Token.objects.filter(user=request.user), pk=pk)
        initial_data = {
            'return_url': reverse('user:token_list'),
        }
        form = ConfirmationForm(initial=initial_data) 

        return render(request, 'generic/object_delete.html', {
            'object': token,
            'form': form,
            'return_url': reverse('user:token_list'),
        })

    def post(self, request, pk):

        token = get_object_or_404(Token.objects.filter(user=request.user), pk=pk)
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            token.delete()
            messages.success(request, "Token deletado")
            return redirect('user:token_list')

        return render(request, 'generic/object_delete.html', {
            'object': token,
            'form': form,
            'return_url': reverse('user:token_list'),
        })
