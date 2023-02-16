from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QTimer
import urllib.request
import requests
import threading
import json
#import random # random sayı gönderme generator

# https://github.com/soumilshah1995/python-youtube-tutorials/blob/master/thingspeak%20Python.py
# https://www.youtube.com/watch?v=whXaVYSXItQ

# Define a function that will post on server every 15 Seconds

t=[]
t2=[]


class SicaklikData():
    def getRawData(self,_series):
     for data in t:
         index = data[0]
         sicaklik = data[1]
         _series.append(index,sicaklik)
    
    def setRawData(self,_feild_1):
     for x in _feild_1:
        print(x['field1'])
        _sicaklik = float(x['field1'])
        _id = int(x['entry_id'])
        t.append((_id,_sicaklik))
        
class NemData():
    def getRawData(self,_series):
     for data in t2:
         index = data[0]
         nem = data[1]
         _series.append(index,nem)
    
    def setRawData(self,_feild_2):
     for x in _feild_2:
        print(x['field2'])
        _nem = float(x['field2'])
        _id = int(x['entry_id'])
        t2.append((_id,_nem))


SicaklikDataClass=SicaklikData() #global class
NemDataClass=NemData() #global class

def thingspeak_post():
    threading.Timer(15,thingspeak_post).start()
    val=26 # random.randint(1,30)
    val2=23
    URl='https://api.thingspeak.com/update?api_key='
    KEY='4CBIKO6PKG827KM7' #WRITE KEY XXXXX  #https://thingspeak.com/channels/2023940/api_keys
    HEADER='&field1={}&field2={}'.format(val,val2)
    NEW_URL=URl+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)
    print(data)

def read_data_thingspeak():
    URL='https://api.thingspeak.com/channels/2023940/fields/1.json?api_key='     #Read a Channel Field buradan linki kopyalla kanal no değişir
    URL2='https://api.thingspeak.com/channels/2023940/fields/2.json?api_key='     #Read a Channel Field buradan linki kopyalla kanal no değişir
    KEY='T8YSWS8UXNTS3Y6E' #READ KEY XXXXX 
    HEADER='&results='
    RESULT=str(20)    # kaç adet data alınacak
    NEW_URL=URL+KEY+HEADER+RESULT
    NEW_URL2=URL2+KEY+HEADER+RESULT

    get_data=requests.get(NEW_URL).json()
    print(get_data)
    #channel_id=get_data['channel']['id']
    feild_1=get_data['feeds']

    get_data2=requests.get(NEW_URL2).json()
    print(get_data2)
    feild_2=get_data2['feeds']

    #feild_2=[w.replace('\r\n\r\n','') for w in feild_2]
    for x in feild_2:                 
       mystr=x['field2']
       x['field2']=mystr.replace('\r','').replace('\n','')
      
    #feild_2=feild_2.remove('\r\n\r\n')
    #feild_2=feild_2.pop('\r\n\r\n')

    return feild_1,feild_2

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQtChart Line")
        self.setGeometry(100,100, 680,500)
        self.chartTimer = QTimer()
        self.chartTimer.timeout.connect(self.Timer1)
        self.chartTimer.start(5000)
        self.show()
        feild_1,feild_2=read_data_thingspeak()
        SicaklikDataClass.setRawData(feild_1)
        NemDataClass.setRawData(feild_2)
        self.chart =  QChart()
        self.create_linechart()

    def create_linechart(self):

        series = QLineSeries(self)
        SicaklikDataClass.getRawData(series)


        self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Line Chart Example")

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(self.chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)

        series = QLineSeries(self)
        NemDataClass.getRawData(series)


        self.chart.addSeries(series)
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.setTitle("Line Chart Example")

        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)

        chartview = QChartView(self.chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)




    def Timer1(self):
        self.chart.removeAllSeries() # seriler üst üste karışmaması için eskiler kaldırılır
        t.clear()    # önceki veriler silinir
        feild_1,feild_2=read_data_thingspeak()  # thinkspeakten 20 adet veri alınır
        SicaklikDataClass.setRawData(feild_1)
        series = QLineSeries(self) # veriler çizilmek için fonksiyon adresi aktarılır
        SicaklikDataClass.getRawData(series) #veriler kullanılmak üzere işlenir 
        self.chart.addSeries(series)  #işlenen veriler chart verisine input olarak alınır 
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        chartview = QChartView(self.chart)
        chartview.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(chartview)

        NemDataClass.setRawData(feild_2)
        series = QLineSeries(self) # veriler çizilmek için fonksiyon adresi aktarılır
        NemDataClass.getRawData(series) #veriler kullanılmak üzere işlenir 
        self.chart.addSeries(series)  #işlenen veriler chart verisine input olarak alınır 
        self.chart.createDefaultAxes()
        self.chart.setAnimationOptions(QChart.SeriesAnimations)
        self.chart.legend().setVisible(True)
        self.chart.legend().setAlignment(Qt.AlignBottom)
        chartview = QChartView(self.chart)
        chartview.setRenderHint(QPainter.Antialiasing)

        self.setCentralWidget(chartview)
       
           

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())