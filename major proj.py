# -*- coding: utf-8 -*-
"""Untitled4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ABihrLWTWDCdFVm8cOhuFhfwn8-Tt6Wk

## Start from here
"""

import os 
from google.colab import drive
drive.mount('/content/drive')

pip install pyfhel

import json
import numpy as np
with open("/content/drive/My Drive/weights.json", "r") as outfile: 
  feature_values = json.load(outfile) 
weights = feature_values['weights']
biases = feature_values['biases']

with open("/content/drive/My Drive/test_set.json", "r") as outfile: 
  feature_values = json.load(outfile) 
x_test = feature_values['x_test']
y_test = feature_values['y_test']


for i in range(len(weights)):
  weights[i]=np.array(weights[i])
for i in range(len(biases)):
  biases[i]=np.array(biases[i])


for i in range(len(x_test)):
  x_test[i]=np.array(x_test[i])
for i in range(len(y_test)):
  y_test[i]=np.array(y_test[i])




from Pyfhel import Pyfhel, PyPtxt, PyCtxt

from Pyfhel import Pyfhel, PyPtxt, PyCtxt
HE = Pyfhel()           # Creating empty Pyfhel object
HE.contextGen(p=2047,m=8192,base=2, intDigits=4, fracDigits = 48, sec=128, flagBatching=False)  # Generating context. The value of p is important.
                        #  There are many configurable parameters on this step
HE.keyGen()

HE.relinKeyGen(10,30)

def relu_act(x):
  r=x*0.784615
  r=r+0.215384
  p=x*x
  HE.relinearize(p)
  q=p*0.065811
  s=x*p
  HE.relinearize(s)
  t=s*(-0.005982)
  u= t+q+r
  #print([HE.decryptFrac(p),HE.decryptFrac(r),HE.decryptFrac(q),HE.decryptFrac(s),HE.decryptFrac(t),HE.decryptFrac(u)])
  return u


def sigm_act(x):
  r1=x*0.25
  r1=r1+0.5
  p1=x*x
  HE.relinearize(p1)
  q1=p1*x
  HE.relinearize(q1)
  t1=q1*-0.020834
  u1= r1+t1
  #print(HE.decryptFrac(r1),HE.decryptFrac(p1),HE.decryptFrac(q1),HE.decryptFrac(t1),HE.decryptFrac(u1))
  return u1

def get_last_layer_outputs(x_inp):
  #HE = Pyfhel()           # Creating empty Pyfhel object
  #HE.contextGen(p=63,m=8192,base=2, intDigits=4, fracDigits = 48, sec=128, flagBatching=False)  # Generating context. The value of p is important.
  #  There are many configurable parameters on this step
  #HE.keyGen()
  x_inp=list(x_inp)
  inp=x_inp.copy()
  for i in range(len(inp)):
    inp[i]=HE.encryptFrac(inp[i])
  # print(inp)
    


  out1=np.dot(inp,weights[0])
  out1+=biases[0]

  #HE.relinKeyGen(10,30)
  #for i in range(len(out1)):
  #  HE.relinearize(out1[i])
  #print(out1)


  out1_act=[]
  for i in range(len(out1)):
    out1_act.append(relu_act(out1[i]))

  #print(out1_act)

  out2=np.dot(out1_act,weights[1])
  out2+=biases[1]

  out2_act=[]
  for i in range(len(out2)):
    out2_act.append(relu_act(out2[i]))
  
  #print(out2_act)

  out3=np.dot(out2_act,weights[2])
  out3+=biases[2]


  out3_act=[]
  for i in range(len(out3)):
    out3_act.append(sigm_act(out3[i]))
  # print(out3)
  print(out3_act)
  return [HE.decryptFrac(i) for i in out3_act]

"""Pramod (0, 4335)
Ashok (4335,8670)
pravallika (8670,13005)
sharan (13005, 17340)

"""

l=[]
acc=0
for i in range(100):
  l=get_last_layer_outputs(x_test[i])
  print(l)
  ind=l.index(max(l))
  if y_test[i][ind] == 1 :
    acc+=1 
  print(y_test[i])
print(acc)

