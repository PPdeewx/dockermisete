from celery import shared_task
from datetime import date
from .models import AttendanceRecord
from apps.leave.models import LeaveRequest
from apps.work_from_outside.models import WorkOutsideRequest
from django.utils import timezone

@shared_task
def calculate_daily_attendance():
    today = timezone.localdate()

    # ตรวจสอบผู้ใช้ทั้งหมด
    from apps.users.models import CustomUser
    users = CustomUser.objects.all()

    for user in users:
        # ตรวจสอบว่ามีวันลาเต็มวัน
        leave = LeaveRequest.objects.filter(
            user=user,
            start_date__lte=today,
            end_date__gte=today,
            status='approved'
        ).first()

        # ตรวจสอบว่ามี work-from-outside
        work_outside = WorkOutsideRequest.objects.filter(
            user=user,
            start_date__lte=today,
            end_date__gte=today,
            status='approved'
        ).first()

        status = 'normal'
        leave_type = None

        if leave:
            status = 'leave'
            leave_type = leave.leave_type.name
        elif work_outside:
            status = 'remote'

        # update หรือ create AttendanceRecord
        record, _ = AttendanceRecord.objects.update_or_create(
            user=user,
            date=today,
            defaults={
                'status': status,
                'leave_type': leave_type,
                # check_in/out จะกรอกด้วย Upload Excel
                # ถ้าไม่มี check_in/out และ status normal => จะขึ้น absent ใน save()
            }
        )
