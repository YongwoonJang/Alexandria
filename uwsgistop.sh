#/bin/bash

kill -9 $(ps -ef | grep "uwsgi --socket" | awk '{print$2}')
