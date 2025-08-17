from django.urls import path
from . import views

urlpatterns = [
    path('requests/', views.WorkOutsideRequestListView.as_view(), name='work_outside_requests'),
    path('request/create/', views.WorkOutsideRequestCreateView.as_view(), name='work_outside_request_create'),
    path('request/<int:pk>/', views.WorkOutsideRequestDetailView.as_view(), name='work_outside_request_detail'),
]