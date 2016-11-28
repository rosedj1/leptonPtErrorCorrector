from subprocess import call
import multiprocessing

sys.path.append('./lambdas_singleCB')

def GetLambda(isData, pTRange, etaRange, fs, iteration):

    lambdaFileName = 'pT_' + str(pTRange[0]) + '_' + str(pTRange[1]) + '_eta_' + str(etaRange[0]) + '_' + str(etaRange[1])
    lambdaFileName.replace('.','p')
    if isData:
       lambdaFileName += '_'+fs+'_data'
    else:
       lambdaFileName += '_'+fs+'_mc'

    tmpLambda =  __import__(lambdaFileName, globals(), locals())
    lambdas = tmpLambda.lambdas
 
    with open('lambdas_singleCB/'+lambdaFileName+'_log.txt', 'a')  as f:
         f.write('iteration ' + str(iteration) + ': ' + str(lambdas)+'\n')
   
    return lambdas



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

    lambdas = GetLambda(isData, pTRange, etaRange, fs)

    return lambdas

def doLambda2(pTRange, etaRange, inpath, outpath, fs, lambda1Info, iterationMax):

    lambda1_pt = lambda1Info[0]
    lambda1_eta = lambda1Info[1]
    lambda1 = lambdaInfo[2]

    cmd = ' python doCorrection.py \
            --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
        + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
        + ' --ptLow_lambda1 ' + str(lambda1_pt[0]) + ' --ptHigh_lambda1 ' + str(lambda1_pt[1]) \
        + ' --etaLow_lambda1 '  + str(lambda1_eta[0]) + ' --etaHigh_lambda1 ' + str(lambda1_eta[1]) \
        + ' --fs ' + fs + ' --doPara --lambdas ' + str(lambda1) + ' 1 ' \
        + ' --inpath ' + inpath + ' --outpath ' + outpath + ';'

    cmd+= ' python doCorrection.py \
            --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
        + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
        + ' --ptLow_lambda1 ' + str(lambda1_pt[0]) + ' --ptHigh_lambda1 ' + str(lambda1_pt[1]) \
        + ' --etaLow_lambda1 '  + str(lambda1_eta[0]) + ' --etaHigh_lambda1 ' + str(lambda1_eta[1]) \
        + ' --fs ' + fs + ' --lambdas ' + str(lambda1) + ' 1 ' \
        + ' --inpath ' + inpath + ' --outpath ' + outpath

    needMoreCorrection = True
    iteration = 0
    lambdas = GetLambda(isData, pTRange, etaRange, fs, iteration)
    lambdas['lambda2'] *= lambdas['lambda']

    if (lambdas['lambda2'] - 1) < 0.1:
       return lambdas

    while (needMoreCorrection):

          iteration += 1
          lambda2 = lambdas['lambda2']
         
          cmd = ' python doCorrection.py \
                  --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
              + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
              + ' --ptLow_lambda1 ' + str(lambda1_pt[0]) + ' --ptHigh_lambda1 ' + str(lambda1_pt[1]) \
              + ' --etaLow_lambda1 '  + str(lambda1_eta[0]) + ' --etaHigh_lambda1 ' + str(lambda1_eta[1]) \
              + ' --fs ' + fs + ' --lambdas ' + str(lambda1) + ' ' + str(lambda2) \
              + ' --inpath ' + inpath + ' --outpath ' + outpath 

          call(cmd, shell=True)          
          lambdas = GetLambda(isData, pTRange, etaRange, fs, iteration)
          lambdas['lambda2'] *= lambdas['lambda']

          if (lambdas['lambda'] - 1) < 0.1 or iteration == iterationMax:
             needMoreCorrection = False

    return lambdas

inpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/'
outpath = '/home/mhl/public_html/2016/20161125_mass/test/'

muonPt = [5,100]
muonEta = [0, 0.9, 1.8, 2.4]

pool = multiprocessing.Pool( len(muonEta) -1 )

tasks = []
for i in range(len(muonEta)-1):
    tasks.append( (muonPt, [muonEta[i],muonEta[i+1]], inpath, outpath) )

results = [pool.apply_async( doMuonCorrection, t ) for t in tasks]

for result in results:
    (pTEta) = result.get()
    print pTEta
