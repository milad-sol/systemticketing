from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

from .forms import UserLoginForm, UserRegisterForm


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home/home.html'


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'You are now logged in.', extra_tags='success')
            return redirect('home:home')
        messages.error(self.request, 'Invalid username or password.', extra_tags='danger')
        return redirect('home:login')


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def form_valid(self, form):
        User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'],
                                 email=form.cleaned_data['email'], first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'])
        messages.success(self.request, 'You are now registered.', extra_tags='success')
        return redirect('home:home')

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags='danger')
        return redirect('home:register')
