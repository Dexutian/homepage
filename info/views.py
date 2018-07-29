from django.shortcuts import render
from django.http import HttpResponse
import json

from lib.extend import get_info_menu
from info.models import Menu

# Create your views here.
def get_menu_data(request):
    menu_root = Menu.objects.filter(parent_menu=None).order_by("slug")
    data_json = []
    for menu in menu_root:
        data_json.append(get_info_menu(menu.slug))
    return HttpResponse(json.dumps(data_json), content_type='application/json')