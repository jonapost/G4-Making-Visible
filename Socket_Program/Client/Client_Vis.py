import os

BUFFER_SIZE = 4096*10

HEADER = 64
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
Send_New_Data = "!NEWDATA"
CHange_Geometry = "!ChangeGeo"
CHANGE_GUN = "!CHANGEGUN"
Make_Statitic = "!STATISTIC"
Send_New_Statistic = "!NEWSTAT"

FileName_HepRep = "Recev_Data.heprep"
FileName_Statistic = "Recev_Statistic.csv"



def send(msg,client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def Stop(client):
    send(DISCONNECT_MESSAGE,client)


def Ask_for_data(msg,FileName,client):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)

    client.send(message)
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
        print("Geometry is not allowed. Simulation with adjusted data or no simulation.")
    msg = client.recv(2048).decode(FORMAT)
    if msg == "Done":
        print("Simulation done.")
    Ask_for_data(Send_New_Data,FileName_HepRep,client)



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
    if Check == "Valid":
        print("Particle gun parameters are permitted.")
    else:
        print("Particle gun parameters are not allowed. Energy to high, wrong Particle name or out of world range.")
   # msg = client.recv(2048).decode(FORMAT)




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
        print("Geometry is not allowed. Simulation with adjusted data or no simulation.")
    msg = client.recv(2048).decode(FORMAT)
    if msg == "Done":
        print("Simulation done.")
    Ask_for_data(Send_New_Data,FileName_HepRep,client)
    Ask_for_data(Send_New_Statistic,FileName_Statistic,client)



