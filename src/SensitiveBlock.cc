#include "SensitiveBlock.hh"
#include "SensitiveBlockHit.hh"
#include "G4THitsCollection.hh"
#include "G4VHit.hh"
#include "Run.hh"
#include "G4RunManager.hh"

#include "G4SDManager.hh"

#include "G4HCofThisEvent.hh"


SensitiveBlock::SensitiveBlock(G4int Copy, G4String name, const G4String& hitsCollectionName) : G4VSensitiveDetector(name),
collectionID(-1), hitCollection(nullptr), fCopy(Copy)
{
    G4cout<< "Creating SD with name: "<<hitsCollectionName <<G4endl;
    collectionName.insert(hitsCollectionName);
    
}
SensitiveBlock::~SensitiveBlock()
{}

void SensitiveBlock::Initialize(G4HCofThisEvent* HCE)
{
    hitCollection = new SensitiveBlockHitCollection(GetName(), collectionName[0]);
    if (collectionID<0) 
    collectionID = G4SDManager::GetSDMpointer()->GetCollectionID(hitCollection); //GetCollectionID(0); //

    HCE->AddHitsCollection(collectionID, hitCollection);


  // fill calorimeter hits with zero energy deposition
  for (auto i=0;i<fCopy;i++) {
    hitCollection->insert(new SensitiveBlockHit());
  }

}

G4bool SensitiveBlock::ProcessHits(G4Step *aStep, G4TouchableHistory *R0hist)
{


 
    // collect energy deposited in this step
    const G4VTouchable *touchable = aStep->GetPreStepPoint()->GetTouchable();
    G4VPhysicalVolume *physVol = touchable->GetVolume();
    const G4String& name = physVol->GetName();

    G4int CopyNV = physVol->GetCopyNo();

    G4double EDep = aStep->GetTotalEnergyDeposit();
 
  
    G4cout << name << ", CopyNumber " << CopyNV << " Energy deposition "<<EDep <<G4endl;

    SensitiveBlockHit* aHit = (*hitCollection)[CopyNV];
    aHit->AddEdep(EDep);
  
    
    return true;

}

void SensitiveBlock::EndOfEvent(G4HCofThisEvent* HCE){

}