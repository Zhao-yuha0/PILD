import os
from flask import Flask, blueprints, Blueprint, render_template, request, json, Response, session, redirect
from datetime import datetime, date, timedelta
import pymysql

testTask = Blueprint("testTask", __name__)


@testTask.route('/siteTest', methods=['GET', 'POST'])
def siteTest(self=None):
    if not session.get('account'):
        return redirect('/login')
    # 获得提交数据
    task_info = dict(request.form)

    testType = '站点测试'
    rules = '什么都不检测'
    url = task_info['siteInput']
    add_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    domain = task_info['domain']

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    sql = "insert into test (type, rules, url, add_time, domain) VALUES (%s,%s,%s,%s,%s)"
    val = (testType,rules,url,add_time,domain)
    cursor.execute(sql, val)
    db.commit()
    db.close()


    # 返回结果页面
    return render_template('result.html')


@testTask.route('/regTest', methods=['GET', 'POST'])
def regTest(self=None):
    if not session.get('account'):
        return redirect('/login')
    # 获得提交数据
    task_info = dict(request.form)

    testType = '规则测试'
    rules = task_info['ruleInput']
    url = task_info['siteInput']
    add_time = datetime.now().strftime('%Y-%m-%d %H:%M')
    domain = '仅本网页'

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    sql = "insert into test (type, rules, url, add_time, domain) VALUES (%s,%s,%s,%s,%s)"
    val = (testType,rules,url,add_time,domain)
    cursor.execute(sql, val)
    db.commit()
    db.close()


    # 返回结果页面
    return render_template('result.html')


@testTask.route('/showTestData', methods=['GET', 'POST'])
def showTestData():
    page = int(request.args["page"])
    limit = int(request.args["limit"])


    data = {
        "code": 200,
        "msg": "",
        "count": 0,
        "data": []

    }

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("select * from test_result ;")

    rules = cursor.fetchall()

    ruleList = []

    for item in rules:
        ruleDict = {'rule': item[0], 'content': item[1],'page': item[2],'count':item[3], 'url':item[4]}
        ruleList.append(ruleDict)

    data['data'] = ruleList[(page - 1) * limit: page  * limit]
    data["count"] = len(ruleList)

    return data


