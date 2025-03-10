from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DetailView, View
from django.shortcuts import redirect, render
from .forms import TicketForm
from .models import Ticket, Messages


class TicketDetailView(LoginRequiredMixin, View):
    template_name = 'ticket/ticket-detail.html'
    form_class = TicketForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user_ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        return render(request, self.template_name, {'ticket': user_ticket, 'form': form})

    def post(self, request, *args, **kwargs):
        user_ticket = Ticket.objects.get(id=self.kwargs['ticket_id'])
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            Messages.objects.create(content=form.cleaned_data['content'], sender=self.request.user, ticket=user_ticket,
                                    file=form.cleaned_data['file'])
            messages.success(request, 'Message has been sent.', 'success')
            return redirect('ticket:ticket-detail', ticket_id=user_ticket.id)
        return render(request, self.template_name, {'ticket': user_ticket, 'form': form})


class TicketCreateView(FormView):
    pass
