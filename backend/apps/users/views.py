from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from rest_framework.decorators import api_view
from .models import CustomUser, Department
from .serializers import CustomUserSerializer, DepartmentSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated, AllowAny
from django.contrib.auth.tokens import default_token_generator
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model, authenticate
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError

User = get_user_model()

class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all().exclude(role='developer')
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

class UserFilterView(generics.ListAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        queryset = CustomUser.objects.exclude(role='developer')
        status_param = self.request.query_params.get('status', 'active')
        group = self.request.query_params.get('group', None)
        department = self.request.query_params.get('department', None)

        if status_param in ['active', 'resigned']:
            queryset = queryset.filter(status=status_param)
        if group:
            queryset = queryset.filter(groups__name=group)
        if department:
            queryset = queryset.filter(department__name=department)

        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(firstname_th__icontains=search) |
                Q(lastname_th__icontains=search) |
                Q(email__icontains=search)
            )
        return queryset

class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        user = serializer.save()
        self.send_set_password_email(user)

    def send_set_password_email(self, user):
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/password3/{uid}/{token}"
        email_body = (
            f"สวัสดี {user.firstname_th} {user.lastname_th},\n\n"
            f"ระบบได้รับการสร้างบัญชีให้คุณแล้ว กรุณาตั้งรหัสผ่านโดยคลิกที่ลิงก์ด้านล่าง:\n\n{reset_url}\n\n"
            "หมายเหตุ: รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร และต้องมีตัวพิมพ์ใหญ่, ตัวพิมพ์เล็ก, ตัวเลข และอักขระพิเศษ.\n\n"
            "หากมีปัญหา กรุณาติดต่อผู้ดูแลระบบ."
        )
        try:
            send_mail(
                'Set Your Password',
                email_body,
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {e}")

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminUser]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'status' in request.data and request.data['status'] == 'active' and instance.status == 'resigned':
            instance.exit_date = None
        return super().update(request, *args, **kwargs)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/password2/{uid}/{token}"
            email_body = (
                f"สวัสดี {user.firstname_th} {user.lastname_th},\n\n"
                f"คุณได้ร้องขอการรีเซ็ตรหัสผ่าน หากเป็นคำขอนี้ให้คลิกที่ลิงก์ด้านล่างเพื่อตั้งรหัสผ่านใหม่:\n\n{reset_url}\n\n"
                "หมายเหตุ: รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร และต้องมีตัวพิมพ์ใหญ่, ตัวพิมพ์เล็ก, ตัวเลข และอักขระพิเศษ.\n\n"
                "หากมีปัญหา กรุณาติดต่อผู้ดูแลระบบ."
            )
            try:
                send_mail(
                    'Reset Your Password',
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            return Response({"message": "Reset link sent"}, status=status.HTTP_200_OK)
        return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

class ProfileUpdateSerializer(CustomUserSerializer):
    class Meta(CustomUserSerializer.Meta):
        fields = ['prefix_th', 'firstname_th', 'lastname_th', 'phone_number', 'address', 'password', 'email']

class UserUpdateProfileView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'password' in request.data:
            password = request.data.get('password')
            try:
                validate_password(password, user=instance)
            except DjangoValidationError as e:
                return Response({"error": list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)
            instance.set_password(password)
            instance.save()
            if isinstance(request.data, dict):
                request.data.pop('password', None)
        return super().update(request, *args, **kwargs)

class SetPasswordView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

        if default_token_generator.check_token(user, token):
            return Response({"message": "Token valid, you can now set your password"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

        password = request.data.get('password')
        if not password:
            return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password, user=user)
        except DjangoValidationError as e:
            return Response({"error": list(e.messages)}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()
        return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=status.HTTP_200_OK)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "employee_code": user.employee_code,
            "firstname_th": user.firstname_th,
            "lastname_th": user.lastname_th,
            "email": user.email,
            "role": user.role,
            "status": user.status
        })

class PasswordResetValidateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({'error': 'Invalid link'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "firstname_th": getattr(user, "firstname_th", None),
            "lastname_th": getattr(user, "lastname_th", None),
            "role": getattr(user, "role", None),
            "profile": getattr(user, "profile_image_url", None),
        })

class UserForListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users = CustomUser.objects.exclude(role='developer')
        data = []
        for u in users:
            data.append({
                "id": u.id,
                "name": f"{u.prefix_th or ''} {u.firstname_th} {u.lastname_th}".strip(),
                "role": u.role
            })
        return Response(data)
    
class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]

class DepartmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        if CustomUser.objects.filter(department=instance).exists():
            raise ValidationError("ไม่สามารถลบ Department ได้เนื่องจากยังมีพนักงานอยู่ในแผนกนี้")
        instance.delete()