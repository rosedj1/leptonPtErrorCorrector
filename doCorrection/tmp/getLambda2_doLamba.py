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
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0}

path = {}
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"
path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/"
path['output'] = "/home/mhl/public_html/2016/20161125_mass/test/"

tag = "doLambda2_getLambda_" + fs + "_v" + str(it)

getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
tmpPara_ =  __import__(getCorr_getLambda.name.replace('getLambda', 'getPara').replace('.','p'), globals(), locals())

getCorr_getLambda.shapePara = tmpPara_.shapePara
getCorr_getLambda.DriverGetLambda()





needMoreCorr = True
it = 0
savedLambda = []

getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
getCorr_getLambda.DriverGetLambda()
tmpLambdas = {'it':it, 'lambda': getCorr_getLambda.Lambdas['lambda'],\
              'lambda2': lambdas['lambda2'], 'lambda2_next': lambdas['lambda2']*getCorr_getLambda.Lambdas['lambda']}
savedLambda.append(tmpLambdas)

while(needMoreCorr):

     it += 1
     tag = "doLambda2_getLambda_" + fs + "_v" + str(it)
     lambdas['lambda2'] = tmpLambdas['lambda2_next']

     print lambdas
     print tmpLambdas

     getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
     getCorr_getLambda.DriverGetLambda()

     tmpLambdas = {'it':it, 'lambda': getCorr_getLambda.Lambdas['lambda'],\
                   'lambda2': lambdas['lambda2'], 'lambda2_next': lambdas['lambda2']*getCorr_getLambda.Lambdas['lambda']}
     savedLambda.append(tmpLambdas)


     if abs(getCorr_getLambda.Lambdas['lambda'] - 1) < 0.01 or it >= 6 : 

        needMoreCorr = False

name = ''
if not args.isData:
   name += 'DY_Pt_' + str(pTLow)  + '_to_' + str(pTHigh) + '_Eta_' + str(etaLow) + '_to_' + str(etaHigh) + '_' + fs
else:
   name += 'Data_Pt_' + str(pTLow)  + '_to_' + str(pTHigh) + '_Eta_' + str(etaLow) + '_to_' + str(etaHigh) + '_' + fs

with open("lambdas_singleCB/" + name + ".txt", "w") as myfile:

     for i in range(len(savedLambda)):

         nit = savedLambda[i]['it']
         Lambda = savedLambda[i]['lambda']
         Lambda2 = savedLambda[i]['lambda2']
         Lambda2_next = savedLambda[i]['lambda2_next']

         myfile.write('it: ' + str(nit) + ', lambda: ' + str(Lambda) + ', lambda2: ' + str(Lambda2) + ', lambda2_next: ' + str(Lambda2_next) + '\n') 

myfile.close()
