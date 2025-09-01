from rest_framework import serializers
from .models import WorkOutsideRequest
from apps.users.models import CustomUser

class WorkOutsideRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # ใช้ request.user
    approver = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    collaborators = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = WorkOutsideRequest
        fields = '__all__'
