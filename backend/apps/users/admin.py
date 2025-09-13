from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Department
from django import forms
from apps.leave.models import LeaveType, LeaveQuota
from django.utils import timezone

class CustomUserAdminForm(forms.ModelForm):
    quota_sick = forms.DecimalField(max_digits=5, decimal_places=1, required=False)
    quota_casual = forms.DecimalField(max_digits=5, decimal_places=1, required=False)
    quota_vacation = forms.DecimalField(max_digits=5, decimal_places=1, required=False)

    class Meta:
        model = CustomUser
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        department = cleaned_data.get('department')
        external_department = cleaned_data.get('external_department')
        if department and external_department:
            self.add_error('external_department', 'Cannot specify both department and external department.')
        for quota_field in ['quota_sick', 'quota_casual', 'quota_vacation']:
            if cleaned_data.get(quota_field) is not None and cleaned_data[quota_field] < 0:
                self.add_error(quota_field, 'Quota cannot be negative.')
        return cleaned_data

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    form = CustomUserAdminForm
    model = CustomUser
    list_display = ('employee_code', 'email', 'firstname_th', 'lastname_th', 'status', 'role', 'is_staff', 'external_department')
    list_filter = ('status', 'role', 'is_staff', 'groups')
    search_fields = ('employee_code', 'firstname_th', 'lastname_th', 'email', 'external_department')
    ordering = ('employee_code',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('employee_code','time_attendance_code','prefix_th','firstname_th','lastname_th','prefix_en','firstname_en','lastname_en','email','phone_number','address','department', 'external_department')}),
        (_('Employment'), {'fields': ('start_date','status','exit_date','role','record_attendance','groups','quota_sick','quota_casual','quota_vacation')}),
        (_('Permissions'), {'fields': ('is_active','is_staff','is_superuser','user_permissions')}),
        (_('Important dates'), {'fields': ('last_login','date_joined')}),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        current_year = timezone.now().year
        leave_types = {lt.name: lt for lt in LeaveType.objects.filter(name__in=['ลาป่วย', 'ลากิจ', 'ลาพักร้อน'])}
        if form.cleaned_data.get('quota_sick'):
            LeaveQuota.objects.update_or_create(
                user=obj,
                leave_type=leave_types.get('ลาป่วย'),
                year=current_year,
                defaults={'quota_total': form.cleaned_data['quota_sick'], 'quota_used': 0}
            )
        if form.cleaned_data.get('quota_casual'):
            LeaveQuota.objects.update_or_create(
                user=obj,
                leave_type=leave_types.get('ลากิจ'),
                year=current_year,
                defaults={'quota_total': form.cleaned_data['quota_casual'], 'quota_used': 0}
            )
        if form.cleaned_data.get('quota_vacation'):
            LeaveQuota.objects.update_or_create(
                user=obj,
                leave_type=leave_types.get('ลาพักร้อน'),
                year=current_year,
                defaults={'quota_total': form.cleaned_data['quota_vacation'], 'quota_used': 0}
            )

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'head_name', 'total_users', 'approvers_count')
    list_filter = ('name_th',)
    search_fields = ('name_th', 'name_en')
    fields = ('name_th', 'name_en', 'head', 'approvers')

    def full_name(self, obj):
        return f"{obj.name_th} ({obj.name_en})"
    full_name.short_description = "ห้องวิจัย"

    def head_name(self, obj):
        return f"{obj.head.firstname_th} {obj.head.lastname_th}" if obj.head else "-"
    head_name.short_description = "หัวหน้าห้องวิจัย"

    def total_users(self, obj):
        return CustomUser.objects.filter(department=obj).count()
    total_users.short_description = "จำนวนพนักงาน"

    def approvers_count(self, obj):
        return obj.approvers.count()
    approvers_count.short_description = "จำนวนผู้มีสิทธิ์อนุมัติ"

    def get_readonly_fields(self, request, obj=None):
        if obj and CustomUser.objects.filter(department=obj).exists():
            return ('name_th', 'name_en')
        return ()

    def delete_model(self, request, obj):
        if CustomUser.objects.filter(department=obj).exists():
            self.message_user(request, "ไม่สามารถลบห้องวิจัยได้เนื่องจากยังมีพนักงานอยู่ในแผนกนี้", level='error')
            return
        obj.delete()