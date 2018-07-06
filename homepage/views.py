from django.shortcuts import render
from django.conf import settings
from datetime import time, datetime
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, 'index/index.html')
