from rest_framework import serializers
from .models import Holiday

class HolidaySerializer(serializers.ModelSerializer):
    holiday_type_display = serializers.CharField(source='get_holiday_type_display', read_only=True)
    
    class Meta:
        model = Holiday
        fields = '__all__'

    def validate_date(self, value):
        if self.instance and self.instance.date == value:
            return value
        if Holiday.objects.filter(date=value).exists():
            raise serializers.ValidationError("วันหยุดนี้มีอยู่แล้ว")
        return value

class HolidayRangeSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    start_date = serializers.DateField()
    end_date = serializers.DateField()

    def validate(self, data):
        if data['start_date'] > data['end_date']:
            raise serializers.ValidationError("วันเริ่มต้นต้องน้อยกว่าหรือเท่ากับวันสิ้นสุด")
        return data

    def create(self, validated_data):
        from datetime import timedelta

        name = validated_data['name']
        start_date = validated_data['start_date']
        end_date = validated_data['end_date']

        holidays = []
        current_date = start_date
        while current_date <= end_date:
            if not Holiday.objects.filter(date=current_date).exists():
                holidays.append(Holiday(name=name, date=current_date))
            current_date += timedelta(days=1)

        return Holiday.objects.bulk_create(holidays)