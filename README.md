# ICMP-Ping-Client
ICMP-Ping-Client implements a Ping application using ICMP request and reply messages by sending ICMP echo request messages to the specified servver, waiting for the echo reply messahes sent in response, 
and keeping statistics on the round-trip time and packet loss. 


This application sends ping requests to a specified host separated by approximately one second. Each message contains a payload of data that includes a timestamp. After sending each packet, the application waits up to one 
second to receive a reply. If one second goes by without a reply from the server, then the client assumes that either the ping packet or the pong packet was lost in the network (or that the server is down)

# Run Instructions 
To ping local host: 
> python ping.py

To ping a server other than localhost 
> python ping.py [webserver] 
> (i.e. python ping.py www.google.com)

To run the programming assignment 3 code with the desired webserver to be pinged, first run the pa03.py file.

# Output 
Once the user inputs their desired webserver, the program will print out the IP address from which 
it receives their packet, the ICMP sequence, the Time to live (TTL), and the round trip time (time) in milliseconds
for each ping. 

# To Quit: 
Once the user presses CTRL-C, the program will stop receiving packets and print out the 
PING statistics. The statistics include the total packets transmitted, the number of packets lost, packet loss 
percentage, and the minimum, maximum, and average round trip times in milliseconds. 