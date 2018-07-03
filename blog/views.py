from django.shortcuts import render
from django.shortcuts import render_to_response, get_object_or_404

from blog.models import Blog

# Create your views here.
def blog_list(request):
    return render_to_response('blog/list.html', {'blogs': Blog.objects.all()})