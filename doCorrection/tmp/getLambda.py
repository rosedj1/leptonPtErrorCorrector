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
    parser.add_argument('--doLambda1', dest='doLambda1', action='store_true', default=False, help='doLambda1')
    parser.add_argument('--lambdas',dest='lambdas', nargs='+', help='', type=float)#, required=True)
    parser.add_argument('--inpath', dest='inpath', type=str)
    parser.add_argument('--outpath', dest='outpath', type=str)

    args = parser.parse_args()
    return args


args=ParseOption()
sys.path.append('./shapeParameters')

pTLow = args.ptLow
pTHigh = args.ptHigh
etaLow = args.etaLow
etaHigh = args.etaHigh
binEdge = {'pTLow': pTLow, 'pTHigh':pTHigh, 'etaLow':etaLow, 'etaHigh':etaHigh}
isData = args.isData
fs = args.fs
doLambda1 = args.doLambda1
lambdas = {'lambda1':args.lambdas[0], 'lambda2':lambdas[1]}
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0}

path = {}
path['input'] = args.inpath #"/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/"
path['output'] = args.output #"/home/mhl/public_html/2016/20161125_mass/test/" #getLambda1/"

tag = 'do'
if doLambda1:
   tag += 'Lambda1_getLambda_' + fs
else:
   tag += 'Lambda2_getLambda_' + fs

#get lambda
getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
#tmpPara_ =  __import__('test', globals(), locals())
tmpPara_ =  __import__(getCorr_getLambda.name.replace('getLambda', 'getPara').replace('.','p'), globals(), locals())

getCorr_getLambda.shapePara = tmpPara_.shapePara
getCorr_getLambda.DriverGetLambda()

