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

    void AddEdep(const double e){eDep += e;}

    G4double GetEdep()   const{ return eDep; }
    //G4int GetBlockNumber() const{ return fBlockNumber; }

private:
    // G4int fBlockNumber;
    //G4int fCellID = -1;
    //G4double eDep[5] = {0.0,0.0,0.0,0.0,0.0};  // Hier is a big problem CD
    G4double eDep;

};

typedef G4THitsCollection<SensitiveBlockHit> SensitiveBlockHitCollection;

#endif