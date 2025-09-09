from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import LeaveRequest, LeaveQuota, LeaveType
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse
from apps.users.models import CustomUser
from django.utils import timezone

@receiver(post_save, sender=LeaveRequest)
def send_leave_email(sender, instance, created, **kwargs):
    if created:

        # 1) แจ้งผู้อนุมัติ
        if instance.approver and instance.approver.email:
            subject = f"คำขอลา #{instance.leave_number} จาก {instance.user}"
            text_content = f"มีคำขอลาจาก {instance.user} กรุณาตรวจสอบ"

            approve_url = f"{settings.BACKEND_URL}/api/leave/leave-requests/{instance.id}/approve/"
            reject_url = f"{settings.BACKEND_URL}/api/leave/leave-requests/{instance.id}/reject/"

            html_content = f"""
                <p>เรียน {instance.approver}</p>
                <p>มีคำขอลาใหม่:</p>
                <ul>
                    <li>เลขที่ใบลา: {instance.leave_number}</li>
                    <li>ผู้ลา: {instance.user}</li>
                    <li>ประเภท: {instance.leave_type.name}</li>
                    <li>วันที่ลา: {instance.start_date} ถึง {instance.end_date}</li>
                    <li>เหตุผล: {instance.reason}</li>
                </ul>
                <p>
                    <a href="{approve_url}" style="background-color:green;color:white;padding:10px 15px;text-decoration:none;border-radius:5px;">อนุมัติ</a>
                    &nbsp;
                    <a href="{reject_url}" style="background-color:red;color:white;padding:10px 15px;text-decoration:none;border-radius:5px;">ไม่อนุมัติ</a>
                </p>
            """

            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [instance.approver.email])
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=True)

        # 2) แจ้งผู้ปฏิบัติงานแทน
        if instance.substitute and instance.substitute.email:
            subject = f"แจ้งปฏิบัติงานแทน - คำขอลา #{instance.leave_number}"
            text_content = f"คุณถูกระบุให้ปฏิบัติงานแทน {instance.user}"

            acknowledge_url = f"{settings.BACKEND_URL}/api/leave/leave-requests/{instance.id}/acknowledge/"

            html_content = f"""
                <p>เรียน {instance.substitute}</p>
                <p>คุณถูกระบุให้ปฏิบัติงานแทนในช่วงที่ {instance.user} ลา</p>
                <ul>
                    <li>เลขที่ใบลา: {instance.leave_number}</li>
                    <li>ประเภท: {instance.leave_type.name}</li>
                    <li>วันที่ลา: {instance.start_date} ถึง {instance.end_date}</li>
                </ul>
                <p>
                    <a href="{acknowledge_url}" style="background-color:blue;color:white;padding:10px 15px;text-decoration:none;border-radius:5px;">รับทราบ</a>
                </p>
            """

            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [instance.substitute.email])
            email.attach_alternative(html_content, "text/html")
            email.send(fail_silently=True)

@receiver(post_save, sender=CustomUser)
def create_leave_quota_for_new_user(sender, instance, created, **kwargs):
    """
    สร้างโควต้าลาให้ User ใหม่โดยอัตโนมัติ
    """
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