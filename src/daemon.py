# coding: utf-8

import os
import sys
import time
import atexit
import signal

import psutil
import pymysql
import time
import re
from urllib.parse import urlparse

import pymysql
import shelve
from datetime import datetime, date, timedelta
import os
import psutil
from SQLAlchemy import *

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler

import start


class Daemon:
    def __init__(self, pidfile='/tmp/daemon.pid', stdin='/dev/null', stdout='/dev/null', stderr='/dev/null'):
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.pidfile = pidfile

    def daemonize(self):
        if os.path.exists(self.pidfile):
            raise RuntimeError('Already running.')

        # First fork (detaches from parent)
        try:
            if os.fork() > 0:
                raise SystemExit(0)
        except OSError as e:
            raise RuntimeError('fork #1 faild: {0} ({1})\n'.format(e.errno, e.strerror))

        os.chdir('/')
        os.setsid()
        os.umask(0o22)

        # Second fork (relinquish session leadership)
        try:
            if os.fork() > 0:
                raise SystemExit(0)
        except OSError as e:
            raise RuntimeError('fork #2 faild: {0} ({1})\n'.format(e.errno, e.strerror))

        # Flush I/O buffers
        sys.stdout.flush()
        sys.stderr.flush()

        # Replace file descriptors for stdin, stdout, and stderr
        with open(self.stdin, 'rb', 0) as f:
            os.dup2(f.fileno(), sys.stdin.fileno())
        with open(self.stdout, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stdout.fileno())
        with open(self.stderr, 'ab', 0) as f:
            os.dup2(f.fileno(), sys.stderr.fileno())

        # Write the PID file
        with open(self.pidfile, 'w') as f:
            print(os.getpid(), file=f)

        # Arrange to have the PID file removed on exit/signal
        atexit.register(lambda: os.remove(self.pidfile))

        signal.signal(signal.SIGTERM, self.__sigterm_handler)

    # Signal handler for termination (required)
    @staticmethod
    def __sigterm_handler(signo, frame):
        raise SystemExit(1)

    def start(self):
        try:
            self.daemonize()
        except RuntimeError as e:
            print(e, file=sys.stderr)
            raise SystemExit(1)

        self.run()

    def stop(self):
        try:
            if os.path.exists(self.pidfile):
                with open(self.pidfile) as f:
                    os.kill(int(f.read()), signal.SIGTERM)
            else:
                print('Not running.', file=sys.stderr)
                raise SystemExit(1)
        except OSError as e:
            if 'No such process' in str(e) and os.path.exists(self.pidfile):
                os.remove(self.pidfile)

    def restart(self):
        self.stop()
        self.start()

    def run(self):
        pass


def sysInfo():
    # 当前1s内cpu的使用率
    cpuPercent = psutil.cpu_percent(interval=1)
    # 逻辑cpu个数
    count = psutil.cpu_count()
    # 磁盘使用
    store = psutil.disk_usage('/')
    storeUsed = store.used / 1024 / 1024
    storeTotal = store.total / 1024 / 1024

    # 内存
    memory = psutil.virtual_memory()
    memoryUsed = memory.used / 1024 / 1024
    memoryTotal = memory.total / 1024 / 1024

    net = psutil.net_io_counters()
    netR = net.bytes_recv / 1024 / 1024
    netS = net.bytes_sent / 1024 / 1024

    taskCount = -1

    task_total = -1

    timeStart = datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M")

    # db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    # cursor = db.cursor()
    update_sys_info(timeStart, taskCount, task_total, cpuPercent, storeTotal, storeUsed, memoryTotal, memoryUsed, netR,
                    netS)
    # sql = "update sys_info SET " \
    #       "start_time=%s, " \
    #       "task_count =%s, " \
    #       "task_total=%s, " \
    #       "cpu_percent=%s, " \
    #       "storage_total=%s, " \
    #       "storage_used=%s," \
    #       "memory_total = %s, " \
    #       "memory_used = %s, " \
    #       "net_recv_M=%s, " \
    #       "net_sent_M=%s"
    # val = (timeStart, taskCount, task_total, cpuPercent, storeTotal, storeUsed, memoryTotal, memoryUsed, netR, netS)
    # cursor.execute(sql, val)

    # db.commit()
    # db.close()


def prdHistoryDel():
    # time1 = '2021-04-18 10:47'
    # time2 = '2021-04-11 14:12'
    #
    # a = parse(time1)
    # b = parse(time2)
    # n = datetime.now()
    # res = (a - b).days
    # print(res)
    print('删除周期历史记录')
    # db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    # cursor = db.cursor()

    delTime = datetime.now() + timedelta(days=-15)
    timeStr = delTime.strftime('%Y-%m-%d %H:%M')
    delete_prd_history(timeStr)
    # cursor.execute("delete from prd_history where time < %s;", timeStr)
    #
    # db.commit()
    #
    # db.close()


# 获得指定类型的空闲爬虫名称
# type：temp,prd,testReg,testSite
def getFreeSpider(taskType):
    # db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    # cursor = db.cursor()
    res = select_spiders('free', taskType)
    # cursor.execute("select name from spiders where state = 'free' and type = %s;", taskType)
    #
    # res = cursor.fetchone()
    # db.close()
    if res is None:
        return None
    else:
        return res.name


# 根据规则名称列表获得规则字典
# in：List[name,name,..]
# out dict{name:content,..}
def getRuleDict(ruleNames):
    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("select * from rule ;")

    ruleData = cursor.fetchall()
    ruleDict = {}
    for rule in ruleData:
        if rule[0] in ruleNames:
            ruleDict[rule[0]] = rule[1]

    db.close()

    return ruleDict


# 检测待执行任务 并且开始执行
def startTask():
    print('检测待执行任务')
    # db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    # cursor = db.cursor()

    # 检测待执行的任务，取一条
    allTaskData = select_task_wait()
    # print(taskData)
    if len(allTaskData) > 0:
        taskData = allTaskData[0]
        spiderName = getFreeSpider(taskData.type)

        if spiderName:
            # 开始任务接口
            start.start_spider_threads(spiderName,
                                       taskData.id,
                                       taskData.name,
                                       taskData.domain,
                                       taskData.start_url,
                                       taskData.type)
            # print(spiderName, taskData.id, taskData.name, taskData.start_url, taskData.domain, taskData.type)

            # 删除任务记录
            delete_task_wait(taskData.id)


            timeN = datetime.now().strftime('%Y-%m-%d %H:%M')
            db = pymysql.connect(user="root", passwd="123456", db="ConTest")
            cursor = db.cursor()
            sql = "insert into sys_log (type, time, obj) VALUES (%s,%s,%s)"
            val = ("执行任务", timeN, taskData.name)
            cursor.execute(sql, val)
            db.commit()
            db.close()



    # cursor.execute("select * from task_wait ;")
    # taskData = cursor.fetchone()
    # if taskData is not None:
    #     taskID = taskData[0]
    #     spiderName = getFreeSpider(taskData[6])
    #     if spiderName is not None:
    #         print('执行任务')
    #         taskName = taskData[1]
    #         startUrl = taskData[3]
    #         domain = taskData[4]
    #         ruleDict = getRuleDict(taskData[5].split(','))
    #
    #         # 开始爬虫任务
    #         start.start_crawler_threads(spiderName, startUrl, taskName, domain, ruleDict, taskID)
    #         # 删除任务记录
    #         delete_task_wait(taskID)
    #         # cursor.execute("delete from task_wait where id = %s;", taskID)
    #         # db.commit()
    #         # db.close()
    #     else:
    #         print('no idle spider')
    # else:
    #     print('无待执行任务')


# 检测待执行任务  并且开始执行
def startTest():
    print('检测待执行测试')
    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    # 检测待执行的任务
    cursor.execute("select * from test ;")
    testData = cursor.fetchone()
    cursor.execute("delete from test")
    db.commit()
    db.close()

    if testData is not None:
        print('执行测试')
        # 规则测试 规则表达式+单个网页  -》 检测内容
        ruleDict = {}
        if testData[0] == '规则测试':
            spiderName = getFreeSpider('规则测试')
            taskName = '规则测试任务'
            domain = '仅本域名'

            ruleDict['rule'] = testData[1]
            startUrl = testData[2]

            # 开始爬虫任务
            start.start_Test_threads(spiderName, startUrl, taskName, domain, ruleDict, 0)
        # 网页测试 起始网页+域名范围  -》 网页数量
        else:
            spiderName = getFreeSpider('站点测试')
            taskName = '站点测试任务'
            domain = testData[4]
            ruleDict['rule'] = 'thisIsTricks'
            startUrl = testData[2]

            # 开始测试任务
            start.start_Test_threads(spiderName, startUrl, taskName, domain, ruleDict, 0)
    else:
        print('无待执行测试')


# 检测中断任务，重新写入到待执行队列
def recoverTask():
    print('检测中断任务')
    # db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    # cursor = db.cursor()
    # 检测中断任务，写回待执行任务
    taskList = select_task_list(task_list, 'running')
    # cursor.execute("select * from task_list where state ='running';")
    # taskList = cursor.fetchall()
    for task in taskList:
        p = psutil.pid_exists(task.pid)
        taskID = task.id
        spiderName = task.spider
        # print(p)
        # 检测到中断pid
        if not p:
            print('恢复中断任务')
            taskName = task.name
            startUrl = task.start_url
            domain = ''
            rules = task.rules
            taskType = task.type

            addTime = datetime.now().strftime('%Y-%m-%d %H:%M')

            # 判断任务域名范围
            # domain == url
            if task.domain == task.start_url:
                domain = '仅本网页'
            # domain = urlparse(task[2]).netloc
            elif task.domain == urlparse(task.start_url).netloc:
                domain = '仅本域名'
            else:
                domain = '同级域名'

            # 添加到待执行任务列表
            insert_task_wait(taskName, addTime, startUrl, domain, rules, type)
            # cursor.execute("insert into task_wait(name, add_time, start_url, domain, rules, type) "
            #                "VALUES (%s,%s,%s,%s,%s,%s) ;", (taskName, addTime, startUrl, domain, rules, taskType))
            #   删除任务记录
            delete_task_wait(taskID)
            # cursor.execute("delete from task_list where id = %s;", task[0])
            # 恢复爬虫空闲状态
            update_spiders(spiderName, 'free')
            # cursor.execute("update spiders SET state='free' WHERE name = %s", spiderName)
    #     db.commit()
    # db.close()


# 周期任务添加任务的方法
def addTask(name, startUrl, domain, rules, taskType, mark):
    print('添加周期任务')
    addTime = datetime.now().strftime('%Y-%m-%d %H:%M')
    # insert_task_wait(name, addTime, startUrl, domain, rules, taskType)
    timeN = datetime.now().strftime('%Y-%m-%d %H:%M')
    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    sql = "insert into task_wait (name, add_time, start_url, domain, rules, type, mark) VALUES (%s,%s,%s,%s,%s,%s)"
    val = (name, timeN, startUrl, domain, 'None', taskType, mark)
    cursor.execute(sql, val)
    db.commit()
    db.close()


def initPrdTask(scheduler):
    print('初始化周期任务')
    # db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    # cursor = db.cursor()
    # cursor.execute("select * from prd_config where state='on';")
    # configs = cursor.fetchall()
    configs = select_prd_config_state(prd_config, 'on')
    # print('config:', configs)
    for config in configs:
        if config.prd == '每周':
            scheduler.add_job(addTask, 'cron', day_of_week=config.date, name=config.name,
                              args=[config.name, config.start_url, config.domain, config.rules, config.type, config.mark])
        if config.prd == '每月':
            scheduler.add_job(addTask, 'cron', day=config.date, name=config.name,
                              args=[config.name, config.start_url, config.domain, config.rules, config.type, config.mark])

    scheduler.start()
    scheduler.print_jobs()
    # db.close()


def modifyPrdTask(scheduler):
    print('检测待修改周期任务')
    # db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    # cursor = db.cursor()
    # cursor.execute("select * from prd_config where modify=1 and state='on';")
    # prdConfig = cursor.fetchall()
    prdConfig = select_prd_config(1, 'on')
    for taskConfig in prdConfig:
        # 置为无需修改
        update_prd_config(taskConfig.id, 0)
    #     cursor.execute("update prd_config SET modify = 0 WHERE id = %s ;", taskConfig[0])
    # db.commit()
    # db.close()

    for config in prdConfig:
        # 删除任务 重新添加
        if scheduler.get_job(config.id):
            scheduler.remove_job(config.id)
        print('进行周期任务修改')
        if config.prd == '每周':
            scheduler.add_job(addTask, 'cron', day_of_week=config.date, name=config.name,
                              args=[config.name, config.start_url, config.domain, config.rules, config.type])
        if config.prd == '每月':
            scheduler.add_job(addTask, 'cron', day=config.date, name=config.name,
                              args=[config.name, config.start_url, config.domain, config.rules, config.type])
        scheduler.print_jobs()


def funRound():
    timeN = datetime.now().strftime('%Y-%m-%d %H:%M')
    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()
    sql = "insert into sys_log (type, time, obj) VALUES (%s,%s,%s)"
    val = ("控制模块启动", timeN, 'pid:'+str(os.getpid()))
    cursor.execute(sql, val)
    db.commit()
    db.close()

    scheduler = BackgroundScheduler()

    initPrdTask(scheduler)

    while 1:
        sysInfo()

        startTask()

        startTest()

        # recoverTask()

        modifyPrdTask(scheduler)

        prdHistoryDel()

        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        print('==========轮询完成==========')

        time.sleep(10)


class MyTestDaemon(Daemon):
    def run(self):
        sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
        funRound()


if __name__ == '__main__':
    PIDFILE = '/tmp/daemon-example.pid'
    LOG = '/tmp/daemon-example.log'
    daemon = MyTestDaemon(pidfile=PIDFILE, stdout=LOG, stderr=LOG)

    if len(sys.argv) != 2:
        print('Usage: {} [start|stop]'.format(sys.argv[0]), file=sys.stderr)
        raise SystemExit(1)

    if 'start' == sys.argv[1]:
        daemon.start()
    elif 'stop' == sys.argv[1]:
        daemon.stop()
    elif 'restart' == sys.argv[1]:
        daemon.restart()
    else:
        print('Unknown command {!r}'.format(sys.argv[1]), file=sys.stderr)
        raise SystemExit(1)
