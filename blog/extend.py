from blog.models import Category

def get_category(category_slug):
    node = {}
    category_object = Category.objects.get(slug=category_slug)
    node = {"id": category_object.slug, "text": category_object.name}
    children_category_set = category_object.category_set.all()
    if children_category_set:
        children_category_dict_list = []
        for children_category in children_category_set:
            print(children_category.slug)
            children_category_dict_list.append(get_category(children_category.slug))
        node.update({"children": children_category_dict_list})
    return node