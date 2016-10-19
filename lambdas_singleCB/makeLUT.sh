cd /cms/data/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/CMSSW_8_0_10/src
eval `scramv1 runtime -sh`

cd -
python makeLUT_mu.py --savePath "/home/mhl/public_html/2016/20161006_2015MCebeCorrection/"
python makeLUT_e.py --savePath "/home/mhl/public_html/2016/20161006_2015MCebeCorrection/"
