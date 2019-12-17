from ROOT import *
from array import array
import argparse
from leptonPtErrorCorrector.doCorrection.tmp.kinem_bins import kinem_bin_dict
from PyUtils.fileUtils import copyFile, makeDirs

gROOT.SetBatch(kTRUE)

def ParseOption():
    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--isData', dest='isData', action="store_true", default=False)
    parser.add_argument('--savePath', dest='savePath', type=str, default=False, help='Storage path of LUT.')  # 
    args = parser.parse_args()
    return args

def getLambda2(txtName):
    data1 = [line.strip() for line in open(txtName+".txt", 'r')]
    lambda2 = (data1[-1].split(":"))[-1]
    return float(lambda2)

args=ParseOption()
savePath = args.savePath #"/home/mhl/public_html/2016/20160926_mass/"
copyFile("/home/rosedj1/","index.php",savePath)

if args.isData:
   file1 = "DoubleLepton_m2eLUT_m2e.root"
else:
   file1 = "DYJetsToLL_M-50_m2eLUT_m2e.root"

f1 = TFile(file1, "RECREATE")
f1.cd()
fs = 'e'

Binx = [7, 100]
#Biny = [0, 0.7, 1, 1.5, 2.5]
# FIXME: Use the kinem_bin[each key['eta_min']] to automate this.
Biny = [0, 0.8, 1, 1.2, 1.44, 1.57, 2, 2.5]
binx = array('f')
biny = array('f')

for i in range(len(Binx)):
    binx.append(Binx[i])
for i in range(len(Biny)):
    biny.append(Biny[i])

LUT = TH2F("2"+fs, "2"+fs, len(binx)-1, binx, len(biny)-1, biny)

for i in range(len(binx)-1):
    for j in range(len(biny)-1):

        pTLow = str(round(Binx[i],1))
        pTHigh = str(round(Binx[i+1],1))
        etaLow = str(round(Biny[j],1))
        etaHigh = str(round(Biny[j+1],1))

#        if float(etaLow) >= 1.5:
#           pTLow = str(round(10.0, 1))
#           pTHigh = str(round(100.0, 1))

#        txtName = "DY_Pt_" + pTLow + "_to_" + pTHigh + "_Eta_" + etaLow + "_to_" + etaHigh + "_" + fs
        if args.isData:
           txtName = "Data_Pt_" + pTLow + "_to_" + pTHigh + "_Eta_" + etaLow + "_to_" + etaHigh + "_" + fs
        else:
           txtName = "DY_Pt_" + pTLow + "_to_" + pTHigh + "_Eta_" + etaLow + "_to_" + etaHigh + "_" + fs + "_jaketest"
#        print i,j, txtName, getLambda2(txtName)
#        LUT.SetBinContent(i+1,j+1,getLambda2(txtName))

#LUT.SetBinContent(1,1,1.245)
#LUT.SetBinContent(1,2,1.140)
#LUT.SetBinContent(1,3,1.070)
#LUT.SetBinContent(1,4,1.178)

# FIXME: Use an enumerate function and loop over kinem_bin_dict.keys(). 
# May not be able to since dictionaries are not ordered! 
LUT.SetBinContent(1,1, kinem_bin_dict['ECAL_barrel_pterrlow_a']['pterrcorrfactor'] )
LUT.SetBinContent(1,2, kinem_bin_dict['ECAL_barrel_pterrlow_b']['pterrcorrfactor'] )
#LUT.SetBinContent(1,3, kinem_bin_dict['ECAL_barrel_pterrhigh' ]['pterrcorrfactor'] )
LUT.SetBinContent(1,3, kinem_bin_dict['ECAL_endcap_pterrlow_a']['pterrcorrfactor'] )
LUT.SetBinContent(1,4, kinem_bin_dict['ECAL_endcap_pterrlow_b']['pterrcorrfactor'] )
LUT.SetBinContent(1,5, kinem_bin_dict['ECAL_endcap_pterrlow_c']['pterrcorrfactor'] )
LUT.SetBinContent(1,6, kinem_bin_dict['ECAL_endcap_pterrlow_d']['pterrcorrfactor'] )
LUT.SetBinContent(1,7, kinem_bin_dict['ECAL_endcap_pterrlow_e']['pterrcorrfactor'] )
#LUT.SetBinContent(1,9, kinem_bin_dict['ECAL_endcap_pterrhigh' ]['pterrcorrfactor'] )

c1 = TCanvas("c1","",800,800)

LUT.Draw("text")
c1.SaveAs(savePath+"LUT_"+fs+".png")

LUT.Write()
f1.Close()
