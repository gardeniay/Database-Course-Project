from flask import Flask, render_template, request, redirect, url_for, session
import pymysql
import datetime
import os
from functools import wraps

import pymysql.cursors

#创建应用
app = Flask(__name__)
app.secret_key = 'simple_zhihu_secret_key'

#管理员列表
manister = [1, 3 ,7]

db_host = os.getenv('DB_HOST', '120.0.0.1')
db_port = int(os.getenv('DB_PORT', '3306'))
db_name = os.getenv('DB_NAME', 'zhihu')
db_user = os.getenv('DB_USER', 'root')
db_password = os.getenv('DB_PASSWORD', '928520zjf.')

#创建数据库链接
def get_db():
    # 返回一个到MySQL的连接，使用字典游标便于数据处理
    conn = pymysql.connect(
        host = db_host,
        port = db_host,
        user = db_user,
        password = db_password,
        database = db_name,
        charset = 'utf8mb4',
        cursortclass=pymysql.cursors.DictCursor
    )
    return conn

#执行查询操作
def query_db(query, args=(), one=False):
    # 执行SQL查询并返回结果，one=True时仅返回第一条记录】
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(query, args)
    rv = cursor.fetchall() 
    conn.commit()
    cursor.close()
    conn.close()
    return (rv[0] if rv else None) if one else rv

#执行插入操作
def insert_db(table, data):
    #向指定表插入数据，data是包含字段名和值的字典
    conn = get_db()
    cursor = conn.cursor()

    columns = 


