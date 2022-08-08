#ifndef SensitiveBlockHit_HH
#define SensitiveBlockHit_HH
#include "G4VHit.hh"
#include "G4Allocator.hh"
#include "G4THitsCollection.hh"
#include "DetectorConstruction.hh"

class SensitiveBlockHit : public G4VHit {
public:
    SensitiveBlockHit();
    SensitiveBlockHit(G4int cellID) : G4VHit(),fCellID(cellID){}
    ~SensitiveBlockHit();
    /*
    SensitiveBlockHit((const SensitiveBlockHit &right) = default;)
    ~SensitiveBlockHit() override;

    SensitiveBlockHit& operator = (const SensitiveBlockHit &right) = default;
    G4bool operator==(const SensitiveBlockHit &right) const;
    */
   // void Print();
    void AddEdep(G4int k, const double e){eDep[k] += e;}

    G4double GetEdep(G4int k)   const{ return eDep[k]; G4cout<<"Test"<<G4endl;}
    G4int GetBlockNumber() const{ return fBlockNumber; }

private:
     G4int fBlockNumber;
    G4int fCellID = -1;
    G4double eDep[5] = {0.0,0.0,0.0,0.0,0.0};  // Hier is a big problem CD


};

typedef G4THitsCollection<SensitiveBlockHit> SensitiveBlockHitCollection;

#endif