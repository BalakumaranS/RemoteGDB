import ctypes
import types
import time
import threading
import sys

import Image

# Define platform constants
PLATFORM_WINDOWS = 0
PLATFORM_LINUX = 1
PLATFORM_OTHER = 99

# Get the platform
if 'win' in sys.platform:
    platform = PLATFORM_WINDOWS
elif 'linux' in sys.platform:
    platform = PLATFORM_LINUX
else:
    platform = PLATFORM_OTHER
    
if platform == PLATFORM_WINDOWS:
    import ImageWin
print platform
##    import pywintypes
##    import win32event

# Get thread lock for use with image buffer
lock = threading.Lock()
callbackLock = threading.Lock()

# Get event for new frame ready
evtNewFrameReady = threading.Event()

# Get events for channel signals
evtEndChannelActivity = threading.Event()
evtSignalAcquisitionFailure = threading.Event()

# Access multicam library through ctypes
if platform == PLATFORM_WINDOWS:
    mc = ctypes.windll.multicam
elif platform == PLATFORM_LINUX:
    # NOTE: In the future this line needs to be modified to be
    # more flexible concerning the library name
    mc = ctypes.cdll.LoadLibrary("/usr/local/euresys/multicam/drivers/lib/libMultiCam.so.6.8.0.1938")

# Define multicam constants
MC_BOARD = 0xE0000000
MC_CONFIGURATION = 0x20000000
MC_CHANNEL = 0x8000FFFF
MC_DEFAULT_SURFACE_HANDLE = 0x4FFFFFFF

# Define signals
MC_SIG_SURFACE_PROCESSING         = 1
MC_SIG_SURFACE_FILLED             = 2
MC_SIG_UNRECOVERABLE_OVERRUN      = 3
MC_SIG_FRAMETRIGGER_VIOLATION     = 4
MC_SIG_START_EXPOSURE             = 5
MC_SIG_END_EXPOSURE               = 6
MC_SIG_ACQUISITION_FAILURE        = 7
MC_SIG_CLUSTER_UNAVAILABLE        = 8
MC_SIG_RELEASE                    = 9
MC_SIG_END_ACQUISITION_SEQUENCE   = 10
MC_SIG_START_ACQUISITION_SEQUENCE = 11
MC_SIG_END_CHANNEL_ACTIVITY       = 12

# Setup structure for callback info
class _MC_CALLBACK_INFO(ctypes.Structure):
    pass
_MC_CALLBACK_INFO._fields_ = [
    ('Context', ctypes.c_void_p),
    ('Instance', ctypes.c_uint),
    ('Signal', ctypes.c_int),
    ('SignalInfo', ctypes.c_uint),
    ('Reserved', ctypes.c_uint),
]

assert ctypes.sizeof(_MC_CALLBACK_INFO) == 20, ctypes.sizeof(_MC_CALLBACK_INFO)
assert ctypes.alignment(_MC_CALLBACK_INFO) == 4, ctypes.alignment(_MC_CALLBACK_INFO)

MCSIGNALINFO = _MC_CALLBACK_INFO
PMCSIGNALINFO = ctypes.POINTER(_MC_CALLBACK_INFO)
PMCCALLBACKINFO = ctypes.POINTER(_MC_CALLBACK_INFO)
MCCALLBACKINFO = _MC_CALLBACK_INFO

# Define error codes
errorCodes = {0:'No Error',
              -1:'No Board Found',
              -2:'Bad Parameter',
              -3:'I/O Error',
              -4:'Internal Error',
              -5:'No More Resources',
              -6:'Object still in use',
              -7:'Operation not supported',
              -8:'Parameter database error',
              -9:'Value out of bound',
              -10:'Object instance not found',
              -11:'Invalid Handle',
              -12:'Timeout',
              -13:'Invalid value',
              -14:'Value not in range',
              -15:'Invalid hardware configuration',
              -16:'No Event',
              -17:'License not granted',
              -18:'Fatal error',
              -19:'Hardware event conflict',
              -20:'File not found',
              -21:'Overflow',
              -22:'Parameter inconsistency',
              -23:'Illegal operation',
              -24:'Cluster busy',
              -25:'MultiCam service error',
              -26:'Invalid surface'}

def checkStatus(status):
    '''
    Raise an exception if the provided status value is < 0.
    '''
    if status < 0:
        if status in errorCodes.keys():
            raise Exception(errorCodes[status])
        else:
            raise Exception('Multicam raised an unknown error with code %d' % status)
        
def open():
    '''
    Open the multicam driver.
    '''
    mcOpenDriver = mc.McOpenDriver
    mcOpenDriver.restype = ctypes.c_int
    
    # Open the driver
    status = mc.McOpenDriver(ctypes.c_void_p(None))
    checkStatus(status)

    # Get number of boards and available board info
    c = Configuration()
    boardCount = c.boardCount
    print 'Opened multicam driver with %d board(s) available:' % boardCount
    for i in range(boardCount):
        b = Board(i)
        print b
    
def close():
    '''
    Close the multicam driver.
    '''
    mc.McCloseDriver()
    print 'Closed multicam driver'

def create(model):
    '''
    Create and return an instance.
    '''
    mcCreate = mc.McCreate
    mcCreate.restype = ctypes.c_int
    
    cModel = ctypes.c_uint(model)
    instance = ctypes.c_uint()
    
    status = mcCreate(cModel, ctypes.byref(instance))
    checkStatus(status)
    return instance

def delete(instance):
    import ctypes
    '''
    Delete the instance.
    '''
    mcDelete = mc.McDelete
    mcDelete.restype = ctypes.c_int
    
    status = mcDelete(instance)
    checkStatus(status)

# Create type for callback function
if platform == PLATFORM_WINDOWS:
    CMPFUNC = ctypes.WINFUNCTYPE(None, ctypes.POINTER(_MC_CALLBACK_INFO))
elif platform == PLATFORM_LINUX:
    CMPFUNC = ctypes.CFUNCTYPE(None, ctypes.POINTER(_MC_CALLBACK_INFO))


class Buffer:
    '''
    Image buffer class.
    '''
    def __init__(self, size = 300):
        self.images = []
        self.size = size
        
    def addImage(self, image):
        try:
            lock.acquire()
            if len(self.images) > self.size:
                self.images.pop(0)
            self.images.append(image)

            # Set the event indicating a new frame
            evtNewFrameReady.set()
        finally:
            lock.release()
            
# Get an instance of the image buffer class
imgBuffer = Buffer()
handle = None

class MulticamBase(object):
    def __init__(self):
        self.handle = None

    def setParamNmStr(self, parameter, value):
        status = mc.McSetParamNmStr(self.handle, parameter, value)
        checkStatus(status)
        
    def getParamNmStr(self, parameter):
        length = 128
        s = ctypes.create_string_buffer(length)
        status = mc.McGetParamNmStr(self.handle, parameter, ctypes.byref(s), ctypes.c_int(length))
        checkStatus(status)
        return s.value

    def setParamNmInt(self, parameter, value):
        parm = ctypes.c_int(parameter)
        val = ctypes.c_int(value)
        status = mc.McSetParamNmInt(self.handle, parm, val)
        checkStatus(status)
        
    def getParamNmInt(self, parameter):
        val = ctypes.c_int()
        status = mc.McGetParamNmInt(self.handle, parameter, ctypes.byref(val))
        checkStatus(status)
        return val.value
    
    def setParamInt(self, parameter, value):
        parm = ctypes.c_int(parameter)
        val = ctypes.c_int(value)
        status = mc.McSetParamInt(self.handle, parm, val)
        checkStatus(status)
        
    def getParamInt(self, parameter):
        parm = ctypes.c_int(parameter)
        val = ctypes.c_int()
        status = mc.McGetParamInt(self.handle, parm, ctypes.byref(val))
        checkStatus(status)
        return val.value

class Configuration(MulticamBase):
    '''
    This class is a wrapper around the multicam Configuration class
    '''
    def __init__(self):
        MulticamBase.__init__(self)

        self.handle = MC_CONFIGURATION

    def getBoardCount(self):
        return self.getParamNmInt('BoardCount')

    boardCount = property(getBoardCount, None)

class Board(MulticamBase):
    '''
    Multicam Board class.

    NOTE: EXPERT level parameters are not exposed through this class.

    MultiCam Board Class parameters

    Parameter       Level      Access       Value list/range
    BoardTopology   SELECT     Get(Set)     MONO
    BoardType       ADJUST     Get only     QUICKPACK_CFA (***)    Grablink_Quickpack_CFA_PCIe
    DriverIndex     ADJUST     Get only     [0:#] (*)
    PciPosition     ADJUST     Get only     (**)
    BoardName       ADJUST     Get only     Any string up to 16 characters
    BoardIdentifier ADJUST     Get only     String composed with BoardType and SerialNumber
    NameBoard       ADJUST     Set only     Any string up to 16 characters
    SerialNumber    ADJUST     Get only     [0:999,999]
    SerialControlA  ADJUST     Set (Get)    A string designating the virtual COM port
    OemSafetyKey    EXPERT     Set only     Any string up to 8 characters
    OemSafetyLock   EXPERT     Set Get   
    PoCL_PowerInput EXPERT     Get only     ON, OFF
    PCIeLinkWidth   EXPERT     Get only     [1,4]
     
    '''
    def __init__(self, index = 0):
        MulticamBase.__init__(self)
        self.index = index

        # Set handle to base value plus specified board index
        self.handle = MC_BOARD + index

    # Define BoardTopology property get/set
    def getBoardTopology(self):
        return self.getParamNmStr('BoardTopology')

    def setBoardTopology(self, value):
        self.setParamNmStr('BoardTopology', value) 

    boardTopology = property(getBoardTopology, setBoardTopology)

    # Define BoardType property get only
    def getBoardType(self):
        return self.getParamNmStr('BoardType')

    boardType = property(getBoardType, None)

    # Define DriverIndex property get only
    def getDriverIndex(self):
        return self.getParamNmStr('DriverIndex')

    driverIndex = property(getDriverIndex, None)

    # Define PciPosition property get
    def getPciPosition(self):
        return self.getParamNmStr('PciPosition')

    pciPosition = property(getPciPosition, None)
    
    # Define BoardName property get/set
    def getBoardName(self):
        return self.getParamNmStr('BoardName')

    def setBoardName(self, value):
        if len(value) > 16:
            raise Exception('Board Name must be 16 characters or less!')
        else:
            self.setParamNmStr('NameBoard', value)
        
    boardName = property(getBoardName, setBoardName)

    # Define SerialNumber property get
    def getSerialNumber(self):
        return self.getParamNmStr('SerialNumber')

    serialNumber = property(getSerialNumber, None)

    # Define BoardIdentifier property get
    def getBoardIdentifier(self):
        return self.getParamNmStr('BoardIdentifier')

    boardIdentifier = property(getBoardIdentifier, None)

    def __str__(self):
        '''
        Format printing of board information
        '''
        
        s = ''
        s += 'Info for board %d\n' % self.index
        s += '-----------------\n'
        s += 'Topology: %s\n' % self.boardTopology
        s += 'Type: %s\n' % self.boardType
        s += 'Driver Index: %s\n' % self.driverIndex
        s += 'PCI Position: %s\n' % self.pciPosition
        s += 'Name: %s\n' % self.boardName
        s += 'Serial Number: %s\n' % self.serialNumber
        s += 'Identifier: %s\n' % self.boardIdentifier
        return s 
        
class Channel(MulticamBase):
    '''
    Multicam Channel class
    '''
    def __init__(self, index, connector):
        MulticamBase.__init__(self)

        self.handle = create(MC_CHANNEL)
        #print 'handle: %s' % self.handle

        self.setParamNmStr('DriverIndex', str(index))
        self.setParamNmStr('Connector', connector)

    def __del__(self):
        if self.handle != None:
            delete(self.handle)
        
    
class Surface(MulticamBase):
    '''
    Multicam Surface class
    '''
    counter = 0
    def __init__(self, handle):
        MulticamBase.__init__(self)
        self.handle = ctypes.c_ulong(handle)
        
#       self.bufferSize = channel.getParamNmStr('BufferSize')
#       self.bufferPitch = channel.getParamNmStr('BufferPitch')
#       
#       #Allocate memory for buffer.
#       BUFFER = (ctypes.c_ubyte * int(self.bufferSize))
#       self.buffer = BUFFER()
#       
#       self.context = Surface.counter
#       Surface.counter += 1 
#       
#       self.setParamNmStr('SurfaceContext', str(self.context))
#       self.setParamNmStr('SurfaceAddr', str(ctypes.addressof(self.buffer)))
#       self.setParamNmStr('SurfaceSize', self.bufferSize)
#       self.setParamNmStr('SurfacePitch', self.bufferPitch)
#       channel.setParamNmStr('Cluster:%d' % self.context, str(self.handle.value))
        
        
def grab(timeoutSec = 5):
    '''
    Grab and return a single image
    '''

    # Record the start time
    startTime = time.time()

    # Wait until new frame is ready
    evtNewFrameReady.wait(timeoutSec)
    
##    while not imgBuffer.newImage:
##        elapsed = time.time() - startTime
##        #print 'No New Image Available in %.3f Sec' % elapsed
##        if elapsed > timeoutSec:
##            raise Exception('Timeout on grab!')
##        time.sleep(0.001)
        
    # Acquire a lock so the image won't be overwritten while accessing
    try:
        lock.acquire()
        l = len(imgBuffer.images)
        img = imgBuffer.images[l - 1].copy()
        evtNewFrameReady.clear()
    finally:
        lock.release()

    grabTime = time.time() - startTime
#    print 'Grab time: %.4f' % grabTime

    return img

def acquire():
    pass

def test():
    open()
    c = Channel(0, 'VID1')

# Create a variable to track timestamp
previousTime = 0

def mcCallBack(info):
    '''
    Callback function executed for every signal
    '''
    global previousTime

    # Clear signal events
    evtEndChannelActivity.clear()
    evtSignalAcquisitionFailure.clear()
    
    # Record start time
    st = time.time()

    #print info.contents.Signal, info.contents.Instance, info.contents.SignalInfo, '%.3f' % st, '%.3f' % (st - previousTime)

    #Print in case of unexpected signal type
    if info.contents.Signal not in [1, 2, 7, 12]:
        print 'Signal:', info.contents.Signal

    # Initialize variables
    address = None
    size = None
    
    if info.contents.Signal == 2:
        # Handle a captured frame

        # Get surface instance        
        s = Surface(info.contents.SignalInfo)

        # Get the number of planes in surface
        planeCount = s.getParamNmInt('PlaneCount')
        
        if planeCount == 1:
            address = s.getParamNmInt('SurfaceAddr')
            size = s.getParamNmInt('SurfaceSize')
            pitch = s.getParamNmInt('SurfacePitch')
            if pitch > 640:
                mode = 'RGB'
            else:
                mode = 'L'
    
            #print address, size, pitch
            ARRAY = ctypes.c_int*size
            array = ARRAY.from_address(address)

            b = buffer(array)
            if mode == 'RGB':
                image = Image.frombuffer('RGB', (640,480), b, 'raw', 'BGR', 0, 1)
            else:
                image = Image.frombuffer('L', (640,480), b, 'raw', 'L', 0, 1)
                            
        elif planeCount == 3:
            b = []
            data = []
            for band in range(3):
                address = s.getParamNmInt('SurfaceAddr:%d' % band)
                size = s.getParamNmInt('SurfaceSize:%d' % band)
    
                ARRAY = ctypes.c_int*size
                array = ARRAY.from_address(address)

                b.append(buffer(array))
            
            data.append(Image.frombuffer('L', (640,480), b[0], 'raw', 'L', 0, 1))
            data.append(Image.frombuffer('L', (640,240), b[1], 'raw', 'L', 0, 1))
            data.append(Image.frombuffer('L', (640,240), b[2], 'raw', 'L', 0, 1))
            
            image = data
            
        # Add the new image to the image buffer
        imgBuffer.addImage(image)
        
          #for Windows platforms 
        if (platform == PLATFORM_WINDOWS) and (handle != None):
            dib = ImageWin.Dib(image)
            hwnd = ImageWin.HWND(handle)
            dib.expose(hwnd)

    elif info.contents.Signal == 7:
        # Set signal acquisition failure event
        evtSignalAcquisitionFailure.set()

    elif info.contents.Signal == 12:
        # Set end of channel activity event
        evtEndChannelActivity.set()
        
    # Record the end time
    et = time.time()
    #print 'Time in callback function:  %.4f' % (et - st)           
    previousTime = st                            

cmp_func = CMPFUNC(mcCallBack)

#def registerCallback(handle):
#    '''
#    Register the callback
#    '''
#    status = mc.McRegisterCallback(handle, cmp_func, None)
#    checkStatus(status)
#    print 'Register callback...', status
    
if __name__ == '__main__':
    '''
    Run capture for a few seconds with some common basic parameter settings.
    '''
    open()
    c = Channel(0, 'VID1')
#   s = []
#   for x in range(8):
#       s.append(Surface(c))
    
    parms = {'CamFile':'NTSC',
             #'ColorFormat':'YUV422PL',
             'ColorFormat':'RGB24',
             #'ColorFormat':'Y8',
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
             #'ImageFlipX':'ON',
             #'ImageFlipY':'ON'}      

    for key in parms.keys():
        print 'Setting', key
        c.setParamNmStr(key, parms[key])
    
    print 'Signal:2 status', c.getParamNmStr('SignalEnable:2')
    print 'Signal:1 status', c.getParamNmStr('SignalEnable:1')
    status = mc.McRegisterCallback(c.handle, cmp_func, None)
    #print status

    c.setParamNmStr('ChannelState', 'ACTIVE')   

    time.sleep(2)
   
    c.setParamNmStr('ChannelState', 'IDLE')
    
    time.sleep(2)
    imObj = grab(timeoutSec = 5)
    pix = imObj.load()
    imNew = Image.new('RGB',(640,480))
    imNew = imObj.copy()
    curTime = time.time()
    imNew_Filename = str(curTime)+'.png'
    imNew.save(imNew_Filename)
#commented by anusha#

#    info = PMCSIGNALINFO()
#    #
#   for x in range(10):#
#       mc.McWaitSignal(c.handle, 2, 3000, info)
#       print time.time()
    
    
#   hFilled = pywintypes.HANDLE(c.getParamNmInt('SignalEvent:2'))
#   
#   for x in range(10):
#       win32event.WaitForSingleObject(hFilled, 3000)
#       print time.time()
#           
#   hProc = pywintypes.HANDLE(c.getParamNmInt('SignalEvent:1'))
#   
#   for x in range(10):
#       win32event.WaitForSingleObject(hProc, 3000)
#       print time.time()