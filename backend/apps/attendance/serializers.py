from rest_framework import serializers
from .models import AttendanceRecord
from apps.users.models import CustomUser

class AttendanceRecordSerializer(serializers.ModelSerializer):
    employee_code = serializers.CharField(source='user.employee_code', read_only=True)
    time_attendance_code = serializers.CharField(source='user.time_attendance_code', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = AttendanceRecord
        fields = '__all__'

    def get_full_name(self, obj):
        return f"{obj.user.firstname_th} {obj.user.lastname_th}"
