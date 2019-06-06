#import sys
#import subprocess as sp
#pwd = sp.check_output(['pwd']).strip('\n')
#print "Executing script from dir:",pwd
#sys.path.append(pwd)
#from pTErrCorrector import GetCorrection
from leptonPtErrorCorrector.doCorrection.pTErrCorrector import GetCorrection
from PyUtils.fileUtils import copyFile
import argparse

def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--ptLow', dest='ptLow', type=float)
    parser.add_argument('--ptHigh', dest='ptHigh', type=float)
    parser.add_argument('--etaLow', dest='etaLow', type=float)
    parser.add_argument('--etaHigh', dest='etaHigh', type=float)
    parser.add_argument('--isData', dest='isData', action="store_true", default=False)
    parser.add_argument('--fs', dest='fs', type=str)

    args = parser.parse_args()
    return args

args=ParseOption()
#sys.path.append('./shapeParameters')

pTLow = args.ptLow
pTHigh = args.ptHigh
etaLow = args.etaLow
etaHigh = args.etaHigh
binEdge = {'pTLow': pTLow, 'pTHigh':pTHigh, 'etaLow':etaLow, 'etaHigh':etaHigh}
isData = args.isData
fs = args.fs
doLambda1 = True
lambdas = {'lambda1':1, 'lambda2':1}
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0}

path = {}
path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/"
path['output'] = "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlots/" #getLambda1/"
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"
#path['output'] = "/home/mhl/public_html/2016/20161125_mass/test/" #getLambda1/"


tag = "doLambda1_getLambda_" + fs

# Get lambda
getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
#tmpPara_ =  __import__('test', globals(), locals())
tmpPara_ =  __import__(getCorr_getLambda.name.replace('getLambda', 'getPara').replace('.','p'), globals(), locals())

getCorr_getLambda.shapePara = tmpPara_.shapePara
getCorr_getLambda.DriverGetLambda()
copyFile("/home/rosedj1/","index.php",path['output'])
