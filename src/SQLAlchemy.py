from sqlalchemy import Column, INTEGER, String, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import pymysql
from sqlalchemy import and_

engine = create_engine('mysql+pymysql://root:""@localhost:3306/contest?charset=utf8')
# con=connect()
# Base = declarative_base(con)
HOST_NAME = '127.0.0.1'  # 数据库所在服务器ip,因为我是本地数据库所以这里是127.0.0.1
HOST_PORT = '3306'  # 数据库端口
DATABASE_NAME = 'ConTest'  # 数据库名
USER_NAME = 'root'  # 链接数据的用户名
PWD = '123456'  # 链接数据库的密码
DB_URI = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}?charset=utf8'.format(USER_NAME, PWD, HOST_NAME, HOST_PORT,
                                                                   DATABASE_NAME)
engine = create_engine(DB_URI)
Base = declarative_base(engine)


# 创建规则表
class rule(Base):
    # 创建数据库表
    __tablename__ = 'rule'  # 表名
    name = Column(String(100), primary_key=True)  # id字段，主键，自增
    content = Column(String(500), nullable=False)  # 用户名字段
    value = Column(String(100), nullable=False)  # 用户名字段

    def __repr__(self):
        """定义数据库查询返回的数据格式"""
        return 'rule(name="%s",content="%s",value="%s")' % (self.name, self.content, self.value)


class prd_config(Base):
    __tablename__ = 'prd_config'  # 表名
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # id字段，主键，自增
    name = Column(String(64), nullable=False)
    state = Column(String(32), nullable=False)
    type = Column(String(32), nullable=False)
    prd = Column(String(64), nullable=False)
    date = Column(INTEGER, nullable=False)
    start_url = Column(String(200), nullable=False)
    domain = Column(String(64), nullable=False)
    rules = Column(String(200), nullable=False)
    last_time = Column(String(64), nullable=False)
    modify = Column(String(32), nullable=False)
    mark = Column(String(200), nullable=False)

    def __repr__(self):
        """定义数据库查询返回的数据格式"""
        return 'prd_config(id="%d",name="%s",state="%s",type="%s",prd="%s",date="%d",star_url="%s",domain="%s",rules="%s",last_time="%s"' \
               'modify="%s",mark="%s")' % (
               self.id, self.name, self.state, self.type, self.prd, self.date, self.start_url, self.domain, self.rules
               , self.last_time, self.modify, self.mark)


# 创建周期任务检测历史表
class prd_history(Base):
    __tablename__ = 'prd_history'  # 表名
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # id字段，主键，自增
    name = Column(String(64), nullable=False)
    task_id = Column(INTEGER, ForeignKey('prd_config.id'), nullable=False)
    url = Column(String(200), nullable=False)
    time = Column(String(64), nullable=False)
    # #声明relationship，注意prd_config不是字段，是关系，不能用于字段检索。是在query后，对应1条记录的对象中存在
    prd_config = relationship('prd_config', backref=('prd_history'))

    def __repr__(self):
        """定义数据库查询返回的数据格式"""
        return 'prd_history(id="%d",task_id="%d",url="%s",time="%s")' % (self.id, self.task_id, self.url, self.time)


# 待执行任务表
class task_wait(Base):
    __tablename__ = 'task_wait'  # 表名
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # id字段，主键，自增
    name = Column(String(32), nullable=False)
    add_time = Column(String(64), nullable=False)
    start_url = Column(String(200), nullable=False)
    domain = Column(String(32), nullable=False)
    rules = Column(String(200), nullable=False)
    type = Column(String(32), nullable=False)
    mark = Column(String(32), nullable=False)

    def __repr__(self):
        """定义数据库查询返回的数据格式"""
        return 'task_wait(id="%s",name="%s",add_time="%s",start_url="%s",domain="%s",rules="%s",type="%s",mark="%s")' % (
        self.id, self.name, self.add_time,
        self.start_url, self.domain, self.rules, self.type, self.mark)


# 执行任务表(task_list)
class task_list(Base):
    __tablename__ = 'task_list'  # 表名
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # id字段，主键，自增
    name = Column(String(64), nullable=False)
    start_url = Column(String(200), nullable=False)
    domain = Column(String(64), nullable=False)
    rules = Column(String(200), nullable=False)
    state = Column(String(32), nullable=False)
    spider = Column(String(64), nullable=False)
    type = Column(String(32), nullable=False)
    start_time = Column(String(64), nullable=False)
    end_time = Column(String(64), nullable=False)
    page = Column(INTEGER, nullable=False)
    count = Column(INTEGER, nullable=False)
    pid = Column(INTEGER, nullable=False)
    red = Column(INTEGER, nullable=False)

    def __repr__(self):
        """定义数据库查询返回的数据格式"""
        return 'task_list(id="%s",name="%s",start_url="%s",domain="%s",rules="%s",states="%s",spider="%s",' \
               'type="%s",start_time="%s",end_time="%s",page="%s",count="%s",pid="%s",red="%s")' % (self.id, self.name,
                                                                                                    self.start_url,
                                                                                                    self.domain,
                                                                                                    self.rules,
                                                                                                    self.state,
                                                                                                    self.spider,
                                                                                                    self.type,
                                                                                                    self.start_time,
                                                                                                    self.end_time,
                                                                                                    self.page,
                                                                                                    self.count,
                                                                                                    self.pid, self.red)


# # #检测结果表(task_result)
class task_result(Base):
    __tablename__ = 'task_result'  # 表名
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # id字段，主键，自增
    task_id = Column(INTEGER, ForeignKey('task_list.id'), nullable=False)
    name = Column(String(64), nullable=False)
    task_type = Column(String(64), nullable=False)
    rules = Column(String(200), nullable=False)
    content = Column(String(200), nullable=False)
    time = Column(String(200), nullable=False)
    url = Column(String(1000), nullable=False)
    task_list = relationship('task_list', backref=('task_result'))

    def __repr__(self):
        return 'task_result(id="%s",task_id="%s",name="%s",task_type="%s",rules="%s",states="%s",content="%s",' \
               'time="%s",url="%s")' % (self.id, self.name, self.start_url, self.domain, self.rules, self.states,
                                        self.spider, self.start_time, self.end_time, self.page, self.count)


# risk_level
class risk_level(Base):
    __tablename__ = 'risk_level'  # 表名
    id = Column(INTEGER, primary_key=True, autoincrement=True)  # id字段，主键，自增
    url = Column(String(3200), nullable=False)
    task_id = Column(INTEGER, ForeignKey('task_list.id'), nullable=False)
    name = Column(String(64), nullable=False)
    time = Column(String(64), nullable=False)
    level = Column(String(32), nullable=False)
    content = Column(String(3200), nullable=False)

    # task_list=relationship('task_list',backref=('risk_level'))
    def __repr__(self):
        return 'risk_level(id="%s",url="%s",task_id="%s",name="%s",time="%s",level="%s",content="%s")' % (self.id,
                                                                                                          self.url,
                                                                                                          self.task_id,
                                                                                                          self.name,
                                                                                                          self.time,
                                                                                                          self.level,
                                                                                                          self.content)


# test_list
class test_list(Base):
    __tablename__ = 'test_list'  # 表名
    type = Column(String(32), primary_key=True, nullable=False)
    rules = Column(String(64), primary_key=True, nullable=False)
    url = Column(String(64), primary_key=True, nullable=False)
    add_time = Column(String(32), primary_key=True, nullable=False)

    def __repr__(self):
        return 'test_list(type="%s",rules="%s",url="%s",add_time="%s")' % (self.type,
                                                                           self.rules, self.url, self.add_time)


# test_result
class test_result(Base):
    __tablename__ = 'test_result'  # 表名
    rule = Column(String(32), primary_key=True, nullable=False)
    content = Column(String(200), primary_key=True, nullable=False)
    page = Column(INTEGER, primary_key=True, nullable=False)
    count = Column(INTEGER, primary_key=True, nullable=False)
    url = Column(String(200), primary_key=True, nullable=False)

    def __repr__(self):
        return 'test_result(rule="%s",content="%s",page="%s",count="%s",url="%s")' % (self.rule,
                                                                                      self.content, self.page,
                                                                                      self.count, self.url)


# sys_info
class sys_info(Base):
    __tablename__ = 'sys_info'  # 表名
    start_time = Column(String(64), primary_key=True, nullable=False)
    task_count = Column(INTEGER, primary_key=True, nullable=False)
    task_total = Column(INTEGER, primary_key=True, nullable=False)
    cpu_percent = Column(INTEGER, primary_key=True, nullable=False)
    storage_total = Column(INTEGER, primary_key=True, nullable=False)
    storage_used = Column(INTEGER, primary_key=True, nullable=False)
    memory_total = Column(INTEGER, primary_key=True, nullable=False)
    memory_used = Column(INTEGER, primary_key=True, nullable=False)
    net_sent_M = Column(INTEGER, primary_key=True, nullable=False)
    net_recv_M = Column(INTEGER, primary_key=True, nullable=False)

    def __repr__(self):
        return 'sys_info(start_time="%s",task_count="%s",task_total="%s",cpu_percent="%s",' \
               'storage_total="%s",storage_used="%s",memory_total="%s",' \
               'meeory_used="%s",net_sent_M="%s",net_recv_M="%s"' \
               ')' % (self.start_time, self.task_count, self.task_total, self.cpu_percent,
                      self.storage_total, self.storage_used, self.memory_total, self.meeory_used,
                      self.net_sent_M, self.net_recv_M)


# user
class user(Base):
    __tablename__ = 'user'  # 表名
    account = Column(INTEGER, primary_key=True, nullable=False)
    pwd = Column(INTEGER, nullable=False)
    auth = Column(String(32), nullable=False)
    deny = Column(String(32), nullable=False)

    def __repr__(self):
        return 'user(account="%s",pwd="%s",auth="%s")' % (self.account, self.pwd, self.auth)


# spiders
class spiders(Base):
    __tablename__ = 'spiders'  # 表名
    name = Column(String(64), primary_key=True, nullable=False)
    state = Column(String(64), nullable=False)
    current_task_id = Column(INTEGER, nullable=False)
    type = Column(String(64), nullable=False)

    def __repr__(self):
        return 'spiders(name="%s",state="%s",current_task_id="%s",type="%s")' % (
        self.name, self.state, self.current_task_id, self.type)


# user_log
class user_log(Base):
    __tablename__ = 'user_log'  # 表名
    id = Column(INTEGER, primary_key=True, nullable=False)
    type = Column(String(64), nullable=False)
    obj = Column(String(64), nullable=False)
    time = Column(String(64), nullable=False)
    account = Column(String(64), nullable=False)

    def __repr__(self):
        return 'user_log(id="%s",type="%s",obj="%s",time="%s",account="%s")' % (self.id, self.type,
                                                                                self.obj, self.time, self.account)


# sys_log
class sys_log(Base):
    __tablename__ = 'sys_log'  # 表名
    id = Column(INTEGER, primary_key=True, nullable=False)
    type = Column(String(64), nullable=False)
    time = Column(String(64), nullable=False)
    obj = Column(String(64), nullable=False)

    def __repr__(self):
        return 'sys_log(id="%s",type="%s",time="%s",obj="%s")' % (self.id, self.type, self.time, self.obj)


# Base.metadata.create_all()
Base.metadata.create_all()
Session = sessionmaker(engine)
session = Session()


# delete_data = session.query(prd_history).filter(prd_history.time =='1').first
# session.delete(delete_data)
# session.commit()
# session.close()
# panda=rule(name='2',content='2')
# session.add(panda)
# session.commit()

# *********************************************
# 插入操作
# def insert_rule(name,content):
#     panda = rule(name=name, content=content)
#     session.add(panda)
#     session.commit()

# 325 and 343
def insert_task_wait(name, add_time, start_url, domain, rules, type):
    data = task_wait(name=name, add_time=add_time, start_url=start_url, domain=domain, rules=rules, type=type)
    session.add(data)
    session.commit()
    session.close()


# task_result表新增
def insert_task_result(url, time, task_id, name, task_type, rules, content):
    data = task_result(task_id=task_id, name=name, task_type=task_type, rules=rules, content=content, time=time,
                       url=url)
    session.add(data)
    session.commit()
    session.close()


def insert_risk_level(url, id, time, name, level, res):
    data = risk_level(url=url, task_id=id, name=name, time=time, level=level, content=str(res))
    session.add(data)
    session.commit()
    session.close()


# ***********************************************

# ***********************************************
# 删除操作
# 175
def delete_prd_history(timeStr):
    delete_data = session.query(prd_history).filter(prd_history.time < timeStr).delete(synchronize_session=False)
    session.commit()
    session.close()


# 240
def delete_task_wait(taskID):
    delete_data = session.query(task_wait).filter(task_wait.id == taskID).first()
    session.delete(delete_data)
    session.commit()
    session.close()


# 258
# def delete_test():
#     delete_data=session.query(test).delete(synchronize_session=False)

# 328
def delete_task_list(task):
    delete_data = session.query(task_list).filter(task_list.id == task).first()  # 返回查找对象的所有的数据，组成一个列表
    session.delete(delete_data)
    session.commit()
    session.close()


# ************************************************

# ************************************************
# 查询操作
# def select_spiders(free,taskType):
# select_data = session.query(spiders).filter(and_(state==free,type==taskType))  # 返回查找对象的所有的数据，组成一个列表
###注意这个为字典类型，可能需要转化为元组，因为赵宇浩那边是元组
# 188
def select_spiders(state, type):
    select_data = None
    select_data0 = session.query(spiders).filter(and_(spiders.state == state, spiders.type == type)).all()
    if select_data0:
        select_data = select_data0[0]
    session.commit()
    return select_data


# 205
def select_rule():
    select_data = session.query(rule).all()
    session.commit()
    return select_data


# 225
def select_task_wait():
    result = session.query(task_wait).all()
    session.commit()

    return result


# 256 (test数据库表格删除了 暂时不需要用)
# def select_test(test):
#     result=session.query(test).all()
#     session.commit()
#     session.close()
#     return result
#
# 296
def select_task_list(task_list, running):
    result = session.query(task_list).filter(task_list.state == running).all()
    # print(result)
    session.commit()
    return result


# select_task_list(task_list,'running')
# 353  TypeError: %d format: a number is required, not str
def select_prd_config_state(prd_config, on):
    result = session.query(prd_config).filter(prd_config.state == on).all()
    session.commit()
    return result


# select_prd_config_state(prd_config,'on')


# 373 TypeError: %d format: a number is required, not str
def select_prd_config(modify, on):
    result = session.query(prd_config).filter(and_(prd_config.modify == modify, prd_config.state == on)).all()
    session.commit()
    return result


# select_prd_config('fdf','on')

# **********************************************
# #更新操作
# 330
def update_spiders(spiderName, state):
    # # cursor.execute("update spiders SET state='free' WHERE name = %s", spiderName)
    res = session.query(spiders).filter(spiders.name == spiderName).all()[0]
    res.state = state
    session.commit()
    session.close()


# 检测到一个泄露信息就在task_list内对应taskid的任务count自增1
def update_count(id):
    res = session.query(task_list).filter(task_list.id == id).all()[0]
    # print(type(res.count))
    res.count += 1

    session.commit()
    session.close()


def update_red(id):
    res = session.query(task_list).filter(task_list.id == id).all()[0]
    # print(type(res.count))
    if res.red:
       res.red+=1
    else:
       res.red=1



    session.commit()
    session.close()


# 378
def update_prd_config(taskConfig, modify):
    res = session.query(prd_config).filter(prd_config.id == taskConfig).all()[0]
    res.modify = modify
    session.commit()
    session.close()


# 141
def update_sys_info(timeStart, taskCount, task_total, cpuPercent, storeTotal, storeUsed, memoryTotal, memoryUsed, netR,
                    netS):
    res = session.query(sys_info).all()[0]
    res.start_time = timeStart
    res.task_count = taskCount
    res.task_total = task_total
    res.cpu_percent = cpuPercent
    res.storage_total = storeTotal
    res.storage_used = storeUsed
    res.memory_total = memoryTotal
    res.memory_used = memoryUsed
    res.net_sent_M = netR
    res.net_recv_M = netS
    session.commit()
    session.close()


# update_sys_info(1,2,3,4,5,6,4,4,7,5)
def gettaskid(id):
    res = session.query(task_list).filter(task_list.id == id).all()

    session.commit()
    session.close()
    return res

def getrule():
    db = pymysql.connect(user="root", passwd="123456", db="ConTest")
    cursor = db.cursor()

    cursor.execute("select * from rule ;")

    rules = cursor.fetchall()

    ruledict = dict()
    for item in rules:
        ruledict['{}'.format(item[0])] = item[1]
        # ruleList.append(ruleDict)

    # data = ruleList

    return ruledict
