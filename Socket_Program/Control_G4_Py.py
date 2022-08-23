

#This code was written by Clemens Dittmar. 
#If you have any questions or problems, please contact Clemens.Dittmar@rwth-aachen.de

#These functions are intended for simplified Geant4 communication and are used for the server - client communication.



from multiprocessing import connection
import socket 
import threading
import os, sys
import pexpect as px 
import time

# Default geometry parametres
BlockPosition = [[-20,-10,0,10,20],[0,0,0,0,0],[0,0,0,0,0]]
BlockSize = [[2,2,2,2,1],[20,20,20,20,20],[10,10,10,10,10]]
Material = ["Scintillator","Aluminium","Silicon","Lead","Scintillator"]
Number_of_Layer = [0,0,0,0,0] #[1,1,1,1,4]  # No block is placed

# List of primary particles
ParticleList = ["e-","e+","mu-","mu+","geantino","gamma"]


# Max Y Block position
MaxBlockPosition = [ 50, -50 ] # Check what is written in Geant4
#Max particle energy
MaxEnergy = 100000 #MeV
# X-Axis gun psition
XGunPosi = -40 #cm
# Number of events for statistic
NEvents = 1000

#//////////////////////////////////////// Functions
# Starts Geant4 child process.
# return child which is used to communicated
# Define number of threads for Geant4 simulations
NThreads = 7
Path = os.path.abspath(os.getcwd())

def Start_G4():
    print("Spawning CalSG")
    child = px.spawn(Path + '/../build/CalSG')
    print("return from spawn")
    child.expect('PreInit> ')
    print("expect return")
    child.sendline('/control/execute Run_Beam_v1.mac')
    print("sent")
    child.expect('Idle>')
    print("got Idle>")
    child.sendline('/run/numberOfThreads ' + str(NThreads))
    print("sent")
    child.expect('Idle>')
    print("got Idle>")
    print("Geant4 is in Idle mode. Commands can be sent.")
    return child

#////////////////////////////////////////////////////
#Stop Geant4 
def Stop_G4(child):
    child.sendline("exit")


#////////////////////////////////////////////////////
# Changes primary particle parameters
# recieves tring from client with new parametres
# check given parameters 
# input like : "e-;20;0"
def Beam_Gun(textline,child):
    Check = True
    
    AllVal = textline #.split("|") # Split at "|" to get info for each Gun if more than one gun is needed
    Particle = []
    Energy = []
    YPosy = []

    value = AllVal.split(";") # Split at ";" to get command Inf: Particle ; Energy (in MeV) ; YPosition
    Particle.append(value[0])
    Energy.append(value[1])
    YPosy.append(value[2])

    print("Recieved Particle gun values ",value)
    for i in range(len(ParticleList)):
        if Particle[0]==ParticleList[i]:
            child.sendline("/gun/particle " + Particle[0])
            print("sent" ,"/gun/particle " + Particle[0] )
            Particle[0] = "F"
            break
    if Particle[0] != "F":
        Check = False
        print("Particle: ", Particle[0], " is unknown, e- was used.")
        child.sendline('/gun/particle e-')

    child.expect('Idle>')
    print("got Idel>") 
    
    if float(Energy[0]) < 0 or float(Energy[0])> MaxEnergy:
        Energy[0] = "1" # Default energy value if sended energy is <0 or over max energy.
        Check = False
    child.sendline("/gun/energy " + Energy[0] + " MeV")
    child.expect('Idle>')
    print("got Idel>") 
    
    print("Sending new position")
    child.sendline("/gun/position " + str(XGunPosi) + " " + YPosy[0] + " 0")
    child.expect('Idle>')
    print("got Idel>") 
    return Check






#///////////////////////////////////////////////////
# sends command to Geant4 to change geometry
def Cpp_Execution(Block,Y,NOL,child):
    BlockPosition[1][Block] += Y
    Number_of_Layer[Block] += NOL
    Text = "/testem/det/setBlock " + str(Block) + " " + str(BlockPosition[0][Block]) + " cm "+ str(BlockPosition[1][Block]) + " cm "+ str(BlockPosition[2][Block]) + " cm " + str(BlockSize[0][Block]) + " cm "+ str(BlockSize[1][Block]) + " cm "+ str(BlockSize[2][Block]) + " cm "+ Material[Block] + " " + str(Number_of_Layer[Block])
    child.sendline(Text)
    print("sent" , Text)
    child.expect('Idle>')
    print("got Idel> got idel sent") 

    

#////////////////////////////////////////////////////
# Run simulation und change geometry 
# If NRum is true N events are simulated
# If NRun is false 1 event is simulated

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
        child.sendline("/run/beamOn 1")
        print("sent")
        child.expect('Idle>')
        child.sendline("/vis/disable")
        print("Disabled visualisation")
        child.expect('Idle>')
        print("Start N events for statistic.")
        child.sendline("/run/beamOn " + str(NEvents))
        print("sent")
        child.expect('Idle>')
        child.sendline("/vis/enable")
        print("Enable visualisation")
    else:
        child.sendline("/run/beamOn 1")
        print("sent")
    child.expect('Idle>')
    print("got Idel>")

#////////////////////////////////////////////////////
# Check geometry changes from client if allowed 
# more needs to be done here

def Geometry_Check(textline):
    value = textline.split("|") # Split at "|" to get command for each block
    print("Checking New geometry changes from client:",value)
    CheckC = True
    for i in range(len(value)):
        vi = value[i].split(";")
        dy = float(vi[0])
        NL = int(vi[1])
        if ( ((BlockPosition[1][i] + BlockSize[1][i]/2 + dy) > MaxBlockPosition[0]  ) or ( (BlockPosition[1][i] - BlockSize[1][i]/2 + dy) < MaxBlockPosition[1]) ): # check new block high if inside world
            CheckC = False
           
            value[i] = "0;" + str(NL)
           # change to 0 change
            print("ERROR: Something was not in size")
    returnText = ""
    for i in range(len(value)):
        returnText += value[i] + "|"

    return returnText[:-1], CheckC



# example code to test functions here or to use Control_G4_Py directly
'''
def NewGeometry(Dy,NL,child):
    Text = str(Dy[0]) + ";" + str(NL[0]) + "|" + str(Dy[1]) + ";" + str(NL[1]) + "|" + str(Dy[2]) + ";" + str(NL[2]) + "|" + str(Dy[3]) + ";" + str(NL[3]) + "|" + str(Dy[4]) + ";" + str(NL[4])
    handle_Geant4Commands(Text,child,False)

def Change_Particle_Gun(Particle,Energy,YP,child):
    Text = Particle + ";" + str(Energy) + ";" + str(YP) 
    Beam_Gun(Text,child)

child = Start_G4()

NewGeometry([0,0,0,0,0],[1,1,1,1,4],child)
Change_Particle_Gun("e-",10,0,child)

N = 20
import time
st = time.time()
for i in range(N):
    NewGeometry([0,-10 + i,0,0.5,0],[0,0,0,0,0],child)
elapsed_time = time.time() - st
print('Execution time:', elapsed_time/N, 'seconds')
Stop_G4(child)
'''