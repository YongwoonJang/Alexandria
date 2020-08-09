#-*-coding:utf8-*-
from sqlalchemy import Table, Column, Integer, String, Text, DateTime
from database import Base

class Company(Base):
    __tablename__ = 'companys'
    id = Column(Integer, primary_key=True)
    corp_code = Column(String(8)) # Dart open api 회사 번호 ":"00258801",
    corp_name = Column(String(30)) # 정식 명칭 ":"(주)카카오",
    corp_name_eng = Column(String(30)) # 영문 명칭 ":"Kakao Corp.",
    stock_name = Column(String(30)) # 종목명(상장사) 또는 약식명칭(기타법인) ":"카카오",
    stock_code = Column(String(6)) # 상장회사인 경우 주식의 종목 코드 ":"035720",
    ceo_nm = Column(String(20)) # 대표자명 ":"여민수, 조수용",
    corp_cls = Column(String(1)) # 법인구분 : Y(유가), K(코스닥), N(코넥스), E(기타) ":"Y",
    jurir_no = Column(String(13), unique=True) # 법인등록번호 ":"1101111129497",
    bizr_no = Column(String(11), unique=True) # 사업자등록번호 ":"1208147521",
    adres = Column(String(30)) # 주소 ":"제주특별자치도 제주시 첨단로 242",
    hm_url = Column(String(30)) # 홈페이지 ":"www.kakaocorp.com",
    ir_url = Column(String(30)) # IR홈페이지 ":"",
    phn_no = Column(String(20)) # 전화번호 ":"02-6718-1082",
    fax_no = Column(String(20)) # 팩스번호 ":"02-6003-5401",
    induty_code = Column(String(5)) #업종코드 ":"63120",
    est_dt = Column(String(9)) #설립일 ":"19950216",
    acc_mt = Column(String(2)) #결산월 ":"12"
    mysql_character='utf8'

    def __init__(self, corp_code=None, corp_name=None, corp_name_eng=None, stock_name=None, stock_code=None, ceo_nm=None, corp_cls=None, jurir_no=None, bizr_no=None, adres=None, hm_url=None, ir_url=None, phn_no=None, fax_no=None, induty_code=None, est_dt=None, acc_mt=None):
        self.corp_code = corp_code
        self.corp_name = corp_name
        self.corp_name_eng = corp_name_eng
        self.stock_name = stock_name
        self.stock_code = stock_code
        self.ceo_nm = ceo_nm
        self.corp_cls = corp_cls
        self.jurir_no = jurir_no
        self.bizr_no = bizr_no
        self.adres = adres
        self.hm_url = hm_url
        self.ir_url = ir_url
        self.phn_no = phn_no
        self.fax_no = fax_no
        self.induty_code = induty_code
        self.est_dt = est_dt
        self.acc_mt = acc_mt

class Menu(Base):
    __tablename__ = 'menus'
    id = Column(Integer, primary_key=True)
    menu_name = Column(String(10)) # menu  이름 
    menu_content = Column(String(3000))
    def __init__(self, menu_name=None, menu_content=None):
        self.menu_name = menu_name
        self.menu_content = menu_content

class Question(Base):
    __tablename__ = 'question'
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(DateTime)
    question = Column(Text)
    answer_category = Column(String(20))
    answer = Column(Text) 
    answer_detail = Column(Text)

    def __init__(self, date=None, question=None, answer_category=None, answer=None, answer_detail=None):
        self.date = date
        self.question = question
        self.answer_category = answer_category
        self.answer = answer
        self.answer_detail = answer_detail

class Keyword(Base):
    __tablename__ = 'keyword'
    id = Column(Integer, primary_key=True)
    keyword = Column(String(20))
    answer = Column(Text)
    def __init__(self, keyword=None, answer=None):
        self.keyword = keyword
        self.answer = answer
