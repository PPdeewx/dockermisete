from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import WorkOutsideRequest
from .serializers import WorkOutsideRequestSerializer
from apps.attendance.models import AttendanceRecord
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
            return qs.filter(user=user)
        
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['get','post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        wr = self.get_object()
        if not (request.user.is_staff or wr.approver == request.user):
            return Response({'detail': 'ไม่มีสิทธิ์อนุมัติ'}, status=status.HTTP_403_FORBIDDEN)
        if wr.status != 'pending':
            return Response({'detail': 'สถานะไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)
        with transaction.atomic():
            wr.status = 'approved'
            wr.save()
            # บันทึก attendance ของ user + collaborators
            day = wr.start_date
            while day <= wr.end_date:
                AttendanceRecord.objects.update_or_create(user=wr.user, date=day, defaults={'status':'ปฏิบัติงานนอก'})
                for c in wr.collaborators.all():
                    AttendanceRecord.objects.update_or_create(user=c, date=day, defaults={'status':'ปฏิบัติงานนอก'})
                day += timezone.timedelta(days=1)
            # ส่ง email แจ้งผู้ขอ + collaborators
            recipients = [wr.user.email] + [c.email for c in wr.collaborators.all() if c.email]
            send_mail(
                subject=f"คำขอ {wr.request_number} อนุมัติแล้ว",
                message=f"คำขอของคุณถูกอนุมัติแล้ว",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                fail_silently=True
            )
        return Response({'status':'approved'})

    @action(detail=True, methods=['get','post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        wr = self.get_object()
        if not (request.user.is_staff or wr.approver == request.user):
            return Response({'detail': 'ไม่มีสิทธิ์ไม่อนุมัติ'}, status=status.HTTP_403_FORBIDDEN)
        if wr.status != 'pending':
            return Response({'detail': 'สถานะไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)
        wr.status = 'rejected'
        wr.save()
        # ส่ง email แจ้งผู้ขอ + collaborators
        recipients = [wr.user.email] + [c.email for c in wr.collaborators.all() if c.email]
        send_mail(
            subject=f"คำขอ {wr.request_number} ไม่อนุมัติ",
            message=f"คำขอของคุณถูกไม่อนุมัติ",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipients,
            fail_silently=True
        )
        return Response({'status':'rejected'})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        wr = self.get_object()
        if wr.status == 'pending':
            wr.status = 'cancelled'
            wr.save()
        return Response({'status':'cancelled'})
