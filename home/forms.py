from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserLoginForm(forms.Form):
    """
    Form for user authentication.

    This form handles user login with username and password fields.
    Both fields have Bootstrap styling applied via form widgets.
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(forms.Form):
    """
    Form for user registration.

    This form collects and validates user registration information including:
    username, first name, last name, email, password, and password confirmation.
    All fields have Bootstrap styling applied via form widgets.

    The form performs validation to ensure:
    - Username uniqueness
    - Email uniqueness
    - Password matching between the two password fields
    """
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        """
        Validate that the username is unique.

        Checks the database to ensure no existing user has the same username.

        Returns:
            str: The validated username

        Raises:
            ValidationError: If the username already exists in the database
        """
        username = self.cleaned_data['username']
        user_in_database = User.objects.filter(username=username).exists()
        if user_in_database:
            raise ValidationError("Username already exists")
        return username

    def clean_confirm_password(self):
        """
        Validate that the password and confirm password fields match.

        Compares the two password fields to ensure they contain the same value.

        Returns:
            str: The validated confirm password

        Raises:
            ValidationError: If the passwords don't match
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords don't match")
        return confirm_password

    def clean_email(self):
        """
        Validate that the email is unique.

        Checks the database to ensure no existing user has the same email address.

        Returns:
            str: The validated email

        Raises:
            ValidationError: If the email already exists in the database
        """
        email = self.cleaned_data['email']
        email_in_database = User.objects.filter(email=email).exists()
        if email_in_database:
            raise ValidationError("Email already exists")
        return email