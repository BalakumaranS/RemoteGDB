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

################################
### Global variables ###
################################
hikip = "10.78.203.159"
hikport = 8000
hikuser = "admin"
hikpwd = "12345"
refimages = {
#'EMM':'refs\\images\\_RefDTAEmm_Zero.jpeg',
#'EMM':'refs\\images\\_RefDTAEmm_Zero.jpg',
'EMM':'refs\\images\\little2.jpeg',
#'NA':'refs\\images\\_RefDTANot_Authorized.jpeg',
'NA':'refs\\images\\Not_Authorized.jpeg',
 'ECM':'refs\\images\\test_ecm2.jpeg'
}

def pointer_pos_received_messages(prmt):
    for x in range(0,3):
        prmt.channel_down()
        time.sleep(2)
    prmt.enter()
	
def pointer_pos_default(prmt):
	prmt.last()
	for x in range(0,3):
		prmt.channel_up()
		time.sleep(2)

def TC_Messages_Clear(channelNo,testName,dtaChannelNo = None):
	#prmt = pydtaremote.PyRemote("172.18.28.171",4002,3,3)
	prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,100)
	#pointer_pos_received_messages(prmt)
	prmt.send_digit(0)
	#pointer_pos_default(prmt)
	
def TC_EMM_Verify_old(channelNo,testName,dtaChannelNo = None):
    # exit from diag if pointing to
    
    prmt= pydtaremote_diag.PyRemote('10.78.203.158', 4002, 0, 1)
    prmt.channel_tune(7)
    prmt.disconnect()

    # diag navigate long press of 7 followed by 6 down key and enter for EMM Count page
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,100)
    #prmt = pydtaremote_diag.PyRemote("172.18.28.171",4002,3,3)
    #pointer_pos_received_messages(prmt)
    prmt.diag_messages()
    prmt.disconnect()
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,1)
    prmt.diag_navigate1()
    #pointer_pos_received_messsages(prmt)
    prmt.disconnect()
    

    #time.sleep(3)
	
    channelNo = int(channelNo)
    increment = False
    for x in range(3):
		image_path = pyhik.captureDTADiag(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg')
		print image_path
		image_path_split = image_path.split('\\')
		print image_path_split
		image_path_split[-1] = testName+'2.jpeg'
		cropped_image_path = '\\'.join(image_path_split)
		print cropped_image_path
		time.sleep(3)
		received_messages_page_image = cv2.imread(image_path,0)
		#emm_image = received_messages_page_image[300:325,100:550]
		emm_image = received_messages_page_image[265:285,100:550]
		cv2.imwrite(cropped_image_path,emm_image)
		
		
		inc_value = videoautomation.testImgSimilar(cropped_image_path,refimages['EMM'])
		print inc_value
                """ for Old DTA BOX """
		#if inc_value > 0.514:
		#	increment = True
                """ For DTA 170 BOX """
		if inc_value > 1.1:
                    increment = True
    if increment is False:
		print "[Output: Message did not increment]"
		print increment
    else:
		print "[Output: Message incremented]"
		print increment

 


def TC_Barker_Verify(channelNo,testName,dtaChannelNo):
    #prmt = pydtaremote.PyRemote("172.18.28.171",4002,3,3)
    #prmt.channel_tune(int(dtaChannelNo))
    prmt= pydtaremote_diag.PyRemote('10.78.203.158', 4002, 0, 1)
    
	
    channelNo = int(channelNo)
    prmt.channel_tune(int(dtaChannelNo))
    time.sleep(5)
    prmt.disconnect()
    barker = False
    for x in range(3):
		image_path = pyhik.captureDTADiag(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg')
		image_path_split = image_path.split('\\')
		image_path_split[-1] = testName+'2.jpeg'
		cropped_image_path = '\\'.join(image_path_split)
		dta_na_image = cv2.imread(image_path,0)
		# for DTA 170 BOX 
		#dta_na_barker_image = dta_na_image[55:95,400:750]
		dta_na_barker_image = dta_na_image[180:250,400:770]
		cv2.imwrite(cropped_image_path,dta_na_barker_image)
		ba_value = videoautomation.testImgSimilar(cropped_image_path,refimages['NA'])
		if ba_value < 1.5:
			barker = True
    if barker is False:
		print "[Output: Authorized channel]"
    else:
		print "[Output: Not Authorized channel]"
		
def TC_VideoPresence(channelNo,testName,dtaChannelNo):
    #prmt = pydtaremote.PyRemote("172.18.28.171",4002,3,3)
    #prmt.channel_tune(int(dtaChannelNo))
    prmt= pydtaremote_diag.PyRemote('10.78.203.158', 4002, 0, 1)
    channelNo = int(channelNo)
    prmt.channel_tune(int(dtaChannelNo))
    # prmt.channel_tune(int(dtachannelnumber))
    time.sleep(5)
    prmt.disconnect()	
    
    image_path1, image_path2 = pyhik.captureDTAVideo(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg',testName+'2.jpeg')
    img1 = cv2.imread(image_path1,0)
    img2 = cv2.imread(image_path2,0)
    # CROPPING TECHNIQUE FOR MAKING A CLEAR IMAGE
    
    #img1 = img1[150:350,150:750]
    #img2 = img2[150:350,150:750]
    #r1,t1 = cv2.threshold(img1,170,255,cv2.THRESH_BINARY)
    #r2,t2 = cv2.threshold(img2,170,255,cv2.THRESH_BINARY)
    #cv2.imwrite(image_path1,t1)
    #cv2.imwrite(image_path2,t2)
    videoautomation.testVideoPresence(image_path1,image_path2)

def TC_ECM_Verify(channelNo,testName,dtaChannelNo = None):
    # exit from diag if pointing to
    
    

    # diag navigate long press of 7 followed by 6 down key and enter for ECM Count page

    
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,100)
    #prmt = pydtaremote_diag.PyRemote("172.18.28.171",4002,3,3)
    #pointer_pos_received_messages(prmt)
    prmt.diag_messages()
    prmt.disconnect()
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,1)
    prmt.diag_navigate1()
    #pointer_pos_received_messsages(prmt)
    prmt.disconnect()
    

    #time.sleep(3)
	
    channelNo = int(channelNo)
    increment = False
    for x in range(3):
		image_path = pyhik.captureDTADiag(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg')
		print image_path
		image_path_split = image_path.split('\\')
		print image_path_split
		image_path_split[-1] = testName+'2.jpeg'
		cropped_image_path = '\\'.join(image_path_split)
		print cropped_image_path
		time.sleep(3)
		received_messages_page_image = cv2.imread(image_path,0)
		ecm_image = received_messages_page_image[325:350,100:550]
		cv2.imwrite(cropped_image_path,ecm_image)
		inc_value = videoautomation.testImgSimilar(cropped_image_path,refimages['ECM'])
		print "data "
		print inc_value
                """ for Old DTA BOX """
		if inc_value > 0.514:
			increment = True
                """ For DTA 170 BOX """
		#if inc_value > 1.1:
                 #   increment = True
    if increment is False:
		print "[Output: Messages did not increment]" 
		print inc_val
    else:
		print "[Output: Messages incremented]" 
		print inc_val

def TC_MSO_Verify(channelNo,testName,dtaChannelNo = None):
    # exit from diag if pointing to
    
    

    # diag navigate long press of 7 followed by 6 down key and enter for ECM Count page

    
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,100)
    #prmt = pydtaremote_diag.PyRemote("172.18.28.171",4002,3,3)
    #pointer_pos_received_messages(prmt)
    prmt.diag_messages()
    prmt.disconnect()
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,1)
    #prmt.diag_navigate1()
    prmt.channel_down()
    time.sleep(1)
    prmt.channel_down()
    time.sleep(1)
    prmt.channel_down()
    time.sleep(1)
    prmt.enter()
    time.sleep(1)
    prmt.channel_up()
    time.sleep(1)

    #pointer_pos_received_messsages(prmt)
    prmt.disconnect()
    

    #time.sleep(3)
    
    channelNo = int(channelNo)
    increment = False
    for x in range(3):
        image_path = pyhik.captureDTADiag(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg')
        print image_path

def TC_Code_Verify(channelNo,testName,dtaChannelNo = None):
    # exit from diag if pointing to
    
    

    # diag navigate long press of 7 followed by 6 down key and enter for ECM Count page

    
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,100)
    #prmt = pydtaremote_diag.PyRemote("172.18.28.171",4002,3,3)
    #pointer_pos_received_messages(prmt)
    prmt.diag_messages()
    prmt.disconnect()
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,1)
    prmt.diag_navigate_code()
    #pointer_pos_received_messsages(prmt)
    prmt.disconnect()
    channelNo = int(channelNo)
    increment = False
    for x in range(3):
		image_path = pyhik.captureDTADiag(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg')
		print image_path
		image_path_split = image_path.split('\\')
		print image_path_split
		image_path_split[-1] = testName+'2.jpeg'
		cropped_image_path = '\\'.join(image_path_split)
		print cropped_image_path
		time.sleep(3)
		received_messages_page_image = cv2.imread(image_path,0)
		#code_image = received_messages_page_image[325:350,100:550]
		#cv2.imwrite(cropped_image_path,code_image)


def TC_EMM_Verify(channelNo,testName,dtaChannelNo = None):
    # exit from diag if pointing to
    
    prmt= pydtaremote_diag.PyRemote('10.78.203.158', 4002, 0, 1)
    prmt.channel_tune(7)
    prmt.disconnect()

    # diag navigate long press of 7 followed by 6 down key and enter for EMM Count page
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,100)
    #prmt = pydtaremote_diag.PyRemote("172.18.28.171",4002,3,3)
    #pointer_pos_received_messages(prmt)
    prmt.diag_messages()
    prmt.disconnect()
    prmt = pydtaremote_diag.PyRemote("10.78.203.158",4002,0,1)
    prmt.diag_navigate1()
    #pointer_pos_received_messsages(prmt)
    prmt.disconnect()
    

    #time.sleep(3)
	
    channelNo = int(channelNo)
    increment = False
    for x in range(3):
		image_path = pyhik.captureDTADiag(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg')
		print image_path
		image_path_split = image_path.split('\\')
		print image_path_split
		image_path_split[-1] = testName+'2.jpeg'
		cropped_image_path = '\\'.join(image_path_split)
		print cropped_image_path
		time.sleep(3)
		received_messages_page_image = cv2.imread(image_path,0)
		#image_split_raw='C:\\EEVAA\\public\\images\\captures\\'
		#emm_image = received_messages_page_image[265:285,100:550]
		emm_image = received_messages_page_image[290:310,100:550]
		cv2.imwrite(cropped_image_path,emm_image)
		#file_path=image_path_split+testName
                #file_path1=file_path + ".txt"
		#val = execute.emm(image_path,testName)
		val=execute_cropped.emm(cropped_image_path,testName)
		#val=image_to_string(image_path)
		#inc_value = videoautomation.testImgSimilar(cropped_image_path,refimages['EMM'])
		#command1='tesseract -psm 6'
                #command=command1 + " " + image_path + " " + file_path
                print val
                
                
                """file_path1='C:\\EEVAA\\public\\images\\captures\\'+ testName 
                print file_path1
                file = open(file_path1, 'r')
                data = file.readlines()
               
                print data[0]
                print data[1]"""

                
                
                """ for Old DTA BOX """
		#if inc_value > 0.514:
		#	increment = True
                """ For DTA 170 BOX """
		if val[1] > 0:
                    increment = True
    if increment is False:
		print "[Output: Message did not increment]"
		#print val[0]
		
    else:
		print "[Output: Message incremented]"
		#print val[0]

    

    

def argparser(arg):
    """
    Parses the command line arguments and invokes the <modulename> (-m) with the <channelnumber> (-c) <testname> (-t) and <dtachannelnumber> (-d)
    """
    try:
        opts, args = getopt.getopt(arg,"hm:c:t:d:")
    except getopt.GetoptError:
        print 'Filename -m <modulename> -c <channelnumber> -t <testcasename> -d <dtachannelnumber>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: Filename -m <modulename> -c <channelnumber> -t <testcasename> -d <dtachannelnumber>'
            sys.exit()
        elif opt == '-m':
            modulename = arg
        elif opt == '-t':
            testname = arg
        elif opt == '-c':
            channelnumber = arg
        elif opt == '-d':
            dtachannelnumber = arg
    globals()[modulename](channelnumber,testname,dtachannelnumber)

if __name__ == "__main__":
	argparser(sys.argv[1:])
