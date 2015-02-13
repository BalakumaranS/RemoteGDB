import sys
import time

from Lib.Io import TelHost
from Base import ResourceBase
from Lib.Io import IrTelnetBlasterBase
from Lib.Io import IrCodes
from Lib.Io import ChanMap
from threading import Thread
import threading

PROMPT = '<s'

EXPLORER = 1
OCAP = 2
IPTV = 3
XMP = 4
MOTOROLA = 5
scrsvrDelay=180
channel =0
OSDDelay = 8
OSDDelay_main=4
CCPageDelay = 2
dvrdelay = 3
class IrTelnetBlaster(IrTelnetBlasterBase.IrTelnetBlasterBase):
    """TEK3 IR Blaster Driver""" 
    __slots__ = ('calcChecksum', 'timeout', 'irport', 'irhost', 'numberMap', 'stbPort', 'irCodes','chanMap','tuneDelay','lock')

    irport = ResourceBase.Parameter(4001, 'Port number of the Telnet Host')
    irhost = ResourceBase.Parameter('10.78.193.106', 'Host address of the Telnet Device')
    timeout = ResourceBase.Parameter(10, 'Timeout period, in seconds')
    burst = ResourceBase.Parameter(3, 'IR Burst')
    inputType = ResourceBase.Parameter(1, 'IR Type')
    waitForAck = ResourceBase.Parameter(True, 'Wait for acknowledgement')
    serialConnection = ResourceBase.Parameter(False, 'Use Serial connection')
    
    def __init__(self, id = 1):
        '''Constructor'''
        IrTelnetBlasterBase.IrTelnetBlasterBase.__init__(self)
        self.name = 'IR Lab Blaster Driver'
        self.numberMap = {'0':self.key0,
                          '1':self.key1,
                          '2':self.key2,
                          '3':self.key3,
                          '4':self.key4,
                          '5':self.key5,
                          '6':self.key6,
                          '7':self.key7,
                          '8':self.key8,
                          '9':self.key9}
        
        self.stbPort = 1
        self.lock = threading.Lock()
        print 'tek3 stbPort', self.stbPort


    def setup(self):
        self.inputType = 5
        if self.inputType == EXPLORER:
            self.irCodes = IrCodes.IrCodes56kHz()
        elif self.inputType == OCAP:
            self.irCodes = IrCodes.IrCodes36kHz()
        elif self.inputType == IPTV:
            self.irCodes = IrCodes.IrCodesRcmm()
        elif self.inputType == XMP:
            self.irCodes = IrCodes.IrCodesXmp()
            self.chanMap = ChanMap.SDV()
        elif self.inputType == MOTOROLA:
            self.irCodes = IrCodes.IrCodesMotorola()
            self.chanMap = ChanMap.SDV()
        

            
    def sendCmd(self, packet):
        
        data = packet
        self.log.debug('Writing packet to server %s and port %s:  %s' % (self.irhost, self.irport, data))
        self.port.write(data)
        if self.waitForAck:
            st = time.time()
            rtnData = ''
            if not(self.serialConnection):
                while 1:
                    rtnData += self.port.readUntil(PROMPT)
                    if rtnData.find(PROMPT) != -1:
                        break
                    et = time.time()
                    if (et - st) >= self.timeout:
                        raise IrTelnetBlasterTimeoutError()
                    time.sleep(0.01)
        #else:
        #    self.port.flush()

    def flush(self):
        """may be required occasionaly if waitForAck is True"""
        self.port.flush()

    def sendTxPacket(self, data, burst = None):
        option = ''
        if burst == None:
            burst = self.burst
        #if burst < 3:
        #    burst = 3
        if burst <> 3:
            option += '4%04x'%(burst)
        unit = int(self.stbPort)-1
        #mask = 1 << unit
        mask = 0xffff
        protocol = self.irCodes.protocol
        bytes = self.irCodes.dataBytes
        #protocol = 08, SA protocol at 56KHz. Standard for most Explorer settops.
        self.lock.acquire()
        if (threading.currentThread().getName() == "script1"):
            
            mask = 0x8a10
        elif (threading.currentThread().getName() == "script2"):
            mask = 0x0000
        else:
            mask = 0xffff                
        p = 't%04x%s%s%s%s0'%(mask, self.irCodes.protocol, self.irCodes.dataBytes, data, option)
        print "command : " + p
        self.sendCmd(p)
        self.lock.release()

    #def sendTxPacketOld(self, data, burst = 3):
    #    if burst < 3:
    #        burst = 3
    #    p = 't0%d5%s%d' % ((int(self.stbPort)-1), data, burst)
    #    self.sendCmd(p)
    
    def dayDown(self, repeat = 1, duration = None):
        if duration == None:
            duration = self.burst
        for x in range(0, repeat):
            self.sendTxPacket(self.irCodes.dayDown, duration)

    def dayUp(self, repeat = 1, duration = None):
        if duration == None:
            duration = self.burst
        for x in range(0, repeat):
            self.sendTxPacket(self.irCodes.dayUp, duration)

    def arrowUp(self, repeat = 1, duration = 3):
        if duration == None:
            duration = self.burst
        for x in range(0, repeat):
            self.sendTxPacket(self.irCodes.arrowUp, duration)

    def arrowLeft(self, repeat = 1, duration = None):
        if duration == None:
            duration = self.burst
        for x in range(0, repeat):
            self.sendTxPacket(self.irCodes.arrowLeft, duration)

    def arrowRight(self, repeat = 1, duration = None):
        if duration == None:
            duration = self.burst
        for x in range(0, repeat):
            self.sendTxPacket(self.irCodes.arrowRight, duration)
    
   
            
    def pause(self, repeat = 1, duration = None):
        if duration == None:
            duration = self.burst
        for x in range(0, repeat):
            self.sendTxPacket(self.irCodes.pause, duration)

    def guide(self):
        self.sendTxPacket(self.irCodes.guide)

    def pwr(self):        
        self.sendTxPacket(self.irCodes.pwr)

    def info(self):        
        self.sendTxPacket(self.irCodes.info)

    def message(self):        
        self.sendTxPacket(self.irCodes.message)
       
    def arrowDown(self, repeat = 1, duration = 3):        
        for x in range(0, repeat):
            self.sendTxPacket(self.irCodes.arrowDown, duration)

    def select(self):        
        self.sendTxPacket(self.irCodes.select)

    def FiOS(self):        
        self.sendTxPacket(self.irCodes.fiosTv)

    def bypass(self):        
        self.sendTxPacket(self.irCodes.bypass)

    def last(self):        
        self.sendTxPacket(self.irCodes.last)

    def ppv(self):        
        self.sendTxPacket(self.irCodes.ppv)
        
    def key1(self):        
        self.sendTxPacket(self.irCodes.key1)

    def key2(self):        
        self.sendTxPacket(self.irCodes.key2)
        
    def key3(self):        
        self.sendTxPacket(self.irCodes.key3)

    def key4(self):        
        self.sendTxPacket(self.irCodes.key4)

    def key5(self):
        self.sendTxPacket(self.irCodes.key5)
        
    def key6(self):
        self.sendTxPacket(self.irCodes.key6)

    def key7(self):
        self.sendTxPacket(self.irCodes.key7)

    def key8(self):
        self.sendTxPacket(self.irCodes.key8)

    def key9(self):
        self.sendTxPacket(self.irCodes.key9)

    def key0(self):
        self.sendTxPacket(self.irCodes.key0)
        
    def live(self):
        self.sendTxPacket(self.irCodes.live)

    def skipAhead(self):
        self.sendTxPacket(self.irCodes.skipAhead)

    def channelUp(self):
        self.sendTxPacket(self.irCodes.channelUp)
        
    def channelDown(self):
        self.sendTxPacket(self.irCodes.channelDown)

    def favorite(self):
        self.sendTxPacket(self.irCodes.favorite)

    def volumeUp(self):
        self.sendTxPacket(self.irCodes.volumeUp)

    def volumeDown(self):
        self.sendTxPacket(self.irCodes.volumeDown)

    def mute(self):
        self.sendTxPacket(self.irCodes.mute)

    def sound(self):
        self.sendTxPacket(self.irCodes.sound)

    def bml(self):
        self.sendTxPacket(self.irCodes.bml)

    def list(self):
        self.sendTxPacket(self.irCodes.list)

    def replay(self):
        self.sendTxPacket(self.irCodes.replay)

    def fastForward(self):
        self.sendTxPacket(self.irCodes.fastForward)

    def rewind(self):
        self.sendTxPacket(self.irCodes.rewind)

    def dot(self):
        self.sendTxPacket(self.irCodes.dot)

    def pound(self):
        self.sendTxPacket(self.irCodes.pound)

    def exit(self):
        self.sendTxPacket(self.irCodes.exit)

    def pipChannelUp(self):
        self.sendTxPacket(self.irCodes.pipChannelUp)

    def A(self):
        self.sendTxPacket(self.irCodes.A)

    def B(self):
        self.sendTxPacket(self.irCodes.B)

    def C(self):
        self.sendTxPacket(self.irCodes.C)

    def play(self):
        self.sendTxPacket(self.irCodes.play)

    def stop(self):
        self.sendTxPacket(self.irCodes.stop)

    def record(self):
        self.sendTxPacket(self.irCodes.record)

    def pageUp(self, repeat = 1, duration = 3):
        for x in range(0, repeat):
            self.sendTxPacket(self.irCodes.pageUp, duration)

    def pageDown(self, repeat = 1, duration = 3):
        for x in range(0, repeat):
            self.sendTxPacket(self.irCodes.pageDown, duration)

    def settings(self):        
        self.sendTxPacket(self.irCodes.settings)
        
    def pip(self):        
        self.sendTxPacket(self.irCodes.pip)
        
    def pipSwap(self):        
        self.sendTxPacket(self.irCodes.pipSwap)

    def pipMove(self):        
        self.sendTxPacket(self.irCodes.pipMove)

    def menu(self):        
        self.sendTxPacket(self.irCodes.menu)

    def pipChannelDown(self):        
        self.sendTxPacket(self.irCodes.pipChannelDown)

    def invokeOSD(self):        
        self.sendTxPacket(self.irCodes.B, 25)
        self.sendTxPacket(self.irCodes.volumeUp)

    def turboChannelUp(self):
        print 'turbo channel Up-start'
        for x in range (0,10):
            self.sendTxPacket(self.irCodes.channelUp,100)
        print 'turbo channel Up-stop'
      
        
    def turboChannelDown(self):
        print 'turbo channel Down-start'
        for x in range (0,10):
            self.sendTxPacket(self.irCodes.channelDown,100)
        print 'turbo channel Down-stop'	

    def changeChannel(self, channel, delay = 0.5, digits = 4):
        #build the chr string
        cStr = '%0'
        cStr+= str(digits)
        cStr += 'd'
        chStr = cStr % channel

        index = 0
        for c in chStr:
            #st = time.time()
            self.numberMap[c]()
            #et = time.time()
            if index < len(chStr) - 1:
                #print 'Delaying %.1f, command time = %.3f' % (delay, et - st)
                time.sleep(delay)
            index += 1

    def channelTune(self,channel):
        print channel
        for x in range (0,4):
            if channel[x]=='1':
                self.sendTxPacket(self.irCodes.key1)
            elif channel[x]=='2':
                self.sendTxPacket(self.irCodes.key2)
            elif channel[x]=='3':
                self.sendTxPacket(self.irCodes.key3)
            elif channel[x]=='4':
                self.sendTxPacket(self.irCodes.key4)
            elif channel[x]=='5':
                self.sendTxPacket(self.irCodes.key5)
            elif channel[x]=='6':
                self.sendTxPacket(self.irCodes.key6)
            elif channel[x]=='7':
                self.sendTxPacket(self.irCodes.key7)
            elif channel[x]=='8':
                self.sendTxPacket(self.irCodes.key8)
            elif channel[x]=='9':
                self.sendTxPacket(self.irCodes.key9)
            elif channel[x]=='0':
                self.sendTxPacket(self.irCodes.key0)
            time.sleep(0.3)
        self.sendTxPacket(self.irCodes.select)
            
    def optionKeys(self):
        self.favorite()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.record()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.volumeUp()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.volumeDown()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.pipSwap()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.pip()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.info()
        time.sleep(5)
        self.list()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.fastForward()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.rewind()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.select()
        time.sleep(2)
        self.select()
        time.sleep(2)

    def unlockChannel(self):
        print 'inside unlock channel'
        self.select()
        time.sleep(3)
        self.key0()
        time.sleep(2)
        self.key0()
        time.sleep(2)
        self.key0()
        time.sleep(2)
        self.key0()
        time.sleep(2)
        self.select()
        time.sleep(3)

    def traverseGuide(self):
        print 'invoking Guide'

        self.guide()
        time.sleep(5)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)

        print 'invoking half guide'
        
        self.guide()
        time.sleep(5)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.exit()
        
        print 'exiting guide'

    def traverseMenu(self):

        print 'invoking menu'
        self.menu()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowUp()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.arrowDown()
        time.sleep(menuDelay)
        self.exit()
        
        print 'Closed Menu'            


    
    def screenSaver(self):
        print 'scrsvr delay = ',scrsvrDelay
        time.sleep(1)
        channel=self.chanMap.H264HD1
        self.channelTune(channel)
        time.sleep(scrsvrDelay)
        self.volumeDown()
        time.sleep(0.5)
        self.exit()
        time.sleep(1)
        channel=self.chanMap.H264HD1
        self.channelTune(channel)
        time.sleep(scrsvrDelay)
        self.select()
        time.sleep(0.5)
        self.exit()
        time.sleep(1)
        
        
    def diagPage(self):
        print 'invoking diag page'
        time.sleep(1)
        print 'surf diag pages with chan up/down'
        self.exit()
        time.sleep(0.5)
        self.pwr()
        time.sleep(0.5)
        self.select()
        for x in range(0,10):
            time.sleep(5)
            self.channelUp()
            time.sleep(5)
            self.channelUp()
            time.sleep(5)
            self.channelUp()
            time.sleep(5)
            self.channelDown()
        print 'surf diag pages with left/right key'
        for x in range(0,30):
            time.sleep(1)
            self.arrowLeft()
            time.sleep(5)
            self.arrowLeft()
            time.sleep(5)
            self.arrowLeft()
            time.sleep(5)
            self.arrowRight()
            time.sleep(5)
        self.exit()
        time.sleep(1)
        self.pwr()
        time.sleep(1)
        print 'completed -diag page'
        
    def OSD_mainMenu(self):

	for x in range(0,3):        
            print 'traversing through OSD main menu'
            print 'D01 Health Check'
            time.sleep(OSDDelay_main)
            self.arrowDown()
            print 'D02 General Status'
            time.sleep(OSDDelay_main)
            self.arrowDown()
            print 'D03 Memory'
            time.sleep(OSDDelay_main)
            self.arrowDown()
            print 'D04 Tuner Status'
            time.sleep(OSDDelay_main)
            self.arrowDown()
            print 'D05 General I/O'
            time.sleep(OSDDelay_main)
            self.arrowDown()
            print 'D06 MoCA'
            time.sleep(OSDDelay_main)
            self.arrowDown()
            print 'D07 Conditional Access'
            time.sleep(OSDDelay_main)
            self.arrowDown()
            print 'D08 Home Networking'
            time.sleep(OSDDelay_main)
            self.arrowDown()
            print 'D09 TR-069'
            time.sleep(OSDDelay_main)
            self.arrowDown()
            print 'D10 CableCard'
            
            time.sleep(OSDDelay_main)
            self.arrowUp()
            print 'D09 TR-069'
            time.sleep(OSDDelay_main)
            self.arrowUp()
            print 'D08 HN'
            time.sleep(OSDDelay_main)
            self.arrowUp()
            print 'D07 CA'
            time.sleep(OSDDelay_main)
            self.arrowUp()
            print 'D06 MoCA'
            time.sleep(OSDDelay_main)
            self.arrowUp()
            print 'D05 Genral I/O'
            time.sleep(OSDDelay_main)
            self.arrowUp()
            print 'D04 Tuner Status'
            time.sleep(OSDDelay_main)
            self.arrowUp()
            print 'D03 Memory'
            time.sleep(OSDDelay_main)
            self.arrowUp()
            print 'D02 Genral Status'
            time.sleep(OSDDelay_main)
            self.arrowUp()
            print 'D01 Health Check'


    def OSD1_browse(self):
        print 'entered OSD1_browse'
        for x in range(0,1):
            self.arrowRight()
            time.sleep(OSDDelay_main)
            self.arrowDown()
            time.sleep(OSDDelay_main)
            self.arrowUp()
            time.sleep(OSDDelay_main)
            self.arrowRight()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay_main)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowRight()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)

        print 'exit OSD1_browse'

    def OSD2_browse(self):
        print 'entered OSD2_browse'
        self.arrowDown()
        time.sleep(OSDDelay_main)
        for x in range(0,1):
            self.arrowRight()
            time.sleep(OSDDelay_main)
            self.arrowDown()
            time.sleep(OSDDelay_main)
            self.arrowDown()
            time.sleep(OSDDelay_main)
            self.arrowUp()
            time.sleep(OSDDelay_main)
            self.arrowUp()
            time.sleep(OSDDelay_main)
            self.arrowRight()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            
            self.arrowLeft()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)
            
        print 'exit OSD2_browse'
            
    def OSD3_browse(self):
        print 'entered OSD3_browse'
        self.arrowDown()
        time.sleep(OSDDelay_main)
        for x in range(0,1):
            self.arrowRight()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)

    def OSD4_browse(self):
        print 'entered OSD4_browse'
        self.arrowDown()
        time.sleep(OSDDelay_main)
        for x in range(0,1):
            self.arrowRight()
            time.sleep(OSDDelay_main)
            self.arrowDown()
            time.sleep(OSDDelay_main)
            self.arrowUp()
            time.sleep(OSDDelay_main)
            self.arrowRight()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)    
          
        print 'exit OSD4_browse'

            
    def OSD5_browse(self):
        print 'entered OSD5_browse'
        self.arrowDown()
        time.sleep(OSDDelay_main)
        for x in range(0,1):
            self.arrowRight()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)
        print 'exit OSD5_browse'
           

    def OSD6_browse(self):
        print 'entered OSD6_browse'
        self.arrowDown()
        time.sleep(OSDDelay_main)
        for x in range(0,1):
            self.arrowRight()
            time.sleep(OSDDelay_main)
            self.arrowDown()
            time.sleep(OSDDelay_main)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)

        print 'exit OSD6_browse'

    def OSD7_browse(self):
        print 'entered OSD7_browse'
        self.arrowDown()
        time.sleep(OSDDelay_main)
        for x in range(0,1):
            self.arrowRight()
            time.sleep(OSDDelay_main)
            self.arrowDown()
            time.sleep(OSDDelay_main)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowRight()
            time.sleep(OSDDelay_main)
            
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowDown()
            time.sleep(OSDDelay)
            self.arrowUp()
            time.sleep(OSDDelay)
            self.arrowUp()
   
            self.arrowLeft()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)

        print 'exit OSD7_browse'


    def OSD8_browse(self):
        print 'entered OSD8_browse'
        self.arrowDown()
        time.sleep(OSDDelay_main)
        for x in range(0,1):
            self.arrowRight()
            time.sleep(OSDDelay_main)
            self.arrowLeft()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)

        print 'exit OSD8_browse'

    def OSD9_browse(self):
        print 'entered OSD9_browse'
        self.arrowDown()
        time.sleep(OSDDelay_main)
        for x in range(0,1):
            self.arrowRight()
            time.sleep(10)
            self.arrowLeft()
            time.sleep(OSDDelay)
            self.arrowLeft()
            time.sleep(OSDDelay)

        print 'exit OSD9_browse'

    def OSD10_browse(self):
        
        print 'entered OSD10_browse'
        self.arrowDown()
        time.sleep(OSDDelay_main)
        for x in range(0,1):
            self.arrowRight()
            time.sleep(OSDDelay_main)
            
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)

            print 'End CA Screen'
                
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)

            print 'End Host Id screen'
            
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)

            print 'End IP service'
            
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)

            print 'End 55-1 Screen'
            
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            
            print 'End CP Info'
            
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.arrowDown()
            time.sleep(CCPageDelay)
            self.select()
            time.sleep(CCPageDelay)
            self.arrowLeft()
            time.sleep(CCPageDelay)
            self.arrowLeft()
            time.sleep(CCPageDelay)

        print 'exit OSD10_browse'



    def exitOSD(self):
        print 'exiting OSD operation'
        time.sleep(OSDDelay)
        self.exit()
        time.sleep(OSDDelay)
        self.exit()
        time.sleep(OSDDelay)

    def OSD_browse(self):
        for x in range(0,1):
            print 'invoke OSD and browse thru pages'
            self.invokeOSD()
            time.sleep(OSDDelay_main)
            self.OSD_mainMenu()
            self.OSD1_browse()
            self.OSD2_browse()
            self.OSD3_browse()
            self.OSD4_browse()
            self.OSD5_browse()
            self.OSD6_browse()
            self.OSD7_browse()
            self.OSD8_browse()
            self.OSD9_browse()
            self.OSD10_browse()
            self.exitOSD()
            print 'finished first OSD operations'

            print 'invoke transparent OSD and browse thru pages'
            self.invokeOSD()
            time.sleep(OSDDelay_main)
            self.A()
            time.sleep(OSDDelay_main)
            self.OSD_mainMenu()
            self.OSD1_browse()
            self.OSD2_browse()
            self.OSD3_browse()
            self.OSD4_browse()
            self.OSD5_browse()
            self.OSD6_browse()
            self.OSD7_browse()
            self.OSD8_browse()
            self.OSD9_browse()
            self.OSD10_browse()
            self.exitOSD()
            print 'finished transparent OSD operations'

##            print 'powering off/on the box'
##            self.pwr()
##            time.sleep(OSDDelay_main)
        print 'finished entire OSD operations'
        self.A()
        time.sleep(OSDDelay)   

    def playback(self):

        print 'starting playback'
        self.list()
        time.sleep(dvrdelay)
        self.arrowRight()
        time.sleep(dvrdelay)
        self.select()
        time.sleep(dvrdelay)
        self.select()
        time.sleep(dvrdelay)
        time.sleep(dvrdelay)
        self.fastForward()
        time.sleep(dvrdelay)
        time.sleep(dvrdelay)
        self.rewind()
        time.sleep(dvrdelay)
        time.sleep(dvrdelay)
        self.play()
        time.sleep(20)
        self.FiOS()
        time.sleep(dvrdelay)
        self.stop()
        time.sleep(dvrdelay)
        self.exit()

        print 'End Playback'

    def switchChannels(self):
        chanNum = 0101
        print 'switiching between channels to test playback'

        self.channelUp()
        time.sleep(5)
        self.channelUp()
        time.sleep(5)
        self.channelDown()
        time.sleep(5)
        self.channelUp()
        time.sleep(5)
        self.channelDown()
        time.sleep(5)
        self.channelUp()
        time.sleep(5)
        self.channelDown()
        time.sleep(5)

        print 'End switching between two channels'
        


def test(ir):
    s = SetupPacket('01FFFF')
    c = TxPacket('011B1D')
    for x in range(20):        
        ir.sendCmd(c)
        time.sleep(1)


class script1(Thread):
    def __init__(self, obj):
        Thread.__init__(self, None, None, "script1")
        self.obj = obj
        print "class script1 - init\n"
    def run(self):        
        print "Script 1 - Started\n"
        while 1:
            rmt.channelUp()
            time.sleep(5)

class script2(Thread):
    def __init__(self, obj):
        Thread.__init__(self, None, None, "script2")
        self.obj = obj
        print "class script2 - init\n"
    def run(self):
        print "Script 2 - Started\n"
        while 1:
            rmt.channelDown()
            time.sleep(5)

if __name__ == '__main__':
    rmt = IrTelnetBlaster()
    rmt.setup()
    rmt.open()
    scr1 = script1(rmt)
    scr2 = script2(rmt)
    scr1.start()
    scr2.start()
    time.sleep(1)
    print 'Press Ctl+c to stop the Script\n'
    while 1:
        try:
            raw_input('')
        except KeyboardInterrupt:
            rmt.close()
            sys.exit(1)
        
       
    
##if __name__ == '__main__':
##    rmt = IrTelnetBlaster()
##    rmt.setup()
##    rmt.open()
##    rmt.channelUp()
##    startTime = time.time()
##
##    tuneDelay = 5
##    menuDelay = 3
##    print 'tuning delay = ',tuneDelay
##    time.sleep(tuneDelay)
##       
##
##    rmt.switchChannels()
##    
##    time.sleep(tuneDelay)        
##    rmt.channelUp()
##    time.sleep(2)
##    rmt.channelUp()
##
##        
##    rmt.playback()
##
##    rmt.switchChannels()
##
##    print 'channel up operations'
##    
##    for x in range (0,30):
##        rmt.channelUp()
##        time.sleep(tuneDelay)
##	
##    print 'channel down operation'        
##
##    for x in range (0,30):
##        rmt.channelDown()
##        time.sleep(tuneDelay)
##
##    rmt.invokeOSD()
##    time.sleep(OSDDelay_main)
##    rmt.OSD_browse()
##    rmt.exitOSD()
##		
##    rmt.playback()
##
##    rmt.switchChannels()
##    
##    while 1:
##
##        rmt.traverseGuide()
##                
##        print 'channel up operations'
##        for x in range (0,20):
##            rmt.channelUp()
##            time.sleep(tuneDelay)
##
##        rmt.volumeUp()
##        rmt.volumeDown()
##
##        rmt.traverseMenu()
##
##        rmt.playback()
##        rmt.switchChannels()
##        
##        print 'channel down operation'        
##        for x in range (0,20):
##            rmt.channelDown()
##            time.sleep(tuneDelay)
##    
##        rmt.traverseGuide()
##
##        rmt.invokeOSD()
##        time.sleep(OSDDelay_main)
##        rmt.OSD_browse()
##        rmt.exitOSD()
##
##        rmt.playback()
##        
##        rmt.volumeUp()
##        rmt.volumeDown()        
##
##        rmt.traverseMenu()
##        rmt.switchChannels()
##        
##        for y in range(0,10):
##            chan= rmt.chanMap.defStart
##            temp = chan
##            #temp = temp+1
##            print temp
##            rmt.channelUp()
##            time.sleep(tuneDelay)
##            for x in range (0,64):
##                rmt.channelUp()
##                time.sleep(tuneDelay)
##            runTime = (time.time())-startTime
##            print 'run time: ',runTime
##            print 'channel up finished'
##
##            rmt.playback()
##                       
##            chan= rmt.chanMap.defEnd
##            rmt.channelUp()
##            time.sleep(tuneDelay)
##            for x in range (0,64):
##                rmt.channelDown()
##                time.sleep(tuneDelay)
##            runTime = (time.time())-startTime
##            print 'run time: ',runTime
##            print 'channel down finished'
##
##            rmt.volumeUp()
##            rmt.volumeDown()
##
##            rmt.traverseGuide()
##            rmt.traverseMenu()
##            rmt.playback()
##            rmt.switchChannels()
##
##            rmt.volumeUp()
##            rmt.volumeDown()        
##                
##            runTime = (time.time())-startTime            
##            print 'run time: ',runTime
##            print'channel swapping finished'
##
##
##        rmt.invokeOSD()
##        time.sleep(OSDDelay_main)
##        rmt.OSD_browse()
##        rmt.exitOSD()
##        rmt.switchChannels()
##        rmt.playback()
##    rmt.close()
   
