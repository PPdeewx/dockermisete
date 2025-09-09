from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser, Department


class UserSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'employee_code', 'firstname_th', 'lastname_th', 'email']

class UserSerializerWithDepartment(serializers.ModelSerializer):
    department = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ['id','firstname_th','lastname_th','department']

    def get_department(self, obj):
        if obj.department:
            return DepartmentSerializer(obj.department).data
            return {"id": obj.department.id, "name_th": obj.department.name_th}
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
        # สมมติเอา approvers คนแรกเป็นหัวหน้า
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
    groupName = serializers.SerializerMethodField()

    employee_code = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    time_attendance_code = serializers.CharField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'employee_code': {'required': True},
            'time_attendance_code': {'required': True},
            'prefix_th': {'required': True},
            'firstname_th': {'required': True},
            'lastname_th': {'required': True},
            'start_date': {'required': True},
            'phone_number': {'required': True},
            'email': {'required': True},
            'quota_sick': {'required': True},
            'quota_casual': {'required': True},
            'quota_vacation': {'required': True},
            'status': {'required': True},
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

    def validate(self, attrs):
        status = attrs.get('status', None)
        exit_date = attrs.get('exit_date', None)
        if status == 'resigned' and not exit_date:
            raise serializers.ValidationError({'exit_date': 'Exit date is required when status is resigned.'})

        groups = attrs.get('groups', None)
        if groups and len(groups) > 1:
            raise serializers.ValidationError({'groups': 'Only one group can be assigned. Send groups as an array with a single item.'})

        return attrs

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        password = validated_data.pop('password', None)

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