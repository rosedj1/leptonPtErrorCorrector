#data
#time python getLambda1.py --ptLow 40 --ptHigh 50 --etaLow 0 --etaHigh 0.7 --fs e  --isData &
#time python getLambda1.py --ptLow 40 --ptHigh 50 --etaLow 0 --etaHigh 0.9 --fs mu --isData &
#dy mc
#time python getLambda1.py --ptLow 40 --ptHigh 50 --etaLow 0 --etaHigh 0.7 --fs e  &
#time python getLambda1.py --ptLow 40 --ptHigh 50 --etaLow 0 --etaHigh 0.9 --fs mu &

#time python getLambda1.py --ptLow 5 --ptHigh 100 --etaLow 0 --etaHigh 0.9 --fs mu &
#time python getLambda1.py --ptLow 5 --ptHigh 100 --etaLow 0.9 --etaHigh 1.8 --fs mu &
#time python getLambda1.py --ptLow 5 --ptHigh 100 --etaLow 1.8 --etaHigh 2.4 --fs mu &

#time python getLambda1_doPara.py --ptLow 7 --ptHigh 100 --etaLow 0 --etaHigh 1 --fs e 
#time python getLambda1_doLambda.py --ptLow 7 --ptHigh 100 --etaLow 0 --etaHigh 1 --fs e &

#time python getLambda1_doPara.py --ptLow 7 --ptHigh 100 --etaLow 1 --etaHigh 1.44 --fs e &
#time python getLambda1_doPara.py --ptLow 7 --ptHigh 100 --etaLow 1.44 --etaHigh 2 --fs e &
#time python getLambda1.py --ptLow 7 --ptHigh 100 --etaLow 1.57 --etaHigh 2 --fs e &
#time python getLambda1_doPara.py --ptLow 7 --ptHigh 100 --etaLow 2 --etaHigh 2.5 --fs e &

#time python getLambda1_doLambda.py --ptLow 7 --ptHigh 100 --etaLow 1 --etaHigh 1.44 --fs e &
#time python getLambda1_doLambda.py --ptLow 7 --ptHigh 100 --etaLow 1.44 --etaHigh 2 --fs e &
#time python getLambda1.py --ptLow 7 --ptHigh 100 --etaLow 1.57 --etaHigh 2 --fs e &
#time python getLambda1_doLambda.py --ptLow 7 --ptHigh 100 --etaLow 2 --etaHigh 2.5 --fs e &

### Jake's stuff below
#time python getLambda1_doPara.py --ptLow 7 --ptHigh 100 --etaLow 0.0 --etaHigh 0.9 --fs mu 
#time python getLambda1_doLambda.py --ptLow 7 --ptHigh 100 --etaLow 0.0 --etaHigh 0.9 --fs mu &

# Tracker electrons


#time python getLambda1_doPara.py --ptLow 10 --ptHigh 100 --etaLow 0.0 --etaHigh 0.9 --fs e \
#    --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/" \
#    --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/" \
#    --inputDir "/raid/raid8/ferrico/HZZ4l/CMSSW_10_2_5/src/leptonPtErrorCorrector/makeSlimTree/output/DY_2018/" \
#    --inputFileName "DYJetsToLL_M-50_kalman_v4_m2e_v2.root" 

#--fileName "DYJetsToLL_M-50_kalman_v4_m2e_v2.root"
time python getLambda1_doLambda.py --ptLow 7 --ptHigh 100 --etaLow 0.0 --etaHigh 0.9 --fs e --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/" --inputDir "/raid/raid8/ferrico/HZZ4l/CMSSW_10_2_5/src/leptonPtErrorCorrector/makeSlimTree/output/DY_2018/" --inputFileName "DYJetsToLL_M-50_kalman_v4_m2e_v2.root" 
