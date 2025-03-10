from django import forms

from ticket.models import Ticket, Messages


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['id', 'subject', 'description', 'file']

        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ticket Subject'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Describe your issue in detail'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),

        }


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = Messages
        fields = ['content', 'file']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),
        }
