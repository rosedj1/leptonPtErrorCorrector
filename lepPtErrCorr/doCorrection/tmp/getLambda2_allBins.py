from subprocess import call

pTs = [10, 40, 50, 100]
etas = [0, 0.7, 1.5]

##DY MC
#lambda1_pre = 1.119
##DATA
lambda1_pre = 1.156

fs = 'e'

for i in range(len(pTs)-1):
    for j in range(len(etas)-1):

        ptLow = pTs[i]
        ptHigh = pTs[i+1]
        etaLow = etas[j]
        etaHigh = etas[j+1]

        binRange = '--ptLow ' + str(ptLow) + ' --ptHigh ' + str(ptHigh) + ' --etaLow ' + str(etaLow) + ' --etaHigh ' + str(etaHigh)
#        call('python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' &', shell=True)
#        print 'python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' &'
        call('python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' --isData &', shell=True)
        print 'python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' --isData &'

extraBins = [[10,100,1.5,1.6],[10,100,1.6,2.5]]

for bin in extraBins:

    ptLow = bin[0]
    ptHigh = bin[1]
    etaLow = bin[2]
    etaHigh = bin[3]

    binRange = '--ptLow ' + str(ptLow) + ' --ptHigh ' + str(ptHigh) + ' --etaLow ' + str(etaLow) + ' --etaHigh ' + str(etaHigh)
#    call('python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' &', shell=True)
#    print 'python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' &'
    call('python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' --isData &', shell=True)
    print 'python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' --isData &'

pTs = [10, 40, 50, 100]
etas = [0, 0.9, 1.2, 2.4]

##DY MC
#lambda1_pre = 1.230
##DATA
lambda1_pre = 0.9903

fs = 'mu'

for i in range(len(pTs)-1):
    for j in range(len(etas)-1):

        ptLow = pTs[i]
        ptHigh = pTs[i+1]
        etaLow = etas[j]
        etaHigh = etas[j+1]

        binRange = '--ptLow ' + str(ptLow) + ' --ptHigh ' + str(ptHigh) + ' --etaLow ' + str(etaLow) + ' --etaHigh ' + str(etaHigh)
#        call('python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' &', shell=True)
#        print 'python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' &'
        call('python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' --isData &', shell=True)
        print 'python getLambda2.py ' + binRange +  ' --lambda1_pre ' + str(lambda1_pre) + ' --fs ' + fs + ' --isData &'

