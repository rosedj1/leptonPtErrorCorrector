# Probably best to make this code use classes...
from leptonPtErrorCorrector.doCorrection.pTErrCorrector import GetCorrection
from PyUtils.fileUtils import copyFile, makeDirs
from kinem_bins import e_region_dict, mu_region_dict
import argparse, sys

#____________________________________________________________________________________________________
### Functions
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
    parser.add_argument('-m','--mode', dest='mode', type=str)
    parser.add_argument('--kinem_bin', dest='kinem_bin', type=str, default='',nargs='+')
    args = parser.parse_args()
    return args
    #parser.add_argument('--kinem_bin', dest='kinem_bin', type=str, default='')
    #parser.add_argument('--getPara', dest='getPara', type=int)
    #parser.add_argument('--getLambda', dest='getLambda', type=int)
    #parser.add_argument('--etaLow', dest='etaLow', type=float)
    #parser.add_argument('--etaHigh', dest='etaHigh', type=float)

def printkeyvalpairs(mydict):
    for key,val in mydict.items():
        print key,":",val
#____________________________________________________________________________________________________
# AUTOMATIC STUFF
args=ParseOption()
pTLow            = args.ptLow           
pTHigh           = args.ptHigh          
fs               = args.fs              
isData           = args.isData          
shapeParaDir     = args.shapeParaDir
inputDir         = args.inputDir
outputDir        = args.outputDir #getLambda1/"
inputfilename    = args.inputFileName
DEBUG            = args.debug
mode             = args.mode
#etaLow           = args.etaLow          
#etaHigh          = args.etaHigh         
#getPara          = args.getPara
#getLambda        = args.getLambda
kinem_bin_list = args.kinem_bin

doLambda1 = True
lambdas = {'lambda1':1, 'lambda2':1} # starting values for all lambdas
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0} # starting values for all parameters

path = {}
path['input']    = inputDir
path['output']   = outputDir
path['filename'] = inputfilename

#poss_region_list = (
#    list(e_region_dict.keys()

# A few checks. 
if fs not in ['e','mu']:
    raise Exception("WARNING: --fs must be: 'e' or 'mu'\nExiting now.")
if mode not in ['getPara','getParaAndLambda','getParaAndLambda']:
    raise Exception("WARNING: --mode must be a string in:\n['getPara','getParaAndLambda','getParaAndLambda']")
#if kinem_bin_list not in list(e_region_dict.keys()) + list(mu_region_dict.keys() + )
#    raise Exception("WARNING: --kinem_bin unknown")
   
# Make output dirs if they don't exist and copy index.php file.
makeDirs(outputDir)
makeDirs(shapeParaDir)
copyFile("/home/rosedj1/","index.php",outputDir)
sys.path.append(shapeParaDir)
#_____________________________________________________________________________________
### MAIN
print "Analyzing 2%s final state." % fs 
#print "Kinematic bin(s) chosen:",kinem_bin_list,"\n   with parameters:",kinem_bin_list[]
print "Kinematic bin(s) chosen:",kinem_bin_list
print "Running over file:\n %s%s" % (inputDir,inputfilename)

# If other e_regions or mu_regions are added to kinem_bins.py, this will accommodate.
if fs == 'e':
    region_dict = e_region_dict
    if 'all_e_regions' in kinem_bin_list:
        kinem_bin_list = list(e_region_dict.keys())
elif fs == 'mu':
    region_dict = mu_region_dict
    if 'all_mu_regions' in kinem_bin_list:
        kinem_bin_list = list(mu_region_dict.keys())

print "kinem_bin_list is:", kinem_bin_list
for kbin in kinem_bin_list:    # kbin is a str.
    region_params = region_dict[kbin]
    etaLow  = region_params['eta_min']
    etaHigh = region_params['eta_max']
    binEdge = {'pTLow': pTLow, 'pTHigh':pTHigh, 'etaLow':etaLow, 'etaHigh':etaHigh}

    if mode in ['getPara','getParaAndLambda']:
        print "Getting PARAMETERS..."
        tag = "doLambda1_getPara_" + fs
        ### Get CB parameters by making a GetCorrection object. shapePara starts off with all zeros.
        getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag, region_params) 

        if DEBUG:
            print "Parameters of getCorr_getPara object BEFORE fit:"
            printkeyvalpairs(getCorr_getPara.__dict__)

        # then it goes through the grind, and the parameters get updated
        PmassZ, chi2, dof, ch, latex = getCorr_getPara.DriverGetPara()

        if DEBUG:
            print "Parameters of getCorr_getPara object AFTER fit:"
            printkeyvalpairs(getCorr_getPara.__dict__)

        # update global shapePara dict
        shapePara = getCorr_getPara.shapePara
        with open(shapeParaDir + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
        #with open('shapeParameters/' + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
             f.write('shapePara = ' + str(shapePara) + ' \n')
        print "getLambda1_doPara.py COMPLETE\n\n"

    ########################
    #_____ Get Lambda _____#
    ########################
    if mode in ['getLambda','getParaAndLambda']:
        print "Getting LAMBDA..."
        tag = "doLambda1_getLambda_" + fs
        getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag, region_params)
        #tmpPara_ =  __import__('test', globals(), locals())

        if DEBUG:
            print "Parameters of getCorr_getLambda object BEFORE __import__(getCorr_getPara):\n"
            printkeyvalpairs(getCorr_getLambda.__dict__)

        ## ???
        tmpPara_ =  __import__(getCorr_getLambda.name.replace('getLambda', 'getPara').replace('.','p'), globals(), locals())

        if DEBUG:
            print "getCorr_getLambda.shapePara AFTER __import__ but BEFORE DriverGetLambda():\n",getCorr_getLambda.shapePara
            printkeyvalpairs(getCorr_getLambda.__dict__)
            print "\ntmpPara_.shapePara AFTER __import__ but BEFORE DriverGetLambda():\n",tmpPara_.shapePara

        getCorr_getLambda.shapePara = tmpPara_.shapePara
        print "\ngetCorr_getLambda.shapePara:\n", getCorr_getLambda.shapePara

        # The big boy. This keeps the old parameters, finds sigma and lambda.
        print "Running DriverGetLambda()"
        PmassZ, chi2, dof, ch, latex = getCorr_getLambda.DriverGetLambda()

        if DEBUG:
            print "\nParameters of getCorr_getLambda.shapePara AFTER fit:"
            printkeyvalpairs(getCorr_getLambda.__dict__)

        print "getLambda1_doLambda COMPLETE\n\n"
