# -*- coding: utf-8 -*-
from Db import Db
import xlsxwriter
import datetime
import re
import sys
import json
import time
reload(sys)
import os
import ast

sys.setdefaultencoding('utf-8')
db = Db()
workbook = xlsxwriter.Workbook('xihu.xlsx')
worksheet = workbook.add_worksheet()
columns = ['O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH',
           'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AV', 'AW', 'AX', 'AY', 'AZ','BA','BB','BC','BD','BE','BF','BG','BH','BI','BJ','BK','BL','BM','BN','BO','BP','BQ','BR','BS','BT','BU','BV','BW','BX','BY','BZ']
keys = []
key = ''
k_c={}

def init_sheet():
    worksheet.write('A1', '商品编号')
    worksheet.write('B1', '大分类')
    worksheet.write('C1', '小分类')
    worksheet.write('D1', '品牌名')
    worksheet.write('E1', '商品名称')
    worksheet.write('F1', '促销类型1')
    worksheet.write('G1', '促销类型1描述')
    worksheet.write('H1', '促销类型2')
    worksheet.write('I1', '促销类型2描述')
    worksheet.write('G1', '促销类型3')
    worksheet.write('K1', '促销类型3描述')
    worksheet.write('L1', '商品网址')
    # worksheet.write('M1', '商品参数')
    worksheet.write('M1', '选择信息')
    worksheet.write('N1', '采集时间')
    global keys
    global k_c
    keys = json.loads(get_source_init()[0]['params']).keys()
    i=0
    for k in keys:
        worksheet.write(columns[i]+'1',k)
        k_c[k]=columns[i]
        i+=1

    del columns[:i]



def patch_sheet(k):
    global keys
    global k_c
    keys.append(k)
    worksheet.write(columns[0]+'1',k)
    k_c[k]=columns[0]
    del columns[0]



def get_source():
    sql = "select *  from goods_detail where group_name like '%洗护%'"
    return db.query(sql)
def get_source_init():
    sql = "select *  from goods_detail where group_name like '%洗护%' and params!=''"
    return db.query(sql)


def write_xls():
    i = 2
    global keys
    global k_c
    for row in get_source():

        try:
            ps = json.loads(row['params'])
        except:
            ps={}
        for k in ps.keys():
            if k not in keys:
                patch_sheet(k)
        goodsid = str(re.search(r"(\d{9})(-.*)?.html", row['goods_url']).group(1))
        selection = ''
        try:
            selection += '尺码:' + (','.join(json.loads(row['selection'])['versions'])) + '  '
        except:
            selection += ''
        try:
            selection += '颜色:' + (','.join(json.loads(row['selection'])['colors'])) + '  '
        except:
            selection += ''

        discount = row['goods_discount'].split('  ')
        # discount=json.dumps(discount,ensure_ascii=False, encoding='utf8')
        d = {}
        for item in discount:
            if item.find('返券') != -1:
                d['fanquan'] = item.split(':')[1]
            if item.find('折扣价') != -1:
                d['coupon'] = item.split(':')[1]
            if item.find('促销信息') != -1:
                d['prom'] = item.split(':')[1]
        # print json.dumps(d,ensure_ascii=False, encoding='utf8')

        worksheet.write('A' + str(i), goodsid)
        worksheet.write('B' + str(i), row['group_name'])
        worksheet.write('C' + str(i), row['category'])
        worksheet.write('D' + str(i), row['brand'])
        worksheet.write('E' + str(i), row['goods_name'])

        if 'fanquan' in d.keys():
            worksheet.write('F' + str(i), '返券')
            worksheet.write('G' + str(i), str(d['fanquan']))
        else:
            worksheet.write('F' + str(i), '')
            worksheet.write('G' + str(i), '')

        if 'coupon' in d.keys():
            worksheet.write('H' + str(i), '团购')
            worksheet.write('I' + str(i), '团购价:' + d['coupon'])
        else:
            worksheet.write('H' + str(i), '')
            worksheet.write('I' + str(i), '')

        if 'prom' in d.keys():
            worksheet.write('J' + str(i), '订单直降')
            worksheet.write('K' + str(i), d['prom'])
        else:
            worksheet.write('J' + str(i), '')
            worksheet.write('K' + str(i), '')

        worksheet.write('L' + str(i), row['goods_url'])
        # worksheet.write('M'+str(i), row['params'].strip('{').strip('}'))
        worksheet.write('M' + str(i), selection)
        worksheet.write('N' + str(i),
                        datetime.datetime.fromtimestamp(int(row['add_time'])).strftime('%Y-%m-%d %H:%M:%S'))
        for k,v in ps.items():
            print k_c[k]
            worksheet.write(k_c[k] + str(i), v)

        i += 1

    workbook.close()


init_sheet()
write_xls()