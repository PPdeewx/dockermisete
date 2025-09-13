from rest_framework import serializers
from .models import WorkOutsideRequest
from apps.users.models import CustomUser
from apps.users.serializers import UserSimpleSerializer

class UserSimpleSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ["id", "full_name"]

    def get_full_name(self, obj):
        return f"{obj.firstname_th} {obj.lastname_th}"

class WorkOutsideRequestSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)
    approver = UserSimpleSerializer(read_only=True)
    collaborators = UserSimpleSerializer(many=True)
    proxy_user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = WorkOutsideRequest
        fields = "__all__"

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')
        user = attrs.get('user')
        approver = attrs.get('approver')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError({'end_date': 'วันที่สิ้นสุดต้องไม่มาก่อนวันที่เริ่มต้น'})
        
        if user and approver and user == approver:
            raise serializers.ValidationError({'approver': 'ผู้ปฏิบัติงานและผู้อนุมัติต้องไม่เป็นคนเดียวกัน'})

        return attrs
