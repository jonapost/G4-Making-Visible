//
// ********************************************************************
// * License and Disclaimer                                           *
// *                                                                  *
// * The  Geant4 software  is  copyright of the Copyright Holders  of *
// * the Geant4 Collaboration.  It is provided  under  the terms  and *
// * conditions of the Geant4 Software License,  included in the file *
// * LICENSE and available at  http://cern.ch/geant4/license .  These *
// * include a list of copyright holders.                             *
// *                                                                  *
// * Neither the authors of this software system, nor their employing *
// * institutes,nor the agencies providing financial support for this *
// * work  make  any representation or  warranty, express or implied, *
// * regarding  this  software system or assume any liability for its *
// * use.  Please see the license in the file  LICENSE  and URL above *
// * for the full disclaimer and the limitation of liability.         *
// *                                                                  *
// * This  code  implementation is the result of  the  scientific and *
// * technical work of the GEANT4 collaboration.                      *
// * By using,  copying,  modifying or  distributing the software (or *
// * any work based  on the software)  you  agree  to acknowledge its *
// * use  in  resulting  scientific  publications,  and indicate your *
// * acceptance of all terms of the Geant4 Software license.          *
// ********************************************************************
//
/// \file electromagnetic/CalSG/CalSG.cc
/// \brief Main program of the electromagnetic/CalSG example
//
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo.....
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo.....

#include "G4Types.hh"

#include "G4RunManagerFactory.hh"
#include "G4UImanager.hh"
#include "G4SteppingVerbose.hh"
#include "Randomize.hh"

#include "DetectorConstruction.hh"
#include "PhysicsList.hh"
#include "ActionInitialization.hh"

#include "G4UIExecutive.hh"
#include "G4VisExecutive.hh"

#include "G4Exception.hh"

#include <stdlib.h>     //for using the function sleep
#include <iostream>   //CD
#include <string>

using namespace std;   // CD
using namespace std::chrono;


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo.....

int main(int argc,char** argv)
{
  G4String  progName="CalSG";
  auto start2 = high_resolution_clock::now();
  auto stop2 = high_resolution_clock::now();
  
  start2 = high_resolution_clock::now();

  // 0. Detect interactive mode (if no arguments) and define UI session
  G4UIExecutive* ui = nullptr;
  if (argc == 1) {
     ui = new G4UIExecutive(argc,argv,"tcsh");  
  }
 
  //   Choose SteppingVerbose with Units
  G4int precision = 4;
  G4SteppingVerbose::UseBestUnit(precision);
  
  // 1. Create run manager (serial or MT)
  // =====================================
  G4RunManager* runManager= nullptr;
  unsigned int nThreads = 0;  //  Default -- enables MT but allows to read 1 = serial
  if (argc>=3) { 
     auto inpThreads = G4UIcommand::ConvertToInt(argv[2]);
     if( inpThreads >= 0 ) 
        nThreads = inpThreads;
     else
        G4cerr << progName << " argv[2] = " << inpThreads << " is NOT valid. Value must be >= 1 . IGNORED." << G4endl;
  }
  
  if( nThreads == 1 ) {
     runManager = new G4RunManager(); //  Sequential only - for simpler testing
  } else {
     runManager = G4RunManagerFactory::CreateRunManager();
     if( nThreads > 1 )
        runManager->SetNumberOfThreads(nThreads);
  }
  if( runManager == nullptr){
     G4ExceptionDescription msg;
     msg << "Geant4 Failed to create a valid G4RunManager.  Threads= " << nThreads; 
     G4Exception("CalSG (main program) ERROR - no G4RunManager", "Main001",
                 FatalException, msg);
  }

  // 2. Create and set mandatory initialization classes
  // ==================================================
  DetectorConstruction* detector = new DetectorConstruction;
  runManager->SetUserInitialization(detector);
  runManager->SetUserInitialization(new PhysicsList);

  // 3. Set user action class(es) - compatible with MT
  runManager->SetUserInitialization(new ActionInitialization(detector));

  // 4. Initialize visualization and UI
  // =======================================  
  G4VisManager* visManager = nullptr;
  G4UImanager* UImanager = G4UImanager::GetUIpointer();

  if (ui)  
  {
    //interactive mode
    G4cout << progName << ": Entering Interactive mode." << G4endl;     
    visManager = new G4VisExecutive();
    visManager->Initialize();
    ui->SessionStart();
    delete ui;

  }
  else
  {
     // Two batch modes: 

     // A. Loop mode
     // ----------------------
     if( strcmp(argv[1], "Loop") == 0) 
     {
        // Loop changing mode for interaktive test
        visManager = new G4VisExecutive();  
        visManager->Initialize();
        G4cout << progName << ": Entering LOOP mode." << G4endl;
        
        G4String command = "/control/execute ";
        G4String commandS = "/control/shell ";
        G4String fileName =  "Run_Beam_v1.mac";
        G4String PyCommand = "python3 ../Control_v2.py ";  // Was "sudo python3 ... 
        for (G4int i=1; i<=20; i++) {
           if (i>1){fileName = "Run_Beam_v2.mac";}
           UImanager->ApplyCommand(commandS+PyCommand+std::to_string(i));
           UImanager->ApplyCommand(command+fileName);
           // sleep(1);
           
        }
     } 
     else 
     {
        // B. Pure batch mode
        // ----------------------        
        visManager = new G4VisExecutive();  
        visManager->Initialize();
        G4cout << progName << ": Entering Batch mode." << G4endl;
        
        G4String command = "/control/execute ";
        G4String fileName =  argv[1];
        
        UImanager->ApplyCommand(command+fileName);
     }
  }
  // G4cout << "Press Return to exit." << G4endl;
  // getchar();

  //job termination
  delete visManager;
  //getchar();
  delete runManager;

    stop2 = high_resolution_clock::now();
    cout << "Program elapsed time in milliseconds: "
        << chrono::duration_cast<chrono::milliseconds>(stop2 - start2).count()
        << " ms" << endl;

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
