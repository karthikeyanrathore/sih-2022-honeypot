#!/usr/bin/env python3
import os
import uuid
from flask import (
    Flask, flash, request, redirect,
    render_template)

#from secure import enc, dec, get_key
from spt import speech_to_text, check_final, processing
UPLOAD_FOLDER = 'WAV'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def home():
  return render_template('home.html')

@app.route('/record' , methods=['POST', 'GET']) 
def root():
  result = None
  scam = None
  if request.method == 'POST':
    if "get" in request.form:
      result = predict()
      scam = predict_scam()
      print(result)
    return render_template('index.html', result=result, scam=scam)
  else:
    return render_template('index.html', result=result, scam=scam)

@app.route('/save-record', methods=['POST'])
def save_record():
  if 'file' not in request.files:
    flash('No file part')
    return redirect(request.url)
  file = request.files['file']
  if file.filename == '':
    flash('No selected file')
    return redirect(request.url)
  file_name = str(uuid.uuid4()) + ".wav"
  full_file_name = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
  file.save(full_file_name)
  #enc(full_file_name, get_key())
  return '<h1>Success</h1>'

def feature_extract(path):
  # decrypt sound
  #dec(path, get_key())
  final_arr=[]
  mfcc=librosa.feature.mfcc(librosa.load(path)[0],n_mfcc=13)
  mfcc_delta=librosa.feature.delta(mfcc, order=1)
  mfcc_delta_delta=librosa.feature.delta(mfcc, order=2)
  final_arr.append((np.mean(mfcc,axis=1),np.mean(mfcc_delta,axis=1),np.mean(mfcc_delta_delta,axis=1)))
  return final_arr    

def normalize(excel,final_arr):
    df=pd.read_csv(excel)
    mean=df["0"].values
    std=df["1"].values
    for i in range(len(final_arr)):
        final_arr[i]=(final_arr[i]-mean[i])/std[i]
    return final_arr

# angry-0, neutral-1, disgust-2, sad-3, fear-4, happy-5, ps-6
def result(model,final_arr):
  with open(model,'rb') as f:
    clf = pickle.load(f)
  prediction=clf.predict(final_arr)
  
  if prediction==0:
    return "angry"
  elif prediction==1:
    return "neutral"
  elif prediction==2:
    return "disgust"
  elif prediction==3:
   return "sad"
  elif prediction==4:
    return "fear"
  elif prediction==5:
    return "happy"
  else:
   return "surprised"

def important(arr):
  big_arr=[]
  for i in arr:
    for j in i:
      for k in j:
        big_arr.append(k)
  return big_arr


import glob
import os
import librosa # 0.8.1
import pickle   
import numpy as np # 1.20.1
import pandas as pd # 1.3.1
def predict():
  files = glob.glob('WAV/*')
  latest = max(files, key=os.path.getctime)
  print(latest)
  #enc(latest, get_key())
  arr=feature_extract(latest)
  arr=important(arr)
  arr=normalize("../model/normalize.csv",arr)
  arr.insert(0,0)
  arr=np.array(arr)
  arr=arr.reshape(1, -1)
  arr.shape
  print("modelout: ", result("../model/svm_tess",arr))
  return result("../model/svm_tess",arr)

def predict_scam():
  files = glob.glob('WAV/*')
  latest = max(files, key=os.path.getctime)
  try:
    text_arr = speech_to_text(latest)
    text_arr = processing(text_arr)
    return check_final(text_arr)
  except:
    return  "not indentifying"

@app.route("/upload", methods=["GET", "POST"])
def upload():
  get=None
  scam=None
  if request.method == "POST":
    sound = request.files['sound']
    path = os.path.join(app.config['UPLOAD_FOLDER'], sound.filename)
    sound.save(path)
    # encrypt sound
    #enc(path, get_key())
    arr=feature_extract(path)
    try:
      text_arr=speech_to_text(path)
      text_arr=processing(text_arr)
      scam = check_final(text_arr)
    except:
      scam = "not indentifying"
    arr=important(arr)
    arr=normalize("../model/normalize.csv",arr)
    arr.insert(0,0)
    arr=np.array(arr)
    arr=arr.reshape(1, -1)
    arr.shape
    print("modelout: ", result("../model/svm_tess",arr))
    get = result("../model/svm_tess",arr)
    print(get)
    return render_template("upload.html", result=get, scam=scam)
  else:
    return render_template("upload.html", result=get,scam=scam) 


if __name__ == '__main__':
  #app.run(debug=True, host="0.0.0.0", port=443, ssl_context="adhoc")
  #app.run(debug=True, host ='0.0.0.0', port="443", ssl_context="adhoc")
  #app.run(debug=True, host ='0.0.0.0')
  app.run(debug=True)

