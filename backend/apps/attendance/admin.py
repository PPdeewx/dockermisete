from django.contrib import admin
from .models import AttendanceRecord

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ['get_user_full_name', 'date', 'check_in', 'check_out', 'late_minutes', 'early_leave_minutes', 'status', 'leave_type']
    list_filter = ['status', 'leave_type', 'date']
    readonly_fields = ['late_minutes', 'early_leave_minutes']

    def get_user_full_name(self, obj):
        return f"{obj.user.firstname_th} {obj.user.lastname_th}"
    get_user_full_name.short_description = 'ชื่อ-นามสกุล'