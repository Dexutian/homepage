from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse

from blog.models import Blog

# Create your views here.
def blog_list(request):
    return render_to_response('blog/list.html', {'blogs': Blog.objects.all()})

def blog_detail(request, slug):
    # return HttpResponse(slug)
    return render_to_response('blog/detail.html', {'blog': get_object_or_404(Blog, slug=slug)})