from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View, FormView

from ticket import forms
from .forms import TicketUpdateForm
from .models import Ticket


# Create your views here.
class TicketDetailView(LoginRequiredMixin, View):
    template_name = 'ticket/ticket-detail.html'
    form_class = TicketUpdateForm

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.ticket.user:
            messages.error(request, 'You are not authorized to view this ticket.', 'danger')
            return redirect('home:profile', self.request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def setup(self, request, *args, **kwargs):
        self.ticket = get_object_or_404(Ticket, id=kwargs['ticket_id'])
        self.all_ticket = self.ticket.messages.all()
        super().setup(request, *args, **kwargs)

    def get(self, request, ticket_id):
        ticket = self.ticket
        form = self.form_class()
        return render(request, self.template_name, {'ticket': ticket, 'form': form, 'all_ticket': self.all_ticket})

    def post(self, request, ticket_id):
        ticket = self.ticket
        all_ticket = self.all_ticket
        form = self.form_class(request.POST)
        if form.is_valid():
            new_ticket = form.save(commit=False)
            new_ticket.ticket = ticket
            new_ticket.sender = request.user
            new_ticket.save()
            messages.success(request, 'Ticket updated successfully', extra_tags='success')
            return render(request, self.template_name, {'ticket': ticket, 'form': form, 'all_ticket': all_ticket})
        return render(request, self.template_name, {'ticket': ticket, 'form': form, 'all_ticket': all_ticket})


class TicketCreateView(FormView):
    template_name = 'ticket/create-ticket.html'
    form_class = forms.TicketForm

    def form_valid(self, form):
        pass
