from django.urls import path

from . import views

app_name = 'ticket'
urlpatterns = [

    path('detail/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('create/', views.TicketCreateView.as_view(), name='ticket-create'),
]
