from flask import Flask, blueprints, Blueprint, render_template, request, json, Response, jsonify, session, redirect
import pymysql

dataPrd = Blueprint("dataPrd", __name__)


@dataPrd.route('/showPrdData', methods=['GET', 'POST'])
def showPrdData():
    if not session.get('account'):
        return redirect('/login')

    data = {
        "code": 200,
        "msg": "",
        "count": 0,
        "data":
            [
            ]

    }

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "select * from prd_config"
    cursor.execute(sql)
    config = cursor.fetchall()

    prdList = []

    for item in config:

        cursor.execute("select count from task_list where name =%s;", item[1])
        counts = cursor.fetchall()

        countForItem = 0
        if counts is not None:
            for one in counts:
                countForItem += one[0]

        ruleDict = {

            'name': item[1],
            'type': item[3],
            'allow_domain': item[7],
            'rules': item[8],
            'lastTime': item[9],
            'count': countForItem,
            'mark': item[11]
        }
        prdList.append(ruleDict)

    data['data'] = prdList
    data["count"] = len(prdList)

    db.close()

    return data


@dataPrd.route('/showPrdConfig', methods=['GET', 'POST'])
def showPrdConfig():
    if not session.get('account'):
        return redirect('/login')

    data = {
        "code": 200,
        "msg": "",
        "count": 0,
        "data":
            [
            ]

    }

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "select * from prd_config"
    cursor.execute(sql)
    config = cursor.fetchall()

    prdList = []

    for item in config:
        ruleDict = {
            'id': item[0],
            'name': item[1],
            'state': item[2],
            'type': item[3],
            'prd': item[4],
            'date': item[5],
            'start_url': item[6],
            'domain': item[7],
            'rules': item[8],
            'mark': item[11]
        }
        prdList.append(ruleDict)

    data['data'] = prdList
    data["count"] = len(prdList)

    db.close()

    return data


@dataPrd.route('/editPrdConfig', methods=['GET', 'POST'])
def editPrdConfig():
    data = json.loads(request.form.get('data'))
    print(data)

    configID = data['id']
    state = data['state']
    taskType = data['type']
    prd = data['prd']
    date = data['date']

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    cursor.execute("select state from prd_config where id = %s;", configID)
    oldState = cursor.fetchone()[0]

    if oldState == 'on' and state == 'on':
        sql = "update prd_config SET state = %s, type = %s, prd = %s, date = %s, modify = %s WHERE id = %s ;"
        val = (state, taskType, prd, date, 1, configID)
    else:
        sql = "update prd_config SET state = %s, type = %s, prd = %s, date = %s WHERE id = %s ;"
        val = (state, taskType, prd, date, configID)
    cursor.execute(sql, val)
    db.commit()
    db.close()

    return render_template('taskPrd.html', account=session.get('account'))


@dataPrd.route('/addPrdConfig', methods=['GET', 'POST'])
def addPrdConfig():
    task_info = dict(request.form)
    print('测试修改')
    print(task_info)

    rules_loaded = []
    for key in task_info:
        if task_info[key] == 'on':
            rules_loaded.append(key)

    name = task_info['name']
    taskType = task_info['taskType']
    prd = task_info['prd']
    date = task_info['date']
    start_url = task_info['startUrl']
    domain = task_info['domain']
    mark = task_info['mark']
    ruleStr = ','.join(rules_loaded)

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    sql = "insert into prd_config (name, state, type, prd, date, start_url, domain, rules, modify, mark) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    val = (name, 'on', taskType, prd, date, start_url, domain, ruleStr, 0, mark)
    cursor.execute(sql, val)
    db.commit()
    db.close()

    return render_template('taskPrd.html', account=session.get('account'))


@dataPrd.route('/delConfig', methods=['GET', 'POST'])
def delConfig():
    data = json.loads(request.form.get('data'))
    configID = data['id']

    print(configID)

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("delete from prd_config where id = %s;", configID)

    db.commit()
    db.close()

    return Response(status=200)


@dataPrd.route('/switchConfig', methods=['GET', 'POST'])
def switchConfig():
    data = json.loads(request.form.get('data'))
    configID = data['id']
    switch = data['switch']

    print(configID)

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "update prd_config set state = %s where id = %s;"
    val = (switch, configID)
    cursor.execute(sql, val)

    db.commit()
    db.close()

    return Response(status=200)


@dataPrd.route('/delPrdData', methods=['GET', 'POST'])
def delPrdData():
    data = json.loads(request.form.get('data'))
    taskName = data['name']

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("delete from task_list where name = %s;", taskName)
    cursor.execute("delete from task_result where name = %s;", taskName)
    cursor.execute("delete from risk_level where name = %s;", taskName)

    db.commit()
    db.close()

    return Response(status=200)


@dataPrd.route('/dataPrdTask/<taskName>', methods=['GET', 'POST'])
def dataPrdTask(taskName):
    return render_template('dataPrdTask.html', taskName=taskName, account=session.get('account'))


@dataPrd.route('/showPrdTaskByName/<taskName>', methods=['GET', 'POST'])
def showPrdTaskByName(taskName):
    data = {
        "code": 200,
        "msg": "",
        "count": 0,
        "data": []

    }

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("select * from task_list where name = %s ;", taskName)

    rules = cursor.fetchall()

    ruleList = []

    for item in rules:
        ruleDict = {
            'id': item[0],
            'name': item[1],
            'domain': item[3],
            'start_time': item[8],
            'end_time': item[9],
            'rules': item[4],
            'page': item[10],
            'count': item[11],
        }
        ruleList.append(ruleDict)

    data['data'] = ruleList
    data["count"] = len(ruleList)

    return data
