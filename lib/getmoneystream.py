from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os, logging
from django.conf import settings

from stock.models import Name, Bigexchange

# 生成logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(os.path.join(settings.MEDIA_ROOT, 'log', 'getmoneystream.log'))
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class download_moneystream(object):
    '''
    下载大单交易数据
    '''
    def __init__(self, code):
        self.code = code
        self.download_url = "http://data.eastmoney.com/zjlx/" + self.code + ".html"
        self.data = []
        self.datastatus = False
        self.msg = ''

    def get_data(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"
        )
        driver = webdriver.PhantomJS(desired_capabilities=dcap, executable_path=os.path.join(settings.MEDIA_ROOT, 'phantomjs.exe'))
        try:
            driver.get(self.download_url)
        except TimeoutException as time_e:
            self.msg = '股票：' + self.code + '，' + self.download_url + '，链接连接超时：' + str(time_e)
        try:
            table_tr_list = driver.find_element_by_xpath("//table[@id='dt_1']/tbody").find_elements_by_tag_name("tr")
            table_list = []     #存放数据
            for tr in table_tr_list:
                table_td_list = tr.find_elements_by_tag_name("td")
                row_list = []
                for td in table_td_list:
                    row_list.append(td.text)
                table_list.append(row_list)
            return table_list
        except NoSuchElementException as elment_e:
            self.msg = '股票：' + self.code + '，' + self.download_url + '，没有相应的表格元素：' + str(elment_e)

    def clean_data(self, origin_data):
        if isinstance(origin_data, list):
            new_data = []
            for row in origin_data:
                row_unit = []
                for data_unit in row:
                    if data_unit.endswith('万'):
                        row_unit.append(data_unit.rstrip('万'))
                    elif data_unit.endswith('亿'):
                        row_unit.append(str(float(data_unit.rstrip('亿'))*10000))
                    elif data_unit.endswith('%'):
                        row_unit.append(data_unit.rstrip('%'))
                    elif data_unit == '-':
                        row_unit.append(str(0))
                    else:
                        row_unit.append(data_unit)
                new_data.append(row_unit)
            self.datastatus = True
            return new_data
        else:
            self.msg = '股票：' + self.code + '，' + self.download_url + '，读取数据格式有误！'

    def update_sql(self):
        data_list = []
        if self.datastatus:
            for data in self.data:
                stockobj = Name.objects.get(stockcode = self.code)
                exist_data = stockobj.bigexchange_set.filter(date = data[0])
                if not exist_data:
                    data_unit = Bigexchange(
                        date = data[0],
                        zhulj = data[3],
                        zhuljper = data[4],
                        chaodd = data[5],
                        chaoddper = data[6],
                        dd = data[7],
                        ddper = data[8],
                        zd = data[9],
                        zdper = data[10],
                        xd = data[11],
                        xdper = data[12],
                        stockname = stockobj
                    )
                    data_list.append(data_unit)
            Bigexchange.objects.bulk_create(data_list)
        else:
            self.msg = '股票：' + self.code + '，' + self.download_url + '，存入数据库数据没准备好！'
        insert_num = len(data_list)
        return insert_num


    def run(self):
        try:
            origin_data = self.get_data()
            self.data = self.clean_data(origin_data = origin_data)
            insert_num = self.update_sql()
            self.msg = '股票：' + self.code + '，' + '大单资金流数据下载' + str(insert_num) + '条成功！'
        except Exception as e:
            self.msg = '股票：' + self.code + '，' + self.download_url + '，资金流数据下载失败！' + str(e)
        finally:
            logger.info(self.msg)