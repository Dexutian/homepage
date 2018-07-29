import xlrd
from stock.models import Name


def get_excel_data_dict(file_excel, col_name_index=0, by_index=0):
    '''
    字典形式获取excel表数据
    :param file_excel:
    :param col_name_index:
    :param by_index:
    :return:row_dict
    '''
    row_dict = {}
    if file_excel:
        data = xlrd.open_workbook(file_excel)
        table = data.sheet_by_index(by_index)
        n_rows = table.nrows    #行数
        col_names = table.row_values(col_name_index)    #表头行
        for row_num in range(1, n_rows):
            row = table.row_values(row_num)
            row_dict[row_num] = row
    return row_dict

def update_name_use_dict(data):
    '''
    用dict形式数据更新股票名称
    :return:
    insert_num:插入记录条数
    '''
    name_list = []
    for key, value in data.items():
        name = value
        if len(name) > 8:
            exist_name = Name.objects.filter(companycode=name[0])
        else:
            exist_name = Name.objects.filter(companycode=str(name[0])[0:6])
        if not exist_name:
            if len(name) > 8:
                #深交所股票
                name_unit = Name(
                    companycode=name[0],
                    companyabb=name[1],
                    stockexchangeno='SZ',
                    stockstyle='A',
                    stockcode=name[5],
                    stockabb=name[6],
                    listingdate=name[7],
                    generalcapital=float(name[8].replace(',','')),
                    circulatingcapital=float(name[9].replace(',','')),
                    bysector=name[18],
                )
            else:
                #上交所股票
                if name[4] == '-':
                    name[4] = None
                name_unit = Name(
                    companycode=str(name[0])[0:6],
                    companyabb=name[1],
                    stockexchangeno='SS',
                    stockstyle='A',
                    stockcode=str(name[2])[0:6],
                    stockabb=name[3],
                    listingdate=name[4],
                    generalcapital=float(name[5]),
                    circulatingcapital=float(name[6]),
                    bysector='',
                )
            name_list.append(name_unit)
    Name.objects.bulk_create(name_list)
    insert_num=len(name_list)
    return insert_num