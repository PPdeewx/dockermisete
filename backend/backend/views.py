from django.http import HttpResponse

def home(request):
    return HttpResponse("ยินดีต้อนรับสู่ MIS ETE API")