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

kuyruk1= queue.Queue()
kuyruk2= queue.Queue()


def thread_islem(kuyruk1,kuyruk2):
 SicaklikNemDataClass=SicaklikNemData()
 while True:  # döngü oluşturulur belirli sürede bir bu kısır döngü tekrar edilir.
     #kuyruk1.put(random.randint(0,100))
     #kuyruk2.put(random.randint(0,10))
     time.sleep(5)
     feild_1,feild_2=Thingspeak.read_data_thingspeak()  # thinkspeakten 20 adet veri alınır
     #datakuyruk.put((sicak,nem))
     SicaklikNemDataClass.setRawDataSicaklik(feild_1,kuyruk1)
     SicaklikNemDataClass.setRawDataNem(feild_2,kuyruk2)
     print("thread girildi")
     

class MplCanvas(FigureCanvasQTAgg):
      
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        #fig = plt(figsize=(width, height), dpi=dpi, facecolor='white', edgecolor='green',linewidth=5)
        fig = plt.figure(facecolor='lightskyblue',layout='constrained')
        #fig.subplots_adjust(left=0.2) #grafiğin sol tarafında boşluk oluşturuldu
        self.axes = fig.add_subplot(121)
        self.axes.grid(True)
        self.axes.set_ylim([10, 40])
        self.axes.tick_params(axis='x', labelrotation=85)
        self.axes2 = fig.add_subplot(122)
        self.axes2.grid(True)
        self.axes2.set_ylim([0, 100])
        self.axes2.tick_params(axis='x', labelrotation=85)
   
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



        n_data = TAKEN_DATA_SAMPLES
        #self.xdata = list(range(n_data))
        dates = ['1991/01/01 10:10:10','1991/01/02 10:10:11','1991/01/03 10:10:12','1991/01/04 10:10:13','1991/01/05 10:10:14','1991/01/06 10:10:15','1991/01/07 10:10:16','1991/01/08 10:10:17','1991/01/09 10:10:18']
        self.xdata = [a for a in dates]

        self.ydata = [random.randint(0, TAKEN_DATA_SAMPLES) for i in range(n_data)]

        n_data2 = TAKEN_DATA_SAMPLES
        self.x2data = [a for a in dates] #list(range(n_data2))
                      
        self.y2data = [random.randint(0, TAKEN_DATA_SAMPLES) for i in range(n_data2)]

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
        global _plot_change_ref
        global kuyruk1,kuyruk2
    
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
       
      
        # Note: we no longer need to clear the axis.
        if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, '.')
            #self.canvas.axes.plot(self.xdata, self.ydata, '.')
            self.canvas.axes.set_title("Temperature Graph")
            self.canvas.axes.set_xlabel("Time")
            self.canvas.axes.set_ylabel("Temperature")
            #self.canvas.axes.set_xscale()
            self._plot_ref = plot_refs[0]


            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs2 = self.canvas.axes2.plot(self.x2data, self.y2data, '.')
            #self.canvas.axes.plot(self.xdata, self.ydata, '.')
            self.canvas.axes2.set_title("Humidity Graph")
            self.canvas.axes2.set_xlabel("Time")
            self.canvas.axes2.set_ylabel("Humidity")
            #self.canvas.axes.set_xscale()
            self._plot_ref2 = plot_refs2[0]

        elif len(self.xdata)==TAKEN_DATA_SAMPLES:
            #canvas siler
            #☻self.canvas.axes2.relim()
            self.canvas.axes.cla()
            self.canvas.axes2.cla()
            
            self.canvas.axes.grid(True)
            self.canvas.axes.set_ylim([10, 40])
            self.canvas.axes.tick_params(axis='x', labelrotation=85)
            self.canvas.axes2.grid(True)
            self.canvas.axes2.set_ylim([0, 100])
            self.canvas.axes2.tick_params(axis='x', labelrotation=85)

            self.canvas.axes.set_title("Temperature Graph")
            self.canvas.axes.set_xlabel("Time")
            self.canvas.axes.set_ylabel("Temperature")

            self.canvas.axes2.set_title("Humidity Graph")
            self.canvas.axes2.set_xlabel("Time")
            self.canvas.axes2.set_ylabel("Humidity")

            # We have a reference, we can use it to update the data for that line.
            self._plot_ref.set_ydata(self.ydata)
            self._plot_ref.set_xdata(self.xdata)
            self.canvas.axes.plot(self.xdata, self.ydata, color='red', marker='.', linestyle='dashed',linewidth=2, markersize=12)
            #https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html

            self._plot_ref2.set_ydata(self.y2data)
            self._plot_ref2.set_xdata(self.x2data)
            self.canvas.axes2.plot(self.x2data, self.y2data,  color='blue', marker='.', linestyle='dashed',linewidth=2, markersize=12) 
 
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
          
        return feild_1,feild_2

class SicaklikNemData():
    def setRawDataSicaklik(self,_feild_1,kuyruk1):
     for x in _feild_1:
        _sicaklik = float(x['field1'])
        mystr=x['created_at']
        _id=mystr.replace('T',' ').replace('Z','') 
        
        kuyruk1.put((_id,_sicaklik))
    
    def setRawDataNem(self,_feild_2,kuyruk2):
     for x in _feild_2:
        _nem = float(x['field2'])
        mystr=x['created_at']
        _id=mystr.replace('T',' ').replace('Z','') 
        
        kuyruk2.put((_id,_nem))

     
def main():
    global kuyruk1,kuyruk2
    th0 = threading.Thread(target=thread_islem,args = (kuyruk1,kuyruk2),daemon=True) #Yani özetle main thread sonlandığında daemon thread çalışıyor olsa bile sonlandırılır.
    th0.start()


    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec_()

try:
    main()
except:
     TerminateProcess(GetCurrentProcess(),0)

