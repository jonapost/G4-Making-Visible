from multiprocessing import connection
import socket 
import threading
import os
import pexpect as px 
import time

##############################################
#Define Parameters
##############################################
BlockPosition = [[-20,-10,0,10,20],[0,0,0,0,0],[0,0,0,0,0]]
BlockSize = [[2,2,2,2,2],[10,10,10,10,10],[10,10,10,10,10]]
Material = ["Aluminium","Lead","Uranium","Scintillator","Scintillator"]
Number_of_Layer = [1,1,1,1,1]


MaxBlockPosition = [ 20, -20 ] # Check what is written in Geant4

FileName_HepRep = '/home/kappe/projects/CERN_SS/Geant_Project/TestEm3_1Block_moveble/build' + "/" + "TestG4Data0.heprep"
FileName_Statistic = "stuff.csv"


#/////////////////////////// Server parameter/////////////////////////////////////////
BUFFER_SIZE = 4096*10 # send 4096 bytes each time step
TestLength = 4096
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
Send_New_Data = "!NEWDATA"
CHange_Geometry = "!ChangeGeo"
Make_Statitic = "!STATISTIC"
Send_New_Statistic = "!NEWSTAT"


#/////////////////////////// Build up server //////////////////////////////////////////
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)


#////////////////////////////////////// Socket Server Funktions////////////////////////
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
                msg , Check = Geometry_Check(msg)
                if Check:
                    conn.send("Valid".encode(FORMAT))
                    handle_Geant4Commands(msg,child,False)
                    conn.send("Done".encode(FORMAT))
                else:
                    conn.send("Invalid".encode(FORMAT)) # What should be done if geometry is invalid? Change to nearest valid geometry and start run?
                    handle_Geant4Commands(msg,child,False)
                    conn.send("Done".encode(FORMAT))

            if msg == Make_Statitic:

                msg = conn.recv(TestLength).decode(FORMAT)
                msg , Check = Geometry_Check(msg)
                if Check:
                    conn.send("Valid".encode(FORMAT))
                    handle_Geant4Commands(msg,child,True)
                    conn.send("Done".encode(FORMAT))
                else:
                    conn.send("Invalid".encode(FORMAT)) # What should be done if geometry is invalid? Change to nearest valid geometry and start run?
                    handle_Geant4Commands(msg,child,True)
                    conn.send("Done".encode(FORMAT))





                
                        
            conn.send("Msg received".encode(FORMAT))
    conn.close()
    child.sendline("exit")

    elapsed_time = time.time() - st
    print('Execution time:', elapsed_time, 'seconds')


def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
  
    while True:
        conn, addr = server.accept()
        print("Start of Geant4")

        print("Spawning CalSG")
        child = px.spawn('./CalSG')
        print("return from spawn")
        child.expect('PreInit> ')
        print("expect return")
        child.sendline('/control/execute Run_Beam_v1.mac')
        print("sent")
        child.expect('Idle>')
        print("got Idle>")
        print("Geant4 is in Idle mode. Commands can be sent.")

        thread = threading.Thread(target=handle_client, args=(conn, addr, child))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
        print("Working")
     
        
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

def Beam_Gun(textline,child):
    AllVal = textline.split(";") # Split at ";" to get info for each Gun if more than one gun is needed
    Particle = []
    Energy = []
    YPosy = []
    for i in range(len(AllVal)):
        value = AllVal[i].split("|") # Split at "|" to get command Inf: Particle | Energy (in MeV) | YPosition
        Particle.append(value[0])
        Energy.append(value[1])
        YPosy.append(value[2])

    print(value)
    for i in range(len(AllVal)):
        if Particle[i]=="e-":
            child.send("/gun/particle " + Particle[i])
            print("sent" ,"/gun/particle " + Particle[i] )
        if Particle[i]=="p+":
            child.send("/gun/particle " + Particle[i])
            print("sent" ,"/gun/particle " + Particle[i] )
        else:
            print("Particle: ", Particle[i], " is unknown, e- was used.")
            child.send("/gun/particle e-" )
        child.expect('Idle>')
        print("got Idel>") 
        
        if float(Energy[i]) < 0 or float(Energy[i])> 10**6:
            Energy[i] = "10" # Default energy value if sended energy is <0 or to hige
        child.send("/gun/energy " + Energy[i] + " MeV")
        child.expect('Idle>')
        print("got Idel>") 
        
        print("Sending new position")
        child.send("/gun/position 0 " + YPosy[i] + " 0")
        child.expect('Idle>')
        print("got Idel>") 









#/////////////////////////////  Geant4 Commands /////////////////////////

def Cpp_Execution(Block,Y,NOL,child):
    BlockPosition[1][Block] += Y
    Number_of_Layer[Block] += NOL
    Text = "/testem/det/setBlock " + str(Block) + " " + str(BlockPosition[0][Block]) + " cm "+ str(BlockPosition[1][Block]) + " cm "+ str(BlockPosition[2][Block]) + " cm " + str(BlockSize[0][Block]) + " cm "+ str(BlockSize[1][Block]) + " cm "+ str(BlockSize[2][Block]) + " cm "+ Material[Block] + " " + str(Number_of_Layer[Block])
    child.sendline(Text)
    print("sent" , Text)
    child.expect('Idle>')
    print("got Idel> got idel sent") 

    


def handle_Geant4Commands(textline,child,NRun):
    value = textline.split("|") # Split at ";" to get command for each block
    print(value)
    for i in range(len(value)):
        vi = value[i].split(";")
        dy = float(vi[0])
        NL = int(vi[1])
        Cpp_Execution(i,dy,NL,child)

    child.sendline("/run/reinitializeGeometry")
    print("sent reinitialize Geometrie")
    child.expect('Idle>')
    print("got Idel> got idel sent")
    if NRun:
        print("Run one event for visualisation data.")
        child.sendline('/control/execute Beam_ON_File.mac')
        print("sent")
        child.expect('Idle>')
        child.sendline("/vis/disable")
        print("Disabled visualisation")
        child.expect('Idle>')
        print("Start N events for statistic.")
        child.sendline('/control/execute Beam_ON_File_100.mac')
        print("sent")
        child.expect('Idle>')
        child.sendline("/vis/enable")
        print("Enable visualisation")
    else:
        child.sendline('/control/execute Beam_ON_File.mac')
        print("sent")
    child.expect('Idle>')
    print("got Idel>")

def Geometry_Check(textline):
    value = textline.split("|") # Split at ";" to get command for each block
    print("Checking New geometry changes from client:",value)
    CheckC = True
    for i in range(len(value)):
        vi = value[i].split(";")
        dy = float(vi[0])
        NL = int(vi[1])
        if BlockPosition[1][i] + BlockSize[1][i]/2 + dy > MaxBlockPosition[0] or BlockPosition[1][i] - BlockSize[1][i]/2 + dy < MaxBlockPosition[1]:
            CheckC = False
           
            value[i] = "0;" + str(NL)
           # break No break, change to 0 change
    returnText = ""
    for i in range(len(value)):
        returnText += value[i] + "|"

    return returnText[:-1], CheckC





print("[STARTING] server is starting...")
start()







