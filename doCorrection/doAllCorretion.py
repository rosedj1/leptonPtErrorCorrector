from subprocess import call
import multiprocessing
import sys
from array import array
from ROOT import *

sys.path.append('./lambdas_singleCB')

def GetLambda(isData, pTRange, etaRange, fs, iteration):

    lambdaFileName = 'pT_' + str(float(pTRange[0])) + '_' + str(float(pTRange[1])) + '_eta_' + str(float(etaRange[0])) + '_' + str(float(etaRange[1]))
    lambdaFileName = lambdaFileName.replace('.','p')
    if isData:
       lambdaFileName += '_'+fs+'_data'
    else:
       lambdaFileName += '_'+fs+'_mc' 

    if iteration >= 0:
       lambdaFileName += '_v' +str(iteration) 

    tmpLambda =  __import__(lambdaFileName, globals(), locals())
    lambdas = tmpLambda.lambdas
 
    with open('lambdas_singleCB/'+lambdaFileName+'_log.txt', 'a')  as f:
         f.write('iteration ' + str(iteration) + ': ' + str(lambdas)+'\n')

    lambdas_tagged = ['pT_' + str(float(pTRange[0])) + '_' + str(float(pTRange[1])) + '_eta_' + str(float(etaRange[0])) + '_' + str(float(etaRange[1])), lambdas]
   
    return lambdas_tagged



def doLambda1(pTRange, etaRange, inpath, outpath, fs, isData):

    cmd  = ' python doCorrection.py \
             --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
         + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
         + ' --ptLow_lambda1 ' + str(pTRange[0]) + ' --ptHigh_lambda1 ' + str(pTRange[1]) \
         + ' --etaLow_lambda1 '  + str(etaRange[0]) + ' --etaHigh_lambda1 ' + str(etaRange[1]) \
         + ' --fs ' + fs + ' --doLambda1 --doPara --lambdas 1 1 ' \
         + ' --inpath ' + inpath + ' --outpath ' + outpath + ';'

    cmd += ' python doCorrection.py \
             --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
         + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
         + ' --ptLow_lambda1 ' + str(pTRange[0]) + ' --ptHigh_lambda1 ' + str(pTRange[1]) \
         + ' --etaLow_lambda1 '  + str(etaRange[0]) + ' --etaHigh_lambda1 ' + str(etaRange[1]) \
         + ' --fs ' + fs + ' --doLambda1 --lambdas 1 1 ' \
         + ' --inpath ' + inpath + ' --outpath ' + outpath 

    call(cmd, shell=True)

    lambdas = GetLambda(isData, pTRange, etaRange, fs, -1)

    return lambdas




def doLambda2(pTRange, etaRange, inpath, outpath, fs, isData, lambda1Info, iterationMax):


    lambda1_pt = lambda1Info[0]
    lambda1_eta = lambda1Info[1]
    lambda1 = lambda1Info[2]

    cmd = ' python doCorrection.py \
            --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
        + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
        + ' --ptLow_lambda1 ' + str(lambda1_pt[0]) + ' --ptHigh_lambda1 ' + str(lambda1_pt[1]) \
        + ' --etaLow_lambda1 '  + str(lambda1_eta[0]) + ' --etaHigh_lambda1 ' + str(lambda1_eta[1]) \
        + ' --fs ' + fs + ' --doPara --lambdas ' + str(lambda1) + ' 1 --iteration 0' \
        + ' --inpath ' + inpath + ' --outpath ' + outpath + ';'

    cmd+= ' python doCorrection.py \
            --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
        + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
        + ' --ptLow_lambda1 ' + str(lambda1_pt[0]) + ' --ptHigh_lambda1 ' + str(lambda1_pt[1]) \
        + ' --etaLow_lambda1 '  + str(lambda1_eta[0]) + ' --etaHigh_lambda1 ' + str(lambda1_eta[1]) \
        + ' --fs ' + fs + ' --lambdas ' + str(lambda1) + ' 1 --iteration 0' \
        + ' --inpath ' + inpath + ' --outpath ' + outpath

    call(cmd, shell=True)

    needMoreCorrection = True
    iteration = 0

    lambdas_tagged = GetLambda(isData, pTRange, etaRange, fs, iteration)
    lambdas = lambdas_tagged[1]
    lambdas['lambda2'] *= lambdas['lambda']

    if (abs(lambdas['lambda'] - 1)) < 0.01:
       return lambdas_tagged

    while (needMoreCorrection):

          iteration += 1
          lambda2 = lambdas['lambda2']
         
          cmd = ' python doCorrection.py \
                  --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
              + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
              + ' --ptLow_lambda1 ' + str(lambda1_pt[0]) + ' --ptHigh_lambda1 ' + str(lambda1_pt[1]) \
              + ' --etaLow_lambda1 '  + str(lambda1_eta[0]) + ' --etaHigh_lambda1 ' + str(lambda1_eta[1]) \
              + ' --fs ' + fs + ' --lambdas ' + str(lambda1) + ' ' + str(lambda2) + ' --iteration ' + str(iteration)\
              + ' --inpath ' + inpath + ' --outpath ' + outpath 

          call(cmd, shell=True)          
          lambdas_tagged = GetLambda(isData, pTRange, etaRange, fs, iteration)
          lambdas = lambdas_tagged[1]
          lambdas['lambda2'] *= lambdas['lambda']

          if (abs(lambdas['lambda'] - 1)) < 0.01 or iteration == iterationMax:
             needMoreCorrection = False

    return lambdas_tagged


def MakeLUT(pTs, etas, allLambdas, isData, fs, outpath, doLambda1):
    #make LUT of corrections
    binPt, binEta = array('f'), array('f')
    for i in range(len(pTs)): binPt.append(pTs[i])
    for i in range(len(etas)): binEta.append(etas[i])

    LUT = TH2F("2"+fs, "", len(binPt)-1, binPt, len(binEta)-1, binEta)
    for i in range(len(binPt)-1):
        for j in range(len(binEta)-1):
            tag = 'pT_' + str(float(pTs[i])) + '_' + str(float(pTs[i+1])) + '_eta_' + str(float(etas[j])) + '_' + str(float(etas[j+1]))
            for k in range(len(allLambdas)):
                if allLambdas[k][0] == tag:
                   if doLambda1:
                      LUT.SetBinContent(i+1,j+1, allLambdas[k][1]['lambda'])
                   else:
                      LUT.SetBinContent(i+1,j+1, allLambdas[k][1]['lambda2'])

    if isData:
       file1 = "DoubleLepton_m2"+fs+"LUT_m2"+fs+".root"
    else:
       file1 = "DYJetsToLL_M-50_m2"+fs+"LUT_m2"+fs+".root"

    c1 = TCanvas("c1","",800,800)
    LUT.Draw("text")
    c1.SaveAs(outpath+"LUT_"+fs+".png")

    f1 = TFile('lambdas_singleCB/'+file1, "RECREATE")
    f1.cd()

    LUT.Write()
    f1.Close()


def doLambda1s(pt, eta, inpath, outpath, isData, fs):
    pool = multiprocessing.Pool( len(eta) -1 )
    tasks = []

    #split jobs into different process
    for i in range(len(eta)-1):
        tasks.append( (pt, [eta[i],eta[i+1]], inpath, outpath, fs, isData) )

    results = [pool.apply_async( doLambda1, t ) for t in tasks]

    allLambdas = []
    for result in results:
        (lambdas) = result.get()
        allLambdas.append(lambdas)
        print lambdas

    MakeLUT(pt, eta, allLambdas, isData, fs, outpath, True)


def doMuon(muonPt, muonEta, inpath, outpath, isData):

    pool = multiprocessing.Pool( len(muonEta) -1 )
    tasks = []

    #split jobs into different process
    for i in range(len(muonEta)-1):
        tasks.append( (muonPt, [muonEta[i],muonEta[i+1]], inpath, outpath, 'mu', isData) )

    results = [pool.apply_async( doLambda1, t ) for t in tasks]
   
    allLambdas = []
    for result in results:
        (lambdas) = result.get()
        allLambdas.append(lambdas)
        print lambdas

    MakeLUT(muonPt, muonEta, allLambdas, isData, 'mu', outpath, True)

def doElectron(electronPt, electronEta, inpath, outpath, isData, firstBin):

    lambda1 = doLambda1([firstBin[0],firstBin[1]], [firstBin[2],firstBin[3]], inpath, outpath, 'e', isData)

    pool = multiprocessing.Pool( (len(electronEta) -1)*(len(electronPt) - 1) )
    tasks = []

    #split jobs into different process
    for i in range(len(electronPt)-1):
        for j in range(len(electronEta)-1):
            tasks.append( ([electronPt[i], electronPt[i+1]], [electronEta[j], electronEta[j+1]], inpath, outpath, 'e', isData, \
                           [[firstBin[0],firstBin[1]], [firstBin[2],firstBin[3]],lambda1[1]['lambda']], 5) )

    results = [pool.apply_async( doLambda2, t ) for t in tasks]

    allLambdas = []
    for result in results:
        (lambdas) = result.get()
        allLambdas.append(lambdas)
        print lambdas

    MakeLUT(electronPt, electronEta, allLambdas, isData, 'e', outpath, False)



inpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut/'
#inpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/'
outpath = '/home/mhl/public_html/2016/20161206_mass/scratch/'

muonPt = [5,100]
muonEta = [0, 0.9, 1.8, 2.4]

#electronPt = [7, 40,50,100]
electronPt = [7,100]
electronEta = [0,0.8,1,1.2,1.45,1.57,2,2.5]
#electronEta = [0,0.8,1.5,2.5]

#doMuon(muonPt, muonEta, inpath, outpath, False)
#doElectron(electronPt, electronEta, inpath, outpath, False, [7,100,0,0.8])
doLambda1s(electronPt, electronEta, inpath, outpath, False, 'e')

call('cp lambdas_singleCB/DYJetsToLL_M-50_m2eLUT_m2e.root /raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/packages/doClosure/ZClosure/LUT_2e.root',shell=True)
