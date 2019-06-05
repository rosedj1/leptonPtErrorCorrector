##import sys
##import subprocess as sp
##pwd = sp.check_output(['pwd']).strip('\n')
##sys.path.append(pwd)
##from leptonPtErrorCorrector.doCorrection.pTErrCorrector import GetCorrection
#import sys, os
#print "sys.path is (hopefully you will find CWD there):\n"
#print "CWD is:", os.getcwd()
#print "Is CWD in path?", os.getcwd() in sys.path
#    
#if os.getcwd() not in sys.path:
#    print "Adding CWD and all parent directories to PYTHONPATH."
#
#    pwd = os.getcwd()
#
#    for count in range( len(pwd.split('/'))-1 ):
#        if count == 0:
#            sys.path.append(pwd)
#        else:
#            pwd,_ = os.path.split(pwd)
#            sys.path.append(pwd)
#
#sys.path
from leptonPtErrorCorrector.doCorrection.pTErrCorrector import GetCorrection
from PyUtils.fileUtils import copyFile
import argparse

#____________________________________________________________________________________________________
# User parameters
pathto_shapeParameters = '/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/'

DEBUG = 1
#____________________________________________________________________________________________________
# MAIN
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
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/"
#path['input'] = "/raid/raid7/rosedj1/ForPeeps/ForFilippo/"
path['input'] = "/raid/raid8/ferrico/HZZ4l/CMSSW_10_2_5/src/leptonPtErrorCorrector/makeSlimTree/output/DY_2018/"
path['output'] = "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlots/" #getLambda1/"
#path['output'] = "/home/mhl/public_html/2016/20161125_mass/test/" #getLambda1/"

tag = "doLambda1_getPara_" + fs

# Get CB parameters
# makes a GetCorrection object
# shapePara starts off with all zeros, then it goes through the grind, and they get updated
# 
getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag) 
getCorr_getPara.DriverGetPara()

if DEBUG:
    getCorr_getPara.

# here is where the shapeParameters gets updated
shapePara = getCorr_getPara.shapePara

with open(pathto_shapeParameters + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
#with open('shapeParameters/' + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
     f.write('shapePara = ' + str(shapePara) + ' \n')

