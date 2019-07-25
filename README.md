# leptonPtErrorCorrector

step to run doCorrection

1, ./doLambda1.sh 
- This will run doLambda1_getPara.py and produce the first mll histo and the fit.
- Then it will run doLambda1_getLambda.py, retain all params (except sigma), and refit, making another mll plot.

Take lambda1 from output/plots and put in doAll.sh

2, ./doAll.sh
(looks almost identical to doLambda1.sh, except it has a --lambda1_pre flag)

other directories:

1, dir to save correction factors: lambdas_singleCB, edit in getLambda2.py
 
2, set inputdirectory in pTErrCorrector.py ("self.fileName")

3, set where to put plots in getLambda1.py and getLambda2.py ("path")
