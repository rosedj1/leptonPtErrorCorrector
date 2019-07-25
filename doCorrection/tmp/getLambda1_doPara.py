from leptonPtErrorCorrector.doCorrection.pTErrCorrector import GetCorrection
from PyUtils.fileUtils import copyFile, makeDirs
import argparse, sys

#____________________________________________________________________________________________________
### AUTOMATIC STUFF
def ParseOption():
    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--ptLow', dest='ptLow', type=float)
    parser.add_argument('--ptHigh', dest='ptHigh', type=float)
    parser.add_argument('--etaLow', dest='etaLow', type=float)
    parser.add_argument('--etaHigh', dest='etaHigh', type=float)
    parser.add_argument('--isData', dest='isData', action="store_true", default=False)
    parser.add_argument('--fs', dest='fs', type=str)
    parser.add_argument('--shapeParaDir', dest='shapeParaDir', type=str)
    parser.add_argument('--inputDir', dest='inputDir', type=str)
    parser.add_argument('--outputDir', dest='outputDir', type=str)
    parser.add_argument('--inputFileName', dest='inputFileName', type=str)
    parser.add_argument('--debug', dest='debug', type=bool)
    parser.add_argument('--getPara', dest='getPara', type=bool)
    parser.add_argument('--getLambda', dest='getLambda', type=bool)
    args = parser.parse_args()
    return args
## Make output dir
makeDirs(pathto_outputdir)
makeDirs(shapeParaDir)
copyFile("/home/rosedj1/","index.php",pathto_outputdir)
#_____________________________________________________________________________________
### MAIN
args=ParseOption()
## Flags passed in from doLambda1.sh
pTLow                   = args.ptLow
pTHigh                  = args.ptHigh
etaLow                  = args.etaLow
etaHigh                 = args.etaHigh
fs                      = args.fs
isData                  = args.isData
pathto_shapeParameters  = args.shapeParaDir
pathto_inputdir         = args.inputDir
pathto_outputdir        = args.outputDir #getLambda1/"
inputfilename           = args.inputFileName
DEBUG                   = args.debug
getPara                 = args.getPara
getLambda               = args.getLambda

binEdge = {'pTLow': pTLow, 'pTHigh':pTHigh, 'etaLow':etaLow, 'etaHigh':etaHigh}
doLambda1 = True
lambdas = {'lambda1':1, 'lambda2':1} # starting values for all lambdas
shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0} # starting values for all parameters

path = {}
path['input']    = pathto_inputdir
path['output']   = pathto_outputdir
path['filename'] = inputfilename
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"
#path['input'] = "/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_useLepFSRForMassZ/"
#path['input'] = "/raid/raid7/rosedj1/ForPeeps/ForFilippo/"
#path['output'] = "/home/mhl/public_html/2016/20161125_mass/test/" #getLambda1/"

# Get Parameters
if getPara and not getLambda:
    ### Get CB parameters
    # makes a GetCorrection object
    # shapePara starts off with all zeros
    tag = "doLambda1_getPara_" + fs
    getCorr_getPara = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag) 
    if DEBUG:
        print "Parameters of getCorr_getPara object BEFORE fit:"
        for key,val in getCorr_getPara.__dict__.items():
            print key,":",val

    # then it goes through the grind, and the parameters get updated
    getCorr_getPara.DriverGetPara()
    if DEBUG:
        print "Parameters of getCorr_getPara object AFTER fit:"
        for key,val in getCorr_getPara.__dict__.items():
            print key,":",val

    # update global shapePara dict
    shapePara = getCorr_getPara.shapePara
    with open(pathto_shapeParameters + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
    #with open('shapeParameters/' + getCorr_getPara.name.replace('.','p') + '.py', 'w') as f:
         f.write('shapePara = ' + str(shapePara) + ' \n')
    print "getLambda1_doPara.py COMPLETE\n\n"

# Get Lambda
elif getLambda and not getPara:
    tag = "doLambda1_getLambda_" + fs
    getCorr_getLambda = GetCorrection(binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag)
    #tmpPara_ =  __import__('test', globals(), locals())
    if DEBUG:
        print "Parameters of getCorr_getLambda object BEFORE __import__(getCorr_getPara):"
        for key,val in getCorr_getLambda.__dict__.items():
            print key,":",val

    ## ???
    tmpPara_ =  __import__(getCorr_getLambda.name.replace('getLambda', 'getPara').replace('.','p'), globals(), locals())
    if DEBUG:
        print "getCorr_getLambda.shapePara after __import__ and before DriverGetLambda():\n",getCorr_getLambda.shapePara
        for key,val in getCorr_getLambda.__dict__.items():
            print key,":",val
        
        print "\ntmpPara_.shapePara after __import__ and before DriverGetLambda():\n",tmpPara_.shapePara
        for key,val in getCorr_getLambda.__dict__.items():
            print key,":",val

    getCorr_getLambda.shapePara = tmpPara_.shapePara
    print "\ngetCorr_getLambda.shapePara:\n", getCorr_getLambda.shapePara

    # The big boy. This keeps the old parameters, finds sigma and lambda.
    getCorr_getLambda.DriverGetLambda()
    if DEBUG:
        print "\nParameters of getCorr_getLambda.shapePara AFTER fit:"
        for key,val in getCorr_getLambda.__dict__.items():
            print key,":",val

    print "getLambda1_doLambda COMPLETE\n\n"

else:
    print """   ERROR!!!
             Either both getPara and getLambda were specified
             at the same time, or neither was given!"""
    #sys.exit()
