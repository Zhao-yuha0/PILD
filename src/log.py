import os
import pymysql

from flask import Flask, blueprints, Blueprint, render_template, request, json, Response, session, redirect

log = Blueprint("log", __name__)


@log.route('/showUsrLog', methods=['GET', 'POST'])
def showUsrLog():

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

    cursor.execute("select * from log_user ;")

    rules = cursor.fetchall()

    ruleList = []

    for item in rules:
        ruleDict = {'type': item[1], 'obj': item[2],'time': item[3],'account':item[4]}
        ruleList.append(ruleDict)

    data['data'] = ruleList[(page - 1) * limit: page  * limit]
    data["count"] = len(ruleList)

    return data


@log.route('/showSysLog', methods=['GET', 'POST'])
def showSysLog():

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

    cursor.execute("select * from sys_log ;")

    rules = cursor.fetchall()

    ruleList = []

    for item in rules:
        ruleDict = {'type': item[1], 'time': item[2],'obj': item[3]}
        ruleList.append(ruleDict)

    data['data'] = ruleList[(page - 1) * limit: page  * limit]
    data["count"] = len(ruleList)

    return data