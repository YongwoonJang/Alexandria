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
        question.append(mecab.morphs(text))
        text_sequence = self.tokenizer.texts_to_sequences(question)
        if(len(text_sequence[0]) == 0):
            text_sequence[0].append(0) # set default value
        response_sequence = self.model.predict(text_sequence)

        # search based on word
        for element in question[0]:
            answer = db_session.query(Question).filter(Question.answer_category == element).first()
            if(answer==None):
                answer = "응답이 준비되지 않았습니다."
            else:
                answer = "범주는 "+answer.answer_category+"입니다. "+"현재 말할 수 있는 답은 " + answer.answer + "이고 " + answer.answer_detail
                break
        
        if(answer == None):
            answer="응답이 준비되지 않았습니다."
        
        print(answer)
        return answer


if __name__ == '__main__':
    school = School()    
    #school.update_tokenizer()
    #school.create_model()
    #school.learn()
    school.predict("이름이 뭐야")
    print("Hello world")
