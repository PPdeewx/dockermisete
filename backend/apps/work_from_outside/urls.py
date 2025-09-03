from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WorkOutsideRequestViewSet

router = DefaultRouter()
router.register(r'requests', WorkOutsideRequestViewSet, basename='work-outside-request')

urlpatterns = [
    path('', include(router.urls)),
]
