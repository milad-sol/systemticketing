from django import forms

from ticket.models import Ticket, Messages


class CreateTicketForm(forms.ModelForm):
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
    class Meta:
        model = Messages
        fields = ['content', 'file']

        widgets = {

            'content': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Describe your issue in detail'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),

        }
