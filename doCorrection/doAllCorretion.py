from subprocess import call
import multiprocessing

def doMuonCorrection(pTRange, etaRange, inpath, outpath):

    cmd = ' time python doCorrection.py \
            --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
        + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
        + ' --fs mu --doLambda1 --doPara --lambdas 1 1 ' \
        + ' --inpath ' + inpath + ' --outpath ' + outpath + ' ;'

    cmd+= ' time python doCorrection.py \
            --ptLow ' + str(pTRange[0]) + ' --ptHigh ' + str(pTRange[1]) \
        + ' --etaLow '  + str(etaRange[0]) + ' --etaHigh ' + str(etaRange[1]) \
        + ' --fs mu --doLambda1 --lambdas 1 1 ' \
        + ' --inpath ' + inpath + ' --outpath ' + outpath 

    call(cmd, shell=True)

    pTEta = [pTRange, etaRange]

    return pTEta 

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
