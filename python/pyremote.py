import sys,serial,getopt,time

serialObj = None
commport = 3
irtekCommands = {'up':'tffff0821b1d0\n','down':'tffff0821b1e0\n','power':'tffff0821b070','v':'v',1:'tffff0821b100',2:'tffff0821b110',3:'tffff0821b120',4:'tffff0821b130',5:'tffff0821b140',6:'tffff0821b150',7:'tffff0821b160',8:'tffff0821b170',9:'tffff0821b180',0:'tffff0821b190'}

def initialize():
	"""
	Initialize a serial object for sending commands to STB via IrTek
	"""
	global serialObj
	if not serialObj:
		try:
			serialObj = serial.Serial(port=commport,baudrate=115200,bytesize=8,parity='N',stopbits=1,timeout=1,xonxoff=0,rtscts=0)
			time.sleep(15)
		except serial.SerialException:
			print 'Serial Port Error : '+str(sys.exc_info()[0])
			serialObj = None
	return not not serialObj

def close():
	"""
	"""
	serialObj.close()
	return serialObj.isOpen()
	
def sendcommand(c):
	"""
	Send commands to STB via a serial object initialized using initialize()
	"""
	if serialObj:
		try:
			serialObj.write(irtekCommands[c])
			time.sleep(1)
			n = serialObj.inWaiting()
			if n:
				serialObj.read(n)
		except serial.SerialException:
			print 'Serial port write error : '+str(sys.exc_info()[0])
	else:
		print 'Serial port not open'

def testCode(c,cn):
	"""
	Skeleton for initializing a serial port and sending command to STB (via IrTek)
	"""
	initialize()
	if c =='channel':
		clist = []
		while(cn):
			clist.append(cn%10)
			cn=cn/10
		while(clist):
			sendcommand(clist.pop())
	else:
		sendcommand(c)
	print close()
		
def argparser(arg):
    """
    Parses the command line arguments and invokes the <modulename> (-m) with the <channelnumber> (-c)
    """
    try:
        opts, args = getopt.getopt(arg,"hm:c:t:")
    except getopt.GetoptError:
        print 'Filename -m <modulename> -c <command>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: Filename -m <modulename> -c <command>'
            sys.exit()
        elif opt == '-m':
			modulename = arg
        elif opt == '-c':
            command = arg
        elif opt == '-t':
            channelnumber = int(arg)
    globals()[modulename](command,channelnumber)

if __name__ == "__main__":
	argparser(sys.argv[1:])