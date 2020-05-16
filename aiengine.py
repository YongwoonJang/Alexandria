#-*-coding:utf8-*-
import sys
sys.path.append('/usr/Alexandria/')

from os import path 

import json

from konlpy.tag import Mecab
mecab = Mecab()

from database import db_session
from models import Question
from sqlalchemy import text


from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import tokenizer_from_json

from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Conv1D, MaxPooling1D

class School:
    def __init__(self):
        self.tokenizer_path = "./tokenizer/tokenizer.json"
        if(path.exists(self.tokenizer_path)):
            with open(self.tokenizer_path) as handle:
                self.tokenizer = tokenizer_from_json(json.load(handle))
        else:
            self.tokenizer = make_tokenizer(init=True)

    def make_tokenizer(self, init=False, **kwargs):
        if(init == True):
            tokenizer = Tokenizer(num_words = 100)        
        elif(init == False):
            with open("./tokenizer/tokenizer.json") as handle:
                tokenizer = tokenizer_from_json(json.load(handle))

        stmt = text("select question, answer, answer_category from question")
        stmt = stmt.columns(Question.question, Question.answer, Question.answer_category)
        question = db_session.query(Question.question, Question.answer, Question.answer_category).from_statement(stmt).all()

        questions = []
        answers = []
        answer_categorys = []
        for element in question:
            questions.append(mecab.morphs(element.question))
            if(element.answer != None):
                answers.append(mecab.morphs(element.answer))
                answer_categorys.append(mecab.morphs(element.answer_category))
            else:
                answers.append("없음")
                answer_categorys.append("없음")
        
        tokenizer.fit_on_texts(questions)
        tokenizer.fit_on_texts(answers)
        tokenizer.fit_on_texts(answer_categorys)

        with open("./tokenizer/tokenizer.json", "w", encoding="utf-8") as handle:
            json.dump(tokenizer.to_json(),handle)
        
        return tokenizer

    def make_model(self, sequence_questions, sequence_answers, sequence_answer_categorys):
        print(0)

    def learn():
        print(0)

    def predict(self, text):
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
    school = School()    
    school.make_tokenizer()
    print("Hello world")
