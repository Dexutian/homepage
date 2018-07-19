import requests
import os, logging
from django.conf import settings

# 生成logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler(os.path.join(settings.MEDIA_ROOT, 'log', 'download_pricedaily_csv.log'))
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
            self.msg = '主页网址链接失败！'
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
            self.msg = '下载网址链接失败！'

    def run(self):
        try:
            if self.link_check():
                self.download(self.stockexchangeno, self.start_date, self.end_date)
                self.msg = '股票：' + self.code + '，' + self.start_date + '-' + self.end_date + '，历史数据文件下载成功！'
        except Exception as e:
            print(e)
        finally:
            logger.info(self.msg)