from PyQt5.QtWidgets import QApplication, QMainWindow # QVBoxLayout
import sys
from PyQt5.QtChart import QChart, QChartView, QLineSeries,QValueAxis,QSplineSeries,QCategoryAxis,QDateTimeAxis
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt,QDateTime
from PyQt5.QtCore import QTimer
import urllib.request
import requests
import threading
import json
#import random # random sayı gönderme generator


#https://doc.qt.io/qtforpython/overviews/qtcharts-multiaxis-example.html#multiple-axes-example
#https://doc.qt.io/qtforpython/overviews/qtcharts-datetimeaxis-example.html#datetimeaxis-example


# https://github.com/soumilshah1995/python-youtube-tutorials/blob/master/thingspeak%20Python.py
# https://www.youtube.com/watch?v=whXaVYSXItQ
# https://stackoverflow.com/questions/57079698/qdatetimeaxis-series-are-not-displayed

# Define a function that will post on server every 15 Seconds

t=[]  # thingspeakten gelen veriler kullanmaya hazır şekilde  bu dizide tutulur
t2=[] # thingspeakten gelen veriler kullanmaya hazır şekilde  bu dizide tutulur


class SicaklikNemData():
    def getRawDataSicaklik(self,_series):
     for data in t:
         index = data[0]
         sicaklik = data[1]
         _series.append(index,sicaklik)
    
    def setRawDataSicaklik(self,_feild_1):
     for x in _feild_1:
        print(x['field1'])
        _sicaklik = float(x['field1'])
       # _id = str(x['created_at'])
        mystr=x['created_at']
        _id=mystr.replace('T','').replace('Z','').replace(':','').replace('-','')
        _id=float(QDateTime.fromString(str(_id), "yyyyMMddhhmmss").toMSecsSinceEpoch())
        t.append((float(_id),_sicaklik))
        
    def getRawDataNem(self,_series):
     for data in t2:
         index = data[0]
         nem = data[1]
         _series.append(index,nem)
    
    def setRawDataNem(self,_feild_2):
     for x in _feild_2:
        print(x['field2'])
        _nem = float(x['field2'])
       # _id = int(x['entry_id'])
        mystr=x['created_at']
        _id=mystr.replace('T','').replace('Z','').replace(':','').replace('-','')
        _id=float(QDateTime.fromString(str(_id), "yyyyMMddhhmmss").toMSecsSinceEpoch())

        t2.append((float(_id),_nem))


SicaklikNemDataClass=SicaklikNemData() #global class


class Thingspeak():
  def thingspeak_post():
      #threading.Timer(15,thingspeak_post).start()
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
        RESULT=str(15)    # kaç adet data alınacak
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
        self.setGeometry(100,100, 1080,720)

        t.clear()    # önceki veriler silinir
        t2.clear()    # önceki veriler silinir
        feild_1,feild_2=Thingspeak.read_data_thingspeak()  # thinkspeakten 20 adet veri alınır
        SicaklikNemDataClass.setRawDataSicaklik(feild_1)
        SicaklikNemDataClass.setRawDataNem(feild_2)

        self.chart = QChart()
        #chart.legend().hide()
        self.chart.setTitle("Multiaxis chart example")
        
        #axisX = QValueAxis()
        axisX = QDateTimeAxis()
        axisX.setTickCount(15)
        #chart.createDefaultAxes()  # x ekseni için 
        self.chart.addAxis(axisX, Qt.AlignBottom) #x ekseni değerleri grafiğin altına konumlandırılır

        #Grafiğin sol tarafı
        series = QLineSeries(name="Sicaklik")
        # series = QSplineSeries(name="Sicaklik")  #bağ interpolasyonu, noktalar arasında QSpline eğri, QLine çizgi oluşturur.
        SicaklikNemDataClass.getRawDataSicaklik(series) #veriler kullanılmak üzere işlenir 
        #series << QPointF(1, 5) << QPointF(3.5, 6) << QPointF(4.8, 7.5) << QPointF(5, 3.5) <<QPointF(5.2, 3.5) << QPointF(7.4, 16.5) << QPointF(8.3, 7.5) << QPointF(10, 17)
        series.setPointsVisible(True) # pointler grafik üzerinde işaretlenir
        series.setPointLabelsVisible(True)   # pointler grafik üzerinde x,y koordinat şeklinde belirtilir
      
        #series.setPointLabelsFormat( "(@xPoint, @yPoint)" )  # pointler grafik üzerinde (x,y) formatında gösterilir
        series.setPointLabelsFormat( "(@yPoint)" ) 
        self.chart.addSeries(series)
        axisY = QValueAxis() 
        axisY.setRange(axisY.min()-1, 55) #   axisY.setRange(axisY.nmin()-1, 55)   axisY.setRange(0, 55)
        axisY.setLinePenColor(series.pen().color())  # soldaki y ekseni ile datanın rengini ilişkilendiriyor
        
        self.chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)
       
        #Grafiğin sağ tarafı
        series = QLineSeries(name="Nem")   # series = QSplineSeries(name="Nem")
        SicaklikNemDataClass.getRawDataNem(series)
        #series << QPointF(1, 0.5) << QPointF(1.5, 4.5) << QPointF(2.4, 2.5) << QPointF(4.3, 70.5)<< QPointF(5.2, 3.5) << QPointF(7.4, 55.5) << QPointF(8.3, 7.5) << QPointF(9, 19)
        series.setPointsVisible(True)  # pointler grafik üzerinde işaretlenir
        series.setPointLabelsVisible(True)
        
        #series.setPointLabelsFormat( "(@xPoint, @yPoint)" )
        series.setPointLabelsFormat( "(@yPoint)" ) 
        self.chart.addSeries(series)
        axisY3 = QValueAxis()       # y ekseni etiketlerini kategori içerisine değilde normal int olarak göstermek istersen
        axisY3.setRange(axisY3.min()-1,100)
       # axisY3 = QCategoryAxis()   # y ekseni etiketlerini kategorilemek için kullanılır
       # axisY3.append("Low", 5)
       # axisY3.append("Medium", 12)
       # axisY3.append("High", 17)
        axisY3.setLinePenColor(series.pen().color())
        #axisY3.setGridLinePen((series.pen()))   # gridleri renklendiriyor
    
        self.chart.addAxis(axisY3, Qt.AlignRight)
        series.attachAxis(axisX)  # Y3 datası için x kordinatı tekrar ayarlanmalı
        series.attachAxis(axisY3)
        
        #axisX.setTickCount(11)
        axisX.setLabelsAngle(70)  # tarihlerin grafiğe göre konumlandırılması
        axisX.setFormat("yyyy-MM-dd  hh:mm:ss")    #("h:mm")
        axisX.setTitleText("Date")
        axisX.setRange(axisX.min(), axisX.max())
        #axisX.setMax(QDateTime.fromString(str(axisX.max()),"yyyyMMddhhmmss"))
        #axisX.setMin(QDateTime.fromString(str(axisX.min()),"yyyyMMddhhmmss")) # 202005070845 X ekseninde grafiğin sınırlarını ayarlar

        self.chart.legend().setVisible(True)  # etiketleri görünürleştirir
        self.chart.legend().setAlignment(Qt.AlignBottom)  #etiketi grafiğin altına konumlandırır
        #chart.setAnimationOptions(QChart.SeriesAnimations) #codu yavaşlatabilir
        self.chartView = QChartView(self.chart)
        self.chartView.setRenderHint(QPainter.Antialiasing)
       
        #vbox = QVBoxLayout()
        #vbox.addWidget(chartView)
        #self.setLayout(vbox)
        self.setCentralWidget(self.chartView)
        self.show()   #yukarıda yapılanları grafik üzerine aktarmak için kullanılır yokluğunda grafik oluşmaz


    def mousePressEvent(self,event):
       self.chartView.setRubberBand(QChartView.HorizontalRubberBand)
              
    def wheelEvent(self,event):
        
        if event.angleDelta().y() > 0:
            self.chart.zoomIn()
        else:
            self.chart.zoomOut()

         

App = QApplication(sys.argv)
window = Window()
#window.resize(1280, 720)
#window.show()
sys.exit(App.exec_())
