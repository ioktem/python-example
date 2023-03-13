#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures

#https://www.youtube.com/watch?v=9Hno1jyWY-w

#veri = pd.read_csv("2016dolaralis.csv")

#x = veri["Gun"]
#y = veri["Fiyat"]

x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]

x=np.array(x)
y=np.array(y)

x = x.reshape(len(x),1)
y= y.reshape(len(y),1)
plt.scatter(x,y)


#Lineer Reg.
lin_reg= LinearRegression()
lin_reg.fit(x,y)
lin_reg.predict(x)
plt.plot(x,lin_reg.predict(x),c="red")

#Polinom Reg.
#Not: Polinom regresyon yapmak için önce lineer regresyon uygulanır!!!
poli_reg = PolynomialFeatures(degree=3)  #polinom regresyon
xPolinom = poli_reg.fit_transform(x)

lin_reg2= LinearRegression()
lin_reg2.fit(xPolinom,y) 
lin_reg2.predict(xPolinom)

plt.plot(x,lin_reg2.predict(xPolinom),c="blue")


for a in range(15):
    hatakaresipolinom = 0
    #Polinom Reg.
    #Not: Polinom regresyon yapmak için önce lineer regresyon uygulanır!!!
    poli_reg = PolynomialFeatures(degree=a+1)  #polinom regresyon (poli_reg)
    xPolinom = poli_reg.fit_transform(x)

    lin_reg2= LinearRegression()
    lin_reg2.fit(xPolinom,y) 
    lin_reg2.predict(xPolinom)

    for i in range(len(xPolinom)):
        hatakaresipolinom += hatakaresipolinom + (float(y[i])-float(lin_reg2.predict(xPolinom)[i]))**2
    print(a+1,"inci dereceden fonksiyonda hata,", hatakaresipolinom)


#Polinom Reg.
#Not: Polinom regresyon yapmak için önce lineer regresyon uygulanır!!!
poli_reg = PolynomialFeatures(degree=10)  #polinom regresyon
xPolinom = poli_reg.fit_transform(x)

lin_reg2= LinearRegression()
lin_reg2.fit(xPolinom,y) 
lin_reg2.predict(xPolinom)

plt.plot(x,lin_reg2.predict(xPolinom),'yellow')
print(lin_reg2.predict(poli_reg.fit_transform([[22]]))) #Tahmin edilen, x=22 için y değeri

plt.show()
print((float(y[17])-float(lin_reg2.predict(xPolinom)[17]))) # Dizinin 17. elemanı, gerçek ile tahmin edilen değer arasındaki hata payı

print("bitti")