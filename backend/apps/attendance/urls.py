from django.urls import path
from . import views

urlpatterns = [
    path('records/', views.AttendanceRecordListView.as_view(), name='attendance_records'),
    path('record/<int:pk>/', views.AttendanceRecordDetailView.as_view(), name='attendance_record_detail'),
    path('my-attendance/', views.MyAttendanceView.as_view(), name='my_attendance'),
    path('user-attendance/<int:user_id>/', views.UserAttendanceView.as_view(), name='user_attendance'),
    path('annual-summary/', views.AnnualAttendanceSummary.as_view(), name='annual_summary'),
    path('upload-excel/', views.UploadAttendanceExcel.as_view(), name='upload_attendance_excel'),
]
