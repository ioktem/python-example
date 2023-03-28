#! /usr/bin/env python
# -*- coding: UTF-8 -*-
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
import random
from math import*
from datetime import datetime,timedelta


#https://www.youtube.com/watch?v=9Hno1jyWY-w

#veri = pd.read_csv("2016dolaralis.csv")

#x = veri["Gun"]
#y = veri["Fiyat"]


ESTIMATE_ERROR_CONSTANT=300
x=[]
y=[]

for a in range(20):
    for i in range(10):
        y.append(50*(random.randint(0,10)*0.02+a*0.2))
        x.append(a*10+i)
    


#x = [1,2,3,5,6,7,8,9,10,12,13,14,15,16,18,19,21,22]
#y = [100,90,80,60,60,55,60,65,70,70,75,76,78,79,90,99,99,100]

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
poli_reg = PolynomialFeatures(degree=3)  #polinom regresyon
xPolinom = poli_reg.fit_transform(x)

lin_reg2= LinearRegression()
lin_reg2.fit(xPolinom,y) 
lin_reg2.predict(xPolinom)

#print((float(y[17])-float(lin_reg2.predict(xPolinom)[17]))) # Dizinin 17. elemanı, gerçek ile tahmin edilen değer arasındaki hata payı
#print(lin_reg2.predict(poli_reg.fit_transform([[300]]))) #Tahmin edilen, x=300 için y değeri

for i in range(len(x)*10):
        if lin_reg2.predict(poli_reg.fit_transform([[i]]))>ESTIMATE_ERROR_CONSTANT:
            datenow=datetime.today()
            Maintanceday=datenow+timedelta(days =i- len(x)) #Elimizde 200 adet data var ve bu dataları i gün sonra eşik değeri aştığı için i-elimizdeki data yaparak kaç gün sonra eşik değer aşılır onu elde ederiz.
            print("Tahmini cihaz bakımı ",i- len(x)," gün sonra", Maintanceday.date())  # bu değerden sonra ESTIMATE_ERROR_CONSTANT geçilmiş olur ve cihaz bakım ister.
            break

        if i==len(x)*10:
            print("Kestirim yapılamıyor algoritma uygun olmayabilir.")  


plt.plot(x,lin_reg2.predict(xPolinom),'yellow')
plt.show()




print("son debug noktası")