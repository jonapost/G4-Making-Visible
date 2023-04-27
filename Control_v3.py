import os
import numpy as np
import time
import keyboard
import time



##############################################
#Define Parameters
##############################################
BlockPosition = [[-20,-10,0,10,20],[0,0,0,0,0],[0,0,0,0,0]]
BlockSize = [[2,2,2,2,2],[10,10,10,10,10],[10,10,10,10,10]]
BlockPosition_D = [[-20,-10,0,10,20],[0,0,0,0,0],[0,0,0,0,0]]
#BlockSize_D = [[50,0,0,0,0],[10,10,10,10,10],[10,10,10,10,10]]
BlockSize_D = [[5,5,5,5,5],[20,20,20,20,20],[20,20,20,20,20]]
Material = ["Aluminium","Lead","Uranium","Scintillator","Scintillator"]
Number_of_Layer = [1,1,1,1,1]

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

    Text = "/det/setBlock " + str(N) + " " + str(X) + " cm "+ str(Y) + " cm "+ str(Z) + " cm " + str(BlockSize[0][N]) + " cm 10.0 cm 10.0 cm " + M + " 1 \n"
    a_file = open('build/Run_Beam_v1.mac', "r")
    list_of_lines = a_file.readlines()
   # print(list_of_lines)
    a_file = open('build/Run_Beam_v1.mac', "w")
    list_of_lines[14 + N] = Text
    a_file.writelines(list_of_lines)
    a_file.close()
    return 0



def SetBlockPosition_v2(N,X,Y,Z,M,B):
    BlockN = Check_Position_v2(N,X,Y,Z,B)

    a_file = open('build/Run_Beam_v1.mac', "r")
    list_of_lines = a_file.readlines()
    a_file = open('build/Run_Beam_v1.mac', "w")

    for i in N:
        Text = "/det/setBlock " + str(i) + " " + str(X[i]) + " cm "+ str(Y[i]) + " cm "+ str(Z[i]) + " cm " + str(BlockN[0][i]) + " cm 10.0 cm 10.0 cm "+ M[i] + " 1 \n"
        list_of_lines[14 + i] = Text
        print(i, Text)
    a_file.writelines(list_of_lines)

    a_file.close()
    return 0


def SetBlockPosition_v3(N,X):
    #BlockN = Check_Position_v2(N,X,Y,Z,B)

    a_file = open('build/Run_Beam_v2.mac', "r")
    list_of_lines = a_file.readlines()
    a_file = open('build/Run_Beam_v2.mac', "w")

    
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





def Cpp_Execution(Block,Y,NOL):
    BlockPosition_D[1][Block] += Y
    Number_of_Layer[Block] += NOL
    #BlockPosition_D[1][Block] += Y[0]  Is note avaleble know
    #BlockPosition_D[1][Block] += Y[0]
     
      
    Text = "/det/setBlock " + str(Block) + " " + str(BlockPosition_D[0][Block]) + " cm "+ str(BlockPosition_D[1][Block]) + " cm "+ str(BlockPosition_D[2][Block]) + " cm " + "2" + " cm 10.0 cm 10.0 cm "+ Material[Block] + " " + str(Number_of_Layer[Block])
    child.sendline(Text)
    print("sent" , Text)
    child.expect('Idle>')
    print("got Idle> promptt") 
    child.sendline("/run/reinitializeGeometry")
    print("sent reinitialize Geometrie")
    child.expect('Idle>')
    print("got Idle> prompt")
    return







q = True

import pexpect as px  
print("-Spawning CalSG in ./build")
child = px.spawn('./build/CalSG')
print("-returned from spawn")
child.expect('PreInit> ')
print("-got PreInit> prompt")
child.sendline('/control/execute Run_Beam_v1.mac')
print("-sent execute Run_Beam_v1")
child.expect('Idle>')
print("got Idle> prompt")
# get the start time
st = time.time()
N = 0
while(q):
    value = input("Please enter an integer:\n")
    print(value)
    if (value[1] == "u"):
        Cpp_Execution(int(value[0]),1,0)
    if (value[1] == "d"):
        Cpp_Execution(int(value[0]),-1,0)
    if (value[1] == "m"):
        Cpp_Execution(int(value[0]),0,1)
    if (value[1] == "l" and Number_of_Layer[int(value[0])]>1):
        Cpp_Execution(int(value[0]),0,-1)
    if (value[1] == "C"):
        Cpp_Execution(int(value[0]),0,0)
    if (value == "q"):
        child.sendline("exit")

        q = False
        break

    child.sendline('/control/execute Beam_ON_File.mac')
    print("sent")
    child.expect('Idle>')
    print("got Idle> prompt")
    #if (N==100):
       # break

    N +=1

et = time.time()

# get the execution time
elapsed_time = et - st
print('Execution time:', elapsed_time/N, 'seconds', "\n" , "For mean time 10 changes with 1 events each")
