
#This code was written by Clemens Dittmar. 
#If you have any questions or problems, please contact Clemens.Dittmar@rwth-aachen.de.

#These functions are intended for simplified socket communication with a Geant4 programme called CalSG.


import os

BUFFER_SIZE = 4096*10

HEADER = 64
FORMAT = 'utf-8'

#Predefined activation texts for simplified server communication.

DISCONNECT_MESSAGE = "!DISCONNECT"  # Disconnect Client from server
Send_New_Data = "!NEWDATA"          # Ask serverr for new data
CHange_Geometry = "!ChangeGeo"      # Activates the server function for changing the geometry.
CHANGE_GUN = "!CHANGEGUN"           # Activates the server function for changing the primary particle parmeter.
Make_Statitic = "!STATISTIC"        # Ask server to generate 1000 energy deposition values for each block
Send_New_Statistic = "!NEWSTAT"     # Ask server to send 1000 energy deposition values for each block 

FileName_HepRep = "Recev_Data.heprep"  # Name of the heprep file 
FileName_Statistic = "Recev_Statistic.csv" # Name of the energy deposition data


#////////////////////////  Functions //////////////////////////////
# 
#Sends the length of the message first and then the message past. If this is part of the predefined messages, the specific functions are started.
def send(msg,client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

#////////////////////////////////////////////////////////////////
# Stop Geant4 and disconnect from server.
def Stop(client):
    send(DISCONNECT_MESSAGE,client)

#////////////////////////////////////////////////////////////////
# Rerun Geant4 simulation and receives new data from the server
def ReRun(client):
    print("Start reruning simulation.")
    NewGeometry([0,0,0,0,0],[0,0,0,0,0],client)
    Ask_for_data(Send_New_Data,FileName_HepRep,client)

#////////////////////////////////////////////////////////////////
# Asks for new data. If Send_New_Data is passed, the existing heprep file is Transmitted to the client. 
# #If Send_New_Statistic is passed, the existing csv file with energy deposition data is transmitted to the client. 
def Ask_for_data(msg,FileName,client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)   #send message length

    client.send(message)  # send message
    #filename = client.recv(BUFFER_SIZE).decode()
    # remove absolute path if there is
    #filename = os.path.basename(filename)

    filename = FileName

    with open(filename, "wb") as file:  
        Data_Comming = True
        while Data_Comming:      
            # read 1024 bytes from the socket (receive)
            bytes_read = client.recv(BUFFER_SIZE)
            #if not bytes_read:   
            if bytes_read[-4:].decode(FORMAT) == "Stop":
                # nothing is received
                # file transmitting is done
                print("no bytes")
                Data_Comming = False
               # break
            # write to the file the bytes we just received
            file.write(bytes_read[:-4])
         
    file.close()
    print("\n File has been copied successfully \n")
  
    client.send(message)

    print(client.recv(2048).decode(FORMAT))

#////////////////////////////////////////////////////////////////
# Chnage the geometry and starts simulation.
# Input is a list of Y-Axis changes and a list of replica number changes
# If this list are full of 0, no geometry change but resimulation
# After simulation heprep file is transmitted to thr client

def NewGeometry(Dy,NL,client):
    Text = str(Dy[0]) + ";" + str(NL[0]) + "|" + str(Dy[1]) + ";" + str(NL[1]) + "|" + str(Dy[2]) + ";" + str(NL[2]) + "|" + str(Dy[3]) + ";" + str(NL[3]) + "|" + str(Dy[4]) + ";" + str(NL[4])
    message = CHange_Geometry.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    client.send(Text.encode(FORMAT))
    Check = client.recv(2048).decode(FORMAT)
    if Check == "Valid":
        print("Geometry is permitted. Simulation running.")
    else:
        print("Geometry is not allowed. Simulation uses old parameters.")
    msg = client.recv(2048).decode(FORMAT)
    if msg == "Done":
        print("Simulation done.")
    Ask_for_data(Send_New_Data,FileName_HepRep,client)

#////////////////////////////////////////////////////////////////
# Changes primary particle parameters
# Input is the particle name, ist energy in MeV, start Y position
def Change_Particle_Gun(Particle,Energy,YP,client):
    Text = Particle + ";" + str(Energy) + ";" + str(YP) # + "|"

    message = CHANGE_GUN.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    client.send(Text.encode(FORMAT))
    Check = client.recv(2048).decode(FORMAT)
    print(Check)
    if Check == "Valid" or Check =="ValidMsg received":
        print("Particle gun parameters are permitted.")
    else:
        print("Particle gun parameters are not allowed. Energy to high, wrong Particle name or out of world range.")
   # msg = client.recv(2048).decode(FORMAT)


#////////////////////////////////////////////////////////////////
# Change geometry and simulate 1000 events and saves deposit energy in an csv file
# For one event the trajectories are stored in an heprep file
# Both files are transmitted to the client
# Input is a list of Y-Axis changes and a list of replica number changes
# If this list are full of 0, no geometry change but resimulation
def MakeStatistic(Dy,NL,client):
    Text = str(Dy[0]) + ";" + str(NL[0]) + "|" + str(Dy[1]) + ";" + str(NL[1]) + "|" + str(Dy[2]) + ";" + str(NL[2]) + "|" + str(Dy[3]) + ";" + str(NL[3]) + "|" + str(Dy[4]) + ";" + str(NL[4])
    message = Make_Statitic.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)

    client.send(Text.encode(FORMAT))
    Check = client.recv(2048).decode(FORMAT)
    if Check == "Valid":
        print("Geometry is permitted. Simulation running.")
    else:
        print("Geometry is not allowed. Simulation uses old parametres.")
    msg = client.recv(2048).decode(FORMAT)
    if msg == "Done":
        print("Simulation done.")
    Ask_for_data(Send_New_Data,FileName_HepRep,client)
    Ask_for_data(Send_New_Statistic,FileName_Statistic,client)



