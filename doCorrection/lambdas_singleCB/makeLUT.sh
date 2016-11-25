cd /cms/data/scratch/osg/mhl/Run2/HZZ4L/PereventMassErrCorr_2016ICHEP/CMSSW_8_0_10/src
eval `scramv1 runtime -sh`

cd -
python makeLUT_mu.py --savePath "/home/mhl/public_html/2016/20161124_mass/test/"
#python makeLUT_e.py --savePath "/home/mhl/public_html/2016/20161020_mass/"

cp *root /raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/packages/liteUFHZZ4LAnalyzer/KinZfitter
cd /raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/HiggsMass_HZZ4L/packages/liteUFHZZ4LAnalyzer/KinZfitter
./make.sh

cd ..
make

python run80XAnaZZ4L.py
