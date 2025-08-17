from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Department(models.Model):
    name = models.CharField(max_length=100)
    approvers = models.ManyToManyField('CustomUser', related_name='approver_departments', blank=True)

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Head of Department'),
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
    quota_sick = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    quota_casual = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    quota_vacation = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)
    record_attendance = models.BooleanField(default=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    exit_date = models.DateField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')

    def __str__(self):
        return f"{self.prefix_th} {self.firstname_th} {self.lastname_th}"

    def clean(self):
        if self.status == 'resigned' and not self.exit_date:
            raise ValidationError({'exit_date': 'Exit date is required when status is resigned.'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
