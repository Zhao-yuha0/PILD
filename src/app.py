import os
import datetime
from urllib.parse import urlparse

import json
import pymysql
from flask import Flask, request, render_template, jsonify, blueprints, session, redirect
import start
from datetime import datetime, date, timedelta
from dataTemp import dataTemp
from dataPrd import dataPrd
from rule import rule
from dataAll import dataAll
from testTask import testTask
from usr import usr
from log import log

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = '123456'

# 在应用对象上注册蓝图对象
app.register_blueprint(testTask)
app.register_blueprint(dataTemp)
app.register_blueprint(dataPrd)
app.register_blueprint(rule)
app.register_blueprint(dataAll)
app.register_blueprint(usr)
app.register_blueprint(log)


@app.route('/', methods=['GET', 'POST'])
def index():
    session.clear()
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    return render_template('index.html')


@app.route('/loginCheck', methods=['GET', 'POST'])
def loginCheck():
    # account1 = request.form.get('username')
    # password1 = request.form.get('password')
    data = json.loads(request.form.get('data'))

    account = data['account']
    password = data['pwd']

    # 1212121212
    db = pymysql.connect(user="root", password="123456", db="ConTest")
    cursor = db.cursor()
    cursor.execute("select auth, deny from usr where account = %s and pwd = %s", (account, password))
    userData = cursor.fetchone()
    db.close()

    if userData is not None:
        auth = userData[0]
        deny = userData[1]
        if deny == '未封禁':
            session['account'] = account
            session['auth'] = auth
            # return redirect('/home')

            timeN = datetime.now().strftime('%Y-%m-%d %H:%M')
            db = pymysql.connect(user="root", passwd="123456", db="ConTest")
            cursor = db.cursor()
            sql = "insert into log_user(type, obj, time, account) VALUES (%s,%s,%s,%s)"
            val = ("登录", session['auth'], timeN, session['account'])
            cursor.execute(sql, val)
            db.commit()
            db.close()

            return jsonify({'res': 111, 'message': '欢迎' + account})

        else:
            return jsonify({'res': 222, 'message': '账户已不可用'})
    else:
        return jsonify({'res': 333, 'message': '用户名和密码不匹配'})


@app.route('/userMange')
def userMange():
    if not session.get('account'):
        return redirect('/login')

    elif session.get('auth') == '管理员':
        return render_template('userMange.html')

    else:
        return render_template('pwdChange.html', account=session.get('account'))


@app.route('/pwdChange')
def pwdChange():
    if not session.get('account'):
        return redirect('/login')

    account = session.get('account')

    return render_template('pwdChange.html', account=session.get('account'))


@app.route('/data')
def data():
    if not session.get('account'):
        return redirect('/login')
    return render_template('data.html')


@app.route('/dataTempList', methods=['GET', 'POST'])
def dataTempList():
    if not session.get('account'):
        return redirect('/login')
    return render_template('dataTemp.html', account=session.get('account'))


@app.route('/dataPrd')
def dataPrd():
    if not session.get('account'):
        return redirect('/login')
    return render_template('dataPrd.html', account=session.get('account'))


@app.route('/getTaskTemp', methods=['GET', 'POST'])
def getTaskTemp():
    if not session.get('account'):
        return redirect('/login')
    a = request.json['fileName']
    print(a)
    return jsonify(a)


@app.route('/home', methods=['GET', 'POST'])
def home():
    if not session.get('account'):
        return redirect('/login')

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from sys_info;")
    sysData = cursor.fetchone()

    cursor.execute("select * from task_list where state = 'finish';")
    taskTotal = len(cursor.fetchall())

    # 获得正在进行任务
    cursor.execute("select name,start_url,domain from task_list where state = 'running';")
    taskRunning = cursor.fetchall()

    # 获得等待进行任务
    cursor.execute("select name,start_url,domain from task_wait;")
    taskWaiting = cursor.fetchall()

    for task in taskWaiting:
        if task['domain'] == '仅本域名':
            task['range'] = urlparse(task['start_url']).netloc
        elif task['domain'] == '同级域名':
            this_str = urlparse(task['start_url']).netloc
            up_str = this_str.split('.', 1)[1]
            task['range'] = up_str
        else:
            task['range'] = task['start_url']

    cursor.execute("select name,count(*) as waitCount from task_wait group by name;")
    waitTask = cursor.fetchall()

    cursor.execute("select name,count(*) as runningCount from task_list where state = 'running' group by name;")
    runningTask = cursor.fetchall()

    # 合并两个列表
    tasks = []
    for task in waitTask:
        tasks.append(task)
    for task in runningTask:
        tasks.append(task)

    # print(tasks)

    batchData = []
    names = []
    for task in tasks:
        name = task['name']
        if name in names:
            pass
        else:
            names.append(name)

    for name in names:
        waitCount = 0
        runningCount = 0
        allCount = 0
        for task in waitTask:
            if task['name'] == name:
                allCount += task['waitCount']
                waitCount = task['waitCount']
        for task in runningTask:
            if task['name'] == name:
                allCount += task['runningCount']
                runningCount = task['runningCount']
        batchData.append({'name': name, 'allCount': allCount, 'waitCount': waitCount, 'runningCount': runningCount})


    db.close()

    return render_template('home.html', account=session.get('account'),
                           sysData=sysData, taskTotal=taskTotal, taskRunning=taskRunning, taskWaiting=taskWaiting, batchData=batchData)


######################
@app.route('/erchart', methods=['GET', 'POST'])
def erchart():
    # 1从数据库查系统信息数据返回给前端（用字典组成json数据）
    # 2
    con = pymysql.connect(
        host="localhost",
        user='root',
        password='123456',
        database="ConTest")
    cursor = con.cursor()
    cursor.execute('select * from sys_info')
    sysData = cursor.fetchone()
    taskTotal = sysData[4]
    taskCount = sysData[5]
    storageTotal = sysData[6]
    storageUsed = sysData[7]
    send = sysData[8]
    rev = sysData[9]
    print(sysData)
    print('123')
    avi_taskCount = taskTotal - taskCount
    avi_storageTotal = storageTotal - storageUsed
    a = {
        "num1": taskCount,
        "num2": avi_taskCount,
        "num3": storageUsed,
        "num4": avi_storageTotal,
        "num5": send,
        "num6": rev
    }
    return a


##########################

@app.route('/logSys')
def logSys():
    if not session.get('account'):
        return redirect('/login')
    return render_template('logSys.html', account=session.get('account'))


@app.route('/logUsr')
def logUsr():
    if not session.get('account'):
        return redirect('/login')
    return render_template('logUsr.html', account=session.get('account'))


@app.route('/taskPrd')
def taskPrd():
    if not session.get('account'):
        return redirect('/login')

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    cursor.execute("select name from rule")
    ruleNames = cursor.fetchall()
    db.close()

    ruleNameList = []
    for name in ruleNames:
        ruleNameList.append({'name': name[0]})

    return render_template('taskPrd.html', ruleList=ruleNameList, account=session.get('account'))


@app.route('/taskRule')
def taskRule():
    if not session.get('account'):
        return redirect('/login')
    return render_template('taskRule.html', account=session.get('account'))


@app.route('/taskTemp')
def taskTemp():
    if not session.get('account'):
        return redirect('/login')

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    cursor.execute("select name from rule")
    ruleNames = cursor.fetchall()
    db.close()

    ruleNameList = []
    for name in ruleNames:
        ruleNameList.append({'name': name[0]})

    return render_template('taskTemp.html', ruleList=ruleNameList, account=session.get('account'))


@app.route('/testRule')
def testRule():
    if not session.get('account'):
        return redirect('/login')
    return render_template('testRule.html', account=session.get('account'))


@app.route('/testSite')
def testSite():
    if not session.get('account'):
        return redirect('/login')
    return render_template('testSite.html', account=session.get('account'))


@app.route('/testReg')
def testReg():
    if not session.get('account'):
        return redirect('/login')
    return render_template('testReg.html', account=session.get('account'))


@app.route('/testHistory')
def testHistory():
    if not session.get('account'):
        return redirect('/login')
    return render_template('testHistory.html', account=session.get('account'))


@app.route('/dataPrdTask')
def dataPrdTask():
    if not session.get('account'):
        return redirect('/login')
    return render_template('dataPrdTask.html', account=session.get('account'))


# 发起临时任务
@app.route('/launchTaskTemp', methods=['GET', 'POST'])
def launchTaskTemp(self=None):
    if not session.get('account'):
        return redirect('/login')
    # 获得提交数据
    task_info = dict(request.form)

    # # 初始化规则
    # with open("static/json/ruleList.json", 'rb') as load_f:
    #     read = json.load(load_f)
    #     rules = read["data"]
    #
    # # 获得页面选中的规则名称
    # rules_loaded = []
    # for key in task_info:
    #     if task_info[key] == 'on':
    #         rules_loaded.append(key)
    #
    # # 获得规则字典列表
    # rule_dicts = {}
    # for name in rules_loaded:
    #     for rule in rules:
    #         if rule['name'] == name:
    #             rule_dicts[name] = rule['content']

    taskName = task_info['taskName']
    sites = str(task_info['sites'])
    timeN = datetime.now().strftime('%Y-%m-%d %H:%M')

    urls = sites.splitlines()
    urls = [item for item in filter(lambda x: x != '', urls)]

    domain = task_info['domain']
    taskType = '临时任务'
    # ruleStr = ','.join(rules_loaded)
    # 添加任务到数据库
    ruleStr = 'None'
    for url in urls:
        db = pymysql.connect(user="root", passwd="123456", db="ConTest")
        cursor = db.cursor()
        sql = "insert into task_wait (name, add_time, start_url, domain, rules, type) VALUES (%s,%s,%s,%s,%s,%s)"
        val = (taskName, timeN, url, domain, ruleStr, taskType)
        cursor.execute(sql, val)
        db.commit()
        db.close()

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    sql = "insert into log_user(type, obj, time, account) VALUES (%s,%s,%s,%s)"
    val = ("下发任务", taskName, timeN, session['account'])
    cursor.execute(sql, val)
    db.commit()
    db.close()

    # 返回结果页面
    return render_template('dataTemp.html', account=session.get('account'))


# @app.route('/siteTest', methods=['GET', 'POST'])
# def siteTest(self=None):
#     if not session.get('account'):
#         return redirect('/login')
#     # 获得提交数据
#     task_info = dict(request.form)
#
#     testType = '网页测试'
#     rules = '什么都不检测'
#     url = task_info['siteInput']
#     add_time = datetime.now().strftime('%Y-%m-%d %H:%M')
#     domain = task_info['domain']
#
#     db = pymysql.connect(user="root", passwd="123456", db="ConTest")
#     cursor = db.cursor()
#     sql = "insert into test (type, rules, url, add_time, domain) VALUES (%s,%s,%s,%s,%s)"
#     val = (testType,rules,url,add_time,domain)
#     cursor.execute(sql, val)
#     db.commit()
#     db.close()
#
#
#     # 返回结果页面
#     return render_template('result.html')
#
#
# @app.route('/regTest', methods=['GET', 'POST'])
# def regTest(self=None):
#     if not session.get('account'):
#         return redirect('/login')
#     # 获得提交数据
#     task_info = dict(request.form)
#
#     testType = '规则测试'
#     rules = task_info['ruleInput']
#     url = task_info['siteInput']
#     add_time = datetime.now().strftime('%Y-%m-%d %H:%M')
#     domain = '仅本网页'
#
#     db = pymysql.connect(user="root", passwd="123456", db="ConTest")
#     cursor = db.cursor()
#     sql = "insert into test (type, rules, url, add_time, domain) VALUES (%s,%s,%s,%s,%s)"
#     val = (testType,rules,url,add_time,domain)
#     cursor.execute(sql, val)
#     db.commit()
#     db.close()
#
#
#     # 返回结果页面
#     return render_template('result.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
