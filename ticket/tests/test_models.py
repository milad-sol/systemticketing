from django.test import TestCase
from ticket.models import Ticket, Messages
from django.contrib.auth.models import User
from model_bakery import baker
from django.shortcuts import render
from django.urls import reverse, resolve
from ticket.views import TicketDetailView, TicketCreateView


class TestTicket(TestCase):

    def setUp(self):
        self.user = baker.make(User)
        self.ticket = baker.make(Ticket, user=self.user)

    def test_model_str(self):
        string = f'{self.ticket.id}- {self.user.username} -  {self.ticket.status}'
        self.assertEqual(str(string), string)

    def test_str_close_status(self):
        self.ticket.status = 'Closed'
        self.ticket.save()
        self.assertEqual(str(self.ticket.status), 'Closed')

    def test_get_absolute_url(self):
        url = reverse('ticket:ticket-detail', kwargs={'ticket_id': self.id})
        self.assertEqual(resolve(url).func.view_class, TicketDetailView)


class TestTicketMessage(TestCase):

    def setUp(self):
        self.user = baker.make(Messages)
        self.ticket = baker.make(Ticket)

    def test_model_str(self):
        string = f'{self.ticket.user.username} - {self.ticket.id}'
        self.assertEqual(str(string), string)
