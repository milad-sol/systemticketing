from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, DetailView, View, TemplateView
from django.shortcuts import redirect, render, get_object_or_404
from .forms import MessageForm, CreateTicketForm
from .models import Ticket, Messages


class TicketDetailView(LoginRequiredMixin, View):
    """
    View for displaying ticket details and handling message submissions.

    This view allows users to view ticket details and add messages to an existing ticket.
    Access is restricted to the ticket owner and staff members.
    """
    template_name = 'ticket/ticket-detail.html'
    form_class = MessageForm

    def setup(self, request, *args, **kwargs):
        """
        Initialize view attributes before dispatch.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments including ticket_id
        """
        self.user_ticket = get_object_or_404(Ticket, id=kwargs['ticket_id'])
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Check permissions before proceeding with request handling.

        Ensures only the ticket owner or staff members can access the ticket details.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home if unauthorized, otherwise proceed with request
        """
        if not (request.user == self.user_ticket.user or request.user.is_staff):
            messages.error(request, 'You are not authorized to view this ticket.', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to display ticket details and message form.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Rendered template with ticket details and message form
        """
        form = self.form_class()
        user_ticket = self.user_ticket
        return render(request, self.template_name, {'ticket': user_ticket, 'form': form})

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to add a new message to the ticket.

        Creates a new message associated with the ticket, differentiating between
        regular user messages and admin responses.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to ticket detail page on success,
                          or rendered template with form errors
        """
        user_ticket = self.user_ticket
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            if request.user.is_staff:
                Messages.objects.create(content=form.cleaned_data['content'], sender=self.request.user,
                                        ticket=user_ticket, is_admin_response=True,
                                        file=form.cleaned_data['file'])
            else:
                Messages.objects.create(content=form.cleaned_data['content'], sender=self.request.user,
                                        ticket=user_ticket,
                                        file=form.cleaned_data['file'])
            messages.success(request, 'Message has been sent.', 'success')
            return redirect('ticket:ticket-detail', ticket_id=user_ticket.id)
        return render(request, self.template_name, {'ticket': user_ticket, 'form': form})


class TicketCreateView(LoginRequiredMixin, FormView):
    """
    View for creating a new support ticket.

    This view handles the creation of new tickets. Only authenticated users can create tickets.
    """
    template_name = 'ticket/create-ticket.html'
    form_class = CreateTicketForm
    model = Ticket

    def dispatch(self, request, *args, **kwargs):
        """
        Check authentication before proceeding with request handling.

        Ensures user is authenticated before allowing ticket creation.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to registration page if not authenticated,
                          otherwise proceed with request
        """
        if not request.user.is_authenticated:
            messages.error(request, 'You do not have an account.First you should create an account', 'danger')
            return redirect('home:register')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """
        Process valid form data to create a new ticket.

        Associates the ticket with the current user and saves it to the database.

        Args:
            form: Valid ticket creation form

        Returns:
            HTTP response: Redirect to the newly created ticket's detail page
        """
        new_ticket = form.save(commit=False)
        new_ticket.user = self.request.user
        new_ticket.save()
        messages.success(self.request, 'Ticket has been created.', 'success')
        return redirect('ticket:ticket-detail', ticket_id=new_ticket.id)


class TicketCloseView(LoginRequiredMixin, View):
    """
    View for closing an open ticket.

    This view allows ticket owners or staff members to close an active ticket.
    """
    template_name = 'ticket/close-ticket.html'

    def setup(self, request, *args, **kwargs):
        """
        Initialize view attributes before dispatch.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments including ticket_id
        """
        self.user_ticket = get_object_or_404(Ticket, id=kwargs['ticket_id'])
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Check permissions before proceeding with request handling.

        Ensures only the ticket owner or staff members can close the ticket.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home if unauthorized, otherwise proceed with request
        """
        if not (request.user == self.user_ticket.user or request.user.is_staff):
            messages.error(request, 'You can not close others ticket!!!', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to display ticket closure confirmation page.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Rendered template with ticket information for confirmation
        """
        ticket = self.user_ticket
        return render(request, self.template_name, {'ticket': ticket})

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to close the ticket.

        Changes the ticket status to "Closed" and redirects to the ticket detail page.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to ticket detail page after closing the ticket
        """
        ticket = self.user_ticket
        ticket.status = "Closed"
        ticket.save()
        return redirect('ticket:ticket-detail', self.user_ticket.id)


class TicketOpenView(LoginRequiredMixin, View):
    """
    View for reopening a closed ticket.

    This view allows ticket owners or staff members to reopen a previously closed ticket.
    """
    template_name = 'ticket/open-ticket.html'

    def setup(self, request, *args, **kwargs):
        """
        Initialize view attributes before dispatch.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments including ticket_id
        """
        self.user_ticket = get_object_or_404(Ticket, id=kwargs['ticket_id'])
        super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        """
        Check permissions before proceeding with request handling.

        Ensures only the ticket owner or staff members can reopen the ticket.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home if unauthorized, otherwise proceed with request
        """
        if not (request.user == self.user_ticket.user or request.user.is_staff):
            messages.error(request, 'You can not open others ticket!!!', 'danger')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to display ticket reopening confirmation page.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Rendered template with ticket information for confirmation
        """
        ticket = self.user_ticket
        return render(request, self.template_name, {'ticket': ticket})

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to reopen the ticket.

        Changes the ticket status to "Open" and redirects to the ticket detail page.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to ticket detail page after reopening the ticket
        """
        ticket = self.user_ticket
        ticket.status = "Open"
        ticket.save()
        return redirect('ticket:ticket-detail', ticket_id=ticket.id)


class TicketOpenListView(LoginRequiredMixin, TemplateView):
    """
    View for displaying a list of all open tickets.

    This view is restricted to staff members only and shows all tickets with an "Open" status.
    """
    template_name = 'ticket/open_tickets_list.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check staff permissions before proceeding with request handling.

        Ensures only staff members can view the list of open tickets.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home if not staff, otherwise proceed with request
        """
        if not request.user.is_staff:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add open tickets list to template context.

        Retrieves all tickets with "Open" status to display in the template.

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            dict: Context dictionary with open_list key containing open tickets
        """
        context = super().get_context_data(**kwargs)
        context['open_list'] = Ticket.objects.filter(status="Open")
        return context


class TicketInProgressListView(LoginRequiredMixin, TemplateView):
    """
    View for displaying a list of all in-progress tickets.

    This view is restricted to staff members only and shows all tickets with an "In Progress" status.
    """
    template_name = 'ticket/in_progress_list.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check staff permissions before proceeding with request handling.

        Ensures only staff members can view the list of in-progress tickets.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home if not staff, otherwise proceed with request
        """
        if not request.user.is_staff:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add in-progress tickets list to template context.

        Retrieves all tickets with "In Progress" status to display in the template.

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            dict: Context dictionary with in_progress_list key containing in-progress tickets
        """
        context = super().get_context_data(**kwargs)
        context['in_progress_list'] = Ticket.objects.filter(status="In Progress")
        return context


class TicketCloseListView(LoginRequiredMixin, TemplateView):
    """
    View for displaying a list of all closed tickets.

    This view is restricted to staff members only and shows all tickets with a "Closed" status.
    """
    template_name = 'ticket/close_list_tickets.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check staff permissions before proceeding with request handling.

        Ensures only staff members can view the list of closed tickets.

        Args:
            request: HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HTTP response: Redirect to home if not staff, otherwise proceed with request
        """
        if not request.user.is_staff:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Add closed tickets list to template context.

        Retrieves all tickets with "Closed" status to display in the template.

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            dict: Context dictionary with close_list key containing closed tickets
        """
        context = super().get_context_data(**kwargs)
        context['close_list'] = Ticket.objects.filter(status="Closed")
        return context