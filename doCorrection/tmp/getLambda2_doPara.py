from leptonPtErrorCorrector.doCorrection.pTErrCorrector import GetCorrection
from PyUtils.fileUtils import copyFile, makeDirs
#from pTErrCorrector import *
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
    parser.add_argument('--lambda1_pre', dest='lambda1_pre', type=float)
    parser.add_argument('--isData', dest='isData', action="store_true", default=False)
    parser.add_argument('--fs', dest='fs', type=str)
    parser.add_argument('--doDebugPara', dest='doDEBUG_para', action="store_true",default=False)
    args = parser.parse_args()
    return args

args=ParseOption()

## Flags passed in from doAll.sh
pTLow = args.ptLow
pTHigh = args.ptHigh
etaLow = args.etaLow
etaHigh = args.etaHigh
fs = args.fs
lambda1_pre = args.lambda1_pre
isData = args.isData

binEdge = {'pTLow': pTLow, 'pTHigh':pTHigh, 'etaLow':etaLow, 'etaHigh':etaHigh}
doLambda1 = False
lambdas = {'lambda1':lambda1_pre, 'lambda2':1}
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "pa1":0, "pa2":0, "fsig":0}
#shapePara = {"mean":0, "alpha":0, "n":0, "alpha2":0, "n2":0, "tau":0, "pa1":0, "pa2":0, "fsig":0}

path = {}
path['input']  = pathto_inputdir
path['output'] = pathto_outputdir
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/"
#path['output'] = "/home/mhl/public_html/2016/20161125_mass/test/"

tag = "doLambda2_getPara_" + fs

#get CB para
getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)

getCorr_getPara.DriverGetPara()

if args.doDEBUG_para:
   sys.exit()

shapePara = getCorr_getPara.shapePara

with open('shapeParameters/' + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
     f.write('shapePara = ' + str(shapePara) + ' \n')

print "getLambda2_doPara COMPLETE\n\n"
