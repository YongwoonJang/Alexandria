<p align="center"><a href="http://14.63.173.117:8080/" target="_blank" rel="noopener noreferrer"><img width="250" src="https://github.com/YongwoonJang/Alexandria/blob/master/images/logo.png" alt="Alexandria logo"></a></p>

<p align="center"><a href="https://discord.gg/MzqWNVB"><img src="https://img.shields.io/discord/743041194631757906" alt="Chat"></a></p>

# Background
- Alexandria Library(Alexandria 도서관BC 323~283 경 프톨레마이오스 1세 때 세워진 도서관)을 따서 만든 프로젝트 이름입니다.
- YongwoonJang(1989.01.29 ~ )의 지식정보를 관리하는 체계를 구축하기 위해 시작했습니다. 
- 향후 세상의 모든 정보를 원하는 모든 사람들이 조회할 수 있게 만드는 것이 목표입니다. 

# Service
- 데이터를 쉽게 수집하고 수집된 데이터를 바탕으로 검색 기능을 제공합니다.

# How to use
- 서버 1대에 WAS를 구성하고, source "Path/to/git_clone_location"/venv/bin/activate 로 환경 전환후, script 폴더에 존재하는 uwsgistart.sh를 사용한다. 

# Maintainer 
- 매 주 토, 일 수행 
- 담당자 : 장용운(royalfamily89@gmail.com)

# Project history
- 2020.05.03 10:46 : 단어 사전 기반조회

# Knowledges
## 프로그램 언어
- python == 3.8.2

## WAS(Web application server/DB와 의사소통하여 웹 응답처리) 구성
- uwsgi == 2.0.18
- flask == 1.1.2 

## 챗봇이 입력을 받는 부분 - 형태소 분석기 
- konlpy == 0.5.2

## DATABASE 구성 
- mariadb == 10.4.12 

## Docker 구성
- docker == 19.03.8
- docker URL == https://hub.docker.com/repository/docker/royalfamily89/alexandria

# Code Convention
## Python
- https://visualgit.readthedocs.io/en/latest/pages/naming_convention.html 의 내용을 따릅니다.  
