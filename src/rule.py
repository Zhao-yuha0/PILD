import os
import pymysql
from flask import Flask, blueprints, Blueprint, render_template, request, json, Response, session, redirect, jsonify

rule = Blueprint("rule", __name__)


@rule.route('/showRules', methods=['GET', 'POST'])
def showRules():
    data = {
        "code": 200,
        "msg": "",
        "count": 0,
        "data": []

    }

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("select * from rule ;")

    rules = cursor.fetchall()

    ruleList = []

    for item in rules:
        ruleDict = {'name': item[0], 'content': item[1],'value':item[2]}
        ruleList.append(ruleDict)

    data['data'] = ruleList
    data["count"] = len(ruleList)

    return data


@rule.route('/addRule', methods=['GET', 'POST'])
def addRule():
    data = json.loads(request.form.get('data'))

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("select * from rule where name = %s;",data['name'])
    res = cursor.fetchall()

    if len(res) == 0:
        # print(data['name'],data['content'],data['value'])
        print(((data['value']=='高')|(data['value']=='中')|(data['value']=='低')))
        print(len(data['name']),len(data['content']),len(data['value']))
        print((len(data['name'])>0)&(len(data['content'])>0)&(len(data['value'])>0))
        if (len(data['name'])>0)&(len(data['content'])>0)&(len(data['value'])>0)&((data['value']=='高')|(data['value']=='中')|(data['value']=='低')):
              cursor.execute("insert into rule (name, content,value) VALUES (%s,%s,%s);", (data['name'], data['content'],data['value']))
              db.commit()
              db.close()
        else:
            db.commit()
            db.close()
            return Response(status=400)
    else:
        db.commit()
        db.close()
        return Response(status=400)

    return Response(status=200)



@rule.route('/delRule', methods=['GET', 'POST'])
def delRule():

    data = json.loads(request.form.get('data'))
    name = data['name']

    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("delete from rule where name = %s;",name)

    db.commit()
    db.close()


    return Response(status=200)


