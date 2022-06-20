import os
import numpy as np
import time
#os.system('/build/make')
#os.system('./build/TestEm3 Run_Beam_v1.mac ')

##############################################
#Define Parameters
##############################################
BlockPosition = [[-20,-10,0,10,20],[0,0,0,0,0],[0,0,0,0,0]]
BlockSize = [[2,2,2,2,2],[10,10,10,10,10],[10,10,10,10,10]]
BlockPosition_D = [[-20,-10,0,10,20],[0,0,0,0,0],[0,0,0,0,0]]
BlockSize_D = [[2,2,2,2,2],[10,10,10,10,10],[10,10,10,10,10]]
Material = ["Aluminium","Aluminium","Aluminium","Aluminium","Aluminium"]

print(BlockSize)
print(BlockSize[1][0])
##############################################
# Change Parameters
##############################################
def Check_Position(N,X,Y,Z):
    OXP = BlockPosition[0][N]
    OXS = BlockSize[0][N]
    for i in range(5):
        if i != N and np.abs(BlockPosition[0][i] - X) < (BlockSize[0][i]/2 + BlockSize[0][N]/2):
            #print( i , N , BlockPosition[0][N], X, np.abs(BlockPosition[0][N] - X) , (BlockSize[0][i]/2 + BlockSize[0][N]/2))
            #BlockSize[0][i] =  np.abs(BlockPosition[0][N] - X)/2
            BlockSize[0][N] =  np.abs(BlockPosition[0][N] - X) - BlockSize[0][N]


            if np.abs(BlockPosition[0][i] - X) <= BlockSize[0][i]/2:
                #BlockSize[0][i] =  0.0
                BlockSize[0][N] =  0.0

        if i != N and BlockSize[0][N] == 0.0  and np.abs(BlockPosition[0][i] - X) != 0.0:
            #BlockSize[0][i] =  BlockSize_D[0][i]
            BlockSize[0][N] =  BlockSize_D[0][N]

            if  np.abs(BlockPosition[0][i] - X) < (BlockSize[0][i]/2 + BlockSize[0][N]/2):
                #print( i , N , BlockPosition[0][N], X, np.abs(BlockPosition[0][N] - X) , (BlockSize[0][i]/2 + BlockSize[0][N]/2))
                #BlockSize[0][i] =  np.abs(BlockPosition[0][N] - X)/2
                BlockSize[0][N] =  np.abs(BlockPosition[0][N] - X) - BlockSize[0][N]

                if np.abs(BlockPosition[0][i] - X) <= BlockSize[0][i]/2:
                    #BlockSize[0][i] =  0.0
                    BlockSize[0][N] =  0.0
            
        

  
    return 0

def Check_Position_v2(N,X,Y,Z):
    for i in N:
        for j in N:
            BlockSize[0][i] =  BlockSize_D[0][i]
            BlockSize[0][j] =  BlockSize_D[0][j]
            if i < j  and np.abs(X[i] - X[j]) < (BlockSize[0][i]/2 + BlockSize[0][j]/2):
                BlockSize[0][i] =  np.abs(X[i] - X[j])/2*0.001
                BlockSize[0][j] =  np.abs(X[i] - X[j])/2*0.001

                print( i, j)

                if  np.abs(X[i] - X[j]) == 0.0:
                    BlockSize[0][i] =  0.0
                    BlockSize[0][j] =  0.0
            if i < j and np.abs(X[i] - X[j]) != 0.0 and BlockSize[0][i] == 0.0 and BlockSize[0][j] == 0.0 :
                BlockSize[0][i] =  BlockSize_D[0][i]
                BlockSize[0][j] =  BlockSize_D[0][j]

                if np.abs(X[i] - X[j]) < (BlockSize[0][i]/2 + BlockSize[0][j]/2):
                    BlockSize[0][i] =  np.abs(X[i] - X[j])/2*0.001
                    BlockSize[0][j] =  np.abs(X[i] - X[j])/2*0.001
            if i != j and X[i] == X[j]:
                BlockSize[0][i] =  0.0
                BlockSize[0][j] =  0.0
    return 0








def SetBlockPosition(N,X,Y,Z,M):
    Check_Position(N,X,Y,Z)

    Text = "/testem/det/setBlock " + str(N) + " " + str(X) + " cm "+ str(Y) + " cm "+ str(Z) + " cm " + str(BlockSize[0][N]) + " cm 10.0 cm 10.0 cm " + M + "\n"
    a_file = open('Run_Beam_v1.mac', "r")
    list_of_lines = a_file.readlines()
   # print(list_of_lines)
    a_file = open('Run_Beam_v1.mac', "w")
    list_of_lines[14 + N] = Text
    a_file.writelines(list_of_lines)
    a_file.close()
    return 0



def SetBlockPosition_v2(N,X,Y,Z,M):
    Check_Position_v2(N,X,Y,Z)

    a_file = open('Run_Beam_v1.mac', "r")
    list_of_lines = a_file.readlines()
    a_file = open('Run_Beam_v1.mac', "w")

    for i in N:
        Text = "/testem/det/setBlock " + str(i) + " " + str(X[i]) + " cm "+ str(Y[i]) + " cm "+ str(Z[i]) + " cm " + str(BlockSize[0][i]) + " cm 10.0 cm 10.0 cm "+ M[i] + "\n"
        list_of_lines[14 + i] = Text
        print(i, Text)
    a_file.writelines(list_of_lines)

    a_file.close()
    return 0



import subprocess

proc = subprocess.Popen("/home/kappe/projects/CERN_SS/Geant_Project/TestEm3_1Block_moveble/build ./TestEm3",
stdin=subprocess.PIPE,
stdout=subprocess.PIPE)

state = "run"
while state == "run":
    input = input("Message to CPP>> ")

    if input == "quit":
        state = "terminate" # any string other than "run" will do

    proc.stdin.write(input + "\n")
    cppMessage = proc.stdout.readline().rstrip("\n") 
    print( "cppreturn message ->" + cppMessage + " written by python \n")





'''

for i in range(5):
    SetBlockPosition(i,BlockPosition[0][i],BlockPosition[1][i],BlockPosition[2][i],Material[i])



#os.system('./build/TestEm3 Run_Beam_v1.mac ')
M3 = ["Lead","Lead","Lead","Lead","Lead","Lead","Aluminium","Aluminium","Aluminium","Aluminium",]
for i in range(10):
    M = ["Aluminium","Scintillator",M3[i],"Aluminium","Aluminium"]
    N = [0,1,2,3,4]
    X = [-20 + i*4,-10 - i, 0, 10,20]
    Y = [i,i,0,-1,i]
    Z = [0,0,0,0,0]
    SetBlockPosition_v2(N,X,Y,Z,M)


    os.system('./build/TestEm3 Run_Beam_v1.mac ')

#Work = True
#while(Work):

'''

