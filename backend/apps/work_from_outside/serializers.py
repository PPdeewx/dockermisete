from rest_framework import serializers
from .models import WorkOutsideRequest

class WorkOutsideRequestSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    approver = serializers.StringRelatedField()
    collaborators = serializers.StringRelatedField(many=True)

    class Meta:
        model = WorkOutsideRequest
        fields = '__all__'