import cv2,time,getopt,sys
import pydtaremote_diag
import pyhik
import imageprocessor
import videoautomation
import execute
import execute_cropped
from pytesser import *
import Image,ImageChops
import subprocess
import os
import json	
image_path="C:\\EEVAA\\public\\images\\captures\\EASText.jpg"
cropped_image_path = "C:\\EEVAA\\public\\images\\captures\\Ashok1.jpeg"
received_messages_page_image = cv2.imread(image_path,0)
ecm_image = received_messages_page_image[8:96,46:600]

#pix=ecm_image.getpixel((10,10))

#im.getpixel
#ecm_image = received_messages_page_image[325:350,100:550]
cv2.imwrite(cropped_image_path,ecm_image)
"""im = Image.open(image_path)
#im = Image.open(cropped_image_path)
#rgb_im = im.convert('RGB')
r, g, b = im.getpixel((363, 71))
print r, g, b
#for raw image 
#r,g,b =im.getpixel((629,53))
#for cropped image 
r,g,b =im.getpixel((248,63))
print r, g, b"""

