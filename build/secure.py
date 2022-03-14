#!/usr/bin/env python3
from cryptography.fernet import Fernet

def get_key():
  with open('key.key','rb') as filekey:
    key=filekey.read()
  return key

def enc(path, key):
  fernet=Fernet(key)
  with open(path, "rb") as file:
    originalaudio=file.read()
  encrypted=fernet.encrypt(originalaudio)
  with open(path,'wb') as encrypted_file:
    encrypted_file.write(encrypted)

def dec(path, key):
  fernet=Fernet(key)
  with open(path, 'rb') as enc_file:
     encrypted=enc_file.read()
  decrypted =fernet.decrypt(encrypted)
  with open(path,'wb') as dec_file:
    dec_file.write(decrypted)


#enc("WAV/074a8384-2683-467e-82ca-569e442b35d1.wav", get_key())
#enc("WAV/074a8384-2683-467e-82ca-569e442b35d1.wav", get_key())
#dec("WAV/074a8384-2683-467e-82ca-569e442b35d1.wav", get_key())
#dec("WAV/074a8384-2683-467e-82ca-569e442b35d1.wav", get_key())
