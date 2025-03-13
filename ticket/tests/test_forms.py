from django.test import TestCase
from ticket.forms import CreateTicketForm, MessageForm
from django.contrib.auth.models import User
from model_bakery import baker
from ticket.models import Ticket, Messages


class TestCreateTicket(TestCase):
    def setUp(self):
        self.ticket = baker.make(Ticket)

    def test_create_ticket(self):
        form = CreateTicketForm(
            data={'subject': self.ticket.subject, 'description': self.ticket.description, 'file': self.ticket.file})
        self.assertTrue(form.is_valid())

    def test_create_ticket_empty(self):
        form = CreateTicketForm(data=None)
        self.assertFalse(form.is_valid())

    def test_create_ticket_without_subject(self):
        form = CreateTicketForm(data={'description': self.ticket.description, 'file': self.ticket.file})
        self.assertTrue(form.has_error('subject'))

    def test_create_ticket_without_description(self):
        form = CreateTicketForm(data={'subject': "test", "file": self.ticket.file})
        self.assertTrue(form.has_error('description'))
        self.assertEqual(len(form.errors), 1)


class TestMessages(TestCase):
    def setUp(self):
        self.ticket = baker.make(Ticket)
        self.user = baker.make(User)
        self.message = baker.make(Messages)

    def test_create_message(self):
        form = MessageForm(data={'content': self.message.content, 'file': self.message.file})
        self.assertTrue(form.is_valid())

    def test_invalid_message(self):
        form = MessageForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 1)

    def test_message_without_content(self):
        form = MessageForm(data={'file': self.message.file})
        self.assertTrue(form.has_error('content'))
