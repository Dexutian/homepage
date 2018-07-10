from django import template
from blog.models import Category
register = template.Library()

@register.inclusion_tag("blog/blog_category_tree_part.html")
def category_tree(cate):
    return {'categories':cate.category_set.all()}