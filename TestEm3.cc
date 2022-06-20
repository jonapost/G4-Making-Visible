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
/// \file electromagnetic/TestEm3/TestEm3.cc
/// \brief Main program of the electromagnetic/TestEm3 example
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

#include <stdlib.h>     //for using the function sleep
#include <iostream>   //CD
#include <string>

using namespace std;   // CD
using namespace std::chrono;


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo.....

int main(int argc,char** argv) {
  
  //  string python_message = "";
    
  auto start = high_resolution_clock::now();
  auto stop = high_resolution_clock::now();
  auto start2 = high_resolution_clock::now();
  auto stop2 = high_resolution_clock::now();
  
  start2 = high_resolution_clock::now();

  //detect interactive mode (if no arguments) and define UI session
  G4UIExecutive* ui = nullptr;
  if (argc == 1) { ui = new G4UIExecutive(argc,argv);}//,"tcsh"); }
 
  //Use SteppingVerbose with Unit
  G4int precision = 4;
  G4SteppingVerbose::UseBestUnit(precision);
  
  //Creating run manager
  auto runManager = G4RunManagerFactory::CreateRunManager();
    
  if (argc==3) { 
     G4int nThreads = G4UIcommand::ConvertToInt(argv[2]);
     runManager->SetNumberOfThreads(nThreads);
  }

  //set mandatory initialization classes
  DetectorConstruction* detector = new DetectorConstruction;
  runManager->SetUserInitialization(detector);
  runManager->SetUserInitialization(new PhysicsList);

  //set user action classes
  runManager->SetUserInitialization(new ActionInitialization(detector));

  //initialize visualization
  G4VisManager* visManager = nullptr;

  //get the pointer to the User Interface manager
  G4UImanager* UImanager = G4UImanager::GetUIpointer();

 

  if (ui)  {
    //interactive mode
    visManager = new G4VisExecutive();
    visManager->Initialize();
  //  ui->SessionStart();
   // delete ui;
  } else {
    //batch mode
      visManager = new G4VisExecutive();  
      visManager->Initialize();
      
      G4String command = "/control/execute ";
      G4String fileName =  argv[1];
      start = high_resolution_clock::now();
      UImanager->ApplyCommand(command+fileName);
      stop = high_resolution_clock::now();
      

   //   for (G4int k=0; k<3; ++k) {
  //    bool quit = false;
  //    int Test = 0;

   //   while (!quit){
    //    cin >> python_message;
   //     G4String ComPy =  python_message; 
    //    UImanager->ApplyCommand(ComPy);
   //     cout<< python_message << "Comming from Geant4" <<endl;
  //      sleep(3);
   //     Test = Test + 1;
    //    if Test == 10;
  //        quit = true;
 //   }
  }
//getchar();


  

//sleep(3);



  //job termination
  delete visManager;
  delete runManager;

  stop2 = high_resolution_clock::now();
  //auto duration = duration_cast<microseconds>(stop - start);
    cout << "Command elapsed time in milliseconds: "
        << chrono::duration_cast<chrono::milliseconds>(stop - start).count()
        << " ms" << endl;
    cout << "Program elapsed time in milliseconds: "
        << chrono::duration_cast<chrono::milliseconds>(stop2 - start2).count()
        << " ms" << endl;

 // cout<< python_message << "Comming from Geant4" <<endl;
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
