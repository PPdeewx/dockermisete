from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'check_in', 'check_out', 'late_minutes', 'early_leave_minutes', 'status', 'leave_type']
    list_filter = ['status', 'leave_type', 'date']
    readonly_fields = ['late_minutes', 'early_leave_minutes']
