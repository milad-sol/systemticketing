from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

# Create your models here.
STARTS_CHOICES = [
    ("Open", "Open"),
    ("In Progress", "In Progress"),
    ("Closed", "Closed"),
]


class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_ticket')
    replay_to_ticket = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                                         related_name='tickets')
    subject = models.CharField(max_length=200)
    description = models.TextField()
    file = models.FileField(upload_to='media/ticket/%Y/%m/%d', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STARTS_CHOICES, default='Open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('ticket:ticket-detail', kwargs={'pk': self.pk})
