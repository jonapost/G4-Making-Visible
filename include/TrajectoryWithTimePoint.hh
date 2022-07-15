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
// TrajectoryWithTimePoint
//
// Class description:
//
// This class represents the trajectory point of a particle being tracked.

// Contact:
//   Questions and comments to this code should be sent to
//     Katsuya Amako  (e-mail: Katsuya.Amako@kek.jp)
//     Takashi Sasaki (e-mail: Takashi.Sasaki@kek.jp)
// --------------------------------------------------------------------
#ifndef TrajectoryWithTimePoint_hh
#define TrajectoryWithTimePoint_hh 

#include "trkgdefs.hh"
#include "G4VTrajectoryPoint.hh"
#include "globals.hh"                // Include from 'global'
#include "G4ThreeVector.hh"          // Include from 'geometry'
#include "G4Allocator.hh"            // Include from 'particle+matter'

class TrajectoryWithTimePoint : public G4VTrajectoryPoint
{
  public:

    // Constructors/Destructor

    TrajectoryWithTimePoint();
    TrajectoryWithTimePoint(G4ThreeVector pos, G4double globalTime);
    TrajectoryWithTimePoint(const TrajectoryWithTimePoint& right);
    virtual ~TrajectoryWithTimePoint();

    // Operators

    inline void *operator new(size_t);
    inline void operator delete(void *aTrajectoryPoint);
    inline G4bool operator==(const TrajectoryWithTimePoint& right) const;

    // Get/Set functions

    inline const G4ThreeVector GetPosition() const
      { return fPosition; }

    // Get method for HEPRep style attributes

    virtual const std::map<G4String,G4AttDef>* GetAttDefs() const;
    virtual std::vector<G4AttValue>* CreateAttValues() const;


  private:

   G4ThreeVector fPosition;
   G4double      fGlobalTime;
};

extern G4TRACKING_DLL
G4Allocator<TrajectoryWithTimePoint>*& aTrajectoryPointWithTimeAllocator();

inline void* TrajectoryWithTimePoint::operator new(size_t)
{
  if (aTrajectoryPointWithTimeAllocator() == nullptr)
  {
    aTrajectoryPointWithTimeAllocator() = new G4Allocator<TrajectoryWithTimePoint>;
  }
  return (void *) aTrajectoryPointWithTimeAllocator()->MallocSingle();
}

inline void TrajectoryWithTimePoint::operator delete(void *aTrajectoryPoint)
{
  aTrajectoryPointWithTimeAllocator()
    ->FreeSingle((TrajectoryWithTimePoint *) aTrajectoryPoint);
}

inline G4bool
TrajectoryWithTimePoint::operator==(const TrajectoryWithTimePoint& right) const
{
  return (this==&right);
}

#endif
