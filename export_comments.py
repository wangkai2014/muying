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
workbook = xlsxwriter.Workbook('comments_sample_suning.xlsx')
worksheet = workbook.add_worksheet()

def init_sheet():
    worksheet.write('A1', '商品编号')
    worksheet.write('B1', '商品名称')
    worksheet.write('C1', '评分')
    worksheet.write('D1', '用户名')
    worksheet.write('E1', '用户图像')
    worksheet.write('F1', '评论内容')
    worksheet.write('G1', '评论时间')
    worksheet.write('H1', '购买时间')



def get_source():
    sql = "select * ,goods_comments.goods_id as goods_id from goods_list join goods_comments on goods_list.id=goods_comments.goods_id where category ='2段奶粉'"
    return db.query(sql)

def write_xls():
    i=2
    for row in get_source():
        worksheet.write('A' + str(i), row['id'])
        worksheet.write('B' + str(i), row['goods_name'].strip('"'))
        worksheet.write('C' + str(i), row['com_score'])
        worksheet.write('D' + str(i), row['com_u_name'])
        worksheet.write('E' + str(i), row['com_u_photo'])
        worksheet.write('F' + str(i), row['com_contents'])
        worksheet.write('G' + str(i), datetime.datetime.fromtimestamp(int(row['com_time'])).strftime('%Y-%m-%d %H:%M:%S'))
        worksheet.write('H' + str(i), datetime.datetime.fromtimestamp(int(row['com_buy_time'])).strftime('%Y-%m-%d %H:%M:%S'))
        i+=1
    workbook.close()

init_sheet()
write_xls()