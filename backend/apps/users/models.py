from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Department(models.Model):
    name_th = models.CharField(max_length=200, verbose_name="ชื่อห้องวิจัย (ไทย)", default="-")
    name_en = models.CharField(max_length=200, verbose_name="ชื่อห้องวิจัย (อังกฤษ)", default="-")
    approvers = models.ManyToManyField('CustomUser', related_name='approver_departments', blank=True)

    def __str__(self):
        return f"{self.name_th} ({self.name_en})"

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('employee', 'Employee'),
    )
    STATUS_CHOICES = (
        ('active', 'พนักงานปัจจุบัน'),
        ('resigned', 'ลาออก'),
    )
    GROUP_CHOICES = (
        ('regular', 'พนักงานประจำ'),
        ('manager', 'ผู้บริหาร'),
        ('temporary', 'พนักงานชั่วคราว'),
        ('developer', 'Developer'),
        ('external', 'บุคลากรภายนอก'),
    )
    employee_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    time_attendance_code = models.CharField(max_length=20, unique=True, blank=True, null=True)
    prefix_th = models.CharField(max_length=10, blank=True, null=True)
    firstname_th = models.CharField(max_length=50, blank=True, null=True)
    lastname_th = models.CharField(max_length=50, blank=True, null=True)
    prefix_en = models.CharField(max_length=10, blank=True)
    firstname_en = models.CharField(max_length=50, blank=True)
    lastname_en = models.CharField(max_length=50, blank=True)
    start_date = models.DateField(default=timezone.now)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True)
    record_attendance = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    exit_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    external_department = models.CharField(max_length=200, blank=True, null=True, verbose_name="หน่วยงานภายนอก")

    def __str__(self):
        return f"{self.prefix_th} {self.firstname_th} {self.lastname_th}"

    def clean(self):
        if self.status == 'resigned' and not self.exit_date:
            raise ValidationError({'exit_date': 'Exit date is required when status is resigned.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def get_quota(self, leave_type_name, year=None):
        from apps.leave.models import LeaveQuota, LeaveType
        if year is None:
            year = timezone.now().year
        try:
            leave_type = LeaveType.objects.get(name=leave_type_name)
            print(f"Found LeaveType: {leave_type_name}, ID: {leave_type.id}, User: {self.username}, Year: {year}")
            quota = LeaveQuota.objects.filter(
                user=self,
                leave_type=leave_type,
                year=year
            ).first()
            if quota:
                print(f"Quota for {leave_type_name}, user {self.username}, year {year}: {quota.quota_total}")
                return float(quota.quota_total)
            else:
                print(f"No quota found for {leave_type_name}, user {self.username}, year {year}")
                return 0.0
        except LeaveType.DoesNotExist:
            print(f"LeaveType {leave_type_name} not found")
            return 0.0

    def get_quota_remaining(self, leave_type_name, year=None):
        from apps.leave.models import LeaveQuota, LeaveType
        if year is None:
            year = timezone.now().year
        try:
            leave_type = LeaveType.objects.get(name=leave_type_name)
            print(f"Found LeaveType for remaining: {leave_type_name}, ID: {leave_type.id}, User: {self.username}, Year: {year}")
            quota = LeaveQuota.objects.filter(
                user=self,
                leave_type=leave_type,
                year=year
            ).first()
            if quota:
                print(f"Quota remaining for {leave_type_name}, user {self.username}, year {year}: {quota.quota_remaining}")
                return float(quota.quota_remaining)
            else:
                print(f"No quota remaining found for {leave_type_name}, user {self.username}, year {year}")
                return 0.0
        except LeaveType.DoesNotExist:
            print(f"LeaveType {leave_type_name} not found for remaining")
            return 0.0