# Routing.py
# Implementation of the FSC Routing project by Jared Knutson, Clayton Franklin, and Ian Grant.
# Class: CPE 400
# Date: 05 Dec 2018
# header files
import socket
import sys
import threading
import threading
import socketserver
import os
import time
import random
from random import randint

# set global variables
NID = 0
hostname = ' '
udp_port = 0
tcp_port = 0
l1_NID = 0
l2_NID = 0
l3_NID = 0
l4_NID = 0
l1_hostname = ' '
l2_hostname = ' '
l3_hostname = ' '
l4_hostname = ' '
l1_udp_port = 0
l2_udp_port = 0
l3_udp_port = 0
l4_udp_port = 0
l1_tcp_port = 0
l2_tcp_port = 0
l3_tcp_port = 0
l4_tcp_port = 0

# create node object variable
node = None

# function: InitializeTopology
def InitializeTopology (nid, itc):

    # global variables
    global node

    # initialize node object
    node = Node(int(nid))

    # open itc.txt file and read to list
    infile = open(itc)
    list = infile.readlines()

    # initialize lists for hostnames and port numbers
    hostnames = []
    ports = []

    # populate hostname and port lists
    for entry in list:
        temp = entry.split(' ')
        hostnames.append(temp[1])
        ports.append(int(temp[2]))

    # use list to populate LinkTable and PortTable
    for entry in list:
        temp = entry.split(' ')
        node.Set_link_table(int(temp[0]), (int(temp[3]), int(temp[4]), int(temp[5]), int(temp[6])))
        node.Set_address_data_table(int(temp[0]), temp[1], int(temp[2]))

        # set parameters for for this node
        if node.GetNID() == int(temp[0]):
            node.SetHostName(temp[1])
            node.SetPort(int(temp[2]))

            # set starting point
            number_of_nodes = len(temp) - 3
            index = 3

            # iterate through and add all links for this node
            for i in range(number_of_nodes):
                corresponding_hostname = hostnames[int(temp[index+i])-1]
                corresponding_port = ports[int(temp[index+i])-1]
                node.AddLink((int(temp[index+i]), corresponding_hostname, corresponding_port))

    # close itc.txt file
    infile.close()

    # return object
    return node

# class: Node
class Node(object):

    # initialize node
    def __init__ (self, nid=0, host_name=None, udp_port=0, links=[], address_data_table = [], link_table={}):
        self.nid = nid
        self.host_name = host_name
        self.udp_port = udp_port
        self.routing_table = {}
        self.removed_nodes = []

        if links is not None:
            self.links = list(links)

        self.upL1 = False
        self.upL2 = False
        self.upL3 = False
        self.upL4 = False
        self.link_table = {}
        self.address_data_table = {}

    # get nid
    def GetNID (self):
        return self.nid

    # get hostname
    def GetHostName (self):
        return self.host_name

    # get port number
    def GetPort (self):
        return self.udp_port

    # get list of links
    def GetLinks (self):
        return self.links

    # get link table (all links)
    def Get_link_table (self):
        return self.link_table

    # get port table (all ports)
    def Get_address_data_table (self):
        return self.address_data_table

    def Get_routing_table (self):
        return self.routing_table

    # get up flag for neighbor 1
    def GetUpFlagL1 (self):
        return self.upL1

    # get up flag for neighbor 2
    def GetUpFlagL2 (self):
        return self.upL2

    # get up flag for neighbor 1
    def GetUpFlagL3 (self):
        return self.upL3

    # get up flag for neighbor 2
    def GetUpFlagL4 (self):
        return self.upL4

    # set up flag for neighbor 1
    def SetUpFlagL1 (self, flag):
        self.upL1 = flag

    # set up flag for neighbor 2
    def SetUpFlagL2 (self, flag):
        self.upL2 = flag

    # set up flag for neighbor 1
    def SetUpFlagL3 (self, flag):
        self.upL3 = flag

    # set up flag for neighbor 2
    def SetUpFlagL4 (self, flag):
        self.upL4 = flag

    # set nid
    def SetNID (self, nid):
        self.nid = nid

    # set hostname
    def SetHostName (self, host_name):
        self.host_name = host_name

    # set port number
    def SetPort (self, udp_port):
        self.udp_port = udp_port

    # add link to links list
    def AddLink (self, individual_link):
        self.links.append(individual_link)

    # set link table
    def Set_link_table (self, source_nid, neighbor_nid):
        self.link_table[source_nid] = neighbor_nid
        #pass

    # set port table
    def Set_address_data_table (self, nid, hostname, port):
        self.address_data_table[nid] = nid, hostname, port

    def Set_routing_table (self, nid, cost, next):
        self.routing_table[nid] = nid, cost, next

# class TCP Handler (this receives all TCP messages)
class MyTCPHandler(socketserver.BaseRequestHandler):

    def handle(self):

        # global variables
        global NID, hostname, tcp_port
        global l1_hostname, l2_hostname, l3_hostname, l4_hostname
        global l1_tcp_port,l2_tcp_port, l3_tcp_port, l4_tcp_port
        global l1_NID, l2_NID, l3_NID, l4_NID
        global add_counter, update_counter, remove_counter

        self.data = self.request.recv(1024)
        message = self.data
        message = ''.join(message.decode().split())
        print(message)
        os.system("""bash -c 'read -s -n 1 -p "Press any key to continue..."'""")

# Class: MyUDPHandler (this receives all UDP messages)
class MyUDPHandler(socketserver.BaseRequestHandler):

    def compareEntries(self, new_routing, sender):
        my_routing = node.Get_routing_table()
        for i in range(0, len(new_routing)):
            nodeE = new_routing[i][0]
            # IF the entry is already in the routing table
            if (int(nodeE) in my_routing):
                if (int(nodeE) == NID):
                    continue
                # If a cheaper path is found
                elif (int(new_routing[i][1])+1 < int(my_routing[int(nodeE)][1])):
                    print("FOUND BETTER PATH TO NODE : "+nodeE+"\nThrough : "+str(sender))
                    node.Set_routing_table(int(nodeE),int(new_routing[i][1])+1,sender)
                else:
                    continue
            # Else add entry to the routing table
            elif not int(nodeE) in node.removed_nodes:
                node.Set_routing_table(int(nodeE),int(new_routing[i][1])+1,sender)
                setUpFlag(int(nodeE))
                print("New Routing Entry Added\nNode : "+nodeE+"\nThrough : "+str(sender))
            #elif (my_routing[i][received[]):


    #Pull information from the distance vector
    def handleDV(self, message):
        received = []
        dead_list = []

        sender = int(message[1])
        for i in range(2, len(message)-1):
            received.append(message[i].strip('()').split(","))
        temp = node.Get_routing_table()
        self.compareEntries(received, sender)


    # interrupt handler for incoming messages
    def handle(self):

        # parse received data
        data = self.request[0].strip()

        # set message and split
        message = data
        message = ''.join(message.decode().split())
        check = message.split(":")
        if (check[0] == "route"):
            print("ROUTE:"+str(check))
            self.handleDV(check)

        # Ping request
        elif (check[0] == "p" and check[1] == "0"):
            print("PING RECIEVED SENDING RESPONSE")
            ping_message = "p:1:"+str(NID)
            send_udp(int(check[2]), ping_message, False, True)
        # Ping echo-reply
        elif (check[0] == "p" and check[1] == "1"):
            print ("Node: "+check[2]+" is up")
            setUpFlag(int(check[2]))
        elif (int(check[0]) == NID):
            print(check[1])
            os.system("""bash -c 'read -s -n 1 -p "Press any key to continue..."'""")
        else:
            send_udp(check[0], message, False, False)

#Setting the Flags when we find that a connected node is up
def setUpFlag(NID):
    if(NID == l1_NID):
        node.SetUpFlagL1(True)
    if(NID == l2_NID):
        node.SetUpFlagL2(True)
    if(NID == l3_NID):
        node.SetUpFlagL3(True)
    if(NID == l4_NID):
        node.SetUpFlagL4(True)

#Setting flags to false when a node is turned off.
def setDownFlag(NID):
    if(NID == l1_NID):
        node.SetUpFlagL1(False)
    if(NID == l2_NID):
        node.SetUpFlagL2(False)
    if(NID == l3_NID):
        node.SetUpFlagL3(False)
    if(NID == l4_NID):
        node.SetUpFlagL4(False)

# Function: sendto()
def send_tcp(dest_nid, message):

    # global variables
    global NID, hostname, tcp_port
    global l1_hostname, l2_hostname, l3_hostname, l4_hostname
    global l1_tcp_port,l2_tcp_port, l3_tcp_port, l4_tcp_port
    global l1_NID, l2_NID, l3_NID, l4_NID

    # look up address information for the destination node
    if dest_nid == str(l1_NID):
        HOST = l1_hostname
        PORT = l1_tcp_port

    elif dest_nid == str(l2_NID):
        HOST = l2_hostname
        PORT = l2_tcp_port

    elif dest_nid == str(l3_NID):
        HOST = l3_hostname
        PORT = l3_tcp_port

    elif dest_nid == str(l4_NID):
        HOST = l4_hostname
        PORT = l4_tcp_port

    else:
        print('no address information for destination')

    # encode message as byte stream
    message = message.encode()

    # send message
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        sock.sendall(message)
        sock.close()

    except:
        print('error, message not sent')
        pass

#A function to check if a node is up and if it does not reply, it is taken out of each node's routing table.
def ping_timeout(NID):
    print("Checking "+str(NID))
    for i in range(15):
        if (NID == l1_NID and node.GetUpFlagL1()):
            return
        elif (NID == l2_NID and node.GetUpFlagL2()):
            return
        elif (NID == l3_NID and node.GetUpFlagL3()):
            return
        elif (NID == l4_NID and node.GetUpFlagL4()):
            return
        time.sleep(.50)

    if (NID in node.routing_table):
        del node.routing_table[NID]

    print("\nNode "+str(NID)+" is down")
    setDownFlag(NID)



# function: hello (alive)
def send_udp(dest_nid, message, dv_flag, ping_flag):

    # global variables
    global NID, hostname, tcp_port
    global l1_hostname, l2_hostname, l3_hostname, l4_hostname
    global l1_tcp_port,l2_tcp_port, l3_tcp_port, l4_tcp_port
    global l1_NID, l2_NID, l3_NID, l4_NID
    local_routing_table = node.Get_routing_table()

    # DV Propagation
    if (dv_flag or ping_flag):
        if str(dest_nid) == str(l1_NID):
            HOST = l1_hostname
            PORT = l1_udp_port

        elif str(dest_nid) == str(l2_NID):
            HOST = l2_hostname
            PORT = l2_udp_port

        elif str(dest_nid) == str(l3_NID):
            HOST = l3_hostname
            PORT = l3_udp_port

        elif str(dest_nid) == str(l4_NID):
            HOST = l4_hostname
            PORT = l4_udp_port


    # Forwarding Messages
    elif int(dest_nid) in local_routing_table:
        next = str(local_routing_table[int(dest_nid)][2])
        print ("Sent to : "+next)

        if next == str(l1_NID):
            HOST = l1_hostname
            PORT = l1_udp_port

        elif next == str(l2_NID):
            HOST = l2_hostname
            PORT = l2_udp_port

        elif next == str(l3_NID):
            HOST = l3_hostname
            PORT = l3_udp_port

        elif next == str(l4_NID):
            HOST = l4_hostname
            PORT = l4_udp_port

    else:
        print('no address information for destination')

    # encode message as byte stream
    message = message.encode()

    try:
        # open socket and send to neighbor 4
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sock.sendto(message, (HOST, PORT))
    except:
        print('error, message not sent')
        pass

# A function to ping nodes in order to update routing tables. Uses threads to scan if nodes are down in the backgroud.
def pingNode():
    pingMessage = "p:0:"+str(NID)
    if (l1_NID != 0):
        setDownFlag(l1_NID)
        send_udp(str(l1_NID), pingMessage, False, True)
        t1 = threading.Thread(target=ping_timeout,args=(l1_NID,))
        t1.start()
    if (l2_NID != 0):
        setDownFlag(l2_NID)
        send_udp(str(l2_NID), pingMessage, False, True)
        t2 = threading.Thread(target=ping_timeout,args=(l2_NID,))
        t2.start()
    if (l3_NID != 0):
        setDownFlag(l3_NID)
        send_udp(str(l3_NID), pingMessage, False, True)
        t3 = threading.Thread(target=ping_timeout,args=(l3_NID,))
        t3.start()
    if (l4_NID != 0):
        setDownFlag(l4_NID)
        send_udp(str(l4_NID), pingMessage, False, True)
        t4 = threading.Thread(target=ping_timeout,args=(l4_NID,))
        t4.start()


# function: start listener
def start_listener():

    # global variables
    global node, NID, hostname, udp_port, tcp_port
    global l1_hostname, l2_hostname, l3_hostname, l4_hostname
    global l1_udp_port, l2_udp_port, l3_udp_port, l4_udp_port
    global l1_tcp_port, l2_tcp_port, l3_tcp_port, l4_tcp_port
    global l1_NID, l2_NID, l3_NID, l4_NID

    # check links for node attributes
    links = node.GetLinks()
    link1 = links[0]
    link2 = links[1]
    link3 = links[2]
    link4 = links[3]

    # set link attributes
    l1_NID = link1[0]
    l1_hostname = link1[1]
    l1_udp_port = link1[2]
    l1_tcp_port = l1_udp_port + 500

    l2_NID = link2[0]
    l2_hostname = link2[1]
    l2_udp_port = link2[2]
    l2_tcp_port = l2_udp_port + 500

    l3_NID = link3[0]
    l3_hostname = link3[1]
    l3_udp_port = link3[2]
    l3_tcp_port = l3_udp_port + 500

    l4_NID = link4[0]
    l4_hostname = link4[1]
    l4_udp_port = link4[2]
    l4_tcp_port = l4_udp_port + 500

    hostname = node.GetHostName()
    NID = node.GetNID()
    udp_port = node.GetPort()
    tcp_port = udp_port + 500

    # slight pause to let things catch up
    time.sleep(2)

    # start thread for listener
    t1 = threading.Thread(target=TCP_listener)
    t1.daemon=True
    t1.start()

    # start thread for listener
    t2 = threading.Thread(target=UDP_listener)
    t2.daemon=True
    t2.start()

# function: TCP listener
def TCP_listener():

    # global variables
    global hostname, tcp_port

    # set socket for listener
    server = socketserver.TCPServer((hostname, tcp_port), MyTCPHandler)
    server.serve_forever()

# function: receiver (listener)
def UDP_listener():

     # global variables
    global hostname, udp_port

    # set socket for listener
    server = socketserver.UDPServer((hostname, udp_port), MyUDPHandler)
    server.serve_forever()

# print status
def PrintInfo():

    # global variables
    global node, NID, hostname, udp_port, tcp_port
    temp = node.Get_routing_table()

    # output data
    os.system('clear')
    print("NID: " + str(NID))
    print("\n\tLink Table:\n\tNODE\tL1\tL2\tL3\tL4")
    for key, value in node.Get_link_table().items():
        print("\t"+str(key)+"\t"+str(value[0])+"\t"+str(value[1])+"\t"+str(value[2])+"\t"+str(value[3]))
    print("\n\tAddress Data Table:\n\tDEST\tADDR\t\tPORT")
    for key, value in node.Get_address_data_table().items():
        print("\t"+str(value[0])+"\t"+str(value[1])+"\t"+str(value[2]))
    print("\n\tRouting Table:\n\tDEST\tCOST\tNEXT")
    for key, value in temp.items():
        print("\t"+str(value[0])+"\t"+str(value[1])+"\t"+str(value[2]))
    os.system("""bash -c 'read -s -n 1 -p "Press any key to continue..."'""")



# update the route
def sendDV():
    message = "route:"+str(NID)
    temp = node.Get_routing_table()


    for key, value in temp.items():
        message += (":"+str(value))
    message+= ":"+str(node.removed_nodes)

    print (message)

    if (l1_NID != 0 ):
        send_udp(str(l1_NID), message, True, False)
    if (l2_NID != 0 ):
        send_udp(str(l2_NID), message, True, False)
    if (l3_NID != 0 ):
        send_udp(str(l3_NID), message, True, False)
    if (l4_NID != 0 ):
        send_udp(str(l4_NID), message, True, False)


def init_routing_table():
    node.Set_routing_table(NID,0,NID)

# Starts the background tasks
def background_tasks():
    i = 0
    while(True):
        if i < 5:
            i = 0
            node.removed_nodes = []
        i += 1
        time.sleep(20)
        #if (len(node.Get_routing_table()) == 1):
        #    continue
        pingNode()
        time.sleep(2)
        sendDV()
        print("Background Running")

# main function
def main(argv):

    # global variables
    global node

    # set initial value for loop
    run = 1

    # check for command line arguments
    if len(sys.argv) != 3:
        print("Usage: <program_file><nid><itc.txt>")
        exit(1)

    # initialize node object
    node = InitializeTopology(sys.argv[1], sys.argv[2])

    # start UDP listener
    start_listener()
    t1 = threading.Thread(target=background_tasks)
    t1.start()

    # initialize routing table
    init_routing_table()

    # loop
    while(run):

        #print menu options
        os.system('clear')
        print("Enter 'info' to check network information")
        print("Enter 'send_tcp' to message another node via TCP")
        print("Enter 'send_udp' to message another node via UDP")
        print("Enter 'q' to end program")

        # set selection value from user
        selection = input("Enter Selection: ")

        # selection: status
        if selection == 'info':
            PrintInfo()

        # selection: send_tcp
        elif(selection == 'send_tcp'):
            os.system('clear')
            dest_nid = input("enter node to message: ")
            message = input("enter the message you want to send: ")
            send_tcp(dest_nid, message)
            os.system("""bash -c 'read -s -n 1 -p "Press any key to continue..."'""")

        # selection: send_udp
        elif(selection == 'send_udp'):
            os.system('clear')
            dest_nid = input("enter node to message: ")
            message = input("enter the message you want to send: ")
            message = dest_nid+":"+message
            send_udp(dest_nid, message, False, False)
            os.system("""bash -c 'read -s -n 1 -p "Press any key to continue..."'""")

        # selection: quit
        elif(selection == 'q'):
            run = 0
            os.system('clear')

        else:

            # default for bad input
            os.system('clear')
            time.sleep(.5)
            continue

# initiate program
if __name__ == "__main__":
    main(sys.argv)
