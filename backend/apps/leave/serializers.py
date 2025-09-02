from rest_framework import serializers
from .models import LeaveType, LeaveRequest, LeaveQuota, HALF_CHOICES
from apps.users.serializers import UserSerializerShort
from decimal import Decimal
from datetime import date, timedelta
from apps.users.models import CustomUser

class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = '__all__'

class LeaveQuotaSerializer(serializers.ModelSerializer):
    leave_type = LeaveTypeSerializer(read_only=True)
    class Meta:
        model = LeaveQuota
        fields = ['id','leave_type','year','quota_total','quota_used']

class LeaveRequestSerializer(serializers.ModelSerializer):
    user = UserSerializerShort(read_only=True)
    leave_type = LeaveTypeSerializer(read_only=True)
    approver_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.none(),
        source='approver',
        write_only=True,
        required=False,
        allow_null=True
    )
    substitute_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.none(),
        source='substitute',
        write_only=True,
        required=False,
        allow_null=True
    )
    leave_type_id = serializers.PrimaryKeyRelatedField(
        queryset=LeaveType.objects.none(),
        source='leave_type',
        write_only=True
    )
    on_behalf_of_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        source='on_behalf_of',
        required=False,
        allow_null=True
    )
    on_behalf_of_name = serializers.CharField(source='on_behalf_of.username', read_only=True)
    
    period = serializers.ChoiceField(choices=HALF_CHOICES)
    
    class Meta:
        model = LeaveRequest
        fields = ['id','leave_number','user','on_behalf_of_id', 'on_behalf_of_name','leave_type','leave_type_id','start_date','end_date','period','days','reason','approver','approver_id','substitute','substitute_id','status','request_date','created_by_admin']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        from apps.users.models import CustomUser
        self.fields['approver_id'].queryset = CustomUser.objects.all()
        self.fields['substitute_id'].queryset = CustomUser.objects.all()
        from .models import LeaveType
        self.fields['leave_type_id'].queryset = LeaveType.objects.all()

    def validate(self, data):
        from .models import LeaveType, LeaveQuota
        user = self.context['request'].user
        leave_type = data.get('leave_type') or getattr(self.instance, 'leave_type', None)
        start = data.get('start_date') or getattr(self.instance, 'start_date', None)
        end = data.get('end_date') or getattr(self.instance, 'end_date', None)
        period = data.get('period') or getattr(self.instance, 'period', None)
        
        if not leave_type or not start or not end:
            raise serializers.ValidationError('leave_type, start_date and end_date are required.')

        if end < start:
            raise serializers.ValidationError('end_date ต้องไม่ต่ำกว่า start_date')

        days = Decimal((end - start).days + 1)

        if start == end:
            if start_half != end_half:
                days = Decimal('1.0')
            else:
                days = Decimal('0.5')
        else:
            if start_half == 'afternoon':
                days -= Decimal('0.5')
            if end_half == 'morning':
                days -= Decimal('0.5')

        data['days'] = days.quantize(Decimal('0.1'))

        from django.utils import timezone
        today = timezone.localdate()
        if not leave_type.allow_backdate:
            min_start = today + timedelta(days=leave_type.advance_days)
            if start < min_start:
                raise serializers.ValidationError(f'ต้องขอล่วงหน้า {leave_type.advance_days} วันสำหรับการลา {leave_type.name}')

        if leave_type.consumes_quota:
            year = start.year
            quota, _ = LeaveQuota.objects.get_or_create(
                user=user,
                leave_type=leave_type,
                year=year,
                defaults={
                    'quota_total': leave_type.default_quota,
                    'quota_used': 0
                }
            )
            if days > Decimal(quota.quota_total) - Decimal(quota.quota_used):
                raise serializers.ValidationError('จำนวนวันลาเกินสิทธิ์คงเหลือ')

        return data