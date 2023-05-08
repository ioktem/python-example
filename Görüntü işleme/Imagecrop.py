import cv2
#import cv2 numpy as np

image=cv2.imread('C:\\Users\\i.oktem\\Desktop\\New folder (3)\\0.png')    #kırpmakistediğim görüntünün bilgisayarımda ki konumunu belirtiyorum
h, w, _ = image.shape
print('width: ', w)
print('height:', h)

#https://note.nkmk.me/en/python-opencv-pillow-image-size/
print('width: ', image.shape[1])
print('height:', image.shape[0])


image= cv2.resize(image, (1280,720), interpolation = cv2.INTER_AREA) #irfan yüksek kaliteli frame video modu için dönüştürüldü    

height, width = image.shape[:2]

start_row, start_col=int(height * .05), int(width * .30)      #kırpmak istediğiniz boyuta göre değerler verebilirsiniz

end_row, end_col=int(height * .75), int(width * .75)

#cropped=image[start_row:end_row , start_col:end_col]
cropped=image[160:560, 0:840 ]  # dikey(0 sol üstten başlar) , yatay (0 sol üstten başlar)

cv2.imshow("Original Image", image)     #açılan pencerede ilk orjinal görüntümüz açılır
cv2.waitKey(0) #açılan pencereyi kapattığımızda ise kırpılmış görüntü ile karşılaşırız

# Filename
filename = 'savedImage.jpg'
  
# Using cv2.imwrite() method
# Saving the image
cv2.imwrite(filename, cropped)  # kesilen fotograf masaüstğne kaydedildi.

cv2.imshow("Cropped Image", cropped)   
cv2.waitKey(0)

cv2.destroyAllWindows()