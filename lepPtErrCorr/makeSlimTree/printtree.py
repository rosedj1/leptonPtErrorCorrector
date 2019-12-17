from ROOT import *

f1 = TFile("inputRootBeforeSkim/DYJetsToLL_M-50_kalman_v4.root")
t1 = f1.Get("Ana/passedEvents")

counter = 0

for i in range(t1.GetEntries()):
    t1.GetEntry(i)
    if len(t1.GENZ_mass) > 1:
       counter+=1

print counter
