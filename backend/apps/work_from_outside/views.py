from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WorkOutsideRequest
from .serializers import WorkOutsideRequestSerializer
from apps.attendance.models import AttendanceRecord
from apps.users.models import CustomUser
from django.utils import timezone
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings

class WorkOutsideRequestViewSet(viewsets.ModelViewSet):
    queryset = WorkOutsideRequest.objects.prefetch_related('collaborators').all()
    serializer_class = WorkOutsideRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if getattr(user, 'role', '') == 'admin':
            return qs
        elif getattr(user, 'role', '') == 'approver':
            return qs.filter(approver=user, status='pending')
        else:
            return qs.filter(Q(user=user) | Q(proxy_user=user))

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def proxy(self, request):
        user_id = request.data.get('user')
        approver_id = request.data.get('approver')
        collaborator_ids = request.data.get('collaborators', [])
        
        try:
            user = CustomUser.objects.get(id=user_id)
            approver = CustomUser.objects.get(id=approver_id)
            collaborators = CustomUser.objects.filter(id__in=collaborator_ids)
        except CustomUser.DoesNotExist:
            return Response({'detail': 'ไม่พบผู้ใช้หรือผู้อนุมัติ'}, status=status.HTTP_404_NOT_FOUND)

        if not (request.user.is_staff or request.user.groups.filter(name='manager').exists()):
            return Response({'detail': 'ไม่มีสิทธิ์ยื่นคำขอแทนผู้อื่น'}, status=status.HTTP_403_FORBIDDEN)

        work_request = WorkOutsideRequest(
            user=user,
            proxy_user=request.user,
            start_date=request.data.get('start_date'),
            end_date=request.data.get('end_date'),
            time_period=request.data.get('time_period'),
            reason=request.data.get('reason'),
            location=request.data.get('location'),
            approver=approver,
            status='pending'
        )
        work_request.save()
        work_request.collaborators.set(collaborators)

        recipients = [user.email, approver.email] + [c.email for c in collaborators if c.email]
        send_mail(
            subject=f"คำขอปฏิบัติงานนอกสถานที่ #{work_request.request_number} (ยื่นโดย {request.user})",
            message=f"คำขอปฏิบัติงานนอกสถานที่สำหรับ {user} ถูกสร้างโดย {request.user}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=True
        )

        serializer = self.get_serializer(work_request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        wr = self.get_object()
        if not (request.user.is_staff or wr.approver == request.user):
            return Response({'detail': 'ไม่มีสิทธิ์อนุมัติ'}, status=status.HTTP_403_FORBIDDEN)
        if wr.status != 'pending':
            return Response({'detail': 'สถานะไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            wr.status = 'approved'
            wr.save()
            day = wr.start_date
            while day <= wr.end_date:
                AttendanceRecord.objects.update_or_create(user=wr.user, date=day, defaults={'status': 'ปฏิบัติงานนอก'})
                for c in wr.collaborators.all():
                    AttendanceRecord.objects.update_or_create(user=c, date=day, defaults={'status': 'ปฏิบัติงานนอก'})
                day += timezone.timedelta(days=1)
            recipients = [wr.user.email, wr.proxy_user.email] + [c.email for c in wr.collaborators.all() if c.email]
            send_mail(
                subject=f"คำขอ {wr.request_number} อนุมัติแล้ว",
                message=f"คำขอของคุณถูกอนุมัติแล้ว",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=True
            )
        return Response({'status': 'approved'})

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        wr = self.get_object()
        if not (request.user.is_staff or wr.approver == request.user):
            return Response({'detail': 'ไม่มีสิทธิ์ไม่อนุมัติ'}, status=status.HTTP_403_FORBIDDEN)
        if wr.status != 'pending':
            return Response({'detail': 'สถานะไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)
        wr.status = 'rejected'
        wr.save()
        recipients = [wr.user.email, wr.proxy_user.email] + [c.email for c in wr.collaborators.all() if c.email]
        send_mail(
            subject=f"คำขอ {wr.request_number} ไม่อนุมัติ",
            message=f"คำขอของคุณถูกไม่อนุมัติ",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=True
        )
        return Response({'status': 'rejected'})