cp DY*root /raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/HZZ4L_Mass/macro_13TeV_KinZfitter_mZ
cp DY*root /cms/data/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/Ana_ZZ4L/KinZfitter
cd /cms/data/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/CMSSW_8_0_10/src
eval `scramv1 runtime -sh`
cd /cms/data/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/Ana_ZZ4L/KinZfitter
./make.sh
cd ..
make clean
make
#python run80XAnaZZ4L.py
cd /raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_2015MC/HZZ4L_Mass/macro_13TeV_KinZfitter_mZ
./doClousre.sh
#echo "closure plot done" > exp.log
