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
// TrajectoryWithTime
//
// Class description:
//
// Variant trajectory which stores the laboratory global time in addition to standard values, e.g. position, ... Started from G4Trajectory

// --------------------------------------------------------------------
#ifndef TrajectoryWithTime_hh
#define TrajectoryWithTime_hh 1

#include <stdlib.h>                 // Include from 'system'
#include <vector>

#include "trkgdefs.hh"
#include "G4VTrajectory.hh"
#include "G4Allocator.hh"
#include "G4ios.hh"                 // Include from 'system'
#include "globals.hh"               // Include from 'global'
#include "G4ParticleDefinition.hh"  // Include from 'particle+matter'
#include "TrajectoryWithTimePoint.hh"     // Include from 'tracking'
#include "G4Track.hh"
#include "G4Step.hh"

class G4Polyline;

class TrajectoryWithTime : public G4VTrajectory
{

  using G4TrajectoryPointContainer = std::vector<G4VTrajectoryPoint*>;

  public:

    // Constructors/Destructor

    TrajectoryWithTime();
    TrajectoryWithTime(const G4Track* aTrack);
    TrajectoryWithTime(TrajectoryWithTime &);
    virtual ~TrajectoryWithTime();

    // Operators

    inline void* operator new(size_t);
    inline void  operator delete(void*);
    inline G4int operator == (const TrajectoryWithTime& r) const;

    // Get/Set functions 

    inline G4int GetTrackID() const
      { return fTrackID; }
    inline G4int GetParentID() const
      { return fParentID; }
    inline G4String GetParticleName() const
      { return ParticleName; }
    inline G4double GetCharge() const
      { return PDGCharge; }
    inline G4int GetPDGEncoding() const
      { return PDGEncoding; }
    inline G4double GetInitialKineticEnergy() const
      { return initialKineticEnergy; }
    inline G4ThreeVector GetInitialMomentum() const
      { return initialMomentum; }

    // Other member functions

    virtual void ShowTrajectory(std::ostream& os=G4cout) const;
    virtual void DrawTrajectory() const;
    virtual void AppendStep(const G4Step* aStep);
    virtual G4int GetPointEntries() const
      { return G4int(positionRecord->size()); }
    virtual G4VTrajectoryPoint* GetPoint(G4int i) const
      { return (*positionRecord)[i]; }
    virtual void MergeTrajectory(G4VTrajectory* secondTrajectory);

    G4ParticleDefinition* GetParticleDefinition();

    virtual const std::map<G4String,G4AttDef>* GetAttDefs() const;
    virtual std::vector<G4AttValue>* CreateAttValues() const;

  private:
    G4TrajectoryPointContainer* positionRecord = nullptr;
    G4int                       fTrackID = 0;
    G4int                       fParentID = 0;
    G4int                       PDGEncoding = 0;
    G4double                    PDGCharge = 0.0;
    G4String                    ParticleName = "";
    G4double                    initialKineticEnergy = 0.0;
    G4ThreeVector               initialMomentum;
};

extern G4TRACKING_DLL G4Allocator<TrajectoryWithTime>*& aTrajectoryWithTimeAllocator();

inline void* TrajectoryWithTime::operator new(size_t)
{
  if (aTrajectoryWithTimeAllocator() == nullptr)
  {
    aTrajectoryWithTimeAllocator() = new G4Allocator<TrajectoryWithTime>;
  }
  return (void*)aTrajectoryWithTimeAllocator()->MallocSingle();
}

inline void TrajectoryWithTime::operator delete(void* aTrajectory)
{
  aTrajectoryWithTimeAllocator()->FreeSingle((TrajectoryWithTime*)aTrajectory);
}

inline G4int TrajectoryWithTime::operator == (const TrajectoryWithTime& r) const
{
  return (this==&r);
}

#endif
