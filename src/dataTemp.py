import os
import shelve

import pymysql
from flask import Flask, blueprints, Blueprint, render_template, request, json, Response, jsonify, session, redirect

dataTemp = Blueprint("dataTemp", __name__)


@dataTemp.route('/dataTempList', methods=['GET', 'POST'])
def dataTempList():
    if not session.get('account'):
        return redirect('/login')
    return render_template('dataTemp.html',account = session.get('account'))


@dataTemp.route('/showTaskList', methods=['GET', 'POST'])
def showTaskList():
    data = {
        "code": 200,
        "msg": "",
        "count": 0,
        "data": []

    }

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("select * from task_list ;")

    rules = cursor.fetchall()

    ruleList = []

    for item in rules:
        ruleDict = {
                    'id' : item[0],
                    'name': item[1],
                    'domain': item[3],
                    'start_time': item[8],
                    'end_time': item[9],
                    'rules': item[4],
                    'page': item[10],
                    'count': item[14],
                    'file':item[13]
                    }
        ruleList.append(ruleDict)

    data['data'] = ruleList
    data["count"] = len(ruleList)

    return data



@dataTemp.route('/delTaskTemp', methods=['GET', 'POST'])
def delTaskTemp():
    if not session.get('account'):
        return redirect('/login')
    data = json.loads(request.form.get('data'))
    taskID = data['id']

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "delete from task_list where id = %s"
    cursor.execute(sql, taskID)

    sql = "delete from task_result where task_id = %s"
    cursor.execute(sql, taskID)

    db.commit()
    db.close()

    return Response(status=200)


# 查看某个临时任务信息的入口
@dataTemp.route('/dataTempInfo/<taskID>', methods=['GET', 'POST'])
def dataTempInfo(taskID):
    if not session.get('account'):
        return redirect('/login')

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "select * from task_list where id = %s"
    cursor.execute(sql, taskID)

    data = cursor.fetchone()

    db.close()

    taskInfo = {'startTime': data[8],
                'endTime': data[9],
                'msg': data[5],
                'startUrl': data[2],
                'domain': data[3],
                'count': data[11],
                'rule': data[4].split(',')}

    return render_template('dataTempInfo.html', info=taskInfo, taskID = taskID)

# 查看某个临时任务信息的入口
@dataTemp.route('/dataTemprisk/<taskID>', methods=['GET', 'POST'])
def dataTemprisk(taskID):
    if not session.get('account'):
        return redirect('/login')

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "select * from task_list where id = %s"
    cursor.execute(sql, taskID)

    data = cursor.fetchone()

    db.close()

    taskInfo = {'startTime': data[8],
                'endTime': data[9],
                'msg': data[5],
                'startUrl': data[2],
                'domain': data[3],
                'count': data[11],
                'rule': data[4].split(',')}

    return render_template('dataTemprisk.html', info=taskInfo, taskID = taskID)

@dataTemp.route('/showTaskInfo/<taskID>', methods=['GET', 'POST'])
def showTaskInfo(taskID):
    if not session.get('account'):
        return redirect('/login')

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "select * from task_list where id = %s"
    cursor.execute(sql, taskID)

    data = cursor.fetchone()

    db.close()

    taskInfo = {'startTime': data[8],
                'endTime': data[9],
                'msg': data[5],
                'startUrl': data[2],
                'domain': data[3],
                'count': data[11],
                'rule': data[4].split(',')}

    return render_template('showTask.html', info=taskInfo, taskID = taskID)

@dataTemp.route('/query/<taskID>', methods=['GET', 'POST'])
def query(taskID):
    if not session.get('account'):
        return redirect('/login')

    print('query id:', taskID)
    content = request.form.get("content")
    rule = request.form.get("rule")
    print(rule)
    data = {
        "code": 200,
        "msg": "",
        "count": 0,
        "data": []

    }

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "select * from task_result where task_id = %s"
    cursor.execute(sql, taskID)
    taskRes = cursor.fetchall()

    db.close()

    dataList = []

    for item in taskRes:
        dataDict = {
            'name' : item[2],
            'rule': item[4],
            'content': item[5],
            'time': item[6],
            'id': item[1],
            'url': item[7]
        }
        if rule or content:
            if rule in dataDict['rule'] and content in dataDict['content']:
                dataList.append(dataDict)
                data['data'] = dataList
                data["count"] = len(dataList)
        else:
            dataList.append(dataDict)
            data['data'] = dataList
            data["count"] = len(dataList)

    return data

@dataTemp.route('/risk/<taskID>', methods=['GET', 'POST'])
def risk(taskID):
    if not session.get('account'):
        return redirect('/login')

    print('query id:', taskID)
    # content = request.form.get("content")
    rule = request.form.get("rule")

    data = {
        "code": 200,
        "msg": "",
        "count": 0,
        "data": []

    }

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    sql = "select * from risk_level where task_id = %s"
    cursor.execute(sql, taskID)
    taskRes = cursor.fetchall()

    db.close()

    dataList = []

    for item in taskRes:
        dataDict = {
            'name' : item[3],
            'taskid': item[2],
            'level': item[5],
            'time': item[4],
            'url': item[1],
            'content':item[6]
           }
        if rule:
            if rule==dataDict['level']:
                dataList.append(dataDict)
                data['data'] = dataList
                data["count"] = len(dataList)
        else:
            dataList.append(dataDict)
            data['data'] = dataList
            data["count"] = len(dataList)
    # data['data'] = dataList
    # data["count"] = len(dataList)
    return data

@dataTemp.route('/org', methods=['GET', 'POST'])
def org():
    # data = request.get_data()
    data = json.loads(request.get_data(as_text=True))
    print(type(data),data)

    taskName = data['name']
    taskId = int(data['id'])
    url = data['url']

    # taskName = 'fileTest'
    # taskId = 1
    # url = 'https://www.cnblogs.com/caibao666/p/6531044.html'

    print(taskName,taskId,url)

    os.chdir('/root/demo/project/store')

    fileName = taskName + '_' + str(taskId)
    # filePath = 'store/' + fileName
    with shelve.open(fileName) as data:
        res = data[url]
    return jsonify(res)
    # return res
    # fileName = 'name' + '_' + 'id'
    # with shelve.open(fileName) as data:
    #     res = data[url]




