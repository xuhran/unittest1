#!/usr/bin/env python
# coding: utf-8
# @Time    : 2018-10-17 14:57
# @Author  : Xuhr
# @E-mail  : xuhr12@chinaunicom.cn
# @File    : test1.py
# @Software: PyCharm Community Edition

import urllib3
from bs4 import BeautifulSoup as bs
import lxml
from DBUtils.PooledDB import PooledDB
import datetime
import time
import pymysql
import configparser
import threading
import xlwt
import csv
global count
count = 0
def baidusearch(wd):
    time1 = str(int(time.time()))
    pm = urllib3.PoolManager()
    def DBpool():#dbpool
        cf = configparser.ConfigParser()
        cf.read("mysql.conf")
        dbport = cf.get('db', 'db_port')
        host = cf.get('db', 'db_host')
        username = cf.get('db', 'db_user')
        passwd = cf.get('db', 'db_pass')
        dbname = cf.get('db', 'db_name')
        pool = PooledDB(pymysql, 10, host=host, user=username, passwd=passwd, db=dbname, port=int(dbport))
        return pool
    dbpool = DBpool()

    def create_table():  # create table
        try:
            conn = dbpool.connection(shareable=False)
            cur = conn.cursor()
            cur.execute("drop table if exists {}".format(wd+time1))
            cur.execute("create table {}("
                        "id int not null primary key AUTO_INCREMENT,"
                        "content varchar(255) not null,"
                        "time_label varchar(255)"
                        ")default charset=gbk".format(wd+time1))
            conn.commit()
            print('create table {} succ!'.format(wd+time1))
        except Exception as e:
            print(e)
            print("create table {} error.".format(wd+time1))
        finally:
            cur.close()
            conn.close()
    create_table()

    def getpageinfo():
        html = pm.request('get','http://www.baidu.com/s?wd='+wd)
        htmldecode = html.data.decode('utf-8')
        soup = bs(htmldecode,"lxml")
        for a in soup.h3.children:
            print(a)

    fileds = ['id', 'title', 'time']
    try:# excel
        filename = wd+time1+'.xls'
        wbook = xlwt.Workbook()
        sheet1 = wbook.add_sheet(filename, cell_overwrite_ok=True)
        sheet1.write(0,0,elements_num.text)
        for f in range(0, len(fileds)):
            sheet1.write(1, f, fileds[f])
    except Exception as e:
        print(e)
    # csv
    try:
        file = wd +time1+'.csv'
        f = open(file, 'w', newline='')
        csv_write = csv.writer(f)
        csv_write.writerow(elements_num.text)
        csv_write.writerow(fileds)
        f.close()
    except Exception as e:
        print(e)

    def get_page():  # get current page infomation
        try:
            elements1 = driver.find_elements_by_xpath("//*/h3")
            for ele in elements1:
                t1 = threading.Thread(target=insert, args=(wd, ele.text))  # multi-threading
                t1.start()
                t1.join()
        except Exception as e:
            print('insert error')
            print(e)
            exit()
        try:
            next_page = driver.find_element_by_link_text('下一页>')
            next_page.click()
            next_page1 = driver.find_element_by_link_text('下一页>')
            while (next_page == next_page1):
                next_page1 = WebDriverWait(driver, 10, 0.1).until(EC.presence_of_element_located((By.LINK_TEXT, '下一页>')))
            get_page()
        except Exception as e:
            print(e)
            print('The End')

    def insert(table_name, title):  # insert into database
        global count
        count = count + 1
        time_now = datetime.datetime.now()
        result = [count, title, time_now]
        try:
            conn = dbpool.connection()
            cur = conn.cursor()
            sql = "insert into {} values ({},'{}','{}')".format(wd+time1, 0, title, time_now)
            print(sql)
            cur.execute(sql)
            conn.commit()
            print('No.%d insert succ' % count)
        except Exception as e:
            conn.rollback()
            count = count - 1
            print(e)
            print("insert error")
        finally:
            cur.close()
            conn.close()
        try:
            for col in range(0, len(result)):
                print(result[col])
                sheet1.write(count+1, col, result[col])
            print('save to excel succ.')
        except Exception as e:
            print(e)
            print('save to excel error...')
        finally:
            wbook.save(filename)
        try:
            file = wd+time1+'.csv'
            f = open(file, 'a', newline='')
            csv_write = csv.writer(f)
            csv_write.writerow(result)
            print('save to csv succ.')
            f.close()
        except Exception as e:
            print(e)
            print('save to csv error...')
    get_page()
    pool.close()
    return res
if __name__ == '__main__':
    baidusearch('hello')






#不可控变量写入配置文件
#开闭原则，开：功能的叠加；闭：已有功能的修改要关闭。
#SQL注入问题，字符串拼接 java:preparestatement