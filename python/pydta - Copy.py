import cv2,time,getopt,sys
import pydtaremote
import pyhik
import imageprocessor
import videoautomation

################################
### Global variables ###
################################
hikip = "10.78.203.159"
hikport = 8000
hikuser = "admin"
hikpwd = "12345"
refimages = {
'EMM':'refs\\images\\_RefDTAEmm_Zero.jpeg',
'NA':'refs\\images\\_RefDTANot_Authorized.jpeg'
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
	prmt = pydtaremote.PyRemote("172.18.28.171",4002,3,3)
	pointer_pos_received_messages(prmt)
	prmt.send_digit(0)
	pointer_pos_default(prmt)
	
def TC_EMM_Verify(channelNo,testName,dtaChannelNo = None):
    #prmt = pydtaremote.PyRemote("172.18.28.171",4002,3,3)
    #pointer_pos_received_messages(prmt)

    #time.sleep(3)
	
    channelNo = int(channelNo)
    increment = False
    for x in range(3):
		image_path = pyhik.captureDTADiag(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg')
		image_path_split = image_path.split('\\')
		image_path_split[-1] = testName+'2.jpeg'
		cropped_image_path = '\\'.join(image_path_split)
		time.sleep(3)
		received_messages_page_image = cv2.imread(image_path,0)
		emm_image = received_messages_page_image[300:325,100:550]
		cv2.imwrite(cropped_image_path,emm_image)
		inc_value = videoautomation.testImgSimilar(cropped_image_path,refimages['EMM'])
		if inc_value > 0.514:
			increment = True
    if increment is False:
		print "[Output: Message did not increment]"
    else:
		print "[Output: Message incremented]"

def TC_Barker_Verify(channelNo,testName,dtaChannelNo):
    #prmt = pydtaremote.PyRemote("172.18.28.171",4002,3,3)
    #prmt.channel_tune(int(dtaChannelNo))

    #time.sleep(3)
	
    channelNo = int(channelNo)
    barker = False
    for x in range(3):
		image_path = pyhik.captureDTADiag(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg')
		image_path_split = image_path.split('\\')
		image_path_split[-1] = testName+'2.jpeg'
		cropped_image_path = '\\'.join(image_path_split)
		dta_na_image = cv2.imread(image_path,0)
		dta_na_barker_image = dta_na_image[55:95,400:750]
		cv2.imwrite(cropped_image_path,dta_na_barker_image)
		ba_value = videoautomation.testImgSimilar(cropped_image_path,refimages['NA'])
		if ba_value < 0.54:
			barker = True
    if barker is False:
		print "[Output: Authorized channel]"
    else:
		print "[Output: Not Authorized channel]"
		
def TC_VideoPresence(channelNo,testName,dtaChannelNo):
    #prmt = pydtaremote.PyRemote("172.18.28.171",4002,3,3)
    #prmt.channel_tune(int(dtaChannelNo))

    #time.sleep(3)
	
    channelNo = int(channelNo)
    image_path1, image_path2 = pyhik.captureDTAVideo(hikip,hikport,hikuser,hikpwd,channelNo,testName+'1.jpeg',testName+'2.jpeg')
    img1 = cv2.imread(image_path1,0)
    img2 = cv2.imread(image_path2,0)
    img1 = img1[150:350,150:750]
    img2 = img2[150:350,150:750]
    r1,t1 = cv2.threshold(img1,170,255,cv2.THRESH_BINARY)
    r2,t2 = cv2.threshold(img2,170,255,cv2.THRESH_BINARY)
    cv2.imwrite(image_path1,t1)
    cv2.imwrite(image_path2,t2)
    videoautomation.testVideoPresence(image_path1,image_path2)


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
