from pTErrCorrector import *
import argparse

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

pTLow = args.ptLow
pTHigh = args.ptHigh
etaLow = args.etaLow
etaHigh = args.etaHigh
binEdge = {'pTLow': pTLow, 'pTHigh':pTHigh, 'etaLow':etaLow, 'etaHigh':etaHigh}
isData = args.isData
fs = args.fs
doLambda1 = False
lambda1_pre = args.lambda1_pre
lambdas = {'lambda1':lambda1_pre, 'lambda2':1}
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "pa1":0, "pa2":0, "fsig":0}
#shapePara = {"mean":0, "alpha":0, "n":0, "alpha2":0, "n2":0, "tau":0, "pa1":0, "pa2":0, "fsig":0}

path = {}
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"
path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/"
path['output'] = "/home/mhl/public_html/2016/20161125_mass/test/"

tag = "doLambda2_getPara_" + fs

#get CB para
getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)

getCorr_getPara.DriverGetPara()

#sys.exit()

if args.doDEBUG_para:
   sys.exit()

shapePara = getCorr_getPara.shapePara

with open('shapeParameters/' + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
     f.write('shapePara = ' + str(shapePara) + ' \n')

