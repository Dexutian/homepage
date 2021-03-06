from blog.models import Category
from info.models import Menu as Info_Menu
from stock.models import Menu as Stock_Menu

def get_category(category_slug):
    node = {}
    category_object = Category.objects.get(slug=category_slug)
    node = {"id": category_object.slug, "text": category_object.name}
    children_category_set = category_object.category_set.all()
    if children_category_set:
        children_category_dict_list = []
        for children_category in children_category_set:
            children_category_dict_list.append(get_category(children_category.slug))
        node.update({"children": children_category_dict_list})
    return node

def get_info_menu(menu_slug):
    node = {}
    menu_object = Info_Menu.objects.get(slug=menu_slug)
    node = {"id": menu_object.slug, "text": menu_object.name, "href":menu_object.href}
    children_menu_set = menu_object.menu_set.all().order_by("slug")
    if children_menu_set:
        children_menu_dict_list = []
        for children_menu in children_menu_set:
            print(children_menu.slug)
            children_menu_dict_list.append(get_info_menu(children_menu.slug))
        node.update({"children": children_menu_dict_list})
    return node

def get_stock_menu(menu_slug):
    node = {}
    menu_object = Stock_Menu.objects.get(slug=menu_slug)
    node = {"id": menu_object.slug, "text": menu_object.name, "href":menu_object.href}
    children_menu_set = menu_object.menu_set.all().order_by("slug")
    if children_menu_set:
        children_menu_dict_list = []
        for children_menu in children_menu_set:
            print(children_menu.slug)
            children_menu_dict_list.append(get_stock_menu(children_menu.slug))
        node.update({"children": children_menu_dict_list})
    return node