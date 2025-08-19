from django.db import models
from apps.users.models import CustomUser
from django.utils import timezone
from datetime import datetime, time, timedelta

class AttendanceRecord(models.Model):
    STATUS_CHOICES = [
        ('normal', 'ปกติ'),
        ('leave', 'ลา'),
        ('remote', 'ปฏิบัติงานนอกสถานที่'),
        ('absent', 'ขาดงาน'),
    ]

    LEAVE_TYPE_CHOICES = [
        ('sick', 'ลาป่วย'),
        ('personal', 'ลากิจ'),
        ('vacation', 'ลาพักร้อน'),
        ('other', 'อื่นๆ'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    check_in = models.TimeField(null=True, blank=True)
    check_out = models.TimeField(null=True, blank=True)
    late_minutes = models.PositiveIntegerField(default=0)
    early_leave_minutes = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='normal')
    leave_type = models.CharField(max_length=50, choices=LEAVE_TYPE_CHOICES, null=True, blank=True)

    def save(self, *args, **kwargs):
        work_start = time(9, 0)
        work_end = time(18, 0)

        if self.status in ['leave', 'remote']:
            self.late_minutes = 0
            self.early_leave_minutes = 0
        else:
            if self.check_in and self.check_in > work_start:
                delta = datetime.combine(self.date, self.check_in) - datetime.combine(self.date, work_start)
                self.late_minutes = int(delta.total_seconds() // 60)
            else:
                self.late_minutes = 0

            if self.check_out and self.check_out < work_end:
                delta = datetime.combine(self.date, work_end) - datetime.combine(self.date, self.check_out)
                self.early_leave_minutes = int(delta.total_seconds() // 60)
            else:
                self.early_leave_minutes = 0

            if not self.check_in and not self.check_out and self.status == 'normal':
                self.status = 'absent'

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.date}"
