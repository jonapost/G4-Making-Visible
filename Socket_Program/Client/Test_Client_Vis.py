import socket
import os

BUFFER_SIZE = 4096

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
Send_New_Data = "!NEWDATA"
CHange_Geometry = "!ChangeGeo"

SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT))

def Ask_for_data(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)

    client.send(message)
    #filename = client.recv(BUFFER_SIZE).decode()
    # remove absolute path if there is
    #filename = os.path.basename(filename)

    filename = "Recev_Data.heprep"

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

def NewGeometry(Dy,NL):
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
    Ask_for_data(Send_New_Data)


print("Befor first send")
send("Hello World!")
input()
#print("After input")
send("Hello World!")
print("After first input")

#Ask_for_data(Send_New_Data)

input()
NewGeometry([0,1,0,0,0],[0,0,0,0,0])

input()
NewGeometry([0,2,0,0,0],[0,0,0,0,0])

input()
NewGeometry([0,3,0,0,0],[0,0,0,0,0])

input()
NewGeometry([0,4,0,0,0],[0,0,0,1,0])
input()

import time
st = time.time()
for i in range(1):
    NewGeometry([0,-10 + i,0,i*0.5,0],[0,0,0,0,0])
elapsed_time = time.time() - st
print('Execution time:', elapsed_time/1, 'seconds')

send(DISCONNECT_MESSAGE)