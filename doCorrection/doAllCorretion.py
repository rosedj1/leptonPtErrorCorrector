from subprocess import call

def doMuonCorrection(inpath, outpath):

    pTBin = [5, 100]
    etaBin = [0, 0.9, 1.8, 2.4]

    for i in range(len(etaBin)-1):
        etaLow = etaBin[i]
        etaHigh = etaBin[i+1]
        cmd = ' time python doCorrection.py \
                --ptLow ' + str(pTBin[0]) + ' --ptHigh ' + str(pTBin[1]) \
            + ' --etaLow '  + str(etaLow) + ' --etaHigh ' + str(etaHigh) \
            + ' --fs mu --doLambda1 --doPara --lambdas 1 1 ' \
            + ' --inpath ' + inpath + ' --outpath ' + outpath + ' ;'

        cmd+= ' time python doCorrection.py \
                --ptLow ' + str(pTBin[0]) + ' --ptHigh ' + str(pTBin[1]) \
            + ' --etaLow '  + str(etaLow) + ' --etaHigh ' + str(etaHigh) \
            + ' --fs mu --doLambda1 --lambdas 1 1 ' \
            + ' --inpath ' + inpath + ' --outpath ' + outpath + ' &'

        call(cmd, shell=True)
              

inpath = '/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/'
outpath = '/home/mhl/public_html/2016/20161125_mass/test/'

doMuonCorrection(inpath, outpath)
