from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, os
from blog.extend import get_category

from blog.models import Blog, Category

# Create your views here.
def index(request):
    return render_to_response('blog/blog_index.html')

def category(request):
    return render_to_response('blog/blog_category.html', {'category_root':Category.objects.get(parent_category = None)})

@csrf_exempt
def get_category_data(request):
    category_root = Category.objects.get(parent_category=None)
    data_json = get_category(category_root.slug)
    return HttpResponse(json.dumps(data_json), content_type='application/json')

def blog_list(request):
    return render_to_response('blog/list.html', {'blogs': Blog.objects.all()})

def blog_detail(request, slug):
    return render_to_response('blog/detail.html', {'blog': get_object_or_404(Blog, slug=slug)})