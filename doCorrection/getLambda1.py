from pTErrCorrector import *
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

pTLow = args.ptLow
pTHigh = args.ptHigh
etaLow = args.etaLow
etaHigh = args.etaHigh
binEdge = {'pTLow': pTLow, 'pTHigh':pTHigh, 'etaLow':etaLow, 'etaHigh':etaHigh}
isData = args.isData
fs = args.fs
doLambda1 = True
lambdas = {'lambda1':1, 'lambda2':1}
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "pa1":0, "pa2":0, "fsig":0}
#shapePara = {"mean":0, "alpha":0, "n":0, "alpha2":0, "n2":0, "tau":0, "pa1":0, "pa2":0, "fsig":0}

path = "/home/mhl/public_html/2016/20161122_mass/getLambda1_e/"

tag = "doLambda1_getPara_" + fs

#get CB para
getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
getCorr_getPara.DriverGetPara()

shapePara = getCorr_getPara.shapePara
tag = "doLambda1_getLambda_" + fs

#get lambda
getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
getCorr_getLambda.DriverGetLambda()


