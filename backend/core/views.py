from django.shortcuts import render
from django.conf import settings
import os

# Create your views here.


def index(request):

    output = dict()
    for setting in dir(settings):
        if setting.isupper():
            value = getattr(settings, setting)
            output[setting] = value

    data = {
        "test": "test",
        "settings": output
    }

    return render(request, 'index.html', context=data)
