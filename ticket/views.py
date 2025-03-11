from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DetailView, View, TemplateView
from django.shortcuts import redirect, render
from .forms import TicketForm
from .models import Ticket, Messages


class TicketDetailView(LoginRequiredMixin, View):
    template_name = 'ticket/ticket-detail.html'
    form_class = TicketForm

    def setup(self, request, *args, **kwargs):
        self.user_ticket = Ticket.objects.get(id=kwargs['ticket_id'])
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user != self.user_ticket.user:
            messages.error(request, 'You are not authorized to view this ticket.', 'danger')
            return redirect('home:profile', username=request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        user_ticket = self.user_ticket
        return render(request, self.template_name, {'ticket': user_ticket, 'form': form})

    def post(self, request, *args, **kwargs):
        user_ticket = self.user_ticket
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            Messages.objects.create(content=form.cleaned_data['content'], sender=self.request.user, ticket=user_ticket,
                                    file=form.cleaned_data['file'])
            messages.success(request, 'Message has been sent.', 'success')
            return redirect('ticket:ticket-detail', ticket_id=user_ticket.id)
        return render(request, self.template_name, {'ticket': user_ticket, 'form': form})


class TicketCreateView(FormView):
    pass


class TicketCloseView(LoginRequiredMixin, View):
    template_name = 'ticket/close-ticket.html'

    def get(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs['ticket_id'])
        return render(request, self.template_name, {'ticket': ticket})

    def post(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs['ticket_id'])
        ticket.status = "Closed"
        ticket.save()
        return redirect('home:profile', username=request.user.username)


class TicketOpenView(LoginRequiredMixin, View):
    template_name = 'ticket/open-ticket.html'

    def get(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs['ticket_id'])
        return render(request, self.template_name, {'ticket': ticket})

    def post(self, request, *args, **kwargs):
        ticket = Ticket.objects.get(id=kwargs['ticket_id'])
        ticket.status = "Open"
        ticket.save()
        return redirect('ticket:ticket-detail', ticket_id=ticket.id)
