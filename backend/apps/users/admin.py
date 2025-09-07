from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Department

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('employee_code', 'email', 'firstname_th', 'lastname_th', 'status', 'role', 'is_staff')
    list_filter = ('status', 'role', 'is_staff', 'groups')
    search_fields = ('employee_code', 'firstname_th', 'lastname_th', 'email')
    ordering = ('employee_code',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('employee_code','time_attendance_code','prefix_th','firstname_th','lastname_th','prefix_en','firstname_en','lastname_en','email','phone_number','address','department')}),
        (_('Employment'), {'fields': ('start_date','status','exit_date','role','record_attendance','quota_sick','quota_casual','quota_vacation','groups')}),
        (_('Permissions'), {'fields': ('is_active','is_staff','is_superuser','user_permissions')}),
        (_('Important dates'), {'fields': ('last_login','date_joined')}),
    )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('full_name',)

    def full_name(self, obj):
        return f"{obj.name_th} ({obj.name_en})"
    full_name.short_description = "ห้องวิจัย"
