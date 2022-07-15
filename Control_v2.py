
#!/usr/bin/python

import sys
import os
import numpy as np
import time
import subprocess
import keyboard
#os.system('/build/make')
#os.system('./build/CalSG Run_Beam_v1.mac ')



##############################################
#Define Parameters
##############################################
BlockPosition = [[-20,-10,0,10,20],[0,0,0,0,0],[0,0,0,0,0]]
BlockSize = [[2,2,2,2,2],[10,10,10,10,10],[10,10,10,10,10]]
BlockPosition_D = [[-20,-10,0,10,20],[0,0,0,0,0],[0,0,0,0,0]]
#BlockSize_D = [[50,0,0,0,0],[10,10,10,10,10],[10,10,10,10,10]]
BlockSize_D = [[5,5,5,5,5],[20,20,20,20,20],[20,20,20,20,20]]
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

def Check_Position_v2(N,X,Y,Z,B):
    BlockSizeN = B
    for i in N:
        for j in N:
            if i< j:
                BlockSizeN[0][i] =  B[0][i]
                BlockSizeN[0][j] =  B[0][j]
                #print( i, j)
                #print(BlockSizeN)
                #print( np.abs(X[i] - X[j]) , (BlockSizeN[0][i]/2 + BlockSizeN[0][j]/2))
                if i < j  and np.abs(X[i] - X[j]) < (BlockSizeN[0][i]/2 + BlockSizeN[0][j]/2):
                    BlockSizeN[0][i] =  np.abs(X[i] - X[j])/2#*0.001
                    BlockSizeN[0][j] =  np.abs(X[i] - X[j])/2#*0.001

                    print( i, j)

                    if  np.abs(X[i] - X[j]) == 0.0:
                        BlockSizeN[0][i] =  0.0
                        BlockSizeN[0][j] =  0.0
                        print( i, j)

  

             
            if i < j and np.abs(X[i] - X[j]) != 0.0 and BlockSizeN[0][i] == 0.0 and BlockSizeN[0][j] == 0.0 :
                BlockSizeN[0][i] =  BlockSize_D[0][i]
                BlockSizeN[0][j] =  BlockSize_D[0][j]
                print( i, j)

                if np.abs(X[i] - X[j]) < (BlockSizeN[0][i]/2 + BlockSizeN[0][j]/2):
                    BlockSizeN[0][i] =  np.abs(X[i] - X[j])/2#*0.001
                    BlockSizeN[0][j] =  np.abs(X[i] - X[j])/2#*0.001
                    print( i, j)
            if i != j and X[i] == X[j]:
                BlockSizeN[0][i] =  0.0
                BlockSizeN[0][j] =  0.0
                print( i, j)
           # BlockSize = BlockSizeN
        
    return BlockSizeN








def SetBlockPosition(N,X,Y,Z,M):
    Check_Position(N,X,Y,Z)

    Text = "/testem/det/setBlock " + str(N) + " " + str(X) + " cm "+ str(Y) + " cm "+ str(Z) + " cm " + str(BlockSize[0][N]) + " cm 10.0 cm 10.0 cm " + M + " 1 "
    a_file = open('Run_Beam_v1.mac', "r")
    list_of_lines = a_file.readlines()
   # print(list_of_lines)
    a_file = open('Run_Beam_v1.mac', "w")
    list_of_lines[14 + N] = Text
    a_file.writelines(list_of_lines)
    a_file.close()
    return 0



def SetBlockPosition_v2(N,X,Y,Z,M,B):
    BlockN = Check_Position_v2(N,X,Y,Z,B)

    a_file = open('Run_Beam_v2.mac', "r")
    list_of_lines = a_file.readlines()
    a_file = open('Run_Beam_v2.mac', "w")

    for i in N:
        Text = "/testem/det/setBlock " + str(i) + " " + str(X[i]) + " cm "+ str(Y[i]) + " cm "+ str(Z[i]) + " cm " + str(BlockN[0][i]) + " cm 10.0 cm 10.0 cm "+ M[i] + " 1 "
        list_of_lines[14 + i] = Text
        print(i, Text)
    a_file.writelines(list_of_lines)

    a_file.close()
    return 0


def SetBlockPosition_v3(N,X):
    #BlockN = Check_Position_v2(N,X,Y,Z,B)

    a_file = open('Run_Beam_v2.mac', "r")
    list_of_lines = a_file.readlines()
    a_file = open('Run_Beam_v2.mac', "w")
    N = 0
    
    TX = list_of_lines[14 + N]
    print(TX)
    print(len(TX))
    Xi = TX[22+8:26+5]
    print(Xi)

    Text = TX[0:30] + str(int( Xi) + X[N] ) + TX[31:74]

    list_of_lines[14 + N] = Text
    print(N, Text)
    a_file.writelines(list_of_lines)

    a_file.close()
    return 0


def Cpp_Execution():
    proc = subprocess.Popen(["./build/CalSG", "Run_Beam_v1.mac"],
    stdin=None ,#subprocess.PIPE,
    stdout=subprocess.PIPE,
    universal_newlines=False)

   # inp = input("Message to CPP>> ")

   # proc.stdin.write("/run/beamOn 1")
    stdout, stderr = proc.communicate()

arg = 0

def main(arg):
    i = int(arg)

    M3 = ["Lead","Lead","Lead","Lead","Lead","Lead","Aluminium","Aluminium","Aluminium","Aluminium",]
  
    M = ["Aluminium","Scintillator",M3[4],"Aluminium","Aluminium"]
    N = [0,1,2,3,4]
   # X = [-20 + i*4,-10 - i, 0, 10,20]
    X = [-30+i*2,-10 - i, 0.0, 10,20]
    Y = [i,i,0,-1,i]
    Z = [0,0,0,0,0]
    
    #value = input("Please enter an integer:\n")
 
    #value = int(value)
    #if value == 1:
    #time.sleep(0.5)
    if keyboard.is_pressed("1"):
        X = [1,0,0,0,0]
        SetBlockPosition_v3(0,X)
        time.sleep(0.1)
    #if value == 2:
    if keyboard.is_pressed("2"):
        X = [-1,0,0,0,0]
        SetBlockPosition_v3(0,X)
        time.sleep(0.1)


        
    
    BlockSize_D = [[2,2,2,2,2],[20,20,20,20,20],[20,20,20,20,20]]
    #SetBlockPosition_v2(N,X,Y,Z,M,BlockSize_D)
     

    # os.system('./build/CalSG Run_Beam_v1.mac ')
   # Cpp_Execution()
   #return 




if __name__ == "__main__":

    main(sys.argv[1])
