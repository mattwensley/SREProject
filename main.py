import sys, os
from subprocess import Popen, PIPE

ips = ["4.4.4.4", "8.8.8.8"]

def ping_ip(name):
    #sys.stdout = open(name+"output.txt","w")
    if os.path.exists(name+"output.txt"):
        os.remove(name+"output.txt")
    if "linux" in sys.platform.lower():
        print("Linux")
        pingcmd = "ping " + name
    elif sys.platform == "win32":
        print("Windows")
        pingcmd = "ping -t " + name + " > " + name+"output.txt"

    os.system(pingcmd)



if __name__ == '__main__':
    for i in range(len(ips)):
        print("pinging:",ips[i])
        ping_ip(ips[i])

