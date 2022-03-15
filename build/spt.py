#!/usr/bin/env python3

import speech_recognition as sr
import pyttsx3

global r 
r = sr.Recognizer()

import subprocess
import os
def speech_to_text(path):
  filename=path
  # open the file
  with sr.AudioFile(filename) as source:
      audio_data = r.record(source)
      text = r.recognize_google(audio_data)
  return text

def check_final(arr):
  check=["pin","creditcard", "cardcredit","lottery","bankaccount", "bank","account","credit","insurance","card","gpay","giftcard","gift","card","paytm"]
  count=0
  for i in arr:
    if i.lower() in check:
      count=count+1
  if count>=1:
    return 1
  else:
    return 0


def processing(arr):
  li=arr.split(" ")
  imp_list=[" ","?","  ","   ",",",".","/","-",":","_"]
  for i in range(len(li)):
    for j in imp_list:
     li[i]=li[i].replace(j,"")
  return li

"""
import wavio
#wavio.write(wav_path, data, fs ,sampwidth=2)
import soundfile


path = "WAV/20b75ac0-1edc-4998-bc43-c164373e4714.wav"
data, samplerate = soundfile.read(path)
print(str(data))

arr  = speech_to_text(path)
arr  = processing(arr)
print(check_final(arr))
"""
