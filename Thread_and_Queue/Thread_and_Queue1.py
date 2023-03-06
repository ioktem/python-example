import threading
import time
import random
from win32api import GetCurrentProcess,TerminateProcess
import queue

import urllib.request
import requests

kuyruk = queue.Queue()

#https://kerteriz.net/python-multithreading-programlama/

###############------MACROS-------------##########################

TAKEN_DATA_SAMPLES=9
_plot_change_ref = False


kuyruk1= queue.Queue()
kuyruk2= queue.Queue()

class Thingspeak():
  def thingspeak_post():
      #threading.Timer(15,thingspeak_post).start()
      val=26 # random.randint(1,30)
      val2=23
      URl='https://api.thingspeak.com/update?api_key='
      KEY='4CBIKO6PKG827KM7' #WRITE KEY XXXXX  #https://thingspeak.com/channels/2023940/api_keys
      HEADER='&field1={}&field2={}'.format(val,val2)
      NEW_URL=URl+KEY+HEADER
      data=urllib.request.urlopen(NEW_URL)

  def read_data_thingspeak():
        t0 = time.time_ns()
        URL='https://api.thingspeak.com/channels/2023940/fields/1.json?api_key='     #Read a Channel Field buradan linki kopyalla kanal no değişir
        URL2='https://api.thingspeak.com/channels/2023940/fields/2.json?api_key='     #Read a Channel Field buradan linki kopyalla kanal no değişir
        KEY='T8YSWS8UXNTS3Y6E' #READ KEY XXXXX 
        HEADER='&results='
        RESULT=str(TAKEN_DATA_SAMPLES)    # kaç adet data alınacak
        NEW_URL=URL+KEY+HEADER+RESULT
        NEW_URL2=URL2+KEY+HEADER+RESULT
    
        get_data=requests.get(NEW_URL).json()
        feild_1=get_data['feeds']
    
        get_data2=requests.get(NEW_URL2).json()
        print(get_data2)
        feild_2=get_data2['feeds']
        
        for x in feild_2:                 
           mystr=x['field2']
           x['field2']=mystr.replace('\r','').replace('\n','')
          
        print((time.time_ns() - t0)/1e9)
        return feild_1,feild_2

class SicaklikNemData():
    def setRawDataSicaklik(self,_feild_1,kuyruk1):
     for x in _feild_1:
        _sicaklik = float(x['field1'])
        mystr=x['created_at']
        _id=mystr.replace('T',' ').replace('Z','') 
        kuyruk1.put((_id,_sicaklik))
     return kuyruk1
    
    def setRawDataNem(self,_feild_2,kuyruk2):
     for x in _feild_2:
        _nem = float(x['field2'])
        mystr=x['created_at']
        _id=mystr.replace('T',' ').replace('Z','') 
        kuyruk2.put((_id,_nem))
     return kuyruk2

SicaklikNemDataClass=SicaklikNemData() #global class





def thread_islem(kuyruk1,kuyruk2):
 while True:  # döngü oluşturulur belirli sürede bir bu kısır döngü tekrar edilir.
     #kuyruk1.put(random.randint(0,100))
     #kuyruk2.put(random.randint(0,10))
     time.sleep(2)
     feild_1,feild_2=Thingspeak.read_data_thingspeak()  # thinkspeakten 20 adet veri alınır
     SicaklikNemDataClass.setRawDataSicaklik(feild_1,kuyruk1)
     SicaklikNemDataClass.setRawDataNem(feild_2,kuyruk2)
     print("thread girildi")
     

     
def main():
    global kuyruk1,kuyruk2
    th0 = threading.Thread(target=thread_islem,args = (kuyruk1,kuyruk2),daemon=True) #Yani özetle main thread sonlandığında daemon thread çalışıyor olsa bile sonlandırılır.
    th0.start()
    while True:
        while not kuyruk1.empty():
            val = kuyruk1.get()
            print("main_thread : " + str(val) + " ->"+str(kuyruk1.qsize()))

        while not kuyruk2.empty():
            val = kuyruk2.get()
            print("main_thread2 : " + str(val) + " ->"+str(kuyruk2.qsize()))
        time.sleep(1)
        
try:
    main()
except:
     TerminateProcess(GetCurrentProcess(),0)

