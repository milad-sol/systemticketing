from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DetailView, View, TemplateView
from django.shortcuts import redirect, render
from .forms import MessageForm, CreateTicketForm
from .models import Ticket, Messages


class TicketDetailView(LoginRequiredMixin, View):
    template_name = 'ticket/ticket-detail.html'
    form_class = MessageForm

    def setup(self, request, *args, **kwargs):
        self.user_ticket = Ticket.objects.get(id=kwargs['ticket_id'])
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):

        if request.user != self.user_ticket.user:
            messages.error(request, 'You are not authorized to view this ticket.', 'danger')
            return redirect('home:profile', username=request.user.username)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
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


class TicketCreateView(LoginRequiredMixin, FormView):
    template_name = 'ticket/create-ticket.html'
    form_class = CreateTicketForm
    model = Ticket

    def form_valid(self, form):
        new_ticket = form.save(commit=False)
        new_ticket.user = self.request.user
        new_ticket.save()
        messages.success(self.request, 'Ticket has been created.', 'success')
        return redirect('ticket:ticket-detail', ticket_id=new_ticket.id)


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


class TicketOpenListView(LoginRequiredMixin, TemplateView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    template_name = 'ticket/open_tickets_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['open_list'] = Ticket.objects.filter(status="Open")
        return context


class TicketInProgressListView(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    template_name = 'ticket/in_progress_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['in_progress_list'] = Ticket.objects.filter(status="In Progress")
        return context


class TicketCloseListView(TemplateView):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    template_name = 'ticket/close_list_tickets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['close_list'] = Ticket.objects.filter(status="Closed")
        return context
