#/bin/bash

apt-get update
apt-get install locales
apt-get install python3-pip
apt-get install vim
apt-get install mysql-client
apt-get install build-essential
apt-get install python3-dev
apt-get install libmysqlclient-dev

#for AI
apt-get install g++ openjdk-8-jdk python3-dev python3-pip curl
apt-get install python3-bs4
pip3 -m pip install konlpy
bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)

