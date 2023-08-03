daemon:

    cd /root/Desktop/Python/flask/

	python3 daemon.py start

	cat /tmp/daemon-example.pid
	-> 8532

	ps -ef|grep 3889 | grep -v grep

	tail -f /tmp/daemon-example.log

	python3 daemon.py stop
	ps -ef|grep 8532 | grep -v grep



flask:

	cd /root/Desktop/Python/flask/
    nohup python3 app.py
	gunicorn -w 3 -b 0.0.0.0:8080 app:app
    gunicorn -w 3 -b 0.0.0.0:80 app:app
	ps -ef | grep python
	kill -9 pid


app

    cd /root/Desktop/Python/flask/

    python daemon.py start
    
