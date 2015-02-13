import os
import itertools
from pytesser import *
import Image,ImageChops
import subprocess
import multiprocessing
from multiprocessing import Queue


def worker(work_queue):
    image_path=work_queue.get()
    testName=work_queue.get()
    print "inside execute emm function to extrace text"
    
    print image_path
    image_path_split = 'C:\\EEVAA\\public\\images\\captures\\'
    print "inside execute emm "
    image_path=image_path_split+image_path
    print "image path inside tessract exe is "
    print image_path
    file_path=image_path_split+testName
    file_path1=file_path + ".txt"
    
    
    
    """image_path='C:\\EEVAA\\public\\images\\captures\\try2.jpeg'
    file_path='C:\\EEVAA\\public\\images\\captures\\try2'
    file_path1='C:\\EEVAA\\public\\images\\captures\\testtry123' + ".txt"""
    
    command1='tesseract -psm 6'
    command=command1 + " " + image_path + " " + file_path

    print command1
    print "command is "
    print command 
    #print subprocess.call('cd C:\Program Files (x86)\Tesseract-OCR', shell=True)
    #os.system("start {cmd.exe cd C:\Program Files (x86)\Tesseract-OCR}")
    
    #os.popen("cd C:\Program Files (x86)\Tesseract-OCR")
    print subprocess.call(command,shell=True)
    #print os.system(command)
    #file = open(file_path1, 'r')
    #data = file.readlines()
    #work_queue.put(data)
    return

def emm(image_path,testName):
    
     jobs=[]
     work_queue = Queue()
     

     print " inside emm function "
     print image_path
     image_path_split = image_path.split('\\')
     data_field=image_path_split[3]
     
     work_queue.put(image_path_split[5])
     work_queue.put(testName)
                  
     
          #work_queue.put(image_path)

     p = multiprocessing.Process(target=worker,args=(work_queue,))
     jobs.append(p)
     p.start()
     #data=work_queue.get()
     #file = open(file_path1, 'r')
     #data = file.readlines()
     #print data
    
     return "pass"
     

