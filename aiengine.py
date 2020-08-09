#-*-coding:utf8-*-
import sys
sys.path.append('/usr/Alexandria/')

from os import path 

import json
import numpy as np

from konlpy.tag import Mecab
mecab = Mecab()

from database import db_session
from models import Question
from sqlalchemy import text
from sqlalchemy import or_

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.text import tokenizer_from_json
from tensorflow.keras.preprocessing import sequence
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Activation
from tensorflow.keras.layers import Embedding
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Conv1D, MaxPooling1D
from tensorflow.keras.models import load_model

from sklearn.model_selection import train_test_split

class School:
    def __init__(self):
        self.tokenizer_path = "./tokenizer/tokenizer.json"
        self.checkpoint_path = "./model/cp.ckpt"
        self.model_path = "./model/model.h5"
        self.max_features = 1000
        self.maxlen = 100 # 학습할때 참조할 문장단 문자 갯수를 정의한다. 

        stmt = text("select question, answer, answer_category from question")
        stmt = stmt.columns(Question.question, Question.answer, Question.answer_category)
        self.question = db_session.query(Question.question, Question.answer, Question.answer_category).from_statement(stmt).all()


        if(path.exists(self.tokenizer_path)):
            with open(self.tokenizer_path) as handle:
                self.tokenizer = tokenizer_from_json(json.load(handle))
        else:
            self.tokenizer = update_tokenizer(init=True)

        if(path.exists(self.model_path)):
            self.model = load_model(self.model_path)
        else:
            self.model = self.create_model()
            self.learn()

    def update_tokenizer(self, init=False, **kwargs):
        if(init == True):
            tokenizer = Tokenizer(num_words = self.max_features)        
        elif(init == False):
            with open(self.tokenizer_path) as handle:
                tokenizer = tokenizer_from_json(json.load(handle))

        questions = []
        answers = []
        answer_categories = []
        for element in self.question:
            questions.append(mecab.morphs(element.question))
            if(element.answer != None):
                answers.append(mecab.morphs(element.answer))
                answer_categories.append(mecab.morphs(element.answer_category))
            else:
                answers.append("없음")
                answer_categories.append("없음")
        
        tokenizer.fit_on_texts(questions)
        tokenizer.fit_on_texts(answers)
        tokenizer.fit_on_texts(answer_categories)

        with open(self.tokenizer_path, "w", encoding="utf-8") as handle:
            json.dump(tokenizer.to_json(),handle)
        
        return tokenizer

    def create_model(self):
        model = Sequential()
        model.add(Embedding(input_dim=self.max_features, output_dim=64, input_length=self.maxlen))
        model.add(Dropout(0.25))
        #model.add(Conv1D(filters = 64, 
        #    kernel_size = 5, 
        #    padding="valid", 
        #    activation="relu",
        #    strides=1))
        #model.add(MaxPooling1D(pool_size=3))
        model.add(LSTM(self.maxlen))
        model.add(Dense(1))
        model.add(Activation("softmax"))
        model.compile(loss='binary_crossentropy',
                optimizer='adam',
                metrics=['accuracy'])
        model.summary()
        return model

    def learn(self): 
        questions = []
        answer_categories = []
        for element in self.question:
            questions.append(mecab.morphs(element.question))
            if(element.answer_category != None):
                answer_categories.append(mecab.morphs(element.answer_category))
            else:
                answer_categories.append("없음")
        
        sequence_questions = self.tokenizer.texts_to_sequences(
                questions
        )
        sequence_answer_categories = self.tokenizer.texts_to_sequences(
                answer_categories
        )
        
        sequence_questions = sequence.pad_sequences(sequence_questions, maxlen=self.maxlen)
        sequence_answer_categories = sequence.pad_sequences(sequence_answer_categories, maxlen=self.maxlen)
        
        X_train, X_test, y_train, y_test = train_test_split(sequence_questions,
                sequence_answer_categories,
                test_size=0.2,
                shuffle=False,
                random_state=1)

        self.model.fit(X_train, 
                y_train,
                epochs=5,
                validation_data=(X_test, y_test),
                verbose=1)
       
        self.model.save(self.model_path)

    def predict(self, text):
        question = []
        
        if ( text == "수정" ) : 
            answer = "<table>"
            
            answer = answer + "<thead><tr>"
            for element in Question.__table__.columns.keys() :
                print(element)
                answer = answer + "<th>" + element + "</th>"
            answer = answer + "</tr></thead>"
        
            answer = answer + "<tbody>"
            for element in db_session.query(Question).all():
                answer = answer + "<tr><td>" + str(element.id) + "</td>"
                answer = answer + "<td>" + str(element.date) + "</td>"
                answer = answer + "<td>" + str(element.question) + "</td>"
                answer = answer + "<td>" + str(element.answer_category) + "</td>"
                answer = answer + "<td>" + str(element.answer) + "</td>"
                answer = answer + "<td>" + str(element.answer_detail) + "</td></tr>"
            answer = answer + "</tbody>"
            
            answer = answer + "</table>"

        else:
            print( "else" )
            print(text)
            question.append(mecab.morphs(text))
            text_sequence = self.tokenizer.texts_to_sequences(question)
            print(text_sequence)

            if(len(text_sequence[0]) == 0):
                text_sequence[0].append(0) # set default value
            response_sequence = self.model.predict(text_sequence)
            print(response_sequence[0])
            
            if(response_sequence[0] != 1.0):
                answer = db_session.query(Question).filter(Question.answer_category == response_sequence[0]).first()
                answer = "범주는 "+answer.answer_category+"입니다. "+"현재 말할 수 있는 답은 " + answer.answer + "이고 " + answer.answer_detail
            
            else:
                hit_point = []
                
                ## It need to revise. because It dosen't count Son's Name in question #342
                ## Concept is counting morphemes by comparing input value with answer_category and answer
                for element in question[0]:
                    print("***question[0]'s elements are***")
                    print(element)
                    count = db_session.query(Question).filter(Question.answer_category == element).count()
                    answer_list = db_session.query(Question.answer)
                    for answer in answer_list:
                        if answer[0] != None :
                            answer_morphs_list = mecab.morphs(answer[0])
                            for answer_morphs in answer_morphs_list:
                                if ( answer_morphs == element ):
                                    count = count + 1
                    print("***count per element****")
                    print(count)
                    if ( count > 0 ) :
                        print("****count is executing****")
                        answer_list = db_session.query(Question).filter(or_(Question.answer_category == element, Question.answer.ilike('%'+element+'%'))).all()
                        index = 0

                        for answer_record in answer_list:
                            hit_point.append(0)
                            
                            print("Answer is")
                            for temp in mecab.morphs(answer_record.answer): #Answer 
                                if(index == 3):
                                    print("**answer comparing**")
                                    print(temp)
                                    print(element)
                                if ( temp == element ):
                                    print(temp)
                                    hit_point[index] = hit_point[index] + 1
                            
                            print("Answer detail is")
                            for temp in mecab.morphs(answer_record.answer_detail): #Answer_detail
                                if ( index == 3 ):
                                    print("**answer_detail comparing**")
                                    print(temp)
                                    print(element)
                                if ( temp == element ):
                                    print(temp)
                                    hit_point[index] = hit_point[index] + 1 
                            
                            index = index + 1
                        
                if len(hit_point) > 0 :
                    answer_index = 0
                    print("***hit_point is***")
                    print(hit_point)
                    for hit_index in range(0, len(hit_point)-1):
                        if ( hit_point[hit_index] < hit_point[hit_index+1] ) :
                            answer_index = hit_index + 1
                
                    answer = "범주는 "+answer_list[answer_index].answer_category+"입니다. "+"현재 말할 수 있는 답은 " + answer_list[answer_index].answer + "이고 " + answer_list[answer_index].answer_detail
                    print(answer)
                        
                else:
                    answer = "응답이 준비되지 않았습니다."

        return answer

if __name__ == '__main__':
    school = School()    
    #school.update_tokenizer()
    #school.create_model()
    #school.learn()
    school.predict("손경준의 이름은 뭐야")
    print("Hello world")
