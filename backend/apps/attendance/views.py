import pandas as pd
from datetime import date, timedelta, datetime
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Sum, Q
from .models import AttendanceRecord
from .serializers import AttendanceRecordSerializer
from apps.users.models import CustomUser

class AttendanceRecordListView(generics.ListCreateAPIView):
    serializer_class = AttendanceRecordSerializer

    def get_queryset(self):
        queryset = AttendanceRecord.objects.all()
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        department_id = self.request.query_params.get('room')
        search_name = self.request.query_params.get('name')

        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d').date()
                end = datetime.strptime(end_date, '%Y-%m-%d').date()
                queryset = queryset.filter(date__range=[start, end])  # เปลี่ยนจาก date__date__range เป็น date__range
            except ValueError:
                return Response(
                    {"error": "รูปแบบวันที่ไม่ถูกต้อง ต้องเป็น YYYY-MM-DD"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        if department_id:
            queryset = queryset.filter(user__department__id=department_id)
        if search_name:
            queryset = queryset.filter(
                Q(user__firstname_th__icontains=search_name) |
                Q(user__lastname_th__icontains=search_name)
            )
        return queryset.order_by('date')

class AttendanceRecordDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AttendanceRecord.objects.all()
    serializer_class = AttendanceRecordSerializer

class MyAttendanceView(APIView):
    def get(self, request):
        today = date.today()
        start_date = today - timedelta(days=30)
        records = AttendanceRecord.objects.filter(
            Q(user=request.user) &
            (Q(date__gte=start_date) & Q(date__lte=today) | Q(status='leave', date__gt=today))
        ).order_by('date')

        serializer = AttendanceRecordSerializer(records, many=True)

        summary = {
            "absent_days": records.filter(status='absent').count(),
            "late_minutes": records.aggregate(Sum('late_minutes'))['late_minutes__sum'] or 0,
            "early_leave_minutes": records.aggregate(Sum('early_leave_minutes'))['early_leave_minutes__sum'] or 0,
            "leave_days": records.filter(status='leave').count(),
        }

        return Response({"records": serializer.data, "summary": summary})

class UserAttendanceView(APIView):
    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        records = AttendanceRecord.objects.filter(user=user).order_by('date')
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data)

class AnnualAttendanceSummary(APIView):
    def get(self, request):
        last_year = date.today().year - 1
        start_date = date(last_year, 1, 1)
        end_date = date(last_year, 12, 31)

        users = CustomUser.objects.filter(
            Q(attendancerecord__date__range=(start_date, end_date))
        ).distinct()

        data = []
        for user in users:
            records = AttendanceRecord.objects.filter(user=user, date__range=(start_date, end_date))
            data.append({
                "employee_code": user.employee_code,
                "full_name": f"{user.firstname_th} {user.lastname_th}",
                "start_date": user.start_date,
                "end_date": user.end_date,
                "total_late_minutes": records.aggregate(Sum('late_minutes'))['late_minutes__sum'] or 0,
                "total_early_leave_minutes": records.aggregate(Sum('early_leave_minutes'))['early_leave_minutes__sum'] or 0,
                "leave_days": records.filter(status='leave').count(),
            })

        return Response(data)

class UploadAttendanceExcel(APIView):
    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "ไม่มีไฟล์อัปโหลด"}, status=status.HTTP_400_BAD_REQUEST)

        df = pd.read_excel(file)
        errors = []
        for _, row in df.iterrows():
            try:
                user = CustomUser.objects.get(time_attendance_code=row['time_attendance_code'])
                AttendanceRecord.objects.update_or_create(
                    user=user,
                    date=row['date'],
                    defaults={
                        "check_in": row.get('check_in'),
                        "check_out": row.get('check_out'),
                        "status": row.get('status', 'normal'),
                        "leave_type": row.get('leave_type'),
                    }
                )
            except CustomUser.DoesNotExist:
                errors.append(f"ไม่พบผู้ใช้ที่มี time_attendance_code: {row['time_attendance_code']}")
                continue

        if errors:
            return Response({"message": "อัปโหลดเสร็จสิ้น แต่มีข้อผิดพลาดบางประการ", "errors": errors}, status=status.HTTP_207_MULTI_STATUS)
        return Response({"message": "อัปโหลดเสร็จสมบูรณ์"})