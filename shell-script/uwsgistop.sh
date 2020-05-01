#/bin/bash

kill -9 $(ps -ef | grep "uwsgi --http-socket" | awk '{print$2}')
