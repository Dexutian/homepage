from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
import json, glob, os, logging
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Max, Min, Count
import time
from datetime import datetime

from lib.extend import get_stock_menu
from lib.manage_stock_name import get_excel_data_dict, update_name_use_dict
from lib.pricedaily_csv import download_pricedaily_file, update_pricedaily_file
from lib.getmoneystream import download_moneystream

from stock.models import Menu,Name

# 生成logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(os.path.join(settings.MEDIA_ROOT, 'log', 'stock.log'))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#进度条数值
per_downloadcsv_progress = 0
per_update_price_progress = 0
per_deletecsv_progress = 0
per_update_dadang_exchange = 0

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

def pricedaily_data(request):
	'''
	每日股票价格数据文件
	:param request:
	:return:
	'''
	stock = Name.objects.all().annotate(max_date=Max("pricedaily__date"), min_date=Min("pricedaily__date"))
	paginator = Paginator(stock, 20)
	page = request.GET.get('page')
	try:
		stock_list = paginator.page(page)
	except PageNotAnInteger:
		stock_list = paginator.page(1)
	except EmptyPage:
		stock_list = paginator.page(paginator.num_pages)
	return render(request, 'stock/stock_pricedaily_data.html',{'stocks':stock_list})

def pricedaily_data_by_code(request, stockcode):
	'''
	股票每日价格数据页，根据股票代码查询数据显示
	:param request:
	:return:
	'''
	stock = Name.objects.filter(stockcode__startswith=stockcode)
	paginator = Paginator(stock, 20)
	page = request.GET.get('page')
	try:
		stock_list = paginator.page(page)
	except PageNotAnInteger:
		stock_list = paginator.page(1)
	except EmptyPage:
		stock_list = paginator.page(paginator.num_pages)
	return render(request, 'stock/stock_pricedaily_data.html',{'stocks':stock_list})

@csrf_exempt
def progress(request):
	type = request.POST.get('type')
	if type == "download_pricedaily_data":
		return HttpResponse(str(per_downloadcsv_progress))
	if type == "update_pricedaily_data":
		return HttpResponse(str(per_update_price_progress))
	if type == "delete_csv_file":
		return HttpResponse(str(per_deletecsv_progress))
	if type == "update_dadang_exchange":
		return HttpResponse(str(per_update_dadang_exchange))
	return HttpResponse(str(0))

@csrf_exempt
def download_pricedaily_csv(request):
	'''
	下载每日股票价格数据文件
	:param request:
	:return:
	'''
	# 请求方法为POST时，进行处理
	if request.method == "POST":
		# 1.获取前端传送的公共信息，初始化进度
		dm = request.POST.get('dm')
		start_date = ''.join(request.POST.get('start_date').split('-'))
		end_date = ''.join(request.POST.get('end_date').split('-'))
		download_path = os.path.join(settings.MEDIA_ROOT, 'pricedaily_csv')
		global per_downloadcsv_progress
		per_downloadcsv_progress = 0
		i = 0

		# 2.获取股票代码列表
		code_list = []
		if dm == 'p':
			code_list = Name.objects.values_list('stockcode', flat=True)
		if dm == 's':
			companycode = request.POST.get('stockcode')
			code_list = json.loads(companycode)
		nlen = len(code_list)

		# # 4.下载股票数据文件,更新数据库记录
		for temp_code in code_list:
			stockexchangeno = Name.objects.get(stockcode=temp_code).stockexchangeno
			download = download_pricedaily_file(temp_code, stockexchangeno, start_date, end_date, download_path)
			download.run()
			Name.objects.filter(stockcode=temp_code).update(
				filename=temp_code+'.csv',
				startdate=request.POST.get('start_date'),
				enddate=request.POST.get('end_date'),
				fupdatetime=datetime.now().strftime("%Y-%m-%d"),
			)

			i += 1
			per_downloadcsv_progress = int((i / nlen) * 100)
			msg = '股票：' + temp_code + '，' + start_date + '-' + end_date + '，历史数据文件记录更新成功！'
			logger.info(msg)

			time.sleep(0.05)

	return HttpResponse(None)

@csrf_exempt
def updatecsv2database(request):
	'''
	更新每日股票价格数据文件到数据库
	:param request:
	:return:
	'''
	# 请求方法为POST时，进行处理
	if request.method == "POST":
		# 1.初始化公共信息，初始化进度
		dm = request.POST.get('dm')
		is_colname = True
		col_index = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
		global per_update_price_progress
		per_update_price_progress = 0
		i = 0
		nlen = 0

		# 2.获取股票文件列表
		file_list = []
		if dm == 'p':
			stockname_list = Name.objects.all()
			nlen = Name.objects.all().count()
			for stock in stockname_list:
				file_name = os.path.join(settings.MEDIA_ROOT, 'pricedaily_csv', stock.filename)
				file_list.append(file_name)
		if dm == 's':
			name_list_0 = request.POST.get('stockname')
			name_list = json.loads(name_list_0)
			nlen = len(name_list)
			for name in name_list:
				stocks = Name.objects.get(filename=name)
				file_name = os.path.join(settings.MEDIA_ROOT, 'pricedaily_csv', stocks.filename)
				file_list.append(file_name)

		# 4.用数据文件更新数据库
		for file in file_list:
			de = update_pricedaily_file(file, col_index, is_colname=is_colname)
			de.run()

			i += 1
			per_update_price_progress = int((i / nlen) * 100)
			msg = '文件：' + file + '，' + '数据导入成功！'
			logger.info(msg)

			time.sleep(0.05)

	return HttpResponse(None)

@csrf_exempt
def delete_pricedaily_csv(request):
	'''
	删除每日股票价格数据文件
	:param request:
	:return:
	'''
	if request.method == 'POST':
		# 1.获取前端传递的文件列表
		dm = request.POST.get("dm")
		global per_deletecsv_progress
		per_deletecsv_progress = 0
		i = 0
		nlen = 0

		# 2.获取股票文件列表
		name_list = []
		if dm == 'p':
			name_list_origin = Name.objects.values_list('filename', flat=True)
			name_list = [name for name in name_list_origin if name not in ['', ' ', None]]
		if dm == 's':
			name_list_0 = request.POST.get('stockname')
			name_list = json.loads(name_list_0)
		nlen = len(name_list)


		# 3.删除文件，同时记录删除文件记录数据
		for name in name_list:
			file_name = os.path.join(settings.MEDIA_ROOT, 'pricedaily_csv', name)
			if os.path.isfile(file_name):
				try:
					os.remove(file_name)
					Name.objects.filter(filename=name).update(
						filename=None,
						startdate=None,
						enddate=None,
						fupdatetime=datetime.now().strftime("%Y-%m-%d"),
					)
					msg = '文件：' + name + '，' + '删除成功！'
				except Exception  as e:
					msg = '文件：' + name + '，' + '删除错误：' + e

				i += 1
				per_deletecsv_progress = int((i / nlen) * 100)
				logger.info(msg)

				time.sleep(0.05)

	return HttpResponse(None)

def dadang_exchange(request):
	'''
	大单交易数据首页
	:param request:
	:return:
	'''
	stock = Name.objects.all().annotate(count=Count("bigexchange__id"),
											 max_date=Max("bigexchange__date"))
	paginator = Paginator(stock, 20)
	page = request.GET.get('page')
	try:
		stock_list = paginator.page(page)
	except PageNotAnInteger:
		stock_list = paginator.page(1)
	except EmptyPage:
		stock_list = paginator.page(paginator.num_pages)
	return render(request, 'stock/stock_dadang_data.html', {'stocks': stock_list})

@csrf_exempt
def update_dadang_exchange(request):
	'''
	更新大单交易数据
	:param request:
	:return:
	'''
	# 请求方法为POST时，进行处理
	if request.method == "POST":
		# 1.初始化公共信息，初始化进度
		dm = request.POST.get('dm')
		global per_update_dadang_exchange
		per_update_dadang_exchange = 0
		i = 0
		nlen = 0

		# 2.获取股票文件列表
		code_list = []
		if dm == 'p':
			code_list_origin = Name.objects.values_list('stockcode', flat=True)
			code_list = [code for code in code_list_origin if code not in ['', ' ', None]]
		if dm == 's':
			code_list_0 = request.POST.get('code_list')
			code_list = json.loads(code_list_0)
		nlen = len(code_list)

		#4.用数据文件更新数据库
		for code in code_list:
			de = download_moneystream(code)
			de.run()

			i += 1
			per_update_dadang_exchange = int((i / nlen) * 100)
			msg = '股票：' + code + '，' + '大单资金数据导入成功！'
			logger.info(msg)

			time.sleep(0.05)

	return HttpResponse(None)

def dadang_exchange_by_code(request, stockcode):
	'''
	股票大单交易数据，根据股票代码查询数据显示
	:param request:
	:return:
	'''
	stock = Name.objects.filter(stockcode__startswith=stockcode).annotate(count=Count("bigexchange__id"),
										max_date=Max("bigexchange__date"))
	paginator = Paginator(stock, 20)
	page = request.GET.get('page')
	try:
		stock_list = paginator.page(page)
	except PageNotAnInteger:
		stock_list = paginator.page(1)
	except EmptyPage:
		stock_list = paginator.page(paginator.num_pages)
	return render(request, 'stock/stock_dadang_data.html', {'stocks': stock_list})