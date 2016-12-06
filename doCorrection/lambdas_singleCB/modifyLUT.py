from ROOT import *
from array import array
from math import sqrt
from subprocess import call

import argparse
def ParseOption():

    parser = argparse.ArgumentParser(description='submit all')
    parser.add_argument('--inFile', dest='inFile', type=str, help='input LUT')
#    parser.add_argument('-outFile', dest='outFile', type=str, help='output LUT')
    parser.add_argument('--fs', dest='fs', type=str, help='fs')

    args = parser.parse_args()
    return args

args=ParseOption()


fileIn = args.inFile
fileTmp = "tmpLUT.root"

#fs = '2mu'
fs = args.fs

f1 = TFile(fileIn)
f2 = TFile(fileTmp, "RECREATE")

h1 = f1.Get(fs)
h2 = h1.Clone()

f2.cd()

h2.SetBinContent(1,5,0.911)

h2.Write()
f2.Close()

call('mv ' + fileTmp + ' ' + fileIn, shell=True)
