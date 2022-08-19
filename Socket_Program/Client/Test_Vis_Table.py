import socket
import Client_Vis as Geant4
SERVER = "127.0.1.1"
PORT = 5050
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)






input()

Geant4.NewGeometry([0,0,0,0,0],[1,1,1,1,4],client)

#input()
Geant4.Change_Particle_Gun("geantino",10,0,client)
input()

Geant4.NewGeometry([0,0,0,0,0],[-1,0,-1,-1,-4],client)

input()
Geant4.Change_Particle_Gun("e-",1,0,client)
input()

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
Geant4.Stop(client)