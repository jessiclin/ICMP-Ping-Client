from socket import *
import os
import sys
import struct
import time
import select
import binascii

ICMP_ECHO_REQUEST = 8
minimum = float(100)
maximum = float(0)
avgRTT = float(0)
totalPings = 0;
lostPings = 0;

def checksum(string):
    csum = 0
    countTo = (len(string) // 2) * 2
    count = 0
    while count < countTo:
        thisVal = string[count+1] * 256 + string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
        
    if countTo < len(string):
        csum = csum + string[len(string) - 1]
        csum = csum & 0xffffffff
        
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    global minimum
    global maximum
    global avgRTT
    global totalPings
    global lostPings
    
    totalPings = totalPings + 1;
    while 1:
        try: 
            startedSelect = time.time()
            whatReady = select.select([mySocket], [], [], timeLeft)
            howLongInSelect = (time.time() - startedSelect)
            #print(whatReady[0])
                
            if whatReady[0] == []: # Timeout
                lostPings = lostPings + 1
                return "Request timed out."
            timeReceived = time.time()
            recPacket, addr = mySocket.recvfrom(1024)

            #Fetch the ICMP header from the IP packet
            header = struct.unpack("bbHHh", recPacket[20:28])
            data = struct.unpack("d", recPacket[28:])[0]
            
            ICMPType = header[0]
            code = header[1]
            sequence = header[4]
            
            if ICMPType == 0 and code == 0:
                #Get the RTT for this ping
                rtt = timeReceived - data
                
                #Update minimu, maximum, and average
                if rtt < minimum:
                    minimum = rtt
                if rtt > maximum:
                    maximum = rtt
                avgRTT = (avgRTT + rtt)/2
                
                TTL = struct.unpack("b", recPacket[8:9])[0]
                
                delay = "Received packet from " + str(destAddr) + " : icmp_seq = " + str(sequence) + " TTL = "  + str(TTL) +  " time(ms): " + str(rtt*1000)

                timeLeft = timeLeft - howLongInSelect

                if timeLeft <= 0:
                    lostPings = lostPings + 1
                    return "Request timed out."
                        
                return delay
        except KeyboardInterrupt:
            print ("\n------" + gethostbyaddr(destAddr)[0] + " (" + destAddr + ") PING statistics------")
            perc = (float(lostPings/totalPings)) * 100       
            print(str(totalPings) + " packets transmitted, " + str((totalPings - lostPings)) + " packets received, "+ str(perc) + "% packet loss")
            print("round-trip (ms)  minimum = " + str(minimum*1000) + "   |   maximum = " + str(maximum*1000) + "   |   average = " + str(avgRTT*1000))
            sys.exit(0)
            #return 2



def sendOnePing(mySocket, destAddr, ID):
    # Header is type (8), code (8), checksum (16), id (16), sequence (16)
    myChecksum = 0

    # Make a dummy header with a 0 checksum
    # struct -- Interpret strings as packed binary data
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    
    # Calculate the checksum on the data and the dummy header.
    myChecksum = checksum(header + data)
    
    # Get the right checksum, and put in the header
    if sys.platform == 'darwin':
        # Convert 16-bit integers from host to network byte order
        myChecksum = htons(myChecksum) & 0xffff
    else:
        myChecksum = htons(myChecksum)

    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)

    packet = header + data
    #print(packet);
    mySocket.sendto(packet, (destAddr, 1)) # AF_INET address must be tuple, not str
    # Both LISTS and TUPLES consist of a number of objects
    # which can be referenced by their position number within the object.

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    
    # SOCK_RAW is a powerful socket type. For more details: http://sockraw.org/papers/sock_raw
    mySocket = socket(AF_INET, SOCK_RAW, icmp)

    myID = os.getpid() & 0xFFFF # Return the current process i
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    mySocket.close()
    return delay

      
def ping(host, timeout=1):
    # timeout=1 means: If one second goes by without a reply from the server,
    # the client assumes that either the client's ping or the server's pong is lost
    global minimum
    global maximum
    global avgRTT
    global totalPings
    global lostPings
    dest = gethostbyname(host)
    print("Pinging host: " + host + " at: " + dest + " using Python:")
    print("")
    # Send ping requests to a server separated by approximately one second
    while 1 :
        try: 
            delay = doOnePing(dest, timeout)
            print(delay)
            time.sleep(1)# one second
        except KeyboardInterrupt:
            #print("return")
            print ("\n------" + host + " (" + gethostbyname(host) + ") PING statistics------")
            perc = (float(lostPings/totalPings)) * 100
            print(str(totalPings) + " packets transmitted, " + str((totalPings - lostPings)) + " packets received, " + str(perc) + "% packet loss")
            print("round-trip (ms)  minimum = " + str(minimum*1000) + "   |   maximum = " + str(maximum*1000) + "   |   average = " + str(avgRTT*1000))
            sys.exit(0)
            #return 1
    return delay

if __name__ == "__main__":
    
    host = sys.argv[1] if len(sys.argv) > 1 else 'localhost'
    #site = input("What webserver do you want ping? ")
    ping(host)
        

