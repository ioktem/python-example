import threading
import time
import random
from win32api import GetCurrentProcess,TerminateProcess
import queue

import urllib.request
import requests
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QTextEdit,QLineEdit, QLabel

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from PyQt5.QtCore import Qt
import sys
import numpy as np


#kuyruk = queue.Queue()

#https://kerteriz.net/python-multithreading-programlama/

###############------MACROS-------------##########################

TAKEN_DATA_SAMPLES=20

kuyruk1= queue.Queue() #sıcalık
kuyruk2= queue.Queue() #nem
kuyruk3= queue.Queue() #vibration
kuyruk4= queue.Queue() #akım 
kuyruk5= queue.Queue() #voltage


def thread_islem(kuyruk1,kuyruk2,kuyruk3,kuyruk4,kuyruk5):
 SicaklikNemDataClass=SicaklikNemData()
 while True:  # döngü oluşturulur belirli sürede bir bu kısır döngü tekrar edilir.
     #kuyruk1.put(random.randint(0,100))
     #kuyruk2.put(random.randint(0,10))
     time.sleep(5)
     feild_1,feild_2,feild_3,feild_4,feild_5=Thingspeak.read_data_thingspeak()  # thinkspeakten 20 adet veri alınır
     #datakuyruk.put((sicak,nem))
     SicaklikNemDataClass.setRawDataSicaklik(feild_1,kuyruk1)
     SicaklikNemDataClass.setRawDataNem(feild_2,kuyruk2)
     SicaklikNemDataClass.setRawDataVibration(feild_3,kuyruk3)
     SicaklikNemDataClass.setRawDataCurrent(feild_4,kuyruk4)
     SicaklikNemDataClass.setRawDataVoltage(feild_5,kuyruk5)
     print("thread girildi")
     

class MplCanvas(FigureCanvasQTAgg):
      
    def __init__(self, parent=None, width=4, height=5, dpi=100):
        #fig = plt(figsize=(width, height), dpi=dpi, facecolor='white', edgecolor='green',linewidth=5)
        fig = plt.figure(facecolor='lightskyblue',layout='constrained')
        #fig.subplots_adjust(left=0.2) #grafiğin sol tarafında boşluk oluşturuldu
        fig.subplots_adjust(bottom=0.17,wspace = 0.1,hspace=1.1)  # the amount of width reserved for space between subplots,
              # expressed as a fraction of the average axis width
        self.axes = fig.add_subplot(3,2,1)
        self.axes.grid(True)
        self.axes.set_ylim([10, 40])
        self.axes.tick_params(axis='x', labelrotation=85,labelsize=9)
        
        self.axes2 = fig.add_subplot(3,2,3)
        self.axes2.grid(True)
        self.axes2.set_ylim([0, 100])
        self.axes2.tick_params(axis='x', labelrotation=85,labelsize=9)

        self.axes3 = fig.add_subplot(3,2,5)
        self.axes3.grid(True)
        self.axes3.set_ylim([0, 250])
        self.axes3.tick_params(axis='x', labelrotation=85,labelsize=9)
   
   
        self.axes4 = fig.add_subplot(2,2,2)
        self.axes4.grid(True)
        self.axes4.set_ylim([0, 40])
        self.axes4.tick_params(axis='x', labelrotation=85)

        self.axes5 = fig.add_subplot(2,2,4)
        self.axes5.grid(True)
        self.axes5.set_ylim([0, 260])
        self.axes5.tick_params(axis='x', labelrotation=85)

        super(MplCanvas, self).__init__(fig)

 

class MainWindow(QtWidgets.QMainWindow):
   
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=20, height=16, dpi=100) 
        #self.setCentralWidget(self.canvas)


        self.nameLabel = QLabel(self)  
        self.nameLabel.setText('Data Sayisi:') 
        self.nameLabel.move(30, 20)

        self.line = QLineEdit(self)
        self.line.setMaxLength(3)
        self.line.move(0, 20)  
        self.line.resize(10, 32) 

        pybutton = QtWidgets.QPushButton('OK', self)
        pybutton.clicked.connect(self.clickMethod)
        pybutton.resize(40,30)
        pybutton.move(20, 20)   
        self.line.setStyleSheet("color: Blue;"
                      "background-color: lightgreen;"
                      "border-style: solid;"
                      "border-width: 3px;"
                      "border-color: #1E90FF")

        self.xdata = []
        self.ydata = []

        self.x2data = []
        self.y2data = []

        self.x3data = []
        self.y3data = []

        self.x4data = []
        self.y4data = []

        self.x5data = []
        self.y5data = []

        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        #_plot_change_ref = False #grafiği tekrar boyutlandırmak için
        self._plot_ref = None
        self.update_plot()

        self.setWindowTitle("Data")
        '''Window Background'''
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.lightGray)
        self.setPalette(p)

         # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)
        layout = QtWidgets.QVBoxLayout()
        layout2 = QtWidgets.QHBoxLayout()
        
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        layout2.addWidget(self.nameLabel)
        layout2.addWidget(self.line)
        layout2.addWidget(pybutton)
        layout.addLayout(layout2)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def clickMethod(self):
        global TAKEN_DATA_SAMPLES
        TAKEN_DATA_SAMPLES=int(self.line.text()) 

    def update_plot(self):
        global kuyruk1,kuyruk2,kuyruk3,kuyruk4,kuyruk5
    
        self.ydata.clear()
        self.xdata.clear()
        while not kuyruk1.empty():
            x = kuyruk1.get()
            self.xdata.append(str(x[0]))
            self.ydata.append(x[1])
         
        self.y2data.clear()
        self.x2data.clear()
        while not kuyruk2.empty():
            x = kuyruk2.get()
            self.x2data.append(str(x[0]))
            self.y2data.append(x[1])

        self.y3data.clear()
        self.x3data.clear()
        while not kuyruk3.empty():
            x = kuyruk3.get()
            self.x3data.append(str(x[0]))
            self.y3data.append(x[1])
       
        self.y4data.clear()
        self.x4data.clear()
        while not kuyruk4.empty():
            x = kuyruk4.get()
            self.x4data.append(str(x[0]))
            self.y4data.append(x[1])
       
        self.y5data.clear()
        self.x5data.clear()
        while not kuyruk5.empty():
            x = kuyruk5.get()
            self.x5data.append(str(x[0]))
            self.y5data.append(x[1])
      
        # Note: we no longer need to clear the axis.
        if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, '.')
            #self.canvas.axes.plot(self.xdata, self.ydata, '.')
            self.canvas.axes.set_title("Temperature Graph",loc='left',font='0.8')
            self.canvas.axes.set_xlabel("Time")
            self.canvas.axes.set_ylabel("Temperature")
            #self.canvas.axes.set_xscale()
            self._plot_ref = plot_refs[0]

            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs2 = self.canvas.axes2.plot(self.x2data, self.y2data, '.')
            #self.canvas.axes.plot(self.xdata, self.ydata, '.')
            self.canvas.axes2.set_title("Humidity Graph",loc='left',font='0.8')
            self.canvas.axes2.set_xlabel("Time")
            self.canvas.axes2.set_ylabel("Humidity")
            #self.canvas.axes.set_xscale()

            #self.canvas.axes.set_xscale()
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            #plot_refs2 = self.canvas.axes4.plot(self.x2data, self.y2data, '.')
            #self.canvas.axes.plot(self.xdata, self.ydata, '.')
            self.canvas.axes3.set_title("Vibration Graph",loc='left',font='0.8')
            self.canvas.axes3.set_xlabel("Time")
            self.canvas.axes3.set_ylabel("Vibration Level(g)")
            #self.canvas.axes.set_xscale()
            
             # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            #plot_refs2 = self.canvas.axes3.plot(self.x2data, self.y2data, '.')
            #self.canvas.axes.plot(self.xdata, self.ydata, '.')
            self.canvas.axes4.set_title("Current Graph",loc='left',font='0.8')
            self.canvas.axes4.set_xlabel("Time")
            self.canvas.axes4.set_ylabel("Current(A)")
            #self.canvas.axes.set_xscale()
            
             # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            #plot_refs2 = self.canvas.axes4.plot(self.x2data, self.y2data, '.')
            #self.canvas.axes.plot(self.xdata, self.ydata, '.')
            self.canvas.axes5.set_title("Voltage Graph",loc='left',font='0.8')
            self.canvas.axes5.set_xlabel("Time")
            self.canvas.axes5.set_ylabel("Voltage(V)")

        elif len(self.xdata)==TAKEN_DATA_SAMPLES:
            #canvas siler
            #☻self.canvas.axes2.relim()
            self.canvas.axes.cla()
            self.canvas.axes2.cla()
            self.canvas.axes3.cla()
            self.canvas.axes4.cla()
            self.canvas.axes5.cla()
            
            self.canvas.axes.grid(True)
            self.canvas.axes.set_ylim([10, 40])
            self.canvas.axes.tick_params(axis='x', labelrotation=85)
            self.canvas.axes.set_ylabel("Temperature")
            self.canvas.axes.plot(self.xdata, self.ydata, color='red', marker='.', linestyle='dashed',linewidth=2, markersize=12)

            self.canvas.axes2.grid(True)
            self.canvas.axes2.set_ylim([0, 100])
            self.canvas.axes2.tick_params(axis='x', labelrotation=85)
            self.canvas.axes2.set_ylabel("Humidity")
            self.canvas.axes2.plot(self.x2data, self.y2data,  color='blue', marker='.', linestyle='dashed',linewidth=2, markersize=12) 

            self.canvas.axes3.grid(True)
            self.canvas.axes3.set_ylim([0, 250])
            self.canvas.axes3.tick_params(axis='x', labelrotation=85,labelsize=9)
            self.canvas.axes3.set_ylabel("Vibration Level(g)")
            self.canvas.axes3.plot(self.x3data, self.y3data,  color='g', marker='.', linestyle='dashed',linewidth=2, markersize=12) 

            self.canvas.axes4.grid(True)
            self.canvas.axes4.set_ylim([0, 160])
            self.canvas.axes4.tick_params(axis='x', labelrotation=85)
            self.canvas.axes4.set_ylabel("Current(A)")
            self.canvas.axes4.plot(self.x4data, self.y4data,  color='m', marker='.', linestyle='dashed',linewidth=2, markersize=12) 

            self.canvas.axes5.grid(True)
            self.canvas.axes5.set_ylim([0, 250])
            self.canvas.axes5.tick_params(axis='x', labelrotation=85)
            self.canvas.axes5.set_ylabel("Voltage(V)")
            self.canvas.axes5.plot(self.x5data, self.y5data,  color='m', marker='.', linestyle='dashed',linewidth=2, markersize=12) 
            
            #https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html   
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
   



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
        URL='https://api.thingspeak.com/channels/2023940/fields/1.json?api_key='     #Read a Channel Field buradan linki kopyalla kanal no değişir
        URL2='https://api.thingspeak.com/channels/2023940/fields/2.json?api_key='     #Read a Channel Field buradan linki kopyalla kanal no değişir
        URL3='https://api.thingspeak.com/channels/2023940/fields/3.json?api_key='     #Read a Channel Field buradan linki kopyalla kanal no değişir
        URL4='https://api.thingspeak.com/channels/2023940/fields/4.json?api_key='     #Read a Channel Field buradan linki kopyalla kanal no değişir
        URL5='https://api.thingspeak.com/channels/2023940/fields/5.json?api_key='     #Read a Channel Field buradan linki kopyalla kanal no değişir
        KEY='T8YSWS8UXNTS3Y6E' #READ KEY XXXXX 
        HEADER='&results='
        RESULT=str(TAKEN_DATA_SAMPLES)    # kaç adet data alınacak
        NEW_URL=URL+KEY+HEADER+RESULT
        NEW_URL2=URL2+KEY+HEADER+RESULT
        NEW_URL3=URL3+KEY+HEADER+RESULT
        NEW_URL4=URL4+KEY+HEADER+RESULT
        NEW_URL5=URL5+KEY+HEADER+RESULT
    
        get_data=requests.get(NEW_URL).json()
        feild_1=get_data['feeds']
    
        get_data2=requests.get(NEW_URL2).json()
        print(get_data2)
        feild_2=get_data2['feeds']
        
        get_data3=requests.get(NEW_URL3).json()
        feild_3=get_data3['feeds']

        get_data4=requests.get(NEW_URL4).json()
        feild_4=get_data4['feeds']

        get_data5=requests.get(NEW_URL5).json()
        feild_5=get_data5['feeds']

        for x in feild_5:                 
           mystr=x['field5']
           x['field5']=mystr.replace('\r','').replace('\n','')
          
        return feild_1,feild_2,feild_3,feild_4,feild_5


class SicaklikNemData():
    def setRawDataSicaklik(self,_feild_1,kuyruk1):
     for x in _feild_1:
        _sicaklik = float(x['field1'])
        mystr=x['created_at']
        _id=mystr.replace('T',' ').replace('Z','')
        _id=_id[:-3]  #"Son 3 karakteri silelim" fakat datalar dakikada 1 kere gönderilmeli saniyeler siliniyor
        kuyruk1.put((_id,_sicaklik))
    
    def setRawDataNem(self,_feild_2,kuyruk2):
     for x in _feild_2:
        _nem = float(x['field2'])
        mystr=x['created_at']
        _id=mystr.replace('T',' ').replace('Z','') 
        _id=_id[:-3] 
        kuyruk2.put((_id,_nem))

    def setRawDataVibration(self,_feild_3,kuyruk3):
     for x in _feild_3:
        _val = float(x['field3'])
        mystr=x['created_at']
        _id=mystr.replace('T',' ').replace('Z','') 
        _id=_id[:-3] 
        kuyruk3.put((_id,_val))

    def setRawDataCurrent(self,_feild_4,kuyruk4):
     for x in _feild_4:
        _val = float(x['field4'])
        mystr=x['created_at']
        _id=mystr.replace('T',' ').replace('Z','') 
        _id=_id[:-3] 
        kuyruk4.put((_id,_val))

    def setRawDataVoltage(self,_feild_5,kuyruk5):
     for x in _feild_5:
        _val = float(x['field5'])
        mystr=x['created_at']
        _id=mystr.replace('T',' ').replace('Z','') 
        _id=_id[:-3] 
        kuyruk5.put((_id,_val))

     
def main():
    global kuyruk1,kuyruk2,kuyruk3,kuyruk4,kuyruk5
    th0 = threading.Thread(target=thread_islem,args = (kuyruk1,kuyruk2,kuyruk3,kuyruk4,kuyruk5),daemon=True) #Yani özetle main thread sonlandığında daemon thread çalışıyor olsa bile sonlandırılır.
    th0.start()


    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()

try:
    main()
except:
     TerminateProcess(GetCurrentProcess(),0)

