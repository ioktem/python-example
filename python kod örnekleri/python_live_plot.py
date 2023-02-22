import sys
import matplotlib
matplotlib.use('Qt5Agg')
import random
from matplotlib.ticker import FixedLocator, NullFormatter


from PyQt5 import QtCore, QtGui, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt5.QtCore import Qt,QDateTime
import urllib.request
import requests
import threading


from matplotlib.widgets import Button

t=[]  # thingspeakten gelen veriler kullanmaya hazır şekilde  bu dizide tutulur
t2=[] # thingspeakten gelen veriler kullanmaya hazır şekilde  bu dizide tutulur


class SicaklikNemData():
    def getRawDataSicaklik(self):
     for data in t:
         index = data[0]
         sicaklik = data[1]

     return t 
    
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
  


class Index():
    #ind = 0

    def next(self, event):
        #self.ind += 1
        print("next button")
        #i = self.ind % len(freqs)
        #ydata = np.sin(2*np.pi*freqs[i]*t)
        #l.set_ydata(ydata)
        #plt.draw()

    def prev(self, event):
        #self.ind -= 1
        print("prev button")
        #i = self.ind % len(freqs)
        #ydata = np.sin(2*np.pi*freqs[i]*t)
        #l.set_ydata(ydata)
        #plt.draw()



class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor='white', edgecolor='green',linewidth=5)
        fig.subplots_adjust(left=0.2) #grafiğin sol tarafında boşluk oluşturuldu
        self.axes = fig.add_subplot(111)
        self.axes.grid(True)
        self.axes.set_ylim([10, 40])
        #self.axes.format_xdata()
       # self.axes.yaxis.set_minor_formatter(NullFormatter())
        

        self.callback = Index()
        axprev = fig.add_axes([0.02, 0.9, 0.05, 0.05])
        axnext = fig.add_axes([0.10, 0.9, 0.05, 0.05])
        self.bnext = Button(axnext, 'Next')
        self.bnext.on_clicked(self.callback.next)
        self.bprev = Button(axprev, 'Previous')
        self.bprev.on_clicked(self.callback.prev)
            
    
        super(MplCanvas, self).__init__(fig)

 

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=20, height=16, dpi=100)    
        self.setCentralWidget(self.canvas)

        n_data = 20
        self.xdata = list(range(n_data))
        self.ydata = [random.randint(0, 10) for i in range(n_data)]



        # We need to store a reference to the plotted line
        # somewhere, so we can apply the new data to it.
        self._plot_ref = None
        self.update_plot()

         # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.canvas, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(self.canvas)
        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)
        self.show()

        # Setup a timer to trigger the redraw by calling update_plot.
        self.timer = QtCore.QTimer()
        self.timer.setInterval(15000)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

    def update_plot(self):
        # Drop off the first y element, append a new one.
        #self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        feild_1,__=Thingspeak.read_data_thingspeak()  # thinkspeakten 20 adet veri alınır
        SicaklikNemDataClass.setRawDataSicaklik(feild_1)
        t3=SicaklikNemDataClass.getRawDataSicaklik()
        self.ydata.clear()
        
        for x in t3:                 
         self.ydata.append(x[1])
        
        t3.clear() # veri kopyalama işlemi bittiyse sil çünkü append ile ekleme yapıyosun taşma yapar
        
        
       
        # Note: we no longer need to clear the axis.
        if self._plot_ref is None:
            # First time we have no plot reference, so do a normal plot.
            # .plot returns a list of line <reference>s, as we're
            # only getting one we can take the first element.
            plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
            #self.canvas.axes.plot(self.xdata, self.ydata, '.')
            self.canvas.axes.set_title("Temperature Graph")
            self.canvas.axes.set_xlabel("Time")
            self.canvas.axes.set_ylabel("Temperature")
            #self.canvas.axes.set_xscale()
            self._plot_ref = plot_refs[0]
        else:
            # We have a reference, we can use it to update the data for that line.
            self._plot_ref.set_ydata(self.ydata)
          
        #self.canvas.axes.plot(self.xdata, self.ydata, '.')  
        # Trigger the canvas to update and redraw.
        self.canvas.draw()
        



     #  sc = MplCanvas(self, width=5, height=4, dpi=100)
     #  sc.axes.plot([0,1,2,3,4], [10,1,20,3,40])

      
     #  layout = QtWidgets.QVBoxLayout()
     #  layout.addWidget(toolbar)
     #  layout.addWidget(sc)

     #  # Create a placeholder widget to hold our toolbar and canvas.
     #  widget = QtWidgets.QWidget()
     #  widget.setLayout(layout)
     #  self.setCentralWidget(widget)

     #  self.show()


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()