#include "SensitiveBlock.hh"
#include "SensitiveBlockHit.hh"
#include "G4THitsCollection.hh"
#include "G4VHit.hh"
#include "Run.hh"
#include "G4RunManager.hh"

#include "G4SDManager.hh"


SensitiveBlock::SensitiveBlock(G4String name, const G4String& hitsCollectionName) : G4VSensitiveDetector(name),
collectionID(1)
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

/*
  // fill calorimeter hits with zero energy deposition
  for (auto i=0;i<fNBlocks;i++) {
    hitCollection->insert(new SensitiveBlockHit(i));
  }
*/
}

G4bool SensitiveBlock::ProcessHits(G4Step *aStep, G4TouchableHistory *R0hist)
{/*
    G4Track *track = aStep->GetTrack();

    G4StepPoint * preStepPoint = aStep->GetPreStepPoint();
    G4StepPoint * postStepPoint = aStep->GetPostStepPoint();

    G4ThreeVector posParticle = preStepPoint->GetPosition();
    G4cout<< "Particle position: " << posParticle <<G4endl;


    // collect energy deposited in this step
    const G4VTouchable *touchable = aStep->GetPreStepPoint()->GetTouchable();
    G4VPhysicalVolume *physVol = touchable->GetVolume();
    const G4String& name = physVol->GetName();
    G4int CopyNV = physVol->GetCopyNo();

    G4double EDep = aStep->GetTotalEnergyDeposit();
 
  
    G4cout << name << " "<<EDep <<G4endl;
G4cout<< "Test SB"<<G4endl;
    SensitiveBlockHit* aHit = new SensitiveBlockHit(-1); //CopyNV);
    //SensitiveBlockHit* aHit = (*hitCollection)[CopyNV];
    aHit->AddEdep(std::stoi(name), EDep);
    //hitCollection->insert(aHit);
    */
    return true;

}

void SensitiveBlock::EndOfEvent(G4HCofThisEvent* HCE){

}