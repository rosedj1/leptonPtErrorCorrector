from leptonPtErrorCorrector.doCorrection.pTErrCorrector import GetCorrection
from leptonPtErrorCorrector.doCorrection.tmp.kinem_bins import kinem_bin_dict
from PyUtils.fileUtils import copyFile, makeDirs
#from kinem_bins import 
import argparse, sys

#____________________________________________________________________________________________________
### AUTOMATIC STUFF
def ParseOption():
    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--ptLow', dest='ptLow', type=float)
    parser.add_argument('--ptHigh', dest='ptHigh', type=float)
    parser.add_argument('--isData', dest='isData', action='store_true', default=False)
    parser.add_argument('--fs', dest='fs', type=str)
    parser.add_argument('--shapeParaDir', dest='shapeParaDir', type=str)
    parser.add_argument('--inputDir', dest='inputDir', type=str)
    parser.add_argument('--outputDir', dest='outputDir', type=str)
    parser.add_argument('--inputFileName', dest='inputFileName', type=str)
    parser.add_argument('--debug', dest='debug', type=int, default=0)
    parser.add_argument('--getPara', dest='getPara', type=int)
    parser.add_argument('--getLambda', dest='getLambda', type=int)
    parser.add_argument('--kinem_bin', dest='kinem_bin', type=str, default='')
    args = parser.parse_args()
    return args
    #parser.add_argument('--etaLow', dest='etaLow', type=float)
    #parser.add_argument('--etaHigh', dest='etaHigh', type=float)

args=ParseOption()
## Flags passed in from doLambda1.sh
pTLow                = args.ptLow           
pTHigh               = args.ptHigh          
fs                   = args.fs              
isData               = args.isData          
shapeParaDir         = args.shapeParaDir
inputDir             = args.inputDir
outputDir            = args.outputDir #getLambda1/"
inputfilename        = args.inputFileName
DEBUG                = args.debug
getPara              = args.getPara
getLambda            = args.getLambda
kinem_bin_str        = args.kinem_bin
kinem_bin_local_dict = kinem_bin_dict[kinem_bin_str]
etaLow               = kinem_bin_local_dict['eta_min']
etaHigh              = kinem_bin_local_dict['eta_max']

## Make output dirs if they don't exist and copy index.php file.
makeDirs(outputDir)
makeDirs(shapeParaDir)
copyFile("/home/rosedj1/","index.php",outputDir)
sys.path.append(shapeParaDir)
#_____________________________________________________________________________________
### MAIN
binEdge = {'pTLow': pTLow, 'pTHigh':pTHigh, 'etaLow':etaLow, 'etaHigh':etaHigh}
doLambda1 = True
lambdas = {'lambda1':1, 'lambda2':1} # starting values for all lambdas
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0} # starting values for all parameters

path = {}
path['input']    = inputDir
path['output']   = outputDir
path['filename'] = inputfilename

print ("Analyzing", fs, "final state.")
print "Running over file:\n %s%s" % (inputDir,inputfilename)
#if fs == 'e':
#    print "Electron region chosen:",args.e_region,"\n   with parameters:",e_region_choice

#_____ Get Parameters _____#
if getPara and not getLambda:
    print "Getting parameters..."
    ### Get CB parameters
    # makes a GetCorrection object
    # shapePara starts off with all zeros
    tag = "doLambda1_getPara_" + fs
    getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag, kinem_bin_str) 
#    getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag, kinem_bin_local_dict) 

    if DEBUG:
        print "Parameters of getCorr_getPara object BEFORE fit:"
        for key,val in getCorr_getPara.__dict__.items():
            print key,":",val

    # then it goes through the grind, and the parameters get updated
    PmassZ, chi2, dof, ch, latex = getCorr_getPara.DriverGetPara()

    if DEBUG:
        print "Parameters of getCorr_getPara object AFTER fit:"
        for key,val in getCorr_getPara.__dict__.items():
            print key,":",val

    # update global shapePara dict
    shapePara = getCorr_getPara.shapePara
    with open(shapeParaDir + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
    #with open('shapeParameters/' + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
         f.write('shapePara = ' + str(shapePara) + ' \n')
    print "getLambda1_doPara.py COMPLETE\n\n"


#_____ Get Lambda _____#
elif getLambda and not getPara:
    print "Getting Lambda..."
    tag = "doLambda1_getLambda_" + fs
    getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag, kinem_bin_str)
#    getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag, kinem_bin_local_dict)
    #getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag, e_region)
    #tmpPara_ =  __import__('test', globals(), locals())

    if DEBUG:
        print "Parameters of getCorr_getLambda object BEFORE __import__(getCorr_getPara):\n"
        for key,val in getCorr_getLambda.__dict__.items():
            print key,":",val

    ## ???
    tmpPara_ =  __import__(getCorr_getLambda.name.replace('getLambda', 'getPara').replace('.','p'), globals(), locals())

    if DEBUG:
        print "getCorr_getLambda.shapePara after __import__ and before DriverGetLambda():\n",getCorr_getLambda.shapePara
        for key,val in getCorr_getLambda.__dict__.items():
            print key,":",val
        
        print "\ntmpPara_.shapePara after __import__ and before DriverGetLambda():\n",tmpPara_.shapePara
        for key,val in getCorr_getLambda.__dict__.items():
            print key,":",val

    getCorr_getLambda.shapePara = tmpPara_.shapePara
    print "\ngetCorr_getLambda.shapePara:\n", getCorr_getLambda.shapePara

    # The big boy. This keeps the old parameters, finds sigma and lambda.
    PmassZ, chi2, dof, ch, latex = getCorr_getLambda.DriverGetLambda()

    if DEBUG:
        print "\nParameters of getCorr_getLambda.shapePara AFTER fit:"
        for key,val in getCorr_getLambda.__dict__.items():
            print key,":",val
    print "getLambda1_doLambda COMPLETE\n\n"

else:
    print """   ERROR!!!
             Either both getPara and getLambda were specified
             at the same time, or neither was given!
             Exiting now."""
    sys.exit()