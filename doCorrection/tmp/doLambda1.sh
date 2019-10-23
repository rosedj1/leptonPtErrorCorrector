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

#time python getLambda1_doBoth.py --ptLow 7 --ptHigh 100 --etaLow 0.9 --etaHigh 1.8 --fs mu --debug 0 --getPara 1 --getLambda 0 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/" --inputDir "/raid/raid8/ferrico/HZZ4l/CMSSW_10_2_5/src/leptonPtErrorCorrector/makeSlimTree/output/DY_2018/" --inputFileName "DYJetsToLL_M-50_kalman_v4_m2mu_v2.root" 
#time ipython -i getLambda1_doBoth.py -- --ptLow 7 --ptHigh 100 --etaLow 0.9 --etaHigh 1.8 --fs mu --debug 0 --getPara 0 --getLambda 1 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/" --inputDir "/raid/raid8/ferrico/HZZ4l/CMSSW_10_2_5/src/leptonPtErrorCorrector/makeSlimTree/output/DY_2018/" --inputFileName "DYJetsToLL_M-50_kalman_v4_m2mu_v2.root" 

############################################
# Skimming Filippo's 2018 Madgraph samples #
############################################
# MUONS
#_____ Getting parameters _____#
#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --etaLow 0.0 --etaHigh 0.9 --fs mu --debug 0 --getPara 1 --getLambda 0 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/ZpeakFit_GetLambda/" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/Skimmed_NTuples/" --inputFileName "2018_m2mu.root" 
#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --etaLow 0.9 --etaHigh 1.8 --fs mu --debug 0 --getPara 1 --getLambda 0 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/ZpeakFit_GetLambda/" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/Skimmed_NTuples/" --inputFileName "2018_m2mu.root" 
#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --etaLow 1.8 --etaHigh 2.4 --fs mu --debug 0 --getPara 1 --getLambda 0 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/ZpeakFit_GetLambda/" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/Skimmed_NTuples/" --inputFileName "2018_m2mu.root" 

#_____ Getting lambda correction factors _____#
#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --etaLow 0.0 --etaHigh 0.9 --fs mu --debug 0 --getPara 0 --getLambda 1 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/ZpeakFit_GetLambda/" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/Skimmed_NTuples/" --inputFileName "2018_m2mu.root" 
#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --etaLow 0.9 --etaHigh 1.8 --fs mu --debug 0 --getPara 0 --getLambda 1 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/ZpeakFit_GetLambda/" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/Skimmed_NTuples/" --inputFileName "2018_m2mu.root" 
#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --etaLow 1.8 --etaHigh 2.4 --fs mu --debug 0 --getPara 0 --getLambda 1 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/ZpeakFit_GetLambda/" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/Skimmed_NTuples/" --inputFileName "2018_m2mu.root" 

# Possible strings for e_regions:
#e_region_dict = {                                                                    
#    'ECAL_barrel_pterrlow_a': {'eta_min':0.0,  'eta_max':0.8,  'rel_pTErr':'< 0.03'},
#    'ECAL_barrel_pterrlow_b': {'eta_min':0.8,  'eta_max':1.0,  'rel_pTErr':'< 0.03'},
#    'ECAL_barrel_pterrhigh' : {'eta_min':0.0,  'eta_max':1.0,  'rel_pTErr':'> 0.03'},
#    'ECAL_endcap_pterrlow_a': {'eta_min':1.0,  'eta_max':1.2,  'rel_pTErr':'< 0.07'},
#    'ECAL_endcap_pterrlow_b': {'eta_min':1.2,  'eta_max':1.44, 'rel_pTErr':'< 0.07'},
#    'ECAL_endcap_pterrlow_c': {'eta_min':1.44, 'eta_max':1.57, 'rel_pTErr':'< 0.07'},
#    'ECAL_endcap_pterrlow_d': {'eta_min':1.57, 'eta_max':2.0,  'rel_pTErr':'< 0.07'},
#    'ECAL_endcap_pterrlow_e': {'eta_min':2.0,  'eta_max':2.5,  'rel_pTErr':'< 0.07'},
#    'ECAL_endcap_pterrhigh' : {'eta_min':1.0,  'eta_max':1.2,  'rel_pTErr':'> 0.07'},
#    'Tracker_barrel'        : {'eta_min':0.0,  'eta_max':1.44, 'rel_pTErr':'> -1.0'},
#    'Tracker_endcap_a'      : {'eta_min':1.44, 'eta_max':1.6,  'rel_pTErr':'> -1.0'},
#    'Tracker_endcap_b'      : {'eta_min':1.6,  'eta_max':2.0,  'rel_pTErr':'> -1.0'},
#    'Tracker_endcap_c'      : {'eta_min':2.0,  'eta_max':2.5,  'rel_pTErr':'> -1.0'},

# Useful kinem_bins:
### all_e_regions
### all_mu_regions

# Modes:
### getPara, getLambda, getParaAndLambda

# ECAL ELECTRONS
#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --etaLow 0.8 --etaHigh 1.0 --fs e --debug 0 --e_region "ECAL_barrel_pterrhigh" --getPara 0 --getLambda 1 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/Electron_Regions/" --inputDir "/raid/raid8/ferrico/Useful_Code_HZZ/CMSSW_10_2_15/src/Full_RunII/madgraph/" --inputFileName "DYJetsToLL_M-50_Full_RunII_madgraph_m2e_2018.root" 
#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --etaLow 0.8 --etaHigh 1.0 --fs e --debug 0 --e_region "ECAL_barrel_pterrlow_a" --getPara 0 --getLambda 1 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/2018_" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/NTuples_Skimmedwith_DYAna/" --inputFileName "2018_MC_MG5_DY_30percentoffiles_m2e.root" 

#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --fs 'e' --debug 0 --kinem_bin "ECAL_barrel_pterrlow_a" --mode 'getPara' --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/2018_TEST/" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/NTuples_Skimmedwith_DYAna/" --inputFileName "2018_MC_MG5_DY_30percentoffiles_m2e.root" 
#time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --fs e --debug 0 --kinem_bin ECAL_endcap_pterrhigh --mode getPara --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/2018_TEST/" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/NTuples_Skimmedwith_DYAna/" --inputFileName "2018_MC_MG5_DY_30percentoffiles_m2e.root" 
time python getLambda1_doEither.py --ptLow 7 --ptHigh 100 --fs e --debug 0 --kinem_bin "ECAL_endcap_pterrlow_b" "ECAL_endcap_pterrlow_c" "ECAL_endcap_pterrlow_d" "ECAL_endcap_pterrlow_e"  --mode getPara --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/2018_TEST/" --inputDir "/raid/raid7/rosedj1/Higgs/HiggsMassMeas/NTuples_Skimmedwith_DYAna/" --inputFileName "2018_MC_MG5_DY_30percentoffiles_m2e.root" 

#######################
# Interactive Session #
#######################
#time ipython -i getLambda1_doEither.py -- --ptLow 7 --ptHigh 100 --etaLow 0.0 --etaHigh 0.8 --fs e --debug 0 --e_region "ECAL_barrel_pterrlow_a" --getPara 1 --getLambda 0 --shapeParaDir "/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/shapeParameters_jake/" --outputDir "/home/rosedj1/public_html/Higgs/HiggsMassMeas/ParameterPlotsTests/" --inputDir "/raid/raid8/ferrico/Useful_Code_HZZ/CMSSW_10_2_15/src/Full_RunII/madgraph/" --inputFileName "DYJetsToLL_M-50_Full_RunII_madgraph_m2e_2018.root" 
