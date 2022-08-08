#ifndef SensitiveBlock_HH
#define SensitiveBlock_HH
#include "G4VSensitiveDetector.hh"
#include "SensitiveBlockHit.hh"

class SensitiveBlock : public G4VSensitiveDetector
{
public:
    SensitiveBlock(G4String, const G4String& hitsCollectionName);
    ~SensitiveBlock();

    virtual void Initialize(G4HCofThisEvent* HCE);
    virtual G4bool ProcessHits(G4Step *, G4TouchableHistory *);
    virtual void EndOfEvent(G4HCofThisEvent* HCE);

    //const G4String& GetCollName()   const{ return hitsCollectionName;}
  
private:
    SensitiveBlockHitCollection * hitCollection;
    int collectionID;
    
};

#endif


