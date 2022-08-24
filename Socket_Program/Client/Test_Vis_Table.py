#This code was written by Clemens Dittmar. 
#If you have any questions or problems, please contact Clemens.Dittmar@rwth-aachen.de.
# This is a test script to show how client, server and Control_Vis work together.  


# Connect to server
import socket
SERVER = "127.0.1.1" # Server IP
PORT = 5050 # Server Port
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# import communication file for Geant4 commands
import Client_Vis as Geant4



input()

# initialize geometry
Geant4.NewGeometry([0,0,0,0,0],[1,1,1,1,4],client)

input()
Geant4.ReRun(client)

input()
# change particle
Geant4.Change_Particle_Gun("geantino",100,0,client)
input()
# change geometry
Geant4.NewGeometry([0,0,0,0,0],[-1,0,-1,-1,-4],client)

input()
# change particle
Geant4.Change_Particle_Gun("e-",10,0,client)
input()

# change geometry
Geant4.NewGeometry([0,0,0,0,0],[-1,0,-1,-1,-4],client)
input()

N = 10
for i in range(N):
    Geant4.NewGeometry([0,1,0,0,0],[0,0,0,0,0],client)

for i in range(N):
    Geant4.NewGeometry([0,-1,0,0,0],[0,0,0,0,0],client)



input()

Geant4.NewGeometry([0,0,0,0,0],[1,1,1,0,0],client)

input()

N = 5
for i in range(N):
    Geant4.NewGeometry([1,2,0,0,0],[0,0,0,0,0],client)

input()

# make dep. energy
Geant4.MakeStatistic([0,0,0,0,0],[0,0,0,0,0],client)
input()

Geant4.NewGeometry([0,-10,0,0,0],[0,0,0,0,6],client)
input()
Geant4.Change_Particle_Gun("gamma",1,0,client)
input()
Geant4.NewGeometry([0,0,0,0,0],[0,0,0,0,2],client)

input()
Geant4.NewGeometry([0,0,0,0,0],[0,0,0,0,2],client)

input()
N = 6
for i in range(N):
    Geant4.NewGeometry([0,0,0,0,2],[0,0,0,0,0],client)

for i in range(N):
    Geant4.NewGeometry([0,0,0,0,-2],[0,0,0,0,0],client)
input()

Geant4.MakeStatistic([0,0,0,0,0],[0,0,0,0,0],client)
input()

'''
N = 20
import time
st = time.time()
for i in range(N):
    Geant4.NewGeometry([0,-10 + i,0,i*0.5,0],[0,0,0,0,0],client)
elapsed_time = time.time() - st
print('Execution time:', elapsed_time/N, 'seconds')
'''

# stop Geant4
Geant4.Stop(client)