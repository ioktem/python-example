from PyQt5.QtWidgets import QApplication, QMainWindow
import sys
from PyQt5.QtChart import QChart, QChartView, QLineSeries,QValueAxis,QSplineSeries,QCategoryAxis
from PyQt5.QtCore import QPointF
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

#https://doc.qt.io/qtforpython/overviews/qtcharts-multiaxis-example.html#multiple-axes-example
#https://doc.qt.io/qtforpython/overviews/qtcharts-datetimeaxis-example.html#datetimeaxis-example


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQtChart Line")
        self.setGeometry(100,100, 1080,720)

        chart = QChart()
        #chart.legend().hide()
        chart.setTitle("Multiaxis chart example")
        
        axisX = QValueAxis()
        #axisX.setTickCount(10)
        #chart.createDefaultAxes()  # x ekseni için 
        chart.addAxis(axisX, Qt.AlignBottom) #x ekseni değerleri grafiğin altına konumlandırılır

        #Grafiğin sol tarafı
        series = QLineSeries(name="Sicaklik")
        # series = QSplineSeries(name="Sicaklik")  #bağ interpolasyonu, noktalar arasında QSpline eğri, QLine çizgi oluşturur. 
        series << QPointF(1, 5) << QPointF(3.5, 6) << QPointF(4.8, 7.5) << QPointF(5, 3.5) <<QPointF(5.2, 3.5) << QPointF(7.4, 16.5) << QPointF(8.3, 7.5) << QPointF(10, 17)
        series.setPointsVisible(True) # pointler grafik üzerinde işaretlenir
        series.setPointLabelsVisible(True)   # pointler grafik üzerinde x,y koordinat şeklinde belirtilir
      
        #series.setPointLabelsFormat( "(@xPoint, @yPoint)" )  # pointler grafik üzerinde (x,y) formatında gösterilir
        series.setPointLabelsFormat( "(@yPoint)" ) 
        chart.addSeries(series)
        axisY = QValueAxis() 
        axisY.setRange(axisY.min()-1, 55) #   axisY.setRange(axisY.nmin()-1, 55)   axisY.setRange(0, 55)
        axisY.setLinePenColor(series.pen().color())  # soldaki y ekseni ile datanın rengini ilişkilendiriyor
        
        chart.addAxis(axisY, Qt.AlignLeft)
        series.attachAxis(axisX)
        series.attachAxis(axisY)
       
        #Grafiğin sağ tarafı
        series = QLineSeries(name="Nem")   # series = QSplineSeries(name="Nem")
        series << QPointF(1, 0.5) << QPointF(1.5, 4.5) << QPointF(2.4, 2.5) << QPointF(4.3, 70.5)<< QPointF(5.2, 3.5) << QPointF(7.4, 55.5) << QPointF(8.3, 7.5) << QPointF(9, 19)
        series.setPointsVisible(True)  # pointler grafik üzerinde işaretlenir
        series.setPointLabelsVisible(True)
        
        #series.setPointLabelsFormat( "(@xPoint, @yPoint)" )
        series.setPointLabelsFormat( "(@yPoint)" ) 
        chart.addSeries(series)
        axisY3 = QValueAxis()       # y ekseni etiketlerini kategori içerisine değilde normal int olarak göstermek istersen
        axisY3.setRange(axisY3.min()-1,100)
       # axisY3 = QCategoryAxis()   # y ekseni etiketlerini kategorilemek için kullanılır
       # axisY3.append("Low", 5)
       # axisY3.append("Medium", 12)
       # axisY3.append("High", 17)
        axisY3.setLinePenColor(series.pen().color())
        #axisY3.setGridLinePen((series.pen()))   # gridleri renklendiriyor
        

        chart.addAxis(axisY3, Qt.AlignRight)
        series.attachAxis(axisX)  # Y3 datası için x kordinatı tekrar ayarlanmalı
        series.attachAxis(axisY3)
       
        axisX.setRange(axisX.min()-1, axisX.max()+1)
        chart.legend().setVisible(True)  # etiketleri görünürleştirir
        chart.legend().setAlignment(Qt.AlignBottom)  #etiketi grafiğin altına konumlandırır
        #chart.setAnimationOptions(QChart.SeriesAnimations) #codu yavaşlatabilir
        
        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(chartView)
        self.show()   #yukarıda yapılanları grafik üzerine aktarmak için kullanılır yokluğunda grafik oluşmaz

        #window = QMainWindow()
        #window.setCentralWidget(chartView)
        #window.resize(800, 600)
        #window.show()

App = QApplication(sys.argv)
window = Window()
sys.exit(App.exec_())
