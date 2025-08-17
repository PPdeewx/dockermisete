from rest_framework import generics
from .models import WorkOutsideRequest
from .serializers import WorkOutsideRequestSerializer  # สร้าง Serializer ต่อไป

class WorkOutsideRequestListView(generics.ListCreateAPIView):
    queryset = WorkOutsideRequest.objects.all()
    serializer_class = WorkOutsideRequestSerializer

class WorkOutsideRequestCreateView(generics.CreateAPIView):
    queryset = WorkOutsideRequest.objects.all()
    serializer_class = WorkOutsideRequestSerializer

class WorkOutsideRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = WorkOutsideRequest.objects.all()
    serializer_class = WorkOutsideRequestSerializer