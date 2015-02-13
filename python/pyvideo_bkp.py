import time,sys,getopt

#val=(int(raw_input("Enter the no: ")))

def test(a):
	val = a
	print "Printing"
	time.sleep(60)
	if val<2:
		print "[Output:Less]"
	elif val>2:
		print "[Output:Greater]"
	else:
		print "[Output:Equal]"
	print "[Image:asdfdsafsadf]"

def argparser(arg):
	"""
	Parses the command line arguments and invokes the <modulename> (-m) with the <channelnumber> (-c)
	"""
	try:
		opts, args = getopt.getopt(arg,"hm:c:")
	except getopt.GetoptError:
		print 'Filename -m <modulename> -c <channelnumber>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'Usage: Filename -m <modulename> -c <channelnumber>'
			sys.exit()
		elif opt == '-m':
			module = arg
		elif opt == '-c':
			channelnumber = arg
	globals()[module](channelnumber)
if __name__ == "__main__":
	argparser(sys.argv[1:])
