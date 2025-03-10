from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


STARTS_CHOICES = [
    ("Open", "Open"),
    ("In Progress", "In Progress"),
    ("Closed", "Closed"),
]


class Ticket(TimeStampedModel):
    subject = models.CharField(max_length=200)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ticket')
    file = models.FileField(upload_to='tickets/%Y/%m/%d', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STARTS_CHOICES, default='Open')

    def __str__(self):
        return f'{self.id}- {self.user.username} -  {self.status}'

    def get_absolute_url(self):
        return reverse('ticket:ticket-detail', kwargs={'ticket_id': self.pk})


class Messages(TimeStampedModel):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_messages')
    content = models.TextField()
    file = models.FileField(upload_to='tickets/%Y/%m/%d', null=True, blank=True)
    is_admin_response = models.BooleanField(default=False)

    def __str__(self):
        return f' {self.ticket.user.username}  -  {self.ticket.id}'
