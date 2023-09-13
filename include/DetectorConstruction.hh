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
/// \file electromagnetic/CalSG/include/DetectorConstruction.hh
/// \brief Definition of the DetectorConstruction class
//
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#ifndef DetectorConstruction_h
#define DetectorConstruction_h 1

#include "G4VUserDetectorConstruction.hh"
#include "globals.hh"
#include "G4Cache.hh"
#include <list>

#include "SensitiveBlock.hh"  //CD
class G4Box;
class G4LogicalVolume;
class G4VPhysicalVolume;
class G4Material;
class DetectorMessenger;

class G4GlobalMagFieldMessenger;

const G4int kMaxAbsor = 10;                        // 0 + 9  
const G4int fNBlocks = 5; // Number of moveble Blocks ,CD
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

class DetectorConstruction : public G4VUserDetectorConstruction
{
public:
  
   DetectorConstruction();
  ~DetectorConstruction();

public:
  
  void SetNbOfAbsor     (G4int);      
  void SetAbsorMaterial (G4int,const G4String&);     
  void SetAbsorThickness(G4int,G4double);
          
  void SetWorldMaterial (const G4String&);
  void SetCalorSizeY   (G4double);  
  void SetCalorSizeZ   (G4double);         
  void SetNbOfLayers    (G4int);   

// Set the parameters of all Blocks CD
  // void SetBlockActiv (G4int blockNo, G4double);     // Unused ...
  G4bool SetNbOfBlockLayers (G4int blockNo, G4int numberOfLayers);
  G4bool SetBlockMaterial (G4int blockNo,const G4String& materialName ); 
  G4bool SetBlockAbsorMaterial (G4int blockNo, const G4String& absorberName);
  G4bool SetBlockPosition(G4int blockNo, G4double xPos, G4double yPos, G4double zPos);
  G4bool SetBlockSize(G4int, G4double, G4double, G4double);
  
  virtual G4VPhysicalVolume* Construct();
  virtual void ConstructSDandField();
     
public:
  
  void PrintCalorParameters(); 
                    
  G4double GetWorldSizeX() const           {return fWorldSizeX;}; 
  G4double GetWorldSizeYZ() const          {return fWorldSizeYZ;};
     
  G4double GetCalorThickness() const       {return fCalorThickness;}; 
  G4double GetCalorSizeY() const          {return fCalorSizeY;};
  G4double GetCalorSizeZ() const          {return fCalorSizeZ;};
      
  G4int GetNbOfLayers() const              {return fNbOfLayers;}; 
     
  G4int       GetNbOfAbsor() const                {return fNbOfAbsor;}; 
  G4double    GetAbsorThickness(G4int i) const    {return fAbsorThickness[i];};
  const G4Material* GetAbsorMaterial(G4int i) const {return fAbsorMaterial[i];};

  const G4VPhysicalVolume* GetphysiWorld() const      {return fPhysiWorld;};
  const G4Material*        GetWorldMaterial() const   {return fWorldMaterial;};
  const G4VPhysicalVolume* GetAbsorber(G4int i) const {return fPhysiAbsor[i];};

  // Methods for Blocks - to set/get block attributes, each one's layers and their Material         
  //   CD 
  G4int GetNbOfBlockLayers(G4int i) const {return fNbOfBlockLayers[i];}; 
  const G4VPhysicalVolume* GetBlock(G4int i) const {return fPhysiBlockLayer[i];}; //New 
  const G4Material* GetBlockMaterial(G4int i) const {return fBlockMaterial[i][0];}; //New  CD
  const G4Material* GetAbsorBlockMaterial(G4int i) const {return fBlockMaterial[i][1];}; //New  CD

  G4double GetBlockSize(G4int iBlock, G4int coord) const {return fBlockSize[iBlock][coord];};
  G4double GetBlockPosition(G4int iBlock, G4int coord) const {return fBlockPosi[iBlock][coord];};


private:

  void DefineMaterials();
  void ComputeCalorParameters();
 // virtual void ConstructSDandField(); //CD

  G4int              fNbOfAbsor;
  G4Material*        fAbsorMaterial[kMaxAbsor];
  G4double           fAbsorThickness[kMaxAbsor];

  G4int              fNbOfLayers;
  G4double           fLayerThickness;

  std::list<G4double> fNCalorSizeZ;

  G4double           fCalorSizeZ;
  G4double           fCalorSizeY;
  G4double           fCalorThickness;

  G4double           fCalorSizeZ1;
  G4double           fCalorSizeY1;
  G4double           fCalorThickness1;

  G4double           fCalorSizeZ2;
  G4double           fCalorSizeY2;
  G4double           fCalorThickness2;

  // G4int              fNActiveBlocks = 0; // Number of active Blocks  JA 
  G4bool             fBlockSampling[fNBlocks];  // Multi-layer block (as in sampling calorimeters)

  // Ints and double for Blocks, CD
  G4int              fNbOfBlockLayers[fNBlocks];
   // G4double           fBlockSizeZ[fNBlocks];  
   // G4double           fBlockSizeY[fNBlocks];
   // G4double           fBlockSizeX[fNBlocks];  
  G4Material*        fBlockMaterial[fNBlocks][2];
   // G4double           fBlockPosiX[fNBlocks];
   // G4double           fBlockPosiY[fNBlocks];
   // G4double           fBlockPosiZ[fNBlocks];

  G4double           fBlockSize[fNBlocks][3];
  G4double           fBlockPosi[fNBlocks][3];

  G4Box*             fSolidBlockPosition[fNBlocks];
  G4LogicalVolume*   fLogicBlockPosition[fNBlocks];
  G4VPhysicalVolume* fPhysiBlockPosition[fNBlocks];

  G4Box*             fSolidBlockLayer[fNBlocks];
  G4LogicalVolume*   fLogicBlockLayer[fNBlocks];
  G4VPhysicalVolume* fPhysiBlockLayer[fNBlocks];

  G4Box*             fSolidBlockAbsor[fNBlocks];
  G4LogicalVolume*   fLogicBlockAbsor[fNBlocks];
  G4VPhysicalVolume* fPhysiBlockAbsor[fNBlocks];


  G4Material*        fWorldMaterial;
  G4double           fWorldSizeYZ;
  G4double           fWorldSizeX;

  G4Box*             fSolidWorld;
  G4LogicalVolume*   fLogicWorld;
  G4VPhysicalVolume* fPhysiWorld;

  G4Box*             fSolidCalor;
  G4LogicalVolume*   fLogicCalor;
  G4VPhysicalVolume* fPhysiCalor;

  G4Box*             fSolidLayer;
  G4LogicalVolume*   fLogicLayer;
  G4VPhysicalVolume* fPhysiLayer;

  G4Box*             fSolidAbsor[kMaxAbsor];
  G4LogicalVolume*   fLogicAbsor[kMaxAbsor];
  G4VPhysicalVolume* fPhysiAbsor[kMaxAbsor];

  DetectorMessenger* fDetectorMessenger;
  G4Cache<G4GlobalMagFieldMessenger*> fFieldMessenger;

  G4bool             fVerbose= false;  // To provide information
};

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#endif
