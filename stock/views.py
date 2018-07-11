from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json, glob, os
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from lib.extend import get_stock_menu
from lib.manage_stock_name import get_excel_data_dict, update_name_use_dict
from stock.models import Menu,Name

# Create your views here.
def index(request):
    '''
    StocAns首页
    :param request:
    无
    :return:
    无
    '''
    return render(request, 'stock/stock_index.html')

def get_menu_data(request):
    '''
    获取StockAns应用首页目录数据
    :param request:
    无
    :return:
    data_json:目录列表数据json序列化
    '''
    menu_root = Menu.objects.filter(parent_menu=None).order_by("id")
    data_json = []
    for menu in menu_root:
        data_json.append(get_stock_menu(menu.slug))
    return HttpResponse(json.dumps(data_json), content_type='application/json')

def name(request):
	'''
	股票名称首页
	:param request:
	:return:
	'''
	files = []
	for file in glob.glob(os.path.join(settings.MEDIA_ROOT, 'stockname', '*')):
		files.append(file)
	names = Name.objects.all()
	paginator = Paginator(names, 20)
	page = request.GET.get('page')
	try:
		name_list = paginator.page(page)
	except PageNotAnInteger:
		name_list = paginator.page(1)
	except EmptyPage:
		name_list = paginator.page(paginator.num_pages)
	return render(request, 'stock/stock_name.html',{'files':files, 'stocknames':name_list})

def upload_name_file(request):
	'''
	上传股票名称xls文件
	:param request:
	:return:
	'''
	# 请求方法为POST时，进行处理
	if request.method == "POST":
		# 获取上传的文件，如果没有文件，则默认为None
		myFile =request.FILES.get("myfile", None)
		if not myFile:
			return HttpResponse("no files for upload!")
		# 打开特定的文件进行二进制的写操作
		destination = open(os.path.join(settings.MEDIA_ROOT, 'stockname', myFile.name),'wb+')
		# 分块写入文件
		for chunk in myFile.chunks():
			destination.write(chunk)
		destination.close()
		return HttpResponseRedirect("/stock/name/")

@csrf_exempt
def update_name(request):
	'''
	更新股票名称
	:param request:
	:return:
	'''
	if request.method=="POST":
		file_excel=request.POST.get("k1")
	data=get_excel_data_dict(file_excel=file_excel, col_name_index=0, by_index=0)
	insert_num = update_name_use_dict(data)
	return HttpResponse(str(insert_num))