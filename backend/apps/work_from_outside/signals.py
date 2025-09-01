from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import WorkOutsideRequest
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

@receiver(post_save, sender=WorkOutsideRequest)
def send_work_outside_email(sender, instance, created, **kwargs):
    if created:
        # URLs สำหรับปุ่มในอีเมล
        approve_url = f"{settings.BACKEND_URL}/api/work-from-outside/requests/{instance.id}/approve/"
        reject_url = f"{settings.BACKEND_URL}/api/work-from-outside/requests/{instance.id}/reject/"

        # 1) แจ้งผู้อนุมัติ
        if instance.approver and instance.approver.email:
            subject = f"คำขอปฏิบัติงานนอกสถานที่ #{instance.request_number} จาก {instance.user}"
            text_content = f"มีคำขอใหม่จาก {instance.user} กรุณาตรวจสอบ"
            html_content = f"""
                <p>เรียน {instance.approver}</p>
                <p>มีคำขอใหม่:</p>
                <ul>
                    <li>เลขที่คำขอ: {instance.request_number}</li>
                    <li>ผู้ขอ: {instance.user}</li>
                    <li>เหตุผล: {instance.reason}</li>
                    <li>สถานที่: {instance.location}</li>
                    <li>วันที่: {instance.start_date} ถึง {instance.end_date}</li>
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

        # 2) แจ้งผู้ร่วมปฏิบัติงาน
        for collaborator in instance.collaborators.all():
            if collaborator.email:
                subject = f"แจ้งปฏิบัติงานร่วม - คำขอ {instance.request_number}"
                text_content = f"คุณถูกระบุให้ปฏิบัติงานร่วมกับ {instance.user}"
                html_content = f"""
                    <p>เรียน {collaborator}</p>
                    <p>คุณถูกระบุให้ปฏิบัติงานร่วมกับ {instance.user} ในคำขอ {instance.request_number}</p>
                    <ul>
                        <li>เหตุผล: {instance.reason}</li>
                        <li>สถานที่: {instance.location}</li>
                        <li>วันที่: {instance.start_date} ถึง {instance.end_date}</li>
                    </ul>
                """
                email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [collaborator.email])
                email.attach_alternative(html_content, "text/html")
                email.send(fail_silently=True)

        # 3) แจ้งผู้ขอ (optional)
        if instance.user.email:
            subject = f"คำขอปฏิบัติงานนอกสถานที่ #{instance.request_number} ถูกสร้างแล้ว"
            text_content = f"คำขอของคุณถูกสร้างเรียบร้อย"
            email = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, [instance.user.email])
            email.send(fail_silently=True)
