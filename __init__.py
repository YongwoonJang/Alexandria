#-*-coding:utf8-*-
from flask import Flask
from flask import render_template
app = Flask(__name__)

import sys

sys.path.append('/usr/local/')
from alexandria.models import Company
from alexandria.database import db_session
from alexandria.database import init_db # database를 Init 할때 사용함.

from sqlalchemy import text

@app.route('/')
def index():
    ## 카카오톡을 return
    company = db_session.query(Company).filter(Company.corp_code == "00258801").all()
    print(type(company))
    companys = []
    for element in company:
        companys.append(element.__dict__)
    print(companys)#list로 등록된 회사를 출력한다.
    return render_template('index.html', companys=companys)

@app.teardown_appcontext 
def shutdown_session(exception=None):
    db_session.remove()

def init_database():
    init_db()

def add_company(corp_code=None, corp_name=None, corp_name_eng=None, stock_name=None, stock_code=None, ceo_nm=None, corp_cls=None, jurir_no=None, bizr_no=None, adres=None, hm_url=None, ir_url=None, phn_no=None, fax_no=None, induty_code=None, est_dt=None, acc_mt=None):
    c = Company(corp_code, corp_name, corp_name_eng, stock_name, stock_code, ceo_nm, corp_cls, jurir_no, bizr_no, adres, hm_url, ir_url, phn_no, fax_no, induty_code, est_dt, acc_mt)
    db_session.add(c)
    db_session.commit()


if __name__ == '__main__':
    print("Hello world")
    #init_db()
    #add_company("00258801","(주)카카오","Kakao Corp","카카오","035720","여민수,조수용","Y","1101111129497","12081475211","제주특별자치도 제주시 첨단로 242","www.kakaocorp.com","","02-6718-1082","02-6003-5401","63120","19950216","12")
    index()
