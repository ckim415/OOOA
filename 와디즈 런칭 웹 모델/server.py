from flask import Flask,request, url_for, render_template
import numpy as np
import random
import os
import datetime
# import tensorflow as tf

app = Flask(__name__)
# run_with_ngrok(app)

# 해당 페이지에선, 모델을 불러오고 그걸 통해 예측하는 것을 해볼거다.
# 예를 들어, 로이터 해보자.


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
      return render_template('index.html')
    if request.method == 'POST':
      # 파라미터를 전달 받습니다.
      X_data = str(request.form['X_data'])

      prediction_value = random.randrange(0,100)
      return render_template('index.html', prediction_value=prediction_value)
if __name__ == '__main__':    
  app.run(debug=True)
