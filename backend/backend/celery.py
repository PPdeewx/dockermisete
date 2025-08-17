import os
from celery import Celery

# ตั้งค่า environment variables สำหรับ Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# สร้าง instance ของ Celery
app = Celery('backend')

# โหลดการตั้งค่า Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# อัตโนมัติค้นหา task ในแอปที่ติดตั้ง
app.autodiscover_tasks()