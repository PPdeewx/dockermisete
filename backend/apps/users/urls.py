from django.urls import path
from .views import (
    UserListView, UserFilterView, UserCreateView, UserDetailView,
    PasswordResetRequestView, UserUpdateProfileView, SetPasswordView,
    CurrentUserView, PasswordResetValidateView, UserForListView,
    DepartmentListCreateView, DepartmentDetailView , GroupListView,
    ChangePasswordView
)

app_name = 'users'

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
    path('me/', CurrentUserView.as_view(), name='current_user'),
    path('filter/', UserFilterView.as_view(), name='user_filter'),
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password_reset'),
    path('profile/', UserUpdateProfileView.as_view(), name='user_profile'),
    path('set-password/<uidb64>/<token>/', SetPasswordView.as_view(), name='set_password'),
    path('password-reset-validate/<uidb64>/<token>/', PasswordResetValidateView.as_view(), name='password_reset_validate'),
    path("for-list/", UserForListView.as_view(), name="users-for-list"),
    path("departments/", DepartmentListCreateView.as_view(), name="department_list_create"),
    path("departments/<int:pk>/", DepartmentDetailView.as_view(), name="department_detail"),
    path("groups/", GroupListView.as_view(), name="group_list"),
    path("change-password/", ChangePasswordView.as_view(), name="change_password"),

]
