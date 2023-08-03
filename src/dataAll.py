import os
import pymysql

from flask import Flask, blueprints, Blueprint, render_template, request, json, Response, session, redirect

dataAll = Blueprint("dataAll", __name__)

@dataAll.route('/showData', methods=['GET', 'POST'])
def showData():
    if not session.get('account'):
        return redirect('/login')
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

    cursor.execute("select * from risk_level ;")

    rules = cursor.fetchall()
    db.close()
    dataList = []

    for item in rules:
        dataDict = {
            'name': item[3],
            'taskid': item[2],
            'level': item[5],
            'time': item[4],
            'url': item[1],
            'content': item[6]
        }
        if rule :
            if rule == dataDict['level'] :
                dataList.append(dataDict)
                data['data'] = dataList
                data["count"] = len(dataList)
        else:
            dataList.append(dataDict)
            data['data'] = dataList
            data["count"] = len(dataList)

    return data

