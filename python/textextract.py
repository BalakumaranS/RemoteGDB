import os
import itertools
from pytesser import *
import Image,ImageChops
import subprocess
import multiprocessing
from multiprocessing import Queue

__author__ = 'anganesa'

# code to run the tesseract -psm  6 command with the cropped image captured from  DTA  

def worker():
    image1="C:\\frame1.jpeg"
    image2="C:\frame.jpg"
    fileop=open("C:\output.txt","a")
    filesave="C:\Result.txt"
    command1='tesseract -psm 6'
    command=command1 + " " + image1 + " " + filesave
    #f=open("C:\Result.txt","r")
    #a=f.readlines()
    #print a
    #fileop.write(a)
    #f.close()
    #command=command1 + " " + image2 + " " + filesave
    #f=open(filesave,"r")
    #a=f.readlines()
    #fileop.write(a)
    #f.close()
    
    #fileop.close()

    
    print subprocess.call(command,shell=True)
    #print os.system(command)
    return

if __name__ == '__main__':
    # the function that is called from the pydta.py code for executing the tesseract commandQueue for storing the image path and the txt file name 
                  
     
          #work_queue.put(image_path)
     # spawn the process for calling the exe to execute the command for converting in to text     
     p = multiprocessing.Process(target=worker)
     #jobs.append(p)
     p.start()
     #data=work_queue.get()
     #file = open(file_path1, 'r')
     #data = file.readlines()
     # extract the data from the file read and stored 
     

