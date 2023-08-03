from datetime import datetime, date, timedelta
import os
import pymysql

from flask import Flask, blueprints, Blueprint, render_template, request, json, Response, session, redirect

usr = Blueprint("usr", __name__)

@usr.route('/showUsr', methods=['GET', 'POST'])
def showUsr():

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

    cursor.execute("select * from usr ;")

    rules = cursor.fetchall()

    usrList = []

    for item in rules:
        ruleDict = {'account': item[0], 'pwd': item[1],'auth': item[2],'deny':item[3]}
        usrList.append(ruleDict)

    data['data'] = usrList[(page - 1) * limit: page  * limit]
    data["count"] = len(usrList)

    return data

@usr.route('/addUsr', methods=['GET', 'POST'])
def addUsr():

    task_info = dict(request.form)


    account = task_info['account']
    pwd = task_info['pwd']
    auth = task_info['type']
    deny = '未封禁'


    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    cursor.execute("select * from usr where account = %s;",account)
    user = cursor.fetchall()
    if user is not None:

        sql = "insert into usr (account, pwd, auth, deny) VALUES (%s,%s,%s,%s)"
        val = (account, pwd, auth, deny)
        cursor.execute(sql, val)
        db.commit()
    db.close()

    timeN = datetime.now().strftime('%Y-%m-%d %H:%M')
    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    sql = "insert into log_user(type, obj, time, account) VALUES (%s,%s,%s,%s)"
    val = ("添加用户", account, timeN, session['account'])
    cursor.execute(sql, val)
    db.commit()
    db.close()

    return render_template('userMange.html',account = session.get('account'))


@usr.route('/delUsr', methods=['GET', 'POST'])
def delUsr():

    data = json.loads(request.form.get('data'))
    account = data['account']


    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("delete from usr where account = %s;",account)

    db.commit()
    db.close()

    timeN = datetime.now().strftime('%Y-%m-%d %H:%M')
    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    sql = "insert into log_user(type, obj, time, account) VALUES (%s,%s,%s,%s)"
    val = ("删除用户", account, timeN, session['account'])
    cursor.execute(sql, val)
    db.commit()
    db.close()

    return Response(status=200)


@usr.route('/switchDeny', methods=['GET', 'POST'])
def switchDeny():

    data = json.loads(request.form.get('data'))
    account = data['account']
    switch = data['switch']


    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "update usr set deny = %s where account = %s;"
    val = (switch,account)
    cursor.execute(sql,val)

    db.commit()
    db.close()


    return Response(status=200)


@usr.route('/editPwd', methods=['GET', 'POST'])
def editPwd():

    data = dict(request.form)

    account = session.get('account')
    old = data['old']
    new = data['new']

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("select * from usr where account = %s and pwd = %s", (account, old))
    userData = cursor.fetchone()


    if userData is not None:
        auth = userData[0]
        deny = userData[1]

        sql = "update usr set pwd = %s where account = %s;"
        val = (new,account)
        cursor.execute(sql,val)
        db.commit()
        db.close()

    timeN = datetime.now().strftime('%Y-%m-%d %H:%M')
    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    sql = "insert into log_user(type, obj, time, account) VALUES (%s,%s,%s,%s)"
    val = ("修改密码", account, timeN, session['account'])
    cursor.execute(sql, val)
    db.commit()
    db.close()

    return render_template('index.html',account = session.get('account'))