from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json, os
from blog.extend import get_category

from blog.models import Blog, Category

# Create your views here.
def category(request):
    return render_to_response('blog/blog_category.html', {'category_root':Category.objects.get(parent_category = None)})

@csrf_exempt
def get_category_data(request):
    output_file = 'json_log.txt'
    filewriter = open(output_file, 'a+', newline=None)

    # category_root = Category.objects.get(parent_category=None)
    # data = {"id":category_root.slug, "text":category_root.name, "children": get_category(category_root.slug)}
    filewriter.write("aaa" + "\n")
    filewriter.close()
    # return HttpResponse(json.dumps(data_json), content_type='application/json')
    return HttpResponse(None)

def blog_list(request):
    return render_to_response('blog/list.html', {'blogs': Blog.objects.all()})

def blog_detail(request, slug):
    # return HttpResponse(slug)
    return render_to_response('blog/detail.html', {'blog': get_object_or_404(Blog, slug=slug)})