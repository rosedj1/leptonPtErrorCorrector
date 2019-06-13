from leptonPtErrorCorrector.doCorrection.pTErrCorrector import GetCorrection
from PyUtils.fileUtils import copyFile, makeDirs
import argparse

#____________________________________________________________________________________________________
### User parameters
pathto_shapeParameters  = '/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/'
pathto_inputdir         = "/raid/raid8/ferrico/HZZ4l/CMSSW_10_2_5/src/leptonPtErrorCorrector/makeSlimTree/output/DY_2018/"
pathto_outputdir        = "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/" #getLambda1/"
inputfilename           = "DYJetsToLL_M-50_kalman_v4_m2e_v2.root"

DEBUG = 1
#____________________________________________________________________________________________________
### AUTOMATIC STUFF
## Make output dir
makeDirs(pathto_outputdir)
copyFile("/home/rosedj1/","index.php",pathto_outputdir)
#____________________________________________________________________________________________________
### MAIN
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--ptLow', dest='ptLow', type=float)
    parser.add_argument('--ptHigh', dest='ptHigh', type=float)
    parser.add_argument('--etaLow', dest='etaLow', type=float)
    parser.add_argument('--etaHigh', dest='etaHigh', type=float)
    parser.add_argument('--isData', dest='isData', action="store_true", default=False)
    #parser.add_argument('--filename', dest='filename', type=str)
    parser.add_argument('--fs', dest='fs', type=str)
    args = parser.parse_args()
    return args

args=ParseOption()
## Flags passed in from doLambda1.sh
pTLow    = args.ptLow
pTHigh   = args.ptHigh
etaLow   = args.etaLow
etaHigh  = args.etaHigh
fs       = args.fs
isData  = args.isData
#filename = args.filename

binEdge = {'pTLow': pTLow, 'pTHigh':pTHigh, 'etaLow':etaLow, 'etaHigh':etaHigh}
doLambda1 = True
lambdas = {'lambda1':1, 'lambda2':1} # starting values for all lambdas
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0} # starting values for all parameters

path = {}
path['input']    = pathto_inputdir
path['output']   = pathto_outputdir
path['filename'] = inputfilename
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/"
#path['input'] = "/raid/raid7/rosedj1/ForPeeps/ForFilippo/"
#path['output'] = "/home/mhl/public_html/2016/20161125_mass/test/" #getLambda1/"

tag = "doLambda1_getPara_" + fs

### Get CB parameters
# makes a GetCorrection object
# shapePara starts off with all zeros
getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag) 
if DEBUG:
    print "Parameters of getCorr_getPara objects BEFORE fit:"
    for key,val in getCorr_getPara.__dict__.items():
        print key,":",val

# then it goes through the grind, and the parameters get updated
getCorr_getPara.DriverGetPara()
if DEBUG:
    print "Parameters of getCorr_getPara objects AFTER fit:"
    for key,val in getCorr_getPara.__dict__.items():
        print key,":",val

# update global shapePara dict
shapePara = getCorr_getPara.shapePara

with open(pathto_shapeParameters + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
#with open('shapeParameters/' + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
     f.write('shapePara = ' + str(shapePara) + ' \n')

print "getLambda1_doPara COMPLETE\n\n"
