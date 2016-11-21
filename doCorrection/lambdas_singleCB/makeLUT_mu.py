from ROOT import *
from array import array

import argparse

def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--isData', dest='isData', action="store_true", default=False)
    parser.add_argument('--savePath', dest='savePath', type=str, default=False)

    args = parser.parse_args()
    return args

def getLambda2(txtName):
    data1 = [line.strip() for line in open(txtName+".txt", 'r')]
    lambda2 = (data1[-1].split(":"))[-1]
    return float(lambda2)

args=ParseOption()

savePath = args.savePath #"/home/mhl/public_html/2016/20160926_mass/"

if args.isData:
   file1 = "DoubleLepton_m2muLUT_m2mu.root"
else:
   file1 = "DYJetsToLL_M-50_m2muLUT_m2mu.root"

f1 = TFile(file1, "RECREATE")
f1.cd()
fs = 'mu'

Binx = [10, 100]
Biny = [0, 0.9, 1.8, 2.4]
binx,biny = array('f'),array('f')

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
# 
        if args.isData:
           txtName = "Data_Pt_" + pTLow + "_to_" + pTHigh + "_Eta_" + etaLow + "_to_" + etaHigh + "_" + fs
        else:
           txtName = "DY_Pt_" + pTLow + "_to_" + pTHigh + "_Eta_" + etaLow + "_to_" + etaHigh + "_" + fs

#        print i,j, txtName, getLambda2(txtName)

#        LUT.SetBinContent(i+1,j+1,getLambda2(txtName))

#LUT.SetBinContent(1,1,1.18)
#LUT.SetBinContent(1,2,1.262)
#LUT.SetBinContent(1,3,1.069)

#LUT.SetBinContent(1,1,1.131)
#LUT.SetBinContent(1,2,1.192)
#LUT.SetBinContent(1,3,1.039)

LUT.SetBinContent(1,1,1.220)
LUT.SetBinContent(1,2,1.284)
LUT.SetBinContent(1,3,1.051)

c1 = TCanvas("c1","",800,800)
LUT.Draw("text")
c1.SaveAs(savePath+"LUT_"+fs+".png")
LUT.Write()
f1.Close()
        
