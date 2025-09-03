from django.db import models

class Holiday(models.Model):
    HOLIDAY_TYPES = [
        ('public', 'วันหยุดราชการ'),
        ('company', 'วันหยุดบริษัท'),
        ('religious', 'วันหยุดทางศาสนา'),
        ('other', 'อื่น ๆ'),
    ]

    name = models.CharField(max_length=100)
    date = models.DateField(unique=True)
    holiday_type = models.CharField(
        max_length=20,
        choices=HOLIDAY_TYPES,
        default='public'
    )

    def __str__(self):
        return f"{self.name} - {self.date} ({self.get_holiday_type_display()})"
