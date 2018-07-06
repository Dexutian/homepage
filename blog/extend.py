from blog.models import Category
def get_category(category_slug):
    category_object = Category.objects.get(slug=category_slug)
    children_category_set = category_object.category_set.all()
    children_node = {}
    if children_category_set:
        children_category_dict_list = []
        for children_category in children_category_set:
            children_category_dict = {"id":children_category.slug,"text":children_category.name}
            children_category_dict_list.append(children_category_dict)
            get_category(children_category.slug)
        children_node.update({"children": children_category_dict})