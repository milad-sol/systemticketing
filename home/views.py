from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect
from django.views.generic import TemplateView, FormView

from .forms import UserLoginForm


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
