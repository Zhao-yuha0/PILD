import pymysql
import re
from detect import *
def getrule():
    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("select * from rule ;")

    rules = cursor.fetchall()

    ruledict=dict()
    for item in rules:
        ruledict['{}'.format(item[0])] = item[1]
        # ruleList.append(ruleDict)

    # data = ruleList

    return ruledict
# item='3,85590744,zhintaihg,13313642261,192.168.1.1,15645002170,230103199711235518,407973365@qq.com'
# pattern_dict=getrule()
# for key in pattern_dict:
#     print(pattern_dict[key])
#     temp_res = re.findall(pattern_dict[key], str(item))
#     print(temp_res)
item={'content': '15645002170', 'taskId': 99, 'taskName': 'demoTask', 'taskType': '临时任务', 'time': '14:22:45', 'url': 'http://cstc.hrbeu.edu.cn/bzrgz/list.htm'}
print(type(item))
detect(item)
