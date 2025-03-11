from django.contrib import admin

from ticket.models import Ticket, Messages


# Register your models here.


class MessageInline(admin.TabularInline):
    model = Messages
    extra = 0
    list_editable = ['sender', 'created_at']
    raw_id_fields = ['sender', ]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'subject', 'status', 'created_at', 'updated_at']
    list_filter = ('status', 'status', 'created_at')
    search_fields = ('subject', 'description', 'user__username')
    list_editable = ('status',)
    inlines = (MessageInline,)

# @admin.register(Messages)
# class MessagesAdmin(admin.ModelAdmin):
#     list_display = ['id', 'ticket', 'sender', 'is_admin_response', 'created_at']
#     list_filter = ('is_admin_response', 'created_at')
#     search_fields = ('content', 'ticket__subject', 'sender__username')
#     raw_id_fields = ['sender']
