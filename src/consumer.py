import pika
import time
from SQLAlchemy import *
from detect import *
def consumer():
    username = 'root'
    pwd = 'root'
    ip_addr = '127.0.0.1'
    port_num = 5672
    credentials = pika.PlainCredentials(username, pwd)
    connection = pika.BlockingConnection(pika.ConnectionParameters(ip_addr, port_num, '/', credentials, 10))
    channel = connection.channel()
    # 声明一个队列，生产者和消费者都要声明一个相同的队列，用来防止万一某一方挂了，另一方能正常运行
    channel.queue_declare(queue='hello3')


    def callback(ch, method, properties, body):
        # 将二进制比特流转换为字符串
        str1 = str(body, encoding="utf-8")

        # 将字符串转化为字典
        dict1 = eval(str1)

        # time.sleep(10)
        if gettaskid(dict1['taskId']):
            detect(dict1)
        else:
            print("任务不存在！")

        # yield a
        # 给mq发送应答信号，表明数据已经处理完成，可以删除
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # 监听随机队列，一旦有值出现，则触发回调函数：callback
    channel.basic_consume(on_message_callback=callback, queue='hello3', auto_ack=False)
    # while循环
    print(' [*] Waiting for messages. To exit press CTRL+C')

    channel.start_consuming()

consumer()