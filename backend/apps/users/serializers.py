from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Department
from apps.leave.models import LeaveType, LeaveQuota
from django.utils import timezone

class UserSerializerShort(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'employee_code', 'firstname_th', 'lastname_th', 'email', 'department']

    def get_department(self, obj):
        if obj.department:
            return {'id': obj.department.id, 'name_th': obj.department.name_th}
        return None

class UserSerializerWithDepartment(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id', 'firstname_th', 'lastname_th', 'department']

    def get_department(self, obj):
        if obj.department:
            return DepartmentSerializer(obj.department).data
        return None

class DepartmentSerializer(serializers.ModelSerializer):
    head = serializers.SerializerMethodField()
    personnel = serializers.SerializerMethodField()
    total_users = serializers.SerializerMethodField()
    approvers = UserSerializerShort(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ["id", "name_th", "name_en", "head", "personnel", "total_users", "approvers"]

    def get_head(self, obj):
        if obj.approvers.exists():
            return f"{obj.approvers.first().firstname_th} {obj.approvers.first().lastname_th}"
        return None

    def get_personnel(self, obj):
        users = CustomUser.objects.filter(department=obj)
        return [f"{u.firstname_th} {u.lastname_th}" for u in users]
    
    def get_total_users(self, obj):
        return CustomUser.objects.filter(department=obj).count()

class CustomUserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        queryset=Group.objects.all(),
        slug_field='name',
        required=False,
        many=True
    )
    department = DepartmentSerializer(read_only=True)
    external_department = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    prefix_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    firstname_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    lastname_en = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    groupName = serializers.SerializerMethodField()
    quota_sick = serializers.SerializerMethodField()
    quota_casual = serializers.SerializerMethodField()
    quota_vacation = serializers.SerializerMethodField()
    quota_other = serializers.SerializerMethodField()

    employee_code = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())],
        required=False,
        allow_null=True
    )
    time_attendance_code = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())],
        required=False,
        allow_null=True
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'employee_code', 'time_attendance_code', 'prefix_th', 'firstname_th', 'lastname_th',
            'prefix_en', 'firstname_en', 'lastname_en', 'email', 'phone_number', 'address', 'department', 'external_department',
            'role', 'status', 'start_date', 'exit_date', 'groups', 'groupName', 'quota_sick', 'quota_casual', 'quota_vacation', 'quota_other'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'prefix_th': {'required': False},
            'firstname_th': {'required': False},
            'lastname_th': {'required': False},
            'start_date': {'required': False},
            'phone_number': {'required': False},
            'email': {'required': True},
            'status': {'required': False},
            'role': {'required': False}
        }

    def get_department(self, obj):
        if obj.department:
            return {
                "id": obj.department.id,
                "name_th": obj.department.name_th,
            }
        return None

    def get_groupName(self, obj):
        if obj.groups.exists():
            return obj.groups.first().name
        return ""

    def get_quota_sick(self, obj):
        return obj.get_quota_remaining('ลาป่วย')

    def get_quota_casual(self, obj):
        return obj.get_quota_remaining('ลากิจ')

    def get_quota_vacation(self, obj):
        return obj.get_quota_remaining('ลาพักร้อน')

    def get_quota_other(self, obj):
        return obj.get_quota_remaining('ลาอื่นๆ')

    def validate(self, attrs):
        status = attrs.get('status', 'active')
        exit_date = attrs.get('exit_date', None)
        department = attrs.get('department', None)
        external_department = attrs.get('external_department', None)
        if status == 'resigned' and not exit_date:
            raise serializers.ValidationError({'exit_date': 'Exit date is required when status is resigned.'})

        if department and external_department:
            raise serializers.ValidationError({'external_department': 'Cannot specify both department and external department.'})

        groups = attrs.get('groups', ['external'])
        if groups and len(groups) > 1:
            raise serializers.ValidationError({'groups': 'Only one group can be assigned. Send groups as an array with a single item.'})

        return attrs

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', ['external'])
        password = validated_data.pop('password', None)
        validated_data.pop('context', None)

        validated_data.setdefault('role', 'employee')
        validated_data.setdefault('status', 'active')
        validated_data.setdefault('start_date', timezone.now())

        username = validated_data.get('employee_code') or validated_data.get('email')
        user = CustomUser(**validated_data)
        if not getattr(user, 'username', None):
            user.username = username

        if password:
            validate_password(password, user=user)
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save()

        if groups_data:
            user.groups.set([Group.objects.get_or_create(name=g)[0] for g in groups_data])

        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)
        password = validated_data.pop('password', None)

        if 'status' in validated_data and validated_data['status'] == 'active' and instance.status == 'resigned':
            instance.exit_date = None

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            validate_password(password, user=instance)
            instance.set_password(password)

        instance.save()

        if groups_data is not None:
            instance.groups.set([Group.objects.get_or_create(name=g)[0] for g in groups_data])

        return instance

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class ProfileUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = [
            'prefix_th', 'firstname_th', 'lastname_th', 'phone_number', 'address', 'password', 'email'
        ]