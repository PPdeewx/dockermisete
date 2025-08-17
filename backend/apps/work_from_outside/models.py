from django.db import models
from apps.users.models import CustomUser
from django.utils import timezone

class WorkOutsideRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'รออนุมัติ'),
        ('approved', 'อนุมัติ'),
        ('rejected', 'ไม่อนุมัติ'),
        ('cancelled', 'ยกเลิก'),
    )
    TIME_CHOICES = (
        ('full', 'ทั้งวัน'),
        ('morning', 'ครึ่งเช้า'),
        ('afternoon', 'ครึ่งบ่าย'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    time_period = models.CharField(max_length=10, choices=TIME_CHOICES)
    reason = models.TextField()
    location = models.CharField(max_length=200)
    approver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='approved_work_outside')
    collaborators = models.ManyToManyField(CustomUser, related_name='collaborated_work_outside', blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    request_date = models.DateTimeField(default=timezone.now)
    request_number = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.request_number:
            year = timezone.now().strftime('%y')
            month = timezone.now().strftime('%m')
            last_number = WorkOutsideRequest.objects.filter(request_number__startswith=f'W-{year}{month}').count()
            self.request_number = f'W-{year}{month}{str(last_number + 1).zfill(3)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.request_number} - {self.user}"