from django.contrib import admin
from .models import LeaveType, LeaveQuota, LeaveRequest

@admin.register(LeaveType)
class LeaveTypeAdmin(admin.ModelAdmin):
    list_display = ['name','advance_days','allow_backdate','consumes_quota','default_quota']

@admin.register(LeaveQuota)
class LeaveQuotaAdmin(admin.ModelAdmin):
    list_display = ['user','leave_type','year','quota_total','quota_used']

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ['leave_number','user', 'on_behalf_of','leave_type','start_date','end_date','days','status']
    readonly_fields = ['leave_number','request_date']
    search_fields = ('user__username', 'on_behalf_of__username')