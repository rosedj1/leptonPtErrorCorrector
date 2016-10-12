# getEBECorrection_HZZ4L

step to run package

1, ./doLambda1.sh 

Take lambda1 from output/plots and put in doAll.sh

2, ./doAll.sh

other directories:

1, dir to save correction factors: lambdas_singleCB, edit in getLambda2.py
 
2, set inputdirectory in pTErrCorrector.py ("self.fileName")

3, set where to put plots in getLambda1.py and getLambda2.py ("path")
