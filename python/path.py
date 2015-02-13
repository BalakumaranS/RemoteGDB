from pytesser import *
import Image,ImageChops
text=[]
image_path='C:\\EEVAA\\public\\images\\captures\\test903.jpeg'

print "inside tesser function "
print "image_path value is "
print image_path
file_path='C:\\EEVAA\\public\\images\\captures\\test902'
print "text file path "
print file_path
im = Image.open(image_path)
print " after image open "
#im=call_tesseract(image_path, file_path)
text = image_to_string(im)
print text
#text=image_file_to_string(im)
#Image.close()
#file = open('C:\\EEVAA\\public\\images\\captures\\test902.txt', 'r')
#data = file.readlines()
#print len(data)
"""data1= data[11:12]
data2= data[29:30]

#print data[29:30]
data3= data1 + data2
print "EMM Count is "
print data3
#return data3"""
"""data2="EMM"
for data2 in range(len[data]):
    i=i+1"""
    
#print data

#file.close()    
