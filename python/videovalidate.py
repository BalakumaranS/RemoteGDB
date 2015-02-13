from pytesser import *
import Image,ImageChops
def emm(image_path) :
    
    text=[]
    image_path='C:\EEVAA\public\images\captures\test901.jpeg'
    print "inside tesser function "
    print "image_path value is "
    print image_path
    file_path='C:\EEVAA\public\images\captures\image_emm'
    print "text file path "
    print file_path
    im = open(image_path,'r')
    print " after image open "
    im=call_tesseract(image_path, file_path)
    #text = image_to_string(im)
    text=image_file_to_string(im)
    #Image.close()
    file = open('C:\EEVAA\public\images\captures\test901', 'r')
    data = file.readlines()
    data1= data[11:12]
    data2= data[29:30]
    #print data[11:12]
    #print data[29:30]
    data3= data1 + data2
    print "EMM Count is "
    print data3
    return data3
    #file.close()

