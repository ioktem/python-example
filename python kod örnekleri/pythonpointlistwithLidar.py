from rplidar import RPLidar
import math
import numpy as np
import open3d as o3d
import struct
import cv2

point_list=[]
store_scan=[]



lidar = RPLidar(port="COM15", baudrate=256000, timeout=3)

def AngleConvertToDistance(distance,angle):
   x=(distance/1000)*math.cos(angle*math.pi/180)
   y=(distance/1000)*math.sin(angle*math.pi/180)
   return(float(x),float(y))

def CalculateTransformMatrix(axes,vertices, theta=0):
    
    
    vertices = np.asanyarray(vertices).reshape(-1, 3)  # nx3 point cloud data, [X,Y,Z]    

    theta = math.radians(-1*theta)  # degree to radian transfor
    

    if axes == 'x':

        _R = np.array([ [1,         0,                  0,                ],
                        [0,         math.cos(theta), -math.sin(theta),    ],
                        [0,         math.sin(theta),  math.cos(theta),    ]
                        ])
    if axes == 'y':

        _R = np.array([ [math.cos(theta),    0,      math.sin(theta), ],
                        [0,                  1,      0,               ],
                        [-math.sin(theta),   0,      math.cos(theta), ]
                        ])
    if axes == 'z':                            

        _R = np.array([ [math.cos(theta),    -math.sin(theta),    0,   ],
                        [math.sin(theta),    math.cos(theta),     0,   ],
                        [0,                     0,                1,   ]
                        ])   


    # reshape rotation matrix
    matrix = np.asanyarray(_R).reshape(3, 3)    

    # multiply rotation matrix and vertices to generate new matrix rotated.    
    mylist= np.matmul(vertices,matrix)    

    mylist = np.asanyarray(mylist).reshape(-1, 3)  

    return mylist

def Transfer3DPointsTo(_points,Tx=0,Ty=0,Tz=0):
     
    Tx = np.asanyarray(Tx) * 1000
    Ty = np.asanyarray(Ty) * 1000
    Tz = np.asanyarray(Tz) * 1000
    _M = np.zeros((_points.shape[0],3)) #create nx3 matrix filled by zeros
    _M[: , 0] = Tx # Fill first coloum with Tx
    _M[: , 1] = Ty # Fill first coloum with Ty
    _M[: , 2] = Tz # Fill first coloum with Tz

    TransferMatrix = np.add(_points,_M)

    return TransferMatrix

def PreFilter3DPointsCloud(_points,HeightofLidar,MaxLengthofLidar):
    
    #RadiusofTurntable = (DiameterofTurntable - 30) / 2

    # Nokta bulutunda "proscandan dışındaki" noktaları sil
    N1 = _points[ (_points[:,0] <= HeightofLidar)]  # x sil
    N2 = N1[ (N1[:,1] <=MaxLengthofLidar)]
    
    return N2 

def calculate_heightbox_points(point_cloud):

    point_cloud = np.transpose(point_cloud)
    offset_for_max_x=100  # max x noktalarından 10cm öncesi 
    if point_cloud.shape[1] > 50:      #irfan 100 dü  

        #coord = np.c_[point_cloud[0,:], point_cloud[2,:]].astype('float32')
        #min_area_rectangle = cv2.minAreaRect(coord) 
        #bounding_box_world_2d = cv2.boxPoints(min_area_rectangle)
        #Caculate the height of the pointcloud
        #Burada amaç ürün boyutu hesaplama 
        #z düzleminde max değerden küçük ikinci değer aynı zamanda x ekseninde ise karşı düz duvardan 10cm önce 
        max_height = max(point_cloud[2,:]) #- min(point_cloud[2,:])  
        max_length = max(point_cloud[0,:])-offset_for_max_x # max x noktalarından 10cm öncesi   
        min_height = min(point_cloud[2,:])

        #min değer eğer negatifse z ekseni 0 a çekilir
        if min(point_cloud[2,:])<0:
         for i in range(len(point_cloud[2,:])):
             point_cloud[2,i]-=min_height
             

        product_height = min(point_cloud[2,:])
        #if product_height<10:
        # return 0

        for i in range(len(point_cloud[2,:])):
         if point_cloud[0,i]<max_length:
            if point_cloud[2,i]>product_height:
             product_height= point_cloud[2,i]         
         
         
        
        
        return product_height 

    else : 
        return 0  


def CalculateDesi(length,width,height):
    vol = float(int(((length/100))*((width/100))*((height/100))*100)/100)
    return vol 


def FloatFormat(numb:float,aftercomma:int):

    number = int(numb * pow(10,aftercomma))
    number = float(number / pow(10,aftercomma))
    return number



info = lidar.get_info()
print(info)

health = lidar.get_health()
print(health)



while(1):
 
 cnt=0
 for i, scan in enumerate(lidar.iter_scans()):
     print('%d: Got %d measurments' % (i, len(scan)))
     if cnt < 10:
         store_scan.extend(scan)
     else:
        break
     cnt+=1
 
 
 for a in range(len(store_scan)):
     
     angle=float(store_scan[a][1])
     distance=float(store_scan[a][2])
     if angle>33 and angle<90:
       x,y=AngleConvertToDistance(distance,angle)
       point=[x,y,0.1]
       point_list.append(point)
       
 print(a)
    
 point_list = np.asanyarray(point_list)*1000
 
 Transfered_vector = Transfer3DPointsTo(point_list,Tx=0,Ty=0,Tz=0)
 
 # Lidar 0 derece aşağı bakarken Z ekseni kapağa bakarken,(konumlandırma)
 _m0 = PreFilter3DPointsCloud(Transfered_vector,700,1000)  #Lidar Yüksekliği,Lidarın göreceği Proscan in Max Eni,
 _m1 = CalculateTransformMatrix("x",_m0,0) #self.RotationAngleX
 _m2 = CalculateTransformMatrix("y",_m1,90) #self.RotationAngleY
 _m3 = CalculateTransformMatrix("z",_m2,-90) #self.RotationAngleZ
 
 
 points = np.asarray(_m3)
 
 height = calculate_heightbox_points(points) 
             
 height = FloatFormat(height,1)
             
 #Volume=CalculateDesi(length,width,height)
 print("height:")
 print(height)
 
 lidar.stop()
 lidar.stop_motor()
 lidar.disconnect()
 
 
 s = struct.pack("fffccc",points[0][0],points[0][1],points[0][2],bytes(chr(127),"utf-8"),bytes(chr(0),"utf-8"),bytes(chr(0),"utf-8"))
 print(s)
 #point_list
 
 filename = "C:\\Users\\i.oktem\\Desktop\\lidar.ply"
 fid = open(filename,'wb')
 fid.write(bytes('ply\n', 'utf-8'))
 fid.write(bytes('format binary_little_endian 1.0\n', 'utf-8'))
 fid.write(bytes('element vertex %d\n' % len(points), 'utf-8'))
 fid.write(bytes('property float x\n', 'utf-8'))
 fid.write(bytes('property float y\n', 'utf-8'))
 fid.write(bytes('property float z\n', 'utf-8'))
 fid.write(bytes('property uchar red\n', 'utf-8'))
 fid.write(bytes('property uchar green\n', 'utf-8'))
 fid.write(bytes('property uchar blue\n', 'utf-8'))
 fid.write(bytes('end_header\n', 'utf-8'))
 # Write 3D points to .ply file
 for xyz_points in points:
     fid.write(bytearray(struct.pack("fffccc",xyz_points[0],xyz_points[1],xyz_points[2],bytes(chr(0),"utf-8"),bytes(chr(0),"utf-8"),bytes(chr(0),"utf-8"))))
 
 fid.close()
 
 print("Load a ply point cloud, print it, and render it")
 pcd = o3d.io.read_point_cloud("C:\\Users\\i.oktem\\Desktop\\lidar.ply")
 print(pcd)
 #print(np.asarray(pcd.points))
 o3d.visualization.draw_geometries([pcd])
 