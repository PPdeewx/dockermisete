from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.users.models import CustomUser
from apps.leave.models import LeaveType, LeaveQuota
from django.utils import timezone

@receiver(post_save, sender=CustomUser)
def create_leave_quota_for_new_user(sender, instance, created, **kwargs):
    if created:
        current_year = timezone.now().year
        leave_types = LeaveType.objects.all()
        for lt in leave_types:
            LeaveQuota.objects.get_or_create(
                user=instance,
                leave_type=lt,
                year=current_year,
                defaults={
                    'quota_total': lt.default_quota,
                    'quota_used': 0
                }
            )
