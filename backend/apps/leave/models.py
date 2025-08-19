from django.db import models
from django.utils import timezone
from decimal import Decimal
from apps.users.models import CustomUser
from django.conf import settings

HALF_CHOICES = (
    ('full', 'ทั้งวัน'),
    ('morning', 'ครึ่งเช้า'),
    ('afternoon', 'ครึ่งบ่าย'),
)

class LeaveType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    advance_days = models.IntegerField(default=0)

    allow_backdate = models.BooleanField(default=False)

    consumes_quota = models.BooleanField(default=True)

    default_quota = models.DecimalField(max_digits=5, decimal_places=1, default=0.0)

    def __str__(self):
        return self.name

class LeaveQuota(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leave_quotas')
    leave_type = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    year = models.PositiveIntegerField()
    quota_total = models.DecimalField(max_digits=6, decimal_places=1, default=0.0)
    quota_used = models.DecimalField(max_digits=6, decimal_places=1, default=0.0)

    class Meta:
        unique_together = ('user', 'leave_type', 'year')

    @property
    def quota_remaining(self):
        return max(Decimal('0.0'), self.quota_total - self.quota_used)

    def __str__(self):
        return f"{self.user} - {self.leave_type} - {self.year}"

class LeaveRequest(models.Model):
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    STATUS_CANCELLED = 'cancelled'

    STATUS_CHOICES = (
        (STATUS_PENDING, 'รออนุมัติ'),
        (STATUS_APPROVED, 'อนุมัติ'),
        (STATUS_REJECTED, 'ไม่อนุมัติ'),
        (STATUS_CANCELLED, 'ยกเลิก'),
    )

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='leave_requests')
    on_behalf_of = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='leave_requests_on_behalf',
        null=True,
        blank=True,
        help_text="ถ้าลาแทนคนอื่น ให้ระบุคนนี้"
    )
    leave_type = models.ForeignKey(LeaveType, on_delete=models.PROTECT)
    start_date = models.DateField()
    end_date = models.DateField()
    start_half = models.CharField(max_length=10, choices=HALF_CHOICES, default='full')
    end_half = models.CharField(max_length=10, choices=HALF_CHOICES, default='full')
    days = models.DecimalField(max_digits=6, decimal_places=1, default=0.0)
    reason = models.TextField(blank=True)
    approver = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='to_approve_leaves')
    substitute = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='substitute_for_leaves')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=STATUS_PENDING)
    request_date = models.DateTimeField(default=timezone.now)
    leave_number = models.CharField(max_length=20, unique=True, blank=True)
    
    created_by_admin = models.BooleanField(default=False)
    substitute_acknowledged = models.BooleanField(default=False)

    class Meta:
        ordering = ['-request_date']

    def save(self, *args, **kwargs):
        from django.db.models import Count
        if not self.leave_number:
            now = timezone.now()
            year = now.strftime('%y')
            month = now.strftime('%m')
            prefix = f'L-{year}{month}'
            same_prefix_count = LeaveRequest.objects.filter(leave_number__startswith=prefix).count() + 1
            self.leave_number = f'{prefix}{str(same_prefix_count).zfill(4)}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.leave_number} - {self.user}"