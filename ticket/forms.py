from django import forms

from ticket.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['subject', 'status', 'description', 'file']

        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter ticket Subject'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'placeholder': 'Describe your issue in detail'}),
            'file': forms.FileInput(attrs={'class': 'form-control'}),

        }
