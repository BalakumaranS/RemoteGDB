import os
import time
import subprocess
import sys
import uuid

env1 = os.system("set sysroot i/home/team_auto/XidToolChains/XiD_BCM_URSR/toolchains/stbgcc-4.5.4-2.7/arm-linux-uclibcgnueabi/sys-root/")
env2 = os.system("set solib-search-path /home/team_auto/XidToolChains/XiD_BCM_URSR/toolchains/stbgcc-4.5.4-2.7/arm-linux-uclibcgnueabi/sys-root/")

coredump = str(sys.argv[1])

newfilename = "Coredump"+str(uuid.uuid4())

if os.path.exists(coredump):
    os.system("mv "+coredump+" /home/team_auto/pyexec/tests/pkdta/CoreDumpResolve/coredumps/"+newfilename)
    if (os.path.exists(coredump) & env1==0 & env2==0):
        p = subprocess.Popen(['/home/team_auto/XidToolChains/XiD_BCM_URSR/toolchains/stbgcc-4.5.4-2.7/bin/arm-linux-gdb'],stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(1)
         
        p.stdin.write('core '+'/home/team_auto/pyexec/tests/pkdta/CoreDumpResolve/coredumps/'+newfilename+'\n')

        time.sleep(0.5)

        p.stdin.write('bt\n')

        time.sleep(0.5)

        p.stdin.write("quit\n")

        time.sleep(1)

        output = p.communicate()

        print "*************************************\n\tResolved Coredump\n*************************************\n\n"
        print output[0][509:]

else:
    print "hey! Check the file name"






