from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveTypeViewSet, LeaveRequestViewSet , LeaveQuotaViewSet

router = DefaultRouter()
router.register(r'leave-types', LeaveTypeViewSet, basename='leave-type')
router.register(r'leave-requests', LeaveRequestViewSet, basename='leave-request')
router.register(r'leave-quotas', LeaveQuotaViewSet, basename='leave-quota')

urlpatterns = [
    path('', include(router.urls)),
]
