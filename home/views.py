from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, View

from ticket.models import Ticket
from .forms import UserLoginForm, UserRegisterForm


# Create your views here.
class HomeView(TemplateView):
    template_name = 'home/home.html'


class LoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:admin')
        elif request.user.is_authenticated:
            return redirect('home:profile', username=request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'You are now logged in.', extra_tags='success')
            return redirect('home:profile', username=user.username)
        messages.error(self.request, 'Invalid username or password.', extra_tags='danger')
        return redirect('home:login')


class RegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:profile', username=request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'],
                                 email=form.cleaned_data['email'], first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'])
        messages.success(self.request, 'You are now registered.', extra_tags='success')
        return redirect('home:login')

    def form_invalid(self, form):
        messages.error(self.request, form.errors, extra_tags='danger')
        return redirect('home:register')


class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/profile.html'
    model = User

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user_instance = get_object_or_404(User, username=kwargs.get('username'))

    def dispatch(self, request, *args, **kwargs):
        if self.request.user != self.user_instance:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        contex['user'] = self.user_instance
        contex['user_ticket'] = Ticket.objects.filter(user=self.user_instance)

        return contex


class LogoutView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home:home')


class AdminView(LoginRequiredMixin, TemplateView):
    template_name = 'users/admin-dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff :
            messages.error(request, 'Just admin can see this page.', extra_tags='danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ticket = Ticket.objects.all()
        context['tickets'] = ticket
        context['open_tickets'] = ticket.filter(status='Open')
        context['in_progress_tickets'] = ticket.filter(status='In Progress')
        context['closed_tickets'] = ticket.filter(status='Closed')
        return context
