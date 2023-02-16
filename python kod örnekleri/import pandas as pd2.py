import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation

#https://www.youtube.com/watch?v=QeO6THdGJvQ
data=((1,2),(3,6),(6,9),(12,6))

x=[]
y=[]
for i in data:
    x.append(i[0])
    y.append(i[1])
 

def draw_graph(i):

 plt.cla()
 plt.scatter(x,y)
 plt.plot(x,y)
      
    
anima= animation.FuncAnimation(plt.gcf(),draw_graph,interval=10)

plt.show()