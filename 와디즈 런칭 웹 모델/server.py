
from flask import Flask,request, url_for, render_template
import numpy as np
import random
import datetime
from krwordrank.word import KRWordRank
from krwordrank.hangle import normalize
from konlpy.tag import Kkma, Hannanum, Komoran, Mecab, Okt
import re
from string import punctuation
from tensorflow.keras.models import load_model
from keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from flask_ngrok import run_with_ngrok
# import tensorflow as tf

app = Flask(__name__)
run_with_ngrok(app)  # 코랩일 경우 필요함.


model = load_model('model/text_process.h5')
# loading
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
      return render_template('index.html')
    if request.method == 'POST':

      # 파라미터를 전달 받습니다. 입력 데이터로 받은 값이 X_data에 담김. 
      X_data = str(request.form['X_data'])
      
      # 단어 전처리 과정을 거쳐야겠지? // 안해도됨
      # X_data = keyword(X_data)
      # X_data = noun(X_data)

      token = Tokenizer()

      # 문자열 정수 인덱스 리스트 출력
      # sequence의 길이를 20으로 통일. 제일 긴 단어 갯수가 20이라서.
      sequences = token.texts_to_sequences(X_data)
      padding_length = 10
      x_padded = pad_sequences(sequences, padding_length)

      prediction_value = format(model.predict(x_padded)[0][0]*100, ".2f")
      print('------>', prediction_value)

      return render_template('index.html', prediction_value= prediction_value)
if __name__ == '__main__':    
  app.run()

# 밑에 에러메시지 나온다. 그거 보고  해결하면 된다!!

