from django.views.generic import TemplateView, FormView

from ticket import forms


# Create your views here.
class TicketDetailView(TemplateView):
    template_name = 'ticket/ticket-detail.html'


class TicketCreateView(FormView):
    template_name = 'ticket/create-ticket.html'
    form_class = forms.TicketForm
    def form_valid(self, form):
        pass