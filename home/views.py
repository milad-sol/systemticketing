from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import TemplateView, FormView, View

from ticket.models import Ticket
from .forms import UserLoginForm, UserRegisterForm


class HomeView(TemplateView):
    """
    Main home page view.

    Renders the application's home page template.
    """
    template_name = 'home/home.html'


class LoginView(FormView):
    """
    User login view.

    Handles user authentication and login functionality.
    Redirects authenticated users to their respective dashboards.
    """
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to redirect already authenticated users.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home if already authenticated,
                          otherwise proceed with normal dispatch
        """
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Process valid form submission for user login.

        Authenticates user credentials and redirects to the appropriate
        dashboard based on user role (staff or regular user).

        Args:
            form: Valid login form with cleaned data

        Returns:
            HTTP response: Redirect to appropriate dashboard on successful login,
                          or back to login page with error message on failure
        """
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            messages.success(self.request, 'You are now logged in.', extra_tags='success')
            if self.request.user.is_staff:
                return redirect('home:admin')
            else:
                return redirect('home:profile', username=user.username)
        messages.error(self.request, 'Invalid username or password.', extra_tags='danger')
        return redirect('home:login')


class RegisterView(FormView):
    """
    User registration view.

    Handles new user registration functionality.
    Creates a new user account and redirects to login page.
    """
    template_name = 'users/register.html'
    form_class = UserRegisterForm

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to redirect already authenticated users.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to profile if already authenticated,
                          otherwise proceed with normal dispatch
        """
        if request.user.is_authenticated:
            return redirect('home:profile', username=request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Process valid form submission for user registration.

        Creates a new user with the provided form data and redirects to login page.

        Args:
            form: Valid registration form with cleaned data

        Returns:
            HTTP response: Redirect to login page with success message
        """
        User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'],
                                 email=form.cleaned_data['email'], first_name=form.cleaned_data['first_name'],
                                 last_name=form.cleaned_data['last_name'])
        messages.success(self.request, 'You are now registered.', extra_tags='success')
        return redirect('home:login')

    def form_invalid(self, form):
        """
        Handle invalid form submission.

        Displays error messages and redirects back to registration page.

        Args:
            form: Invalid registration form with errors

        Returns:
            HTTP response: Redirect to registration page with error messages
        """
        messages.error(self.request, form.errors, extra_tags='danger')
        return redirect('home:register')


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    User profile view.

    Displays user profile information and their tickets.
    Access is restricted to the profile owner only.
    """
    template_name = 'users/profile.html'
    model = User

    def setup(self, request, *args, **kwargs):
        """
        Initialize view attributes before dispatch.

        Sets up the user instance based on the username URL parameter.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments including username
        """
        super().setup(request, *args, **kwargs)
        self.user_instance = get_object_or_404(User, username=kwargs.get('username'))

    def dispatch(self, request, *args, **kwargs):
        """
        Check permissions before proceeding with request handling.

        Ensures users can only view their own profiles.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home if not the profile owner,
                          otherwise proceed with normal dispatch
        """
        if self.request.user != self.user_instance:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add user profile and ticket data to template context.

        Retrieves user information and their tickets to display in the template.

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            dict: Context dictionary with user profile and ticket information
        """
        contex = super().get_context_data(**kwargs)
        contex['user'] = self.user_instance
        contex['user_ticket'] = Ticket.objects.filter(user=self.user_instance)

        return contex


class LogoutView(LoginRequiredMixin, View):
    """
    User logout view.

    Handles user logout functionality.
    Redirects to home page after successful logout.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to log out the user.

        Logs out the current user and redirects to the home page.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home page with success message
        """
        logout(request)
        messages.success(request, 'You are now logged out.', extra_tags='success')
        return redirect('home:home')


class AdminView(LoginRequiredMixin, TemplateView):
    """
    Admin dashboard view.

    Displays ticket statistics and system overview.
    Access is restricted to staff members only.
    """
    template_name = 'users/admin-dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check staff permissions before proceeding with request handling.

        Ensures only staff members can access the admin dashboard.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home if not staff,
                          otherwise proceed with normal dispatch
        """
        if not request.user.is_staff:
            messages.error(request, 'Just admin can see this page.', extra_tags='danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add ticket statistics to template context.

        Retrieves tickets in different statuses to display in the admin dashboard.

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            dict: Context dictionary with ticket statistics by status
        """
        context = super().get_context_data(**kwargs)
        ticket = Ticket.objects.all()
        context['tickets'] = ticket
        context['open_tickets'] = ticket.filter(status='Open')
        context['in_progress_tickets'] = ticket.filter(status='In Progress')
        context['closed_tickets'] = ticket.filter(status='Closed')
        return context