import cv2
#import cv2 numpy as np

image=cv2.imread('C:\\Users\\i.oktem\\Desktop\\New folder (3)\\0.png')    #kırpmakistediğim görüntünün bilgisayarımda ki konumunu belirtiyorum
image= cv2.resize(image, (1280,720), interpolation = cv2.INTER_AREA) #irfan yüksek kaliteli frame video modu için dönüştürüldü    
#ConvertToQtFormat = QImage(DisplayedRGBFrame.data, window_size[0],window_size[1], QImage_Format)
#Pic = ConvertToQtFormat.scaled(self.myparent.cameraframewidth, self.myparent.cameraframeheight) 

height, width = image.shape[:2]

start_row, start_col=int(height * .05), int(width * .30)      #kırpmak istediğiniz boyuta göre değerler verebilirsiniz

end_row, end_col=int(height * .75), int(width * .75)

#cropped=image[start_row:end_row , start_col:end_col]
cropped=image[160:560, 0:840 ]  # dikey(0 sol üstten başlar) , yatay (0 sol üstten başlar)

cv2.imshow("Original Image", image)     #açılan pencerede ilk orjinal görüntümüz açılır
cv2.imshow("Cropped Image", cropped)   #çarpıya tıkladığımız da ise kırpılmış görüntü ile karşılaşırız

cv2.waitKey(0)

cv2.imshow("Cropped Image", cropped)   #çarpıya tıkladığımız da ise kırpılmış görüntü ile karşılaşırız

cv2.waitKey(0)

cv2.destroyAllWindows()