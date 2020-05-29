# ICMP-Ping-Client

# Run Instructions 
To ping local host: 
> python ping.py

To ping a server other than localhost 
> python ping.py [webserver] (i.e. python ping.py www.google.com)

To run the programming assignment 3 code with the desired webserver to be pinged, first run the pa03.py file.

# Output 
Once the user inputs their desired webserver, the program will print out the IP address from which 
it receives their packet, the ICMP sequence, the Time to live (TTL), and the round trip time (time) in milliseconds
for each ping. 

# To Quit: 
Once the user presses CTRL-C, the program will stop receiving packets and print out the 
PING statistics. The statistics include the total packets transmitted, the number of packets lost, packet loss 
percentage, and the minimum, maximum, and average round trip times in milliseconds. 