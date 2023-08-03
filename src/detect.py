import re
from SQLAlchemy import *
from shelve0 import *


def detect(dict1):
    # 遍历爬虫结果 进行匹配
    pattern_dict=getrule()
    res = ''
    flag = 0

    risk = {'姓名': 0, '地址': 0, '身份证号': 0, '银行卡号': 0, '账号': 0, '健康信息': 0, '电话号': 0, '电子邮箱': 0, 'ip': 0,
            '国籍': 0}
    # print(pattern_dict)
    for key in pattern_dict:
        # print(key)
        temp_res = re.findall(pattern_dict[key], str(dict1['content']))
        if len(temp_res) != 0:
            # temp_dict = {key: temp_res[0]}
            print(dict1['url'], dict1['time'], dict1['taskId'], dict1['taskName'], dict1['taskType'], key, temp_res[0])

            insert_task_result(dict1['url'], dict1['time'], dict1['taskId'], dict1['taskName'], dict1['taskType'], key,
                               str(temp_res[0]))
            if flag==0:
                temp_str = '{}'.format(key) + ':{}'.format(temp_res[0])
                flag+=1
            else:
                temp_str = '<br>'+'{}'.format(key)+':{}'.format(temp_res[0])+'</br>'
            res=res+temp_str

            risk['{}'.format(key)] = 1
            update_count(dict1['taskId'])
            saveFile(dict1['url'], str(dict1['content']), dict1['taskName'], dict1['taskId'])
    # print("res:", res)

    risk0 = risk_level(risk,dict1['taskId'])
    # print(risk0,risk)
    if risk0:
        # print(dict1['taskId'], dict1['url'], dict1['time'], dict1['taskName'], risk_level(risk))
        insert_risk_level(dict1['url'], dict1['taskId'], dict1['time'], dict1['taskName'], str(risk0), res)
    return res, risk

def risk_level(risk,id):
    high = risk['地址'] + risk['身份证号'] + risk['银行卡号'] + risk['电话号']
    medium = risk['电子邮箱'] + risk['ip'] + risk['姓名']
    low = risk['账号'] + risk['健康信息'] + risk['国籍']
    if high >= 2:
        update_red(id)
        return 'high'
    elif high == 1 & medium >= 2:
        update_red(id)
        return 'medium-high'
    elif medium >= 2 | (high == 1 & medium == 1):
        update_red(id)
        return 'medium'
    elif (medium == 1 & low >= 2) | (high == 1 & low == 1):
        return 'medium-low'
    elif low | high | medium:
        return 'low'
    else:
        return None
