from django.shortcuts import render
from django.http import HttpResponse
import json, os, logging

from lib.extend import get_menu
from info.models import Menu

# Create your views here.
def get_menu_data(request):
    path = os.getcwd()
    filename = os.path.join(path, 'log.txt')
    logging.basicConfig(filename=filename, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    menu_root = Menu.objects.filter(parent_menu=None).order_by("id")
    data_json = []
    for menu in menu_root:
        data_json.append(get_menu(menu.slug))
    logger.info(json.dumps(data_json))
    return HttpResponse(json.dumps(data_json), content_type='application/json')
