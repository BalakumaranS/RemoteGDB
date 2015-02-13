import multicam
import itertools
import ImageChops,Image
import time,sys,getopt,os
import math,operator

VERSION = 1.0
__all__=[]
__imagedir__="C:\\EEVAA\\public\\images\\captures\\"

def OpenMCDriver():
    """
    Opens an instance of Multicam driver using the open() function of multicam library
    """
    multicam.open()

def CloseMCDriver():
    """
    Closes a opened instance of Multicam driver using the close() function of multicam library
    """
    multicam.close()

def StartMCChannel(DriverIndex,Connector):
    """
    Starts a dedicated channel for grabbing video from the capture card, using the Channel class of multicam library.
    It returns an instance of the Channel which has DriverIndex and Connector associated with its handle.
    Example:  startMCChannel(0,'VID1')
    """
    ChannelInstance=multicam.Channel(DriverIndex,Connector)
    return ChannelInstance

def StopMCChannel(ChannelInstance):
    """
    Stops a previously created dedicated channel for grabbing video from the capture card (using StartMCChannel()).
    It uses the __del__() funciton of Channel class of multicam library.
    Example:  stopMCChannel(startMCChannel(0,'VID1'))
    """
    ChannelInstance.__del__()

def SetParameter(ChannelInstance,Parameter,Value):
    """
    Sets a single parameter to your Channel Instance using the setParamNmStr() function of MulticamBase class of multicam library.
    Example: SetParameter(ChannelInstance,'ColorFormat','RGG24')
    """
    ChannelInstance.setParamNmStr(Parameter,Value)

def SetParameters(ChannelInstance,ParamDict):
    """
    Sets multiple paramter to your Channel Instance using the setParamNmStr() function of MulticamBase class of multicam library.
    Example: SetParameters(ChannelInstance,{'CamFile':'NTSC','ColorFormat':'RGB24'})
    """
    for Param in ParamDict.keys():
        print "Setting->",Param,":",ParamDict[Param]
        ChannelInstance.setParamNmStr(Param,ParamDict[Param])

def GetParameter(ChannelInstance,Parameter):
	"""
	Gets a single parameter from your Channel Instance using the getParamNmStr() function of MulticamBase class of multicam library.
	Example: SetParameter(ChannelInstance,'ColorFormat','RGG24')
	"""
	return ChannelInstance.getParamNmStr(Parameter)

def GetParameters(ChannelInstance,ParamTuple):
	"""
	Sets multiple parameter to your Channel Instance using the setParamNmStr() function of MulticamBase class of multicam library.
	Example: SetParameters(ChannelInstance,{'CamFile':'NTSC','ColorFormat':'RGB24'})
	"""
	ParamDict={}
	for Param in ParamTuple:
		Value=ChannelInstance.getParamNmStr(Param)
		ParamDict[Param]=Value
	return ParamDict

def RegisterCallback(ChannelInstance):
    """
    Registers a callback function to the ChannelHandle, using the McRegisterCallback() funciton of the multicam dll instance (mc) in multicam library, which will be called every time the callee function is called.
    """
    status = multicam.mc.McRegisterCallback(ChannelInstance.handle, multicam.cmp_func, None)
    multicam.checkStatus(status)
    return status
    

def Sleep(TimeDuration=5):
	"""
	Makes your script execution to sleep for a given TimeDuration.
	Example: sleep(TimeDuration=5)
	"""
	time.sleep(TimeDuration)
	
def CaptureFrame(TimeOutSec=0.1):
	"""
	Returns the latest frame from the image buffer, which is continuously updated with frames from the Capture Card.
	TimeOutSec variable in in seconds. The function uses grab() function of the multicam library. It returns Image.image instance.
	Example: CaptureFrame(TimeOutSec=0.1)
	"""
	return multicam.grab(TimeOutSec)
	
def ImgToPix(Img):
	"""
	Returns a Pixel Access Object which behaves like a 2-dimensional array of pixels.
	Example: ImgToPix(Image.open('image.png'))
	"""
	return Img.load()
	
def ImgSize(Img):
	"""
	Returns a tuple containing (width,height) of the Image
	Example: ImgSize(Image.open('image.png'))
	"""
	return Img.size
	
def PixToTuple(PixObj,ImgSizeTuple):
    """
    Returns a tuple of pixel values from a pixel access object created using ImgToPix() function
    """
    _width = ImgSizeTuple[0]
    _height = ImgSizeTuple[1]
    _ImgList = []
    for row,column in itertools.product(range(_width),range(_height)):
        _ImgList.append(PixObj[row,column])
    _ImgTuple = tuple(_ImgList)
    return _ImgTuple

def ImgMinPix(ImgTuple):
	"""
	Returns the minimum pixel value in the image tuple obtained from PixToTuple() function
	"""
	return min(ImgTuple)
	
def ImgMaxPix(ImgTuple):
	"""
	Returns the maximum pixel value in the image tuple obtained from PixToTuple() function
	"""
	return max(ImgTuple)
	
def ImgDiff(Img1,Img2):
	"""
	Computes the difference between Img1 and Img2, and gets the bounding box of non-zero regions in the difference image.
	Returns a tuple containing (left,upper,right,lower) of the non-zero regions if Img1 and Img2 are different or None if Img1 and Img2 are identical.
	"""
	diff = ImageChops.difference(Img1,Img2).getbbox()
	print "the image difference is " , diff
	return diff

def ImgSimilar(Img1,Img2):
    """
    Computes the degree of similarity between Img1 and Img2 and returns the RMS (Root Means Squared) value of the absolute difference
    """
    Img1Hist = Img1.histogram()
    Img2Hist = Img2.histogram()
    return math.sqrt(reduce(operator.add,map(lambda ImH1,ImH2: abs(ImH1-ImH2),Img1Hist,Img2Hist)) / (float(Img1.size[0]) * Img1.size[1]))
    
def ImgSave(Img,Name):
    """
    Saves Img in the Name given. The image will be saved by default in the directory in which the calling script is present.
    The default nature can be modified by providing destination directory along with the Name.
    """
    Img.save(Name)

def testImageSimilarity(channelno,testname):
    OpenMCDriver()
    c=StartMCChannel(0,channelno)
    params = {
            'CamFile':'NTSC',
             'ColorFormat':'RGB24',
             'AcquisitionMode':'VIDEO',
             'TrigMode':'IMMEDIATE',
             'NextTrigMode':'REPEAT',
             'SeqLength_Fr':'-1', #3407 << 14
             'SignalEnable:1':'ON',              
             'SignalEnable:2':'ON',
             'SignalEnable:7':'ON',              
             'SignalEnable:12':'ON',              
             'GrabField':'UPDW',
             'NextGrabField':'SAME',
             'OffsetX_Px':'-2',
             'SurfaceCount': '8'}
    SetParameters(c,params)
    RegisterCallback(c)
    SetParameter(c,'ChannelState','ACTIVE')
    Img = CaptureFrame(TimeOutSec = 0.1)
    ImgSave(Img,__imagedir__+testname+"1.jpeg")
    #ImageValidate=ImgSimilar(Img,Image.open("python\\_RefNotAuthor.jpeg"))
    ImageValidate=ImgSimilar(Img,Image.open("C:\EEVAA\python\_RefNotAuthor.jpeg"))
    print ImageValidate
    if (ImageValidate < 1.5):
        print "[Output:Not authorised Channel]"
    else:
        print "[Output:Authorised Channel]"
    Sleep(5)
    Img1 = CaptureFrame(TimeOutSec = 0.1)
    ImgSave(Img1,__imagedir__+testname+"2.jpeg")
    
    #ImageValidate=ImgSimilar(Img1,Image.open("python\\_RefNotAuthor.jpeg"))
    ImageValidate=ImgSimilar(Img,Image.open("C:\EEVAA\python\_RefNotAuthor.jpeg"))
    print ImageValidate
    if (ImageValidate < 1.5):
        print "[Output:Not authorised Channel]"
    else:
        print "[Output:Authorised Channel]"
    SetParameter(c,'ChannelState','IDLE')
    StopMCChannel(c)
    CloseMCDriver()


def testImageBrick(channelno,testname):
    OpenMCDriver()
    c=StartMCChannel(0,channelno)
    params = {
            'CamFile':'NTSC',
             'ColorFormat':'RGB24',
             'AcquisitionMode':'VIDEO',
             'TrigMode':'IMMEDIATE',
             'NextTrigMode':'REPEAT',
             'SeqLength_Fr':'-1', #3407 << 14
             'SignalEnable:1':'ON',              
             'SignalEnable:2':'ON',
             'SignalEnable:7':'ON',              
             'SignalEnable:12':'ON',              
             'GrabField':'UPDW',
             'NextGrabField':'SAME',
             'OffsetX_Px':'-2',
             'SurfaceCount': '8'}
    SetParameters(c,params)
    RegisterCallback(c)
    SetParameter(c,'ChannelState','ACTIVE')
    Img = CaptureFrame(TimeOutSec = 0.1)
    ImgSave(Img,__imagedir__+testname+"1.jpeg")
    #ImageValidate=ImgSimilar(Img,Image.open("python\\_BrickMode.jpeg"))
    ImageValidate=ImgSimilar(Img,Image.open("C:\EEVAA\python\Brick.jpg"))
    print ImageValidate
    if (ImageValidate < 1.6):
        print "[Output:Brick Mode]"
    else:
        print "[Output:Authorised Channel]"
    SetParameter(c,'ChannelState','IDLE')
    StopMCChannel(c)
    CloseMCDriver()
  
def testVideoPresence(channelno,testname):
    OpenMCDriver()
    c=StartMCChannel(0,channelno)
    params = {
            'CamFile':'NTSC',
             'ColorFormat':'RGB24',
             'AcquisitionMode':'VIDEO',
             'TrigMode':'IMMEDIATE',
             'NextTrigMode':'REPEAT',
             'SeqLength_Fr':'-1', #3407 << 14
             'SignalEnable:1':'ON',              
             'SignalEnable:2':'ON',
             'SignalEnable:7':'ON',              
             'SignalEnable:12':'ON',              
             'GrabField':'UPDW',
             'NextGrabField':'SAME',
             'OffsetX_Px':'-2',
             'SurfaceCount': '8'}
    SetParameters(c,params)
    RegisterCallback(c)
    SetParameter(c,'ChannelState','ACTIVE')
    Img1 = CaptureFrame(TimeOutSec = 1)
    ImgSave(Img1,__imagedir__+testname+"1.jpeg")
    Sleep(10)
    Img2 = CaptureFrame(TimeOutSec = 1)
    ImgSave(Img2,__imagedir__+testname+"2.jpeg")
    Img1Pix = ImgToPix(Img1)
    Img2Pix = ImgToPix(Img2)
    (Img1W, Img1H) = ImgSize(Img1)
    (Img2W, Img2H) = ImgSize(Img2)
    Img1Size = (Img1W, Img1H)
    Img2Size = (Img2W, Img2H)
    Img1Tuple = PixToTuple(Img1Pix,Img1Size)
    Img2Tuple = PixToTuple(Img2Pix,Img2Size)
    Img1MaxPix = ImgMaxPix(Img1Tuple)
    Img2MaxPix = ImgMaxPix(Img2Tuple)
    if Img1MaxPix < (40,40,40) and Img2MaxPix < (40,40,40):
        print "[Output:Black screen detected]"
    elif Img1MaxPix < (40,40,40) and Img2MaxPix > (40,40,40):
        print "[Output:Initially Black screen later video running]"
    elif Img1MaxPix > (40,40,40) and Img2MaxPix < (40,40,40):
        print "[Output:Initially later video running later Black Screen]"
    elif ImgDiff(Img1,Img2) is not None:
        print "[Output:Video running]"
    else:
        print "[Output: Video Freeze]"
    SetParameter(c,'ChannelState','IDLE')
    StopMCChannel(c)
    CloseMCDriver()
def testVideoPresence_eas(channelno,testname):
    OpenMCDriver()
    c=StartMCChannel(0,channelno)
    params = {
            'CamFile':'NTSC',
             'ColorFormat':'RGB24',
             'AcquisitionMode':'VIDEO',
             'TrigMode':'IMMEDIATE',
             'NextTrigMode':'REPEAT',
             'SeqLength_Fr':'-1', #3407 << 14
             'SignalEnable:1':'ON',              
             'SignalEnable:2':'ON',
             'SignalEnable:7':'ON',              
             'SignalEnable:12':'ON',              
             'GrabField':'UPDW',
             'NextGrabField':'SAME',
             'OffsetX_Px':'-2',
             'SurfaceCount': '8'}
    SetParameters(c,params)
    RegisterCallback(c)
    SetParameter(c,'ChannelState','ACTIVE')
    Img1 = CaptureFrame(TimeOutSec = 1)
    ImgSave(Img1,__imagedir__+testname+"1.jpeg")
    Sleep(10)
    Img2 = CaptureFrame(TimeOutSec = 1)
    ImgSave(Img2,__imagedir__+testname+"2.jpeg")
    Sleep(10)
    Img3 = CaptureFrame(TimeOutSec = 1)
    ImgSave(Img3,__imagedir__+testname+"3.jpeg")
    Sleep(10)
    Img4 = CaptureFrame(TimeOutSec = 1)
    ImgSave(Img4,__imagedir__+testname+"4.jpeg")
    Sleep(10)
    Img5 = CaptureFrame(TimeOutSec = 1)
    ImgSave(Img5,__imagedir__+testname+"5.jpeg")
    Img1Pix = ImgToPix(Img1)
    Img2Pix = ImgToPix(Img2)
    Img3Pix = ImgToPix(Img3)
    Img4Pix = ImgToPix(Img4)
    Img5Pix = ImgToPix(Img5)
    (Img1W, Img1H) = ImgSize(Img1)
    (Img5W, Img5H) = ImgSize(Img5)
    Img1Size = (Img1W, Img1H)
    Img5Size = (Img5W, Img5H)
    Img1Tuple = PixToTuple(Img1Pix,Img1Size)
    Img5Tuple = PixToTuple(Img5Pix,Img5Size)
    Img1MaxPix = ImgMaxPix(Img1Tuple)
    Img5MaxPix = ImgMaxPix(Img5Tuple)
    if Img1MaxPix < (40,40,40) and Img5MaxPix < (40,40,40):
        print "[Output:Black screen detected]"
    elif Img1MaxPix < (40,40,40) and Img5MaxPix > (40,40,40):
        print "[Output:Initially Black screen later video running]"
    elif Img1MaxPix > (40,40,40) and Img5MaxPix < (40,40,40):
        print "[Output:Initially later video running later Black Screen]"
    elif ImgDiff(Img1,Img2) is not None:
        print "[Output:Video running]"
    else:
        print "[Output: Video Freeze]"
    SetParameter(c,'ChannelState','IDLE')
    StopMCChannel(c)
    CloseMCDriver()
def testVideoCapture(channelno,testname):
    OpenMCDriver()
    c=StartMCChannel(0,channelno)
    params = {
            'CamFile':'NTSC',
             'ColorFormat':'RGB24',
             'AcquisitionMode':'VIDEO',
             'TrigMode':'IMMEDIATE',
             'NextTrigMode':'REPEAT',
             'SeqLength_Fr':'-1', #3407 << 14
             'SignalEnable:1':'ON',              
             'SignalEnable:2':'ON',
             'SignalEnable:7':'ON',              
             'SignalEnable:12':'ON',              
             'GrabField':'UPDW',
             'NextGrabField':'SAME',
             'OffsetX_Px':'-2',
             'SurfaceCount': '8'}
    SetParameters(c,params)
    RegisterCallback(c)
    SetParameter(c,'ChannelState','ACTIVE')
    Img = CaptureFrame(TimeOutSec = 1)
    ImgSave(Img,__imagedir__+testname+".jpeg")
    SetParameter(c,'ChannelState','IDLE')
    StopMCChannel(c)
    CloseMCDriver()

def argparser(arg):
    """
    Parses the command line arguments and invokes the <modulename> (-m) with the <channelnumber> (-c)
    """
    try:
        opts, args = getopt.getopt(arg,"hm:c:t:")
    except getopt.GetoptError:
        print 'Filename -m <modulename> -c <channelnumber>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: Filename -m <modulename> -c <channelnumber>'
            sys.exit()
        elif opt == '-m':
            modulename = arg
        elif opt == '-t':
            testname = arg
        elif opt == '-c':
            channelnumber = arg
    globals()[modulename](channelnumber,testname)

if __name__ == "__main__":
	argparser(sys.argv[1:])
    
