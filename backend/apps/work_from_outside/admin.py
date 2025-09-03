from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import WorkOutsideRequest

@admin.register(WorkOutsideRequest)
class WorkOutsideRequestAdmin(admin.ModelAdmin):
    list_display = ('request_number', 'user', 'approver', 'status', 'start_date', 'end_date')
    list_filter = ('status', 'approver')
    search_fields = ('request_number', 'user__username', 'approver__username')
