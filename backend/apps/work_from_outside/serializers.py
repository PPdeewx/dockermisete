from rest_framework import serializers
from .models import WorkOutsideRequest
from apps.users.models import CustomUser

class UserSimpleSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = CustomUser
        fields = ["id", "full_name"]  # ส่งแค่ id กับชื่อ

    def get_full_name(self, obj):
        return f"{obj.firstname_th} {obj.lastname_th}"

class WorkOutsideRequestSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)  # หรือจะใช้ UserSimpleSerializer ก็ได้
    approver = UserSimpleSerializer(read_only=True)  # ส่ง object เลย
    collaborators = UserSimpleSerializer(many=True, read_only=True)

    class Meta:
        model = WorkOutsideRequest
        fields = "__all__"
