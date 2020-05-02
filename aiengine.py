#-*-coding:utf8-*-
import sys
sys.path.append('/usr/Alexandria/')

from konlpy.tag import Mecab
mecab = Mecab()

from database import db_session
from models import Question

def predict(text):
    morphs = mecab.morphs(text)
    answer = None
    for element in morphs:
        answer = db_session.query(Question).filter(Question.answer_category == element).first()
        if(answer==None):
            answer = "응답이 준비되지 않았습니다."
        else:
            answer = answer.answer + "이고 " + answer.answer_detail
            break
    
    if(answer == None):
        answer="응답이 준비되지 않았습니다."

    return answer

if __name__ == '__main__':
    print(mecab.morphs("나는 천재가 아무래도 맞는것 같아."))
    print(predict("이 사이트 주인 이름이 뭐야?"))
    print("Hello world")
