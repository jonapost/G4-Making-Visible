#This code was written by Clemens Dittmar. 
#If you have any questions or problems, please contact Clemens.Dittmar@rwth-aachen.de

#Server for socket communication with client

from multiprocessing import connection
import socket 
import threading
import os, sys
import pexpect as px 
import time

#import Geant4 control
import Control_G4_Py as ConG4

# if no print out 
def blockPrint():
    sys.stdout = open(os.devnull, 'w')
#blockPrint()


##############################################
#Data path and name
##############################################
Path = os.path.abspath(os.getcwd())
FileName_HepRep = Path + "/../Test/" + "TrajectoryData.heprep"
FileName_Statistic = "stuff.csv"


#/////////////////////////// Server parameter/////////////////////////////////////////
BUFFER_SIZE = 4096*10 # send 4096*10 bytes each time step
TestLength = 4096
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
Send_New_Data = "!NEWDATA"
CHange_Geometry = "!ChangeGeo"
CHANGE_GUN = "!CHANGEGUN"
Make_Statitic = "!STATISTIC"
Send_New_Statistic = "!NEWSTAT"


#/////////////////////////// Build up server //////////////////////////////////////////
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)


#////////////////////////////////////// Socket Server Funktions////////////////////////
# Processes all new commands from the client
def handle_client(conn, addr,child):
    st = time.time()
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        print("Wait")
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f"[{addr}] {msg}")

            if msg == DISCONNECT_MESSAGE:
                connected = False

            if msg == Send_New_Data:
                Send_File(conn,msg)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"[{addr}] {msg}")

            if msg == Send_New_Statistic:
                Send_File(conn,msg)
                msg = conn.recv(msg_length).decode(FORMAT)
                print(f"[{addr}] {msg}")   

            if msg == CHange_Geometry:

                msg = conn.recv(TestLength).decode(FORMAT)
                msg , Check = ConG4.Geometry_Check(msg)
                if Check:
                    conn.send("Valid".encode(FORMAT))
                    ConG4.handle_Geant4Commands(msg,child,False)
                    conn.send("Done".encode(FORMAT))
                else:
                    conn.send("Invalid".encode(FORMAT)) 
                    ConG4.handle_Geant4Commands(msg,child,False)
                    conn.send("Done".encode(FORMAT))

            if msg == Make_Statitic:

                msg = conn.recv(TestLength).decode(FORMAT)
                msg , Check = ConG4.Geometry_Check(msg)
                if Check:
                    conn.send("Valid".encode(FORMAT))
                    ConG4.handle_Geant4Commands(msg,child,True)
                    conn.send("Done".encode(FORMAT))
                else:
                    conn.send("Invalid".encode(FORMAT)) 
                    ConG4.handle_Geant4Commands(msg,child,True)
                    conn.send("Done".encode(FORMAT))
            
            if msg == CHANGE_GUN:
                msg = conn.recv(TestLength).decode(FORMAT)
                Check = ConG4.Beam_Gun(msg,child)
                if Check:
                    conn.send("Valid".encode(FORMAT))
                    print("Checht True")
                else:
                    conn.send("Invalid".encode(FORMAT)) 
                    print("Check False")

                #conn.send("Done".encode(FORMAT))
                        
            conn.send("Msg received".encode(FORMAT))
    conn.close()
    ConG4.Stop_G4(child)

    elapsed_time = time.time() - st
    print('Execution time:', elapsed_time, 'seconds')


#//////////////////////////////////////////////////////
#Starts server and waits for client connections

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
  
    while True:
        conn, addr = server.accept()
        print("Start of Geant4")

        child = ConG4.Start_G4()

        thread = threading.Thread(target=handle_client, args=(conn, addr, child))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        print("Working")
     
        
#/////////////////////////////////////////////////////
#Sends data files to client if called
#at the end of transmission a "Stop" is send. This is a bit tinkered and should be improved.
def Send_File(conn,msg):
    if msg == Send_New_Data:
        filename = FileName_HepRep
    else:
        filename = FileName_Statistic

    with open(filename, "rb") as file:
        print("Sending")
        while True:
            # read the bytes from the file
            bytes_read = file.read(BUFFER_SIZE)
            if not bytes_read:
                # file transmitting is done
                print("no bytes")
                conn.send("  Stop".encode(FORMAT))
                break
            # we use sendall to assure transimission in 
            # busy networks
            conn.sendall(bytes_read)  
        
    file.close()


print("[STARTING] server is starting...")
start()







