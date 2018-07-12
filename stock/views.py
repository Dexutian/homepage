from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json, glob, os, logging
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from lib.extend import get_stock_menu
from lib.manage_stock_name import get_excel_data_dict, update_name_use_dict
from stock.models import Menu,Name

# 生成logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(os.path.join(settings.MEDIA_ROOT, 'log', 'stock.log'))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

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

def name_file(request):
	'''
	股票名称数据文件
	:param request:
	:return:
	'''
	files = []
	for file in glob.glob(os.path.join(settings.MEDIA_ROOT, 'stockname', '*.xls*')):
		files.append(file)
	return render(request, 'stock/stock_name_file.html', {'files':files})

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
			logger.info("no files for upload!")
			return HttpResponse("no files for upload!")
		else:
			file_suffix = myFile.name.split(".")[-1]
			if file_suffix not in ["xls", "xlsx"]:
				logger.info("uploading file type is not supported!")
				return HttpResponse("uploading file type is not supported!")
			else:
				# 打开特定的文件进行二进制的写操作
				destination = open(os.path.join(settings.MEDIA_ROOT, 'stockname', myFile.name),'wb+')
				# 分块写入文件
				for chunk in myFile.chunks():
					destination.write(chunk)
				destination.close()
				logger.info(myFile.name + "---上传成功！")
				return HttpResponseRedirect("/stock/name_file/")

@csrf_exempt
def update_name(request):
	'''
	更新股票名称
	:param request:
	:return:
	'''
	if request.method=="POST":
		file_excel=request.POST.get("k1")
		action = request.POST.get("action")
	if action == "更新数据":
		data=get_excel_data_dict(file_excel=file_excel, col_name_index=0, by_index=0)
		insert_num = update_name_use_dict(data)
		msg = "成功更新" + str(insert_num) + "数据！"
		logger.info(msg)
	if action == "删除文件":
		try:
			os.remove(file_excel)
			logger.info(file_excel + '---删除成功')
			msg = "文件删除成功！"
		except Exception as e:
			logger.info(file_excel + '---删除错误，错误信息：' + e)
			msg = "文件删除错误！"
	return HttpResponse(msg)

def name_data(request):
	'''
	股票名称数据页
	:param request:
	:return:
	'''
	names = Name.objects.all()
	paginator = Paginator(names, 20)
	page = request.GET.get('page')
	try:
		name_list = paginator.page(page)
	except PageNotAnInteger:
		name_list = paginator.page(1)
	except EmptyPage:
		name_list = paginator.page(paginator.num_pages)
	return render(request, 'stock/stock_name_data.html',{ 'stocknames':name_list})

def name_data_by_code(request, stockcode):
	'''
	股票名称数据页，根据股票代码查询数据显示
	:param request:
	:return:
	'''
	names = Name.objects.filter(stockcode__startswith=stockcode)
	paginator = Paginator(names, 20)
	page = request.GET.get('page')
	try:
		name_list = paginator.page(page)
	except PageNotAnInteger:
		name_list = paginator.page(1)
	except EmptyPage:
		name_list = paginator.page(paginator.num_pages)
	return render(request, 'stock/stock_name_data.html',{ 'stocknames':name_list})