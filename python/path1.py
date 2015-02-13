from pytesser import *
import Image,ImageChops
image = Image.open('C:\\EEVAA\\public\\images\\captures\\test901.jpg') # Open image object using PIL
print image_file_to_string('C:\\EEVAA\\public\\images\\captures\\test901.jpeg','C:\\EEVAA\\public\\images\\captures\\test901.txt')
