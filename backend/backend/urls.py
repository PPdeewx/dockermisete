from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from apps.users.views import UserCreateView, LoginView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('api/users/', include('apps.users.urls')),
    path('api/leave/', include('apps.leave.urls')),
    path('api/work-from-outside/', include('apps.work_from_outside.urls')),
    path('api/holiday/', include('apps.holiday.urls')),
    path('api/attendance/', include('apps.attendance.urls')),
    path('api/login/', LoginView.as_view(), name='api_login'),
]