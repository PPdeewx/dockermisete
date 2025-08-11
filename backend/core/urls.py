from django.urls import path
from . import views

urlpatterns = [
    # This maps the root URL to index.html
    path('', views.index, name='index'),
]
