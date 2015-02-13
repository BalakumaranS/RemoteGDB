import telnetlib,time
import ircodes

__author__ = 'gmuralit and anganesa'


### Box types ###
EXPLORER = 0
OCAP = 1
IPTV = 2
DTA_XMP = 3
MOTOROLA = 4
EXPLORERDIAG=5

### IrTekClient class ###

class IrTekClient():
    """
    Base class of IrTekClient
    """

    def __init__(self, host, port, rtype, burst):
        self.host = host
        self.port = port
        self.connect_state = False
        self.connect_instance = None
        self.burst = burst
        if rtype == EXPLORER:
            self.ir_codes = ircodes.IRCodes56()
        elif rtype == DTA_XMP:
            self.ir_codes = ircodes.IRCodesDTA()
        elif rtype == MOTOROLA:
            self.ir_codes = ircodes.IRCodesMotorola()
        elif rtype == EXPLORERDIAG:
            self.ir_codes = ircodes.IRCodes56Burst()
            print "burst"


    def connect(self):
        """
        Connect to the IrTek host:port
        """
        if not self.connect_state:
            self.connect_instance = telnetlib.Telnet(self.host,self.port)
            self.connect_state = True
            print "Connected to the device"
        else:
            print "Already connected to the device"

    def disconnect(self):
        """
        Disconnect from IrTek host:port
        """
        if self.connect_state:
            self.connect_instance.close()
            self.connect_state = False
            self.connect_instance = None
            print "Disconnect from the device"
        else:
            print "Already disconnected from the device"

    def send_cmd(self,data):
        """
        Send command to the IrTek host:port device
        """
        print 'Writing to device - %s'%data
        self.connect_instance.write(data)
        #time.sleep(0.8)

    def cmd_wrap(self,cmd):
        """
        Wrap the command with appropriate details to be sent to the IrTek

        @Params:
        cmd - IrTek command for a specific operation

        @Return:
        cmd - cmd wrapped with appropriate headers and terminators
        """
        ir_codes = self.ir_codes
        protocol = ir_codes.protocol
        data_size = ir_codes.data_size
        mask = 0xffff
        option = ''
        
        if self.burst <> 3:
            option += '4%04x'%(self.burst)
            #print "option inside <>"
        cmd = 't%04x%s%s%s%s0'%(mask,protocol,data_size,cmd,option)
        
        return cmd

### PyRemote class ###

class PyRemote(IrTekClient):
    """
    PyRemote class inheriting IrTekClient class
    """

    def __init__(self, host, port, rtype, burst=None):
        IrTekClient.__init__(self, host, port, rtype, burst)
        self.connect()

    def __del__(self):
        self.disconnect()

    def channel_up(self):
        """
        Send Channel Up code to IrTek host:port
        """
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_up))

    def channel_down(self):
        """
        Send Channel Down code to IrTek host:port
        """
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))

    def channel_info(self):
        """
        Send Channel Down code to IrTek host:port
        """
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_info))
        
    def channel_tune(self,channel_number):
        """
        Tune to channel_number

        @Params:
        channel_number - Channel number, integer
        """
        channel_array = []
        while channel_number>0:
            digit = channel_number % 10
            channel_number /= 10
            channel_array.append(digit)
        while channel_array:
            digit = channel_array.pop()
            if digit == 0:
                key = self.ir_codes.key0
            elif digit == 1:
                key = self.ir_codes.key1
            elif digit == 2:
                key = self.ir_codes.key2
            elif digit == 3:
                key = self.ir_codes.key3
            elif digit == 4:
                key = self.ir_codes.key4
            elif digit == 5:
                key = self.ir_codes.key5
            elif digit == 6:
                key = self.ir_codes.key6
            elif digit == 7:
                key = self.ir_codes.key7
            elif digit == 8:
                key = self.ir_bcodes.key8
            elif digit == 9:
                key = self.ir_codes.key9
            IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,key))
            time.sleep(0.5)
	
	def send_digit(self,digit):
		"""
		Send a key code to the IrTek host:port
		
		@Params:
		digit - number to be sent, integer
		"""
		if digit == 0:
			key = self.ir_codes.key0
		elif digit == 1:
			key = self.ir_codes.key1
		elif digit == 2:
			key = self.ir_codes.key2
		elif digit == 3:
			key = self.ir_codes.key3
		elif digit == 4:
			key = self.ir_codes.key4
		elif digit == 5:
			key = self.ir_codes.key5
		elif digit == 6:
			key = self.ir_codes.key6
		elif digit == 7:
			key = self.ir_codes.key7
		elif digit == 8:
			key = self.ir_codes.key8
		elif digit == 9:
			key = self.ir_codes.key9
		elif digit == 11:
                        key = self.ir_codes_key0 + self.ir_codes_key0
		IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,key))
		
    def enter(self):
        """
        Press enter key
        """
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.select))

    def last(self):
        """
        Press last key
        """
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.last))

    def diag_page(self):
        """
        Invoke diagnostics page (Not working)
        """
        key = self.ir_codes.key7
        for x in range(0,1):
            print 'send'
            IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.exit))
            time.sleep(0.5)
            IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.select))
            time.sleep(0.5)
            IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.info))
            time.sleep(0.5)

    def arrowDown(self, repeat =15 , duration =1000):
        for x in range(0, repeat):
            
            IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.key7))
            #time.sleep(10)
           # IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.key7))
           # IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.key7))
       
    def arrowDown_mod(self):
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.key7))
        time.sleep(3)
         
    def  diag_messages(self):
        # invoking the diag screen by pressing the info and then a long delay 
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.info))
        time.sleep(5)
       
        
        
    def diag_navigate_code(self):
        # Navigate to Code download Page 
        
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.select))
        time.sleep(1)

        
    def diag_navigate1(self):	
        # Navigate to Received Messages Page 		
	
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)

        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.select))
        time.sleep(1)
    def diag_navigate_270(self):	
        # Navigate to Received Messages Page 		
	
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.channel_down))
        time.sleep(1)
        

        IrTekClient.send_cmd(self,IrTekClient.cmd_wrap(self,self.ir_codes.select))
        time.sleep(1)
        

        	
            
	


if __name__ == '__main__':
    
      # Commented foe checking each function individually 
      """p = PyRemote('10.78.203.158', 4002, 0, 100)
      p.diag_messages()
      p.disconnect()
      
      
      p = PyRemote('10.78.203.158', 4002, 0, 1)
      p.diag_navigate1()
      p.disconnect()"""
      
      """p = PyRemote('10.78.203.158', 4002, 0, 0)
      #p.connect()
      p.enter()
      p.disconnect() """
      p = PyRemote('10.78.203.158', 4002, 0, 1)
      p.channel_tune(7)
      #p.channel_down()
      #p.channel_up()
      #p.last()
      #p.channel_up()
      #p.arrowDown()
      #p.diag_messages()
      #p.diag_navigate1()
     # p.arrowDown()
     # p.arrowDown_mod()
     #p.send_digit(11)
     #p.send_digit(11)
     # p.channel_info()
