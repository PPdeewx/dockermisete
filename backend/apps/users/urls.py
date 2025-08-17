from django.urls import path
from .views import (
    UserListView, UserFilterView, UserCreateView, UserDetailView,
    PasswordResetRequestView, UserUpdateProfileView, SetPasswordView  # import view ใหม่
)

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('filter/', UserFilterView.as_view(), name='user_filter'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('profile/', UserUpdateProfileView.as_view(), name='user_profile'),
    path('set-password/<uidb64>/<token>/', SetPasswordView.as_view(), name='set_password'),  # เพิ่มบรรทัดนี้
]
