
#
#  Run script for CalSG with local input files
#  
#    - saves output files 
#
#  v0.1   J. Apostolakis  2023.09.14    18:25
#
runType=${1:-"2vol"}
runNo=${2:-""}

if [[ $runNo == "" || $runType == "" ]]; then
  echo " usage:  2 arguments - both mandatory: "
  echo "        1st:  run number 001, 002, etc (used to label output)  " 
  echo "        2nd:  input file id -  X in runX.mac" 
  exit
fi
# shift 

#xe="../../build-debug/CalSG" 
exe="../../build/CalSG" 

inputFl="run${runType}.mac"

if [[ ! -f $inputFl ]]; then
  echo "Cannot find input file " $inputFl
  exit 1
fi

runId="${runType}.n$runNo"
#utputFl="out-run${runId}.log"
outputFl="out-run${runType}.n$runNo.log"
## $exe $inputFl  2>&1  | grep -v 'is not found' |& tee $outputFl  ## out-run${runType}.n$runNo.log

$exe $inputFl  2>&1  | grep -v 'is not found' > $outputFl
tail -10 $outputFl

sleep 1
echo
echo "Results: "
echo "---------------------"
echo " Per layer energy deposition ( MeV )  " 
lines=`cat stuff.csv | wc -l`
if [ $lines -lt 30 ]; then
   cat  stuff.csv
else
   good=`../scripts/select-1e-30.pl stuff.csv | wc -l`    
   echo " Non-zero lines:  $good  of  $lines"
   echo 
   echo "Ten with least Energy in first layer: "
   grep -v '#' stuff.csv  | sort -nb -k 1 | head -10 
   echo
   echo "Ten with  most Energy in first layer: "
   grep -v '#' stuff.csv  | sort -nb -k 1 | tail -10 
   echo
fi
echo

mv -i stuff.csv              stuff-${runId}.csv

echo "Output files:"

# ls -l $outputFl  stuff-${runId}.csv

if [[ -f TrajectoryData.heprep ]]; then
    mv -i TrajectoryData.heprep  TrajectoryData-${runId}.heprep
    ls -l $outputFl  stuff-${runId}.csv  TrajectoryData-${runId}.heprep
else
    ls -l $outputFl  stuff-${runId}.csv
fi
echo
