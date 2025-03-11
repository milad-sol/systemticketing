from django.urls import path

from . import views

app_name = 'ticket'
urlpatterns = [

    path('detail/<ticket_id>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('create/', views.TicketCreateView.as_view(), name='ticket-create'),
    path('close/<ticket_id>/', views.TicketCloseView.as_view(), name='ticket-close'),
    path('open/<ticket_id>/', views.TicketOpenView.as_view(), name='ticket-open'),

]
