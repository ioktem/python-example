#Arka plan beyaz olan resimde 2 adet yuvarlak yeşil buton olmalı bunların konumunu bulmamızı sağlar.
import numpy as np
import cv2 as cv
import time

img = cv.imread('./Images3.jpg',cv.IMREAD_COLOR) # bir klasör oluştur bu kodu ve resmi aynı klasöre koy 
img= cv.resize(img, (1920,1080),interpolation = cv.INTER_AREA) #INTER_CUBIC  INTER_AREA  INTER_LINEAR 1920, 1080 Ekrana sığması için resmi boyutlandırdık
img = cv.medianBlur(img,5) # yeşil daireler içindeki sapmaları en aza indirir. 

window_name2 = "RGB Color Image"
cv.namedWindow(window_name2)
cv.imshow(window_name2, img) # Input olarak verilen resmin görüntüsü

img = cv.cvtColor(img , cv.COLOR_RGB2BGR) 
# Convert BGR to HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

uh = 72
us = 255
uv = 255
lh = 51
ls = 125
lv = 72
lower_hsv = np.array([lh,ls,lv])
upper_hsv = np.array([uh,us,uv])
# Threshold the HSV image to get only green colors
# Filter the image and get the binary mask, where white represents 
# your target color
mask = cv.inRange(hsv, lower_hsv, upper_hsv)
window_name = "HSV Calibrator"
cv.namedWindow(window_name)

def nothing(x):
    print("Trackbar value: " + str(x))
    pass

# create trackbars for Upper HSV
cv.createTrackbar('UpperH',window_name,0,255,nothing)
cv.setTrackbarPos('UpperH',window_name, uh)

cv.createTrackbar('UpperS',window_name,0,255,nothing)
cv.setTrackbarPos('UpperS',window_name, us)

cv.createTrackbar('UpperV',window_name,0,255,nothing)
cv.setTrackbarPos('UpperV',window_name, uv)

# create trackbars for Lower HSV
cv.createTrackbar('LowerH',window_name,0,255,nothing)
cv.setTrackbarPos('LowerH',window_name, lh)

cv.createTrackbar('LowerS',window_name,0,255,nothing)
cv.setTrackbarPos('LowerS',window_name, ls)

cv.createTrackbar('LowerV',window_name,0,255,nothing)
cv.setTrackbarPos('LowerV',window_name, lv)

font = cv.FONT_HERSHEY_SIMPLEX

contours, _ = cv.findContours(mask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) #beyaz renk ile işaretlenmiş noktalar

center_coord = []

for cnt in contours:
    area = cv.contourArea(cnt)

    counter = 0
    xfin = 0 ; yfin=0; wfin=0; hfin=0
    xavg=0;yavg=0;wavg=0;havg=0

    if area > 100:
        print("bulundu")
        cv.drawContours(hsv,[cnt],-1,(255,255,255),2)
    
        window_name3 = "hsv"
        cv.namedWindow(window_name3)
        cv.imshow(window_name3,hsv)

        x,y,w,h = cv.boundingRect(cnt)
        xavg = xavg + x 
        yavg = yavg + y 
        wavg = wavg + w 
        havg = havg + h 

        #rect_coord[counter] = ([x,y],[x+w,y],[x,y+h],[x+w,y+h])
        center_coord.append( [(wavg/2)+xavg,(havg/2)+yavg])
        #center_coord[counter] = [(wavg/2)+xavg,(havg/2)+yavg]
        counter = counter + 1
            
        print("x: " + str(x) + "    y: " + str(y) + "    w: " + str(w)+    "   h:"  + str(h))
        cv.rectangle(mask,(x,y),(x+w,y+h),(255,255,255),1)
        window_name4 = "rectangle"
        cv.namedWindow(window_name4)
        cv.imshow(window_name4,mask)


if(counter >= 3):
    print("2 den fazla nokta var")
    
cv.putText(img, "Y coord: " + str(center_coord[0][1]), (20,20), cv.FONT_HERSHEY_PLAIN, 2, (0,0,255) )
cv.putText(img, "Y2 coord: " + str(center_coord[1][1]), (20,40), cv.FONT_HERSHEY_PLAIN, 2, (0,0,255) )
cv.putText(img, "distance between two point: " + str(abs(center_coord[1][1]-center_coord[0][1])), (20,60), cv.FONT_HERSHEY_PLAIN, 2, (0,0,255) )



cv.circle(img,(int(center_coord[0][0]),int(center_coord[0][1])), 20, (0,0,255), 2)   
cv.circle(img,(round(center_coord[0][0]),int(center_coord[0][1])), 1, (255,0,0), 1)  
cv.circle(img,(int(center_coord[1][0]),int(center_coord[1][1])), 20, (0,0,255), 2)   
cv.circle(img,(round(center_coord[1][0]),int(center_coord[1][1])), 1, (255,0,0), 1)   
window_name5 = "rectangle img"
cv.namedWindow(window_name5)
cv.imshow(window_name5,img)
            

while(1):
    # Threshold the HSV image to get only blue colors
    mask = cv.inRange(hsv, lower_hsv, upper_hsv)
    cv.putText(mask,'Lower HSV: [' + str(lh) +',' + str(ls) + ',' + str(lv) + ']', (10,30), font, 0.5, (200,255,155), 1, cv.LINE_AA)
    cv.putText(mask,'Upper HSV: [' + str(uh) +',' + str(us) + ',' + str(uv) + ']', (10,60), font, 0.5, (200,255,155), 1, cv.LINE_AA)

    cv.imshow(window_name,mask)

    k = cv.waitKey(1) & 0xFF
    if k == 27:
        break
    # get current positions of Upper HSV trackbars
    uh = cv.getTrackbarPos('UpperH',window_name)
    us = cv.getTrackbarPos('UpperS',window_name)
    uv = cv.getTrackbarPos('UpperV',window_name)
    upper_blue = np.array([uh,us,uv])
    # get current positions of Lower HSCV trackbars
    lh = cv.getTrackbarPos('LowerH',window_name)
    ls = cv.getTrackbarPos('LowerS',window_name)
    lv = cv.getTrackbarPos('LowerV',window_name)
    upper_hsv = np.array([uh,us,uv])
    lower_hsv = np.array([lh,ls,lv])

    time.sleep(.1)

cv.destroyAllWindows()
