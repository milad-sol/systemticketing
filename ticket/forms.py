from django import forms

from ticket.models import Ticket, Messages


class CreateTicketForm(forms.ModelForm):
    """
    Form for creating a new support ticket.

    This ModelForm is tied to the Ticket model and collects the following information:
    - subject: Brief description of the ticket issue
    - description: Detailed explanation of the problem
    - file: Optional attachment for additional information

    All fields have Bootstrap styling applied via form widgets,
    with appropriate placeholders to guide user input.
    """

    class Meta:
        model = Ticket
        fields = ['subject', 'description', 'file']

        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Describe your issue in detail'}),
            'file': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'File'}),
        }


class MessageForm(forms.ModelForm):
    """
    Form for adding messages to an existing ticket.

    This ModelForm is tied to the Messages model and collects the following information:
    - content: The message text from the user or staff member
    - file: Optional attachment to provide additional context

    All fields have Bootstrap styling applied via form widgets,
    with appropriate placeholders to guide user input.
    """

    class Meta:
        model = Messages
        fields = ['content', 'file']

        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Describe your issue in detail'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
