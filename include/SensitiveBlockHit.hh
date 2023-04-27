#ifndef SensitiveBlockHit_HH
#define SensitiveBlockHit_HH
#include "G4VHit.hh"
#include "G4Allocator.hh"
#include "G4THitsCollection.hh"
#include "DetectorConstruction.hh"

class SensitiveBlockHit : public G4VHit {
public:
    SensitiveBlockHit();
    ~SensitiveBlockHit();

    void AddEdep(double e){ fEneryDeposit += e;}

    G4double GetEdep() const{ return fEneryDeposit; }
    //G4int GetBlockNumber() const{ return fBlockNumber; }

private:
    // G4int fBlockNumber;
    //G4int fCellID = -1;
    //G4double fEneryDepositArr[5] = {0.0,0.0,0.0,0.0,0.0};  // Here is a big problem ClemD/CD
    G4double fEneryDeposit;

};

typedef G4THitsCollection<SensitiveBlockHit> SensitiveBlockHitCollection;

#endif