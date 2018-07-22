import requests
import os, logging, csv
from django.conf import settings
from stock.models import Name, Pricedaily

# 生成logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(os.path.join(settings.MEDIA_ROOT, 'log', 'pricedaily_csv.log'))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class download_pricedaily_file(object):
    '''
    下载每日价格数据文件
    '''
    def __init__(self, code, stockexchangeno, start_date, end_date, download_path):
        self.code = code
        self.stockexchangeno = stockexchangeno
        self.start_date = start_date
        self.end_date = end_date
        self.download_path = download_path
        self.start_url = "http://quotes.money.163.com/trade/lsjysj_" + self.code + ".html"
        self.msg = ''
        self.download_url = ''

    def link_check(self):
        response = requests.get(self.start_url)
        if response.status_code == 200:
            return True
        else:
            self.msg = '股票：' + self.code +'主页网址链接失败！'
            return False

    def download(self, stockexchangeno, start_date, end_date):
        if stockexchangeno == 'SZ':
            self.download_url = "http://quotes.money.163.com/service/chddata.html?code=1"+self.code+"&start="+start_date+"&end="+end_date+"&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER"
        else:
            self.download_url = "http://quotes.money.163.com/service/chddata.html?code=0"+self.code+"&start="+start_date+"&end="+end_date+"&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER"
        data = requests.get(self.download_url)
        if data:
            f = open( self.download_path + '/' + self.code + '.csv', 'wb')
            for chunk in data.iter_content(chunk_size=10000):
                if chunk:
                    f.write(chunk)
        else:
            self.msg = '股票：' + self.code +'下载网址链接失败！'

    def run(self):
        try:
            if self.link_check():
                self.download(self.stockexchangeno, self.start_date, self.end_date)
                self.msg = '股票：' + self.code + '，' + self.start_date + '-' + self.end_date + '，历史数据文件下载成功！'
        except Exception as e:
            self.msg = '股票：' + self.code + '，' + '下载异常：' + str(e)
        finally:
            logger.info(self.msg)

class update_pricedaily_file(object):
    def __init__(self, file_name, col_num, is_colname=True):
        self.file_name = file_name
        self.is_colname = is_colname
        self.col_num = col_num
        self.msg = ''

    def read_csv_data(self):
        try:
            with open(self.file_name, 'r', newline='') as csv_in_file:
                filereader = csv.reader(csv_in_file, delimiter=',')
                if self.is_colname:
                    header = next(filereader)   #跳过表头
                row_dict = []
                for row_list in filereader:
                    row_unit = []
                    if "None" not in row_list:
                        for col_index in self.col_num:
                            row_unit.append(row_list[col_index])
                        row_dict.append(row_unit)
                return row_dict
        except Exception as e:
            self.msg = '文件：' + self.file_name + '读取异常：' + str(e)

    def import_stock_data(self, row_dict):
        '''
        data = read_excel_data()
        股票数据
        :return:
        insert_num:插入记录条数
        '''
        data_list = []
        if row_dict:
            for value in row_dict:
                data = value
                stock_obj = Name.objects.get(stockcode=data[1].lstrip("'"))
                exist_data = stock_obj.pricedaily_set.filter(date=data[0])
                if not exist_data:
                    data_unit = Pricedaily(
                        date = data[0],
                        tclose = data[2],
                        high = data[3],
                        low = data[4],
                        topen = data[5],
                        lclose = data[6],
                        chg = data[7],
                        pchg = data[8],
                        voturnover = data[9],
                        vaturnover = data[10],
                        stockname = stock_obj,
                    )
                    data_list.append(data_unit)
            Pricedaily.objects.bulk_create(data_list)
        else:
            self.msg = '文件：' + self.file_name + '文件没有数据！'
        insert_num=len(data_list)
        return insert_num

    def run(self):
        try:
            row_dict = self.read_csv_data()
            if  '异常' not in self.msg:
                insert_num = self.import_stock_data(row_dict)
                self.msg = '文件：' + self.file_name + '成功更新'+str(insert_num)+'条数据！'
        except Exception as e:
            self.msg = '文件：' + self.file_name + '更新数据异常：' + str(e)
        finally:
            logger.info(self.msg)