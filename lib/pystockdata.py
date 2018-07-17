import requests
from datetime import datetime

class Download_HistoryStock(object):
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
            self.msg = '主页网址链接失败'
            return False

    def download(self, stockexchangeno, start_date, end_date):
        # self.msg = "运行到此处"
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
            self.msg = '下载网址链接失败'

    def run(self):
        output_file = 'F:/pycode/env_python3.6.5/homepage/media/log/downloadcsv.txt'
        filewriter = open(output_file, 'a+', newline=None)
        try:
            if self.link_check():
                self.download(self.stockexchangeno, self.start_date, self.end_date)
                self.msg = '股票：' + self.code + '，' + self.start_date + '-' + self.end_date + '，历史数据文件下载成功'
        except Exception as e:
            print(e)
        finally:
            filewriter.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '  ' + self.msg + "\n")
            filewriter.close()
