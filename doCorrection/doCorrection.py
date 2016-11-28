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
    parser.add_argument('--doPara', dest='doPara', action='store_true', default=False, help='doPara')
    parser.add_argument('--lambdas',dest='lambdas', nargs='+', help='', type=float)#, required=True)
    parser.add_argument('--inpath', dest='inpath', type=str)
    parser.add_argument('--outpath', dest='outpath', type=str)
    parser.add_argument('--ptLow_lambda1', dest='ptLow_lambda1', type=float)
    parser.add_argument('--ptHigh_lambda1', dest='ptHigh_lambda1', type=float)
    parser.add_argument('--etaLow_lambda1', dest='etaLow_lambda1', type=float)
    parser.add_argument('--etaHigh_lambda1', dest='etaHigh_lambda1', type=float)
    
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
doLambda1[0] = args.doLambda1
doLambda1[1] = {'pTLow': args.pTLow_lambda1, 'pTHigh':args.pTHigh_lambda1, 'etaLow':args.etaLow_lambda1, 'etaHigh':args.etaHigh_lambda1}
doPara = args.doPara
lambdas = {'lambda1':args.lambdas[0], 'lambda2':args.lambdas[1]}
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0}

path = {}
path['input'] = args.inpath #"/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/"
path['output'] = args.outpath #"/home/mhl/public_html/2016/20161125_mass/test/" #getLambda1/"

tag = 'do'
if doLambda1[0]:
   tag += 'Lambda1_'
else:
   tag += 'Lambda2_'

if doPara:

   tag += 'getPara_' + fs
   getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
   getCorr_getPara.DriverGetPara()
   shapePara = getCorr_getPara.shapePara
   with open('shapeParameters/' + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
        f.write('shapePara = ' + str(shapePara) + ' \n')

else:

   tag += 'getLambda_' + fs
   getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
   tmpPara_ =  __import__(getCorr_getLambda.name.replace('getLambda', 'getPara').replace('.','p'), globals(), locals())
   getCorr_getLambda.shapePara = tmpPara_.shapePara
   getCorr_getLambda.DriverGetLambda()
   lambdaFileName = 'pT_' + str(binEdge['pTLow']) + '_' + str(binEdge['pTHigh']) + '_eta_' + str(binEdge['etaLow']) + '_' + str(binEdge['etaHigh'])
   lambdaFileName.replace('.','p')
   if isData:
      lambdaFileName += '_'+fs+'_data.py'
   else: 
      lambdaFileName += '_'+fs+'_mc.py'
   with open('lambdas_singleCB/'+lambdaFileName, 'w')  as f:
        f.write('lambdas = ' + str(getCorr_getLambda.Lambdas)+'\n')
