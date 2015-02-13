import os
import itertools
from pytesser import *
import Image,ImageChops
import subprocess
import multiprocessing
from multiprocessing import Queue

__author__ = 'anganesa'

# code to run the tesseract -psm  6 command with the cropped image captured from  DTA  

def worker(work_queue,done_queue):
    cropped_image_path=work_queue.get()
    testName=work_queue.get()
    print "inside execute emm function to extrace text"
    
    print cropped_image_path
    cropped_image_path_split = 'C:\\EEVAA\\public\\images\\captures\\'
    print "inside execute emm "
    cropped_image_path=cropped_image_path_split+cropped_image_path
    print "image path inside tessract exe is "
    print cropped_image_path
    file_path=cropped_image_path_split+testName
    file_path1=file_path + ".txt"
    
    
    
    """image_path='C:\\EEVAA\\public\\images\\captures\\try2.jpeg'
    file_path='C:\\EEVAA\\public\\images\\captures\\try2'
    file_path1='C:\\EEVAA\\public\\images\\captures\\testtry123' + ".txt"""
    
    command1='tesseract -psm 6'
    command=command1 + " " + cropped_image_path + " " + file_path

    print command1
    print "command is "
    print command 
    #print subprocess.call('cd C:\Program Files (x86)\Tesseract-OCR', shell=True)
    #os.system("start {cmd.exe cd C:\Program Files (x86)\Tesseract-OCR}")
    
    #os.popen("cd C:\Program Files (x86)\Tesseract-OCR")
    print subprocess.call(command,shell=True)
    #print os.system(command)
    file = open(file_path1, 'r')
    data = file.readlines()
    print data
    done_queue.put(data)
    return

def emm(cropped_image_path,testName):
    # the function that is called from the pydta.py code for executing the tesseract command 
     jobs=[]
     # Queue for storing the image path and the txt file name 
     work_queue = Queue()
     # queue for storing the text file location after extraction process is spawned 
     done_queue=Queue()
     

     print " inside emm function "
     print cropped_image_path
     image_path_split = cropped_image_path.split('\\')
     data_field=image_path_split[3]
     
     work_queue.put(image_path_split[5])
     work_queue.put(testName)
                  
     
          #work_queue.put(image_path)
     # spawn the process for calling the exe to execute the command for converting in to text     
     p = multiprocessing.Process(target=worker,args=(work_queue,done_queue))
     jobs.append(p)
     p.start()
     #data=work_queue.get()
     #file = open(file_path1, 'r')
     #data = file.readlines()
     # extract the data from the file read and stored 
     data=done_queue.get()
     print data
     return data
     

