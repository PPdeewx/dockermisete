from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .models import Holiday
from .serializers import HolidaySerializer, HolidayRangeSerializer


# แสดงวันหยุด (Table/Calendar)
class HolidayListView(generics.ListAPIView):
    queryset = Holiday.objects.all().order_by('date')
    serializer_class = HolidaySerializer


# เพิ่มวันหยุดทีละวัน (admin เท่านั้น)
class HolidayCreateView(generics.CreateAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [IsAdminUser]


# เพิ่มวันหยุดเป็นช่วง (admin เท่านั้น)
class HolidayRangeCreateView(generics.CreateAPIView):
    serializer_class = HolidayRangeSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        holidays = serializer.save()
        return Response({"created": len(holidays)}, status=status.HTTP_201_CREATED)


# แก้ไข/ลบ วันหยุดทีละวัน (admin เท่านั้น)
class HolidayDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [IsAdminUser]
