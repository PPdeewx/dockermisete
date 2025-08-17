from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import LeaveType, LeaveRequest, LeaveQuota
from .serializers import LeaveTypeSerializer, LeaveRequestSerializer, LeaveQuotaSerializer
from django.utils import timezone
from django.db import transaction
from apps.attendance.models import AttendanceRecord
from django.db import models

class IsApproverOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # approver or staff
        return request.user.is_staff or obj.approver == request.user

class LeaveTypeViewSet(viewsets.ModelViewSet):
    queryset = LeaveType.objects.all()
    serializer_class = LeaveTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.select_related('user','leave_type','approver','substitute').all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        
        # ถ้าเป็น admin/staff เห็นทุกคน
        if user.is_staff or getattr(user, 'role', '') == 'admin':
            return qs
        
        # ถ้าเป็นพนักงาน เห็นเฉพาะของตัวเอง
        if getattr(user, 'role', '') == 'employee':
            return qs.filter(user=user)
        
        # ถ้าไม่เข้าเงื่อนไขอื่น ๆ ให้ return ว่าง
        return qs.none()

    def perform_create(self, serializer):
        # ⭐ เพิ่มฟีเจอร์ลาแทน
        on_behalf_of = serializer.validated_data.get('on_behalf_of')
        if on_behalf_of:
            # ลาแทนคนอื่น
            serializer.save(user=self.request.user, on_behalf_of=on_behalf_of)
        else:
            # ลาให้ตัวเอง
            serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        instance = self.get_object()
        user = self.request.user

        # ตรวจสิทธิ์
        if not (user.is_staff or getattr(user, 'role', '') == 'admin' or instance.user == user):
            raise PermissionError('คุณไม่มีสิทธิ์แก้ไขการลานี้')

        if instance.status != LeaveRequest.STATUS_PENDING:
            raise Exception('ไม่สามารถแก้ไขได้เมื่ออนุมัติ/ไม่อนุมัติแล้ว')

        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def cancel(self, request, pk=None):
        lr = self.get_object()
        if lr.status == LeaveRequest.STATUS_APPROVED:
            # remove attendance records for that user/dates
            start = lr.start_date
            end = lr.end_date
            AttendanceRecord.objects.filter(user=lr.user, date__range=(start,end), status='ลา').delete()
            # decrease quota
            if lr.leave_type.consumes_quota:
                from decimal import Decimal
                year = start.year
                quota = LeaveQuota.objects.filter(user=lr.user, leave_type=lr.leave_type, year=year).first()
                if quota:
                    quota.quota_used = max(Decimal('0.0'), quota.quota_used - lr.days)
                    quota.save()
        lr.status = LeaveRequest.STATUS_CANCELLED
        lr.save()
        return Response({'status':'cancelled'})

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def approve(self, request, pk=None):
        lr = self.get_object()
        if not (request.user.is_staff or lr.approver == request.user):
            return Response({'detail':'ไม่มีสิทธิ์อนุมัติ'}, status=status.HTTP_403_FORBIDDEN)
        if lr.status != LeaveRequest.STATUS_PENDING:
            return Response({'detail':'สถานะไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)
        # approve
        with transaction.atomic():
            lr.status = LeaveRequest.STATUS_APPROVED
            lr.save()
            # create attendance records
            start = lr.start_date
            end = lr.end_date
            day = start
            while day <= end:
                AttendanceRecord.objects.update_or_create(user=lr.user, date=day, defaults={'status':'ลา'})
                day = day + timezone.timedelta(days=1)
            # increase quota
            if lr.leave_type.consumes_quota:
                from decimal import Decimal
                year = lr.start_date.year
                quota, _ = LeaveQuota.objects.get_or_create(user=lr.user, leave_type=lr.leave_type, year=year, defaults={
                    'quota_total': lr.leave_type.default_quota,
                    'quota_used': 0
                })
                quota.quota_used = quota.quota_used + lr.days
                quota.save()
        return Response({'status':'approved'})

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def reject(self, request, pk=None):
        lr = self.get_object()
        if not (request.user.is_staff or lr.approver == request.user):
            return Response({'detail':'ไม่มีสิทธิ์ไม่อนุมัติ'}, status=status.HTTP_403_FORBIDDEN)
        if lr.status != LeaveRequest.STATUS_PENDING:
            return Response({'detail':'สถานะไม่ถูกต้อง'}, status=status.HTTP_400_BAD_REQUEST)
        lr.status = LeaveRequest.STATUS_REJECTED
        lr.save()
        return Response({'status':'rejected'})

    @action(detail=True, methods=['get', 'post'], permission_classes=[permissions.IsAuthenticated])
    def acknowledge(self, request, pk=None):
        """
        ผู้ปฏิบัติงานแทนกดรับทราบ
        """
        lr = self.get_object()
        user = request.user

        # ตรวจสอบว่าเป็น substitute หรือไม่
        if lr.substitute != user:
            return Response({'detail': 'คุณไม่ได้ถูกระบุให้ปฏิบัติงานแทน'}, status=status.HTTP_403_FORBIDDEN)

        # ตรวจสอบว่า acknowledge ยังไม่ถูกทำ
        if getattr(lr, 'substitute_acknowledged', False):
            return Response({'detail': 'คุณได้ยืนยันการปฏิบัติงานแทนแล้ว'}, status=status.HTTP_400_BAD_REQUEST)

        # ทำเครื่องหมาย acknowledge
        lr.substitute_acknowledged = True
        lr.save()
        return Response({'status': 'acknowledged'})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def history(self, request):
        import datetime
        qyear = int(request.query_params.get('year', datetime.date.today().year))
        user = request.user
        qs = self.get_queryset().filter(start_date__year=qyear) | self.get_queryset().filter(start_date__gte=datetime.date.today())
        qs = qs.distinct().order_by('-start_date')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='history-user/(?P<user_id>[^/.]+)', permission_classes=[permissions.IsAuthenticated])
    def history_user(self, request, user_id=None):
        if not (request.user.is_staff or getattr(request.user, 'role', '') == 'admin'):
            return Response({'detail': 'ไม่มีสิทธิ์เข้าถึง'}, status=status.HTTP_403_FORBIDDEN)

        import datetime
        qyear = int(request.query_params.get('year', datetime.date.today().year))
        qs = LeaveRequest.objects.filter(user_id=user_id, start_date__year=qyear).order_by('-start_date')
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
