from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.HolidayListView.as_view(), name='holiday_list'),
    path('create/', views.HolidayCreateView.as_view(), name='holiday_create'),
    path('create-range/', views.HolidayRangeCreateView.as_view(), name='holiday_create_range'),
    path('<int:pk>/', views.HolidayDetailView.as_view(), name='holiday_detail'),
]
