#/bin/bash 

uwsgi --http-socket 0.0.0.0:9080 --wsgi-file $HOME/__init__.py --callable app --processes 4 --threads 2 1>/tmp/uwsgi.log 2>/tmp/uwsgierr.log &
