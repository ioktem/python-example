#Arka plan beyaz olan resimde 2 adet yuvarlak yeşil buton olmalı bunların konumunu bulmamızı sağlar.
import numpy as np
import cv2 as cv
import time

# -------------Images Input Method 1-------------------------
#Görüntü sisteme bağlı kameradan, real time olarak alınır.

# define a video capture object
cap = cv.VideoCapture(0)

if not (cap.isOpened()):
   print("Could not open video device")
   # To set the resolution

cap.set(3,4656)
cap.set(4,3496)

# Capture the video frame
    # by frameq
ret, img = cap.read()
time.sleep(2)     #Kamera açılır açılmaz görüntü almayın 2 saniye gecikme ekleyin.Bu görüntüde netlik kazandıracaktır. Olmazsa camerayı açıp nesneye odaklayın sonra kodu çalıştırın.
ret, img = cap.read()

  
    # Display the resulting frame
#cv.imshow('frame', frame) # bunu kapatabilirsin zaten görüntü çok büyük olacak

# -------------Images Input Method 2-------------------------
#Görüntü bir resim olarak çalışma klasöründen çekilir.

#img = cv.imread('./Images3.jpg',cv.IMREAD_COLOR) # bir klasör oluştur bu kodu ve resmi aynı klasöre koy 
#img= cv.resize(img, (1280, 720),interpolation = cv.INTER_AREA) #INTER_CUBIC  INTER_AREA  INTER_LINEAR 1920, 1080  4656,3496 Ekrana sığması için resmi boyutlandırdık



img = cv.medianBlur(img,5) # yeşil daireler içindeki sapmaları en aza indirir.
window_name2 = "RGB Color Image"
cv.namedWindow(window_name2)
cv.imshow(window_name2, img) # Input olarak verilen resmin görüntüsü

img = cv.cvtColor(img , cv.COLOR_RGB2BGR) 
# Convert BGR to HSV
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# görüntü yaklaştığında ışık zayıf olunca renk değişiyor tekrar ayarlandı.
uh =80 #81 #63 #72
us = 255
uv = 255
lh = 44#47 #56 #51
ls = 167 #167 #210 #125
lv = 36#24 #29 #72
lower_hsv = np.array([lh,ls,lv])
upper_hsv = np.array([uh,us,uv])
# Threshold the HSV image to get only green colors
# Filter the image and get the binary mask, where white represents 
# your target color
mask = cv.inRange(hsv, lower_hsv, upper_hsv)

font = cv.FONT_HERSHEY_SIMPLEX

contours, _ = cv.findContours(mask,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE) #beyaz renk ile işaretlenmiş noktalar

center_coord = []
counter = 0

for cnt in contours:
    area = cv.contourArea(cnt)

    xfin = 0 ; yfin=0; wfin=0; hfin=0
    xavg=0;yavg=0;wavg=0;havg=0

    #Kameradan 34 cm uzakta tabladan 2cm içeride, çapı 12mm olan yeşil buton tam arasında (4656,3496) çözünürlükte areası (12626-12340) ölçüldü.(Area>5000)Noktalar arası pixel sayısı 1092.0
    #Kameradan 61.5 cm uzakta, çapı 12mm olan yeşil buton tam ortada(4656,3496) çözünürlükte areası (4340-4640) ölçüldü.(Area>3000)Noktalar arası pixel sayısı 597.0
    #Kameradan 58.5 cm uzakta, çapı 12mm olan yeşil buton tam orta (4656,3496) çözünürlükte areası (4340-4640) ölçüldü.(Area>3000)Noktalar arası pixel sayısı 629
   
    #Kameradan 59 cm uzakta,tabladan 26.5cm içeride çapı 12mm olan yeşil buton tam orta (4656,3496) çözünürlükte areası (8340-9640) ölçüldü.(Area>3000)Noktalar arası pixel sayısı 2178
    #Kameradan 40.2 cm uzakta,tabladan 8cm içeride çapı 12mm olan yeşil buton tam orta (4656,3496) çözünürlükte areası (8340-9640) ölçüldü.(Area>3000)Noktalar arası pixel sayısı 3202
    #Kameradan 61.5 cm uzakta, çapı 12mm olan yeşil buton (1920x1080) çözünürlükte areası (549-288.5) ölçüldü.(Area>500) Noktalar arası pixel sayısı 250
    #Kameradan 61.5 cm uzakta, çapı 12mm olan yeşil buton (1280x720) çözünürlükte areası (241-143) ölçüldü.(Area>150) Noktalar arası pixel sayısı 167.5

    if area > 3000:
        print("bulunan area: "+ str(area))
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

if(counter == 0):
    print("Area kontrolü yapın")

else:
    cv.putText(img, "Y coord: " + str(center_coord[0][1]), (20,20), cv.FONT_HERSHEY_PLAIN, 2, (0,0,255) )
    cv.putText(img, "Y2 coord: " + str(center_coord[1][1]), (20,40), cv.FONT_HERSHEY_PLAIN, 2, (0,0,255) )
    cv.putText(img, "distance between two point: " + str(abs(center_coord[1][1]-center_coord[0][1])), (20,60), cv.FONT_HERSHEY_PLAIN, 2, (0,0,255) )
    #iki nokta bulunduğuna emin olunuz.
    print("distance between two point:" + str(abs(center_coord[1][1]-center_coord[0][1])))

    cv.circle(img,(int(center_coord[0][0]),int(center_coord[0][1])), 20, (0,0,255), 2)   
    cv.circle(img,(round(center_coord[0][0]),int(center_coord[0][1])), 1, (255,0,0), 1)  
    cv.circle(img,(int(center_coord[1][0]),int(center_coord[1][1])), 20, (0,0,255), 2)   
    cv.circle(img,(round(center_coord[1][0]),int(center_coord[1][1])), 1, (255,0,0), 1)   
    window_name5 = "rectangle img"
    cv.namedWindow(window_name5)
    cv.imshow(window_name5,img)

# Filename
filename = 'CalculatedDistance2Point.jpg'
  
# Using cv2.imwrite() method
# Saving the image
cv.imwrite(filename,img)  # kesilen fotograf çalışma dosyasına kaydedildi.
            
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
# bar çubuklarını kullanmak için çözünürlük 1080,720 yapın

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



# aşağıdaki kodda pc ye bağlı cameradan görüntüyü alırsın 
"""
# import the opencv library
import cv2
  
  
# define a video capture object
cap = cv2.VideoCapture(0)

if not (cap.isOpened()):
   print("Could not open video device")
   # To set the resolution

cap.set(3, 4656)
cap.set(4, 3496)

# çok büyük görüntü 
  
while(True):
      
    # Capture the video frame
    # by frameq
    ret, frame = cap.read()
  
    # Display the resulting frame
    cv2.imshow('frame', frame)
      
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
cap.release()
# Destroy all the windows
cv2.destroyAllWindows()

"""

# arduinodaki map fonksiyon
"""
def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
  
print(map_range(12, 0,100,0,50)) 

"""