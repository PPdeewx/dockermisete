from django.core.management.base import BaseCommand
from apps.leave.models import LeaveType, LeaveQuota
from apps.users.models import CustomUser
import datetime

class Command(BaseCommand):
    help = 'Reset leave quotas for all users at the start of year (run on Jan 1 via cron/celery-beat)'

    def handle(self, *args, **options):
        year = datetime.date.today().year
        users = CustomUser.objects.all()
        leave_types = LeaveType.objects.filter(default_quota__gt=0)
        for user in users:
            for lt in leave_types:
                obj, created = LeaveQuota.objects.get_or_create(user=user, leave_type=lt, year=year, defaults={
                    'quota_total': lt.default_quota,
                    'quota_used': 0
                })
                if not created:
                    obj.quota_total = lt.default_quota
                    obj.quota_used = 0
                    obj.save()
        self.stdout.write(self.style.SUCCESS(f'Reset leave quotas for year {year}'))
