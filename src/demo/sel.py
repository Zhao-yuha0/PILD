import pika
import redis, time

# r = redis.Redis(host='localhost', port=6379, decode_responses=True)
#
#
#
# r.lpush('slave1', 'https://www.cnblogs.com/xtt-w/p/6085646.html')
# r.lpush('slave1', 'http://cstc.hrbeu.edu.cn/bzrgz/list.htm')
# r.lpush('slave1', 'https://blog.csdn.net/lh_python/article/details/79704102')
# r.lpush('slave1', 'https://www.jianshu.com/p/63dad93d7000')
# r.lpush('slave1', 'https://www.8684.cn/today_d0106')
#
#
#
# # r.lpush('slave1', 'https://www.cnblogs.com/xtt-w/p/6085646.html')

body = 'https://www.cnblogs.com/xtt-w/p/6085646.html'

username = 'root'
pwd = 'root'
ip_addr = '127.0.0.1'
# ip_addr = '192.168.102.201'
# ip_addr = '82.156.107.90'

port_num = 5672
credentials = pika.PlainCredentials(username, pwd)
connection = pika.BlockingConnection(pika.ConnectionParameters(ip_addr, port_num, '/', credentials, 10))

channel = connection.channel()
channel.queue_declare(queue='hello3', durable=False)
channel.basic_publish(exchange='', routing_key='hello3', body=body)
channel.confirm_delivery()
print("[x] Sent %s" % body)
connection.close()
