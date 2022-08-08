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
/// \file electromagnetic/CalSG/src/EventAction.cc
/// \brief Implementation of the EventAction class
//
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "EventAction.hh"

#include "Run.hh"
#include "HistoManager.hh"

#include "G4RunManager.hh"
#include "G4Event.hh"

#include "G4VHit.hh"
#include "G4Allocator.hh"
#include "G4THitsCollection.hh"
#include "SensitiveBlockHit.hh"
#include "SensitiveBlockHit.hh"
#include "G4SDManager.hh"
// Utility function which finds a hit collection with the given Id
// and print warnings if not found
G4VHitsCollection* GetHC(const G4Event* event, G4int collId) {
  auto HCE = event->GetHCofThisEvent();
  if (!HCE) {
      G4ExceptionDescription msg;
      msg << "No hits collection of this event found." << G4endl;
      G4Exception("EventAction::EndOfEventAction()",
                  "Code001", JustWarning, msg);
      return nullptr;
  }

  auto hitsCollection = HCE->GetHC(collId);
  if ( ! hitsCollection) {
    G4ExceptionDescription msg;
    msg << "Hits collection " << collId << " of this event not found." << G4endl;
    G4Exception("EventAction::EndOfEventAction()",
                "Code001", JustWarning, msg);
  }
  return hitsCollection;
}


//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

EventAction::EventAction(DetectorConstruction* det)
:G4UserEventAction(),fDetector(det)
{ }

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

EventAction::~EventAction()
{ }

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void EventAction::BeginOfEventAction(const G4Event*)
{    
  //auto sdManager = G4SDManager::GetSDMpointer();   
  G4SDManager* sdManager = G4SDManager::GetSDMpointer();
  //initialize EnergyDeposit per event
  //
  for (G4int k=0; k<kMaxAbsor; k++) {
    fEnergyDeposit[k] = fTrackLengthCh[k] = 0.0;   
  }
/*
  //initialize EnergyDeposit per event for each block  CD
  for (G4int k=0; k<fNBlocks; k++) {
    fEnergyDepositBlock[k] = 0.0;  
    fCalHCID[k]   = sdManager->GetCollectionID("HitsCollectionB" + std::to_string(k+1) + "L1");
  }


*/

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void EventAction::EndOfEventAction(const G4Event*event)
{
  //get Run
  Run* run = static_cast<Run*>(
             G4RunManager::GetRunManager()->GetNonConstCurrentRun());
             
  for (G4int k=1; k<=fDetector->GetNbOfAbsor(); k++) {
     run->FillPerEvent(k,fEnergyDeposit[k],fTrackLengthCh[k]);
     if (fEnergyDeposit[k] > 0.)
             G4AnalysisManager::Instance()->FillH1(k, fEnergyDeposit[k]);
  }

/*
  //G4double SumEventEdep[NB][NBL];
  //G4String SensB[NB]= ["HitsCollectionB1","HitsCollectionB2","HitsCollectionB3","HitsCollectionB4","HitsCollectionB5"];
  //G4String SensBL[NBL] = ["L1","L2","L3","L4","L5"];
  // index is a data member, representing the hits collection index of the considered collection
  // It was initialized to 1 in the class constructor
  int index = 1;


  for (G4int i = 0; i<fNBlocks; i++){
    //for (G4int t = 0; t<NBL; t++){
   
      //if (index < 0) index = G4SDManager::GetSDMpointer()->GetCollectionID("HitsCollectionB" + std::to_string(i+1) + "L1");
      G4cout<<"Test"<<G4endl;
      G4HCofThisEvent* HCE = event->GetHCofThisEvent();
      auto hitsCollection = GetHC(event, fCalHCID[i]);
      if ( ! hitsCollection ) return;

//      SensitiveBlockHitCollection* hitsCollection = 0;
   //   if (HCE) hitsCollection = (SensitiveBlockHitCollection*)(HCE->GetHC(index)); // cast
      G4cout<< "HitsCollectionB" + std::to_string(i+1) + "L1" << index << HCE->GetHC(index) <<G4endl;

      if (hitsCollection) {
      for (G4int j = 0; j < hitsCollection->GetSize(); ++j) {
      G4double energy = 0.;
      // The EM and Had calorimeter hits are of different types

        auto hit = static_cast<SensitiveBlockHit*>(hitsCollection->GetHit(j));
        energy = hit->GetEdep(i);


      //  G4cout<< "HitsCollectionB" + std::to_string(i+1) + "L1 " << index << " " <<HCE->GetHC(index) <<G4endl;

        //G4int numberHits = hitsCollection->entries();
        //G4cout << "Hit number " << numberHits << G4endl;
       /// for (G4int j= 0; j < numberHits ; j++) {

      //    SensitiveBlockHit* hit = (*hitsCollection)[j];
          // Retrieve information from hit object, e.g.
    //      energy = hit ->GetEdep(i);
          G4cout << i << " Value from Hit collection " << energy << G4endl;
          SumEnergyPerBlock(i,energy);
       // }    
      }
    }
  }
    #ifdef G4MULTITHREADED
    static G4Mutex stuffMutex = G4MUTEX_INITIALIZER;
    G4AutoLock al(&stuffMutex);
    #endif
    static std::ofstream stuff("stuff.csv");
    static bool first = true;
    if (first) {
    first = false;
    stuff << "#,eDep,  Block 1,  Block 2,  Block 3,  Block 4, Block 5" << std::endl;
    }
    G4cout<<"Saving energy depo to csv file."<<G4endl;
    //if (fEnergyDepositBlock[0])
    stuff << fEnergyDepositBlock[0] << ",  "<< fEnergyDepositBlock[1] << ",  "<< fEnergyDepositBlock[2] << ",  "<< fEnergyDepositBlock[3] << ",  "<< fEnergyDepositBlock[4] << std::endl;
    */
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

