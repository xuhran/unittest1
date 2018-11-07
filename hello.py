#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018-10-26 20:09
# @Author  : Xuhr
# @E-mail  : xuhr12@chinaunicom.cn
# @File    : hello.py
# @Software: PyCharm
import pymysql
from csvtotable import convert
from flask import Flask, request, render_template
from baidu import baidusearch
import csv,sys
app = Flask(__name__)

if __name__ == '__main__':
    app.run()

@app.route('/', methods=['GET','POST']) #login in
def create_table():
    name = 'baidu_search'
    user_name = request.form['username']
    passwd = request.form['password']
    try:
        conn = pymysql.connect('localhost', user_name, passwd, 'testdb')
        cur = conn.cursor()
        cur.execute("drop table if exists %s" % name)
        cur.execute("create table %s("
                    "id int not null primary key,"
                    "content varchar(255) not null,"
                    "time_label varchar(255)"
                    ")default charset=gbk" % name)
        conn.commit()
        conn.close()
        return render_template('succ.html')
    except:
        return render_template('error.html')

@app.route('/result',methods=['GET','POST']) #search function
def result():
    kw = request.form['keywords']
    all = baidusearch(kw)
    return render_template('end.html', para=all)
