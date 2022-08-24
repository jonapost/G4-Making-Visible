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
/// \file electromagnetic/CalSG/src/DetectorMessenger.cc
/// \brief Implementation of the DetectorMessenger class
//
//
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

#include "DetectorMessenger.hh"

#include <sstream>

#include "DetectorConstruction.hh"
#include "G4UIdirectory.hh"
#include "G4UIcommand.hh"
#include "G4UIparameter.hh"
#include "G4UIcmdWithAnInteger.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "G4UIcmdWithoutParameter.hh"

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorMessenger::DetectorMessenger(DetectorConstruction * Det)
:G4UImessenger(),fDetector(Det),
 fTestemDir(0),
 fDetDir(0),
 fSizeYCmd(0),
 fSizeZCmd(0),
 fNbLayersCmd(0),
 fNbAbsorCmd(0),
 fAbsorCmd(0),
 fBlockCmd(0),  // CD  Block parameter for the messenger
 fAbsorBlockCmd(0) //CD
{ 
  fTestemDir = new G4UIdirectory("/testem/");
  fTestemDir->SetGuidance("UI commands specific to this example");
  
  fDetDir = new G4UIdirectory("/testem/det/");
  fDetDir->SetGuidance("detector construction commands");
  
  fSizeYCmd = new G4UIcmdWithADoubleAndUnit("/testem/det/setSizeY",this);
  fSizeYCmd->SetGuidance("Set tranverse Y size of the calorimeter");
  fSizeYCmd->SetParameterName("Size",false);
  fSizeYCmd->SetRange("Size>0.");
  fSizeYCmd->SetUnitCategory("Length");
  fSizeYCmd->AvailableForStates(G4State_PreInit);
  fSizeYCmd->SetToBeBroadcasted(false);

  fSizeZCmd = new G4UIcmdWithADoubleAndUnit("/testem/det/setSizeZ",this);
  fSizeZCmd->SetGuidance("Set tranverse Z size of the calorimeter");
  fSizeZCmd->SetParameterName("Size",false);
  fSizeZCmd->SetRange("Size>=0.");
  fSizeZCmd->SetUnitCategory("Length");
  fSizeZCmd->AvailableForStates(G4State_PreInit);
  fSizeZCmd->SetToBeBroadcasted(false);
    
  fNbLayersCmd = new G4UIcmdWithAnInteger("/testem/det/setNbOfLayers",this);
  fNbLayersCmd->SetGuidance("Set number of layers.");
  fNbLayersCmd->SetParameterName("NbLayers",false);
  fNbLayersCmd->SetRange("NbLayers>0");
  fNbLayersCmd->AvailableForStates(G4State_PreInit);
  fNbLayersCmd->SetToBeBroadcasted(false);
    
  fNbAbsorCmd = new G4UIcmdWithAnInteger("/testem/det/setNbOfAbsor",this);
  fNbAbsorCmd->SetGuidance("Set number of Absorbers.");
  fNbAbsorCmd->SetParameterName("NbAbsor",false);
  fNbAbsorCmd->SetRange("NbAbsor>0");
  fNbAbsorCmd->AvailableForStates(G4State_PreInit);
  fNbAbsorCmd->SetToBeBroadcasted(false);
     
  fAbsorCmd = new G4UIcommand("/testem/det/setAbsor",this);
  fAbsorCmd->SetGuidance("Set the absor nb, the material, the thickness.");
  fAbsorCmd->SetGuidance("  absor number : from 1 to NbOfAbsor");
  fAbsorCmd->SetGuidance("  material name");
  fAbsorCmd->SetGuidance("  thickness (with unit) : t>0."); 
  //
  G4UIparameter* AbsNbPrm = new G4UIparameter("AbsorNb",'i',false);
  AbsNbPrm->SetGuidance("absor number : from 1 to NbOfAbsor");
  AbsNbPrm->SetParameterRange("AbsorNb>0");
  fAbsorCmd->SetParameter(AbsNbPrm);
  //
  G4UIparameter* MatPrm = new G4UIparameter("material",'s',false);
  MatPrm->SetGuidance("material name");
  fAbsorCmd->SetParameter(MatPrm);
  //    
  G4UIparameter* ThickPrm = new G4UIparameter("thickness",'d',false);
  ThickPrm->SetGuidance("thickness of absorber");
  ThickPrm->SetParameterRange("thickness>0.");
  fAbsorCmd->SetParameter(ThickPrm);
  //
  G4UIparameter* unitPrm = new G4UIparameter("unit",'s',false);
  unitPrm->SetGuidance("unit of thickness");
  G4String unitList = G4UIcommand::UnitsList(G4UIcommand::CategoryOf("mm"));
  unitPrm->SetParameterCandidates(unitList);
  fAbsorCmd->SetParameter(unitPrm);
  //
  fAbsorCmd->AvailableForStates(G4State_PreInit);
  fAbsorCmd->SetToBeBroadcasted(false);  



  //// New command for Block control  CD, Set the block position, size, material and number of layers
  fBlockCmd = new G4UIcommand("/testem/det/setBlock",this);
  fBlockCmd->SetGuidance("Set the Block Number, the X Position, the Y Position, the Z Position, the X size, the Y size, the Z size, the first material, nb of layer");
  fBlockCmd->SetGuidance(" Block number : from 1 to fNBlock");
  fBlockCmd->SetGuidance(" Block X position (with unit)");
  fBlockCmd->SetGuidance(" Block Y position (with unit)");
  fBlockCmd->SetGuidance(" Block Z position (with unit)");
  fBlockCmd->SetGuidance(" Block X size (with unit)");
  fBlockCmd->SetGuidance(" Block Y size (with unit)");
  fBlockCmd->SetGuidance(" Block Z size (with unit)");
  fBlockCmd->SetGuidance(" first material name");
  fBlockCmd->SetGuidance(" nb of layers : from 1 to 10");
  fBlockCmd->AvailableForStates(G4State_PreInit,G4State_Idle);
  

  G4UIparameter* BlockNbPrm = new G4UIparameter("BlockNb",'i',false);
  BlockNbPrm->SetGuidance("Block number : from 1 to fNBlocks");
  BlockNbPrm->SetParameterRange("BlockNb>=0 & BlockNb<5");
  fBlockCmd->SetParameter(BlockNbPrm);

  G4UIparameter* PosiXPrm = new G4UIparameter("positionx",'d',false);
  PosiXPrm->SetGuidance("Block X position");
  PosiXPrm->SetParameterRange("positionx>-100. & positionx<100");
  fBlockCmd->SetParameter(PosiXPrm);

  G4UIparameter* unitBPrm = new G4UIparameter("unit",'s',false);
  unitBPrm->SetGuidance("unit of length");
  G4String unitBList = G4UIcommand::UnitsList(G4UIcommand::CategoryOf("mm"));
  unitBPrm->SetParameterCandidates(unitBList);
  fBlockCmd->SetParameter(unitBPrm);

  G4UIparameter* PosiYPrm = new G4UIparameter("positiony",'d',false);
  PosiYPrm->SetGuidance("Block Y position");
  PosiYPrm->SetParameterRange("positiony>-100. & positiony<100");
  fBlockCmd->SetParameter(PosiYPrm);
  fBlockCmd->SetParameter(unitBPrm);

  G4UIparameter* PosiZPrm = new G4UIparameter("positionz",'d',false);
  PosiZPrm->SetGuidance("Block Z position");
  PosiZPrm->SetParameterRange("positionz>-100. & positionz<100");
  fBlockCmd->SetParameter(PosiZPrm);
  fBlockCmd->SetParameter(unitBPrm);

  G4UIparameter* SizeXPrm = new G4UIparameter("sizex",'d',false);
  SizeXPrm->SetGuidance("Block X size");
  SizeXPrm->SetParameterRange("sizex>0.0 & sizex<100");
  fBlockCmd->SetParameter(SizeXPrm);
  fBlockCmd->SetParameter(unitBPrm);

  G4UIparameter* SizeYPrm = new G4UIparameter("sizey",'d',false);
  SizeYPrm->SetGuidance("Block Y size");
  SizeYPrm->SetParameterRange("sizey>0.0 & sizey<100");
  fBlockCmd->SetParameter(SizeYPrm);
  fBlockCmd->SetParameter(unitBPrm);

  G4UIparameter* SizeZPrm = new G4UIparameter("sizez",'d',false);
  SizeZPrm->SetGuidance("Block Z size");
  SizeZPrm->SetParameterRange("sizez>0.0 & sizez<100");
  fBlockCmd->SetParameter(SizeZPrm);
  fBlockCmd->SetParameter(unitBPrm);

  G4UIparameter* MatBPrm = new G4UIparameter("material",'s',false);
  MatBPrm->SetGuidance("first material name");
  fBlockCmd->SetParameter(MatBPrm);

  G4UIparameter* LayerNbPrm = new G4UIparameter("LayerNb",'i',false);
  LayerNbPrm->SetGuidance("layer number : from 1 to 10");
  LayerNbPrm->SetParameterRange("LayerNb>=0 & LayerNb<11");
  fBlockCmd->SetParameter(LayerNbPrm);

  //
  fBlockCmd->SetToBeBroadcasted(false); 


  // Command which defines the absorbers per plock
  fAbsorBlockCmd = new G4UIcommand("/testem/det/setAbsorBlock",this);
  fAbsorBlockCmd->SetGuidance("Set the Block nb, the material");
  fAbsorBlockCmd->SetGuidance("  Block number : from 1 to fNBlocks");
  fAbsorBlockCmd->SetGuidance("  material name");
  //
  fAbsorBlockCmd->SetParameter(BlockNbPrm);
  //
  G4UIparameter* MatAPrm = new G4UIparameter("material",'s',false);
  MatAPrm->SetGuidance("material name");
  fAbsorBlockCmd->SetParameter(MatAPrm);
  //    
  //
  fAbsorBlockCmd->AvailableForStates(G4State_PreInit,G4State_Idle);

  fAbsorBlockCmd->SetToBeBroadcasted(false); 
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

DetectorMessenger::~DetectorMessenger()
{
  
  delete fSizeZCmd;
  delete fSizeYCmd;
  delete fNbLayersCmd;
  delete fNbAbsorCmd;
  delete fAbsorCmd;
  delete fAbsorBlockCmd;
  delete fDetDir;  
  delete fTestemDir;

}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......

void DetectorMessenger::SetNewValue(G4UIcommand* command,G4String newValue)
{
  if( command == fSizeYCmd )
   { fDetector->SetCalorSizeY(fSizeYCmd->GetNewDoubleValue(newValue));}
     
  if( command == fSizeZCmd )
   { fDetector->SetCalorSizeZ(fSizeZCmd->GetNewDoubleValue(newValue));}

  if( command == fNbLayersCmd )
   { fDetector->SetNbOfLayers(fNbLayersCmd->GetNewIntValue(newValue));}

  if( command == fNbAbsorCmd )
   { fDetector->SetNbOfAbsor(fNbAbsorCmd->GetNewIntValue(newValue));}
   
  if (command == fAbsorCmd)
   {
     G4int num; G4double tick;
     G4String unt, mat;
     std::istringstream is(newValue);
     is >> num >> mat >> tick >> unt;
     G4String material=mat;
     tick *= G4UIcommand::ValueOf(unt);
     fDetector->SetAbsorMaterial (num,material);
     fDetector->SetAbsorThickness(num,tick);
   }
  if (command == fAbsorBlockCmd)
   {
     G4int num; 
     G4String mat;
     std::istringstream is(newValue);
     is >> num >> mat;
     G4String material=mat;
     fDetector->SetBlockAbsorMaterial (num,material);
   }

  if (command == fBlockCmd) 
   {
    G4int num; G4double Px; G4double Py; G4double Pz;
    G4double Sx; G4double Sy; G4double Sz;
    G4String unt1,unt2,unt3,unt4,unt5,unt6, mat; G4int Nl;
    std::istringstream is(newValue);
     is >> num >> Px >> unt1 >> Py >> unt2 >> Pz >> unt3 >> Sx >> unt4 >> Sy >> unt5 >> Sz >> unt6 >> mat >> Nl;
     G4String material=mat;
     Px *= G4UIcommand::ValueOf(unt1);
     Py *= G4UIcommand::ValueOf(unt2);
     Pz *= G4UIcommand::ValueOf(unt3);
     Sx *= G4UIcommand::ValueOf(unt4);
     Sy *= G4UIcommand::ValueOf(unt5);
     Sz *= G4UIcommand::ValueOf(unt6);

     fDetector->SetBlockMaterial (num,material);
     fDetector->SetBlockPosition (num,Px,Py,Pz);
     fDetector->SetBlockSize (num,Sx,Sy,Sz);
     fDetector->SetNbOfBlockLayers (num,Nl);
     

   }
}

//....oooOO0OOooo........oooOO0OOooo........oooOO0OOooo........oooOO0OOooo......
