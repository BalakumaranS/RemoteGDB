import pyaudio
import wave
from array import array
import time,sys,getopt

#####################################################
#Variables and constants
#####################################################

CHUNK = 256
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 2
WAVE_OUTPUT_FILENAME = "Recorded_"+str(int(time.time()))+".wav"
WAVE_OUTPUT_FILEPATH = "C://EEVAA/public/Recordings/"+WAVE_OUTPUT_FILENAME


#####################################################
#Initialize and Terminate PyAudio Functions
#####################################################

def initialize():
	"""
	Initialize PyAudio API before calling any other functions
	"""
	return pyaudio.PyAudio()

def terminate(pyaudioInstance):
	"""
	Terminate a previously initialized PyAudio instance creating using initialize() function.
	"""
	pyaudioInstance.terminate()
	
#####################################################
#Stream Management Functions
#####################################################

def openStream(pa,input=False,output=False,channels=CHANNELS,format=FORMAT,rate=RATE,frames_per_buffer=CHUNK):
	"""
	Opens a Stream using PortAudio API for recording from and/or playing through input and/or output audio devices.
	
	Parameters : *args
	pa - instance of pyaudio.PyAudio class,
	rate - Sampling rate,
    channels - Number of channels,
    format - PyAudio Formats,
    input=False - for Output only stream,
    output=False - for Input only stream,
    input_device_index=None - for default input device,
    output_device_index=None - for default output device,
    frames_per_buffer=1024,
    start=True - if you want the stream to be started immediately after creation, else call stream.start_stream(),
    input_host_api_specific_stream_info=None,
    output_host_api_specific_stream_info=None,
    stream_callback=None
	"""
	stream = pa.open(channels=channels,format=format,rate=rate,input=input,output=output,frames_per_buffer=frames_per_buffer)
	return stream

def closeStream(pa,stream):
	"""
	Closes a previously opened Stream using openStream() function.
	"""
	stream = pa.close(stream)

def startStream(stream):
	"""
	Call this function if start=True was not sent while calling the openStream() function.
	"""
	stream.start_stream()
	return stream._is_running

def stopStream(stream):
	"""
	Call this function to stop the stream opened using openStream() with start=True / started using startStream().
	"""
	stream.stop_stream()
	return stream._is_running

	
#####################################################
#Stream Access Functions
#####################################################

def readStream(pa,stream,sampRate=RATE,dataChunk=CHUNK,recordSeconds=RECORD_SECONDS,saveFile=False,saveFileName=WAVE_OUTPUT_FILEPATH):
	"""
	Reads from the input stream instance in a blocking-mode and returns the data list.
	
	Returns : A string of the data read from the input stream.
	"""
	buffers = []
	nBuffers = int(sampRate/dataChunk)*recordSeconds
	print "Recording - [",
	for i in range(0,nBuffers):
		tempData = stream.read(CHUNK)
		buffers.append(tempData)
	print "* ]"
	print "Finished Recording"
	if saveFile is True:
		saveAudio(filepath=saveFileName,data=buffers,sampSize=pa.get_sample_size(format=FORMAT))
	return buffers

def writeStream(stream,wfI=False,rdI=False,dataChunk=CHUNK,wFileO=None,rData=None):
	"""
	Writes to the output stream instance in a blocking-mode.
	"""
	print "Playback"
	if wfI is True:
		data = wFileO.readframes(dataChunk)
		while data != '':
			stream.write(data)
			data = wFileO.readframes(CHUNK)
	elif rdI is True:
		for i in range(0,len(rData)):
			stream.write(rData[i])
	print "Finished Playback"

#####################################################
#WAV Functions
#####################################################

def saveAudio(filepath=None,data=None,channels=CHANNELS,sampSize=None,rate=RATE):
	"""
	Saves the recorded audio as a file. The user is suggested to use the .wav extension in the filename
	"""
	wf = wave.open(filepath, 'wb')
	wf.setnchannels(channels)
	wf.setsampwidth(sampSize)
	wf.setframerate(rate)
	wf.writeframes(b''.join(data))
	wf.close()
	print "[Assertion : Saved Audio. File at "+filepath+"]"

#####################################################
#Audio Processing Functions
#####################################################

def audioPresence(data):
	"""
	"""
	Ordframes = map(ord,"".join(data))
	#print Ordframes.count(0), len(Ordframes)
	if Ordframes.count(0) < 0.35 *len(Ordframes):
		return True
	else:
		return False

#####################################################
#Unit test
#####################################################

def testRecord(recordtime,testname):	
	filename = testname+".mp3"
	filepath = "C://EEVAA/public/Recordings/"+filename
	pa = initialize()
	stream = openStream(pa,input=True,output=False,channels=CHANNELS,format=FORMAT,rate=RATE,frames_per_buffer=CHUNK)
	recordedData = readStream(pa,stream,sampRate=RATE,dataChunk=CHUNK,recordSeconds=recordtime,saveFile=True,saveFileName=filepath)
	#writeStream(stream,rdI=True,rData=recordedData)
	stopStream(stream)
	closeStream(pa,stream)
	if audioPresence(recordedData) is True:
		print "[Output: Audio was detected]"
	else:
		print "[Output: Audio was not detected]"
	terminate(pa)

def testPlayback(recordtime,testname):
	#WAVE_OUTPUT_FILEPATH = "Recordings/"+testname+".wav"
	pa = initialize()
	wf = wave.open(testname,'rb')
	stream = openStream(pa,output=True,format=pa.get_format_from_width(wf.getsampwidth()),channels=wf.getnchannels(),rate=wf.getframerate())
	writeStream(stream,wfI=True,wFileO=wf)
	wf.close()
	stopStream(stream)
	closeStream(pa,stream)	
	terminate(pa)

def argparser(arg):
    """
    Parses the command line arguments and invokes the <modulename> (-m) with the <channelnumber> (-c)
    """
    try:
        opts, args = getopt.getopt(arg,"hm:c:t:")
    except getopt.GetoptError:
        print 'Filename -m <modulename> -c <recordtime>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage: Filename -m <modulename> -c <recordtime>'
            sys.exit()
        elif opt == '-m':
            modulename = arg
        elif opt == '-t':
            testname = arg
        elif opt == '-c':
            recordtime = int(arg)
    globals()[modulename](recordtime,testname)

if __name__ == "__main__":
	argparser(sys.argv[1:])
    