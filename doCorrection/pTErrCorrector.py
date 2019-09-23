#!/bin/bash
####################################################
## PURPOSE: 
## SYNTAX:  
## NOTES:   Applies the following cuts: 60<mZ<120, 0.2<mZerr<7.2, and various pT and eta cuts
##          depending on what flags are passed to: doLambda1.sh
## AUTHOR:  Hualin Mei
## DATE:    
## UPDATED: 
## TO-DO:   Add flag for inputfilename instead of hardcoding it below
####################################################

#____________________________________________________________________________________________________
# User Parameters
import sys, os, string, re
# Probably don't need import ROOT
from ROOT import * 
from array import array
from math import *
from tdrStyle import *
from subprocess import call
RooMsgService.instance().setStreamStatus(1,False);
setTDRStyle()

gROOT.SetBatch(kTRUE)   # kTRUE will NOT draw plots to screen
# Possible strings for e_regions (NEWNAME):
## OLDNAME           NEWNAME                   ETABIN          RELPTERR      
## ECAL_region_1a:   ECAL_barrel_pterrlow_a    [0, 0.8]        rel_pTErr < 3%
## ECAL_region_1b:   ECAL_barrel_pterrlow_b    [0.8, 1.0]      rel_pTErr < 3%
##                                                                           
## ECAL_region_2:    ECAL_barrel_pterrhigh     [0, 1.0]        rel_pTErr > 3%
##                                                                           
## ECAL_region_3a:   ECAL_endcap_pterrlow_a    [1.0, 1.2]      rel_pTErr < 7%
## ECAL_region_3b:   ECAL_endcap_pterrlow_b    [1.2, 1.44]     rel_pTErr < 7%
## ECAL_region_3c:   ECAL_endcap_pterrlow_c    [1.44, 1.57]    rel_pTErr < 7%
## ECAL_region_3d:   ECAL_endcap_pterrlow_d    [1.57, 2.0]     rel_pTErr < 7%
## ECAL_region_3e:   ECAL_endcap_pterrlow_e    [2.0, 2.5]      rel_pTErr < 7%
##                                                                           
## ECAL_region_4:    ECAL_endcap_pterrhigh     [1.0, 1.2]      rel_pTErr > 7%
##                                                                           
## Tracker_region_1  Tracker_barrel            [0, 1.44]                                  
## Tracker_region_2  Tracker_endcap_a          [1.44, 1.6]                                
## Tracker_region_3  Tracker_endcap_b          [1.6, 2.0]                                 
## Tracker_region_4  Tracker_endcap_c          [2.0, 2.5]                                 

e_region_dict = {
    'ECAL_barrel_pterrlow_a': {'eta_min':0.0,  'eta_max':0.8,  'rel_pTErr':'< 0.03'},
    'ECAL_barrel_pterrlow_b': {'eta_min':0.8,  'eta_max':1.0,  'rel_pTErr':'< 0.03'},
    'ECAL_barrel_pterrhigh' : {'eta_min':0.0,  'eta_max':1.0,  'rel_pTErr':'> 0.03'},
    'ECAL_endcap_pterrlow_a': {'eta_min':1.0,  'eta_max':1.2,  'rel_pTErr':'< 0.07'},
    'ECAL_endcap_pterrlow_b': {'eta_min':1.2,  'eta_max':1.44, 'rel_pTErr':'< 0.07'},
    'ECAL_endcap_pterrlow_c': {'eta_min':1.44, 'eta_max':1.57, 'rel_pTErr':'< 0.07'},
    'ECAL_endcap_pterrlow_d': {'eta_min':1.57, 'eta_max':2.0,  'rel_pTErr':'< 0.07'},
    'ECAL_endcap_pterrlow_e': {'eta_min':2.0,  'eta_max':2.5,  'rel_pTErr':'< 0.07'},
    'ECAL_endcap_pterrhigh' : {'eta_min':1.0,  'eta_max':1.2,  'rel_pTErr':'> 0.07'},
    'Tracker_barrel'        : {'eta_min':0.0,  'eta_max':1.44, 'rel_pTErr':'> -1.0'},
    'Tracker_endcap_a'      : {'eta_min':1.44, 'eta_max':1.6,  'rel_pTErr':'> -1.0'},
    'Tracker_endcap_b'      : {'eta_min':1.6,  'eta_max':2.0,  'rel_pTErr':'> -1.0'},
    'Tracker_endcap_c'      : {'eta_min':2.0,  'eta_max':2.5,  'rel_pTErr':'> -1.0'},
}

class GetCorrection():

      #def __init__(self, binEdge, isData, fs, doLambda1, lambdas, shapePara, paths, tag):
      def __init__(self, binEdge, isData, fs, doLambda1, lambdas, shapePara, paths, tag, e_region=''):
          """
          ARGUMENTS:
            binEdge   =  {pTLow:<> ,pTHigh:<>, etaLow:<>, etaHigh:<>}
            isData    = bool
            fs        = 'e' or 'mu'
            doLambda1 = bool. 
                If True: 
                    Use binEdge values, else use hardcoded binEdge values below.
                    Apply pT and eta cuts to lep1 and lep2 assuming they are in SAME BIN.
                    MySelector.C will use massZErr values originally in "massZErr" branch of skimmed NTuple.
                    doLambda==True: leptons in same bin! lep1 and lep2 both in bin1 (eta_1st vals)
                If False: 
                    MySelector.C will calculate a new massZErr based off of varying the pT of each lep individually.
                    doLambda==False: leptons in different bins! (lep1 in bin1 and lep2 in bin2) or (lep1 in bin2 and lep2 in bin1)
            lambdas   = {'lambda1':1, 'lambda2':1}
            shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0}
            paths     = {'input':<input_DIR_to_NTuple>, 'output':<output_DIR>}
            tag       = "doLambda1_getPara_" + fs
          """

          # Hard-coded parameters
          self.massZ_lo = 60
          self.massZ_hi = 120
          self.massZErr_lo = 0.2 # Not sure why this value
          self.massZErr_hi = 7.2 # Not sure why this value
          self.GENZ_mean = 91.19
          self.GENZ_width = 2.44

          self.selectors = {}

          self.doLambda1 = doLambda1 
          if not self.doLambda1:
             # doLambda1 == False in getLambda2_doPara.py
             # leptons in different bins!
             self.pTLow_1st   = binEdge['pTLow']
             self.pTHigh_1st  = binEdge['pTHigh']
             self.etaLow_1st  = binEdge['etaLow']
             self.etaHigh_1st = binEdge['etaHigh']
#          if not self.doLambda1:
#             self.pTLow_1st = doLambda1[1]['pTLow']
#             self.pTHigh_1st = doLambda1[1]['pTHigh']
#             self.etaLow_1st = doLambda1[1]['etaLow']
#             self.etaHigh_1st = doLambda1[1]['etaHigh']
          # pT cuts for bin1, both leps in bin1
          if doLambda1:
              self.pTLow_1st = binEdge['pTLow']
              self.pTHigh_1st = binEdge['pTHigh']
              self.etaLow_1st = binEdge['etaLow']
              self.etaHigh_1st = binEdge['etaHigh']
          # I don't think the dictionary below follows the structure of the rest of the code
          # Therefore, commented out!
          #else:
          #    self.pTLow_1st = {'e': 7, 'mu': 40}
          #    self.pTHigh_1st = {'e': 100, 'mu': 50}
          #    self.etaLow_1st = {'e': 0, 'mu': 0}
          #    self.etaHigh_1st = {'e': 1, 'mu': 0.9}

          # pT cuts for bin2
          self.pTLow = binEdge['pTLow']
          self.pTHigh = binEdge['pTHigh']
          self.etaLow = binEdge['etaLow']
          self.etaHigh = binEdge['etaHigh']

          # Lambdas is a dictionary of the original lambdas (which all start off at 1)
          self.Lambdas = lambdas
          self.Lambdas = {'lambda1': lambdas['lambda1'],
                          'lambda2': lambdas['lambda2'],
                          'lambda': 1}
          #self.Lambdas.update({'lambda': 1}) # this should work but I dont' want to test it yet

          self.fs = fs
          #cut to make dataset
          self.cut = " (massZ > "+str(self.massZ_lo)+" && massZ < "+str(self.massZ_hi)+") && "
          self.cut += " (massZErr > "+str(self.massZErr_lo)+" && massZErr < "+str(self.massZErr_hi)+") && "
          # Appends more cuts to lepton selection, like pT cuts and eta cuts
          self.doLambdaCut() # doLambda1Cut or doLambda2Cut

          #tree to get information
#          self.filename = "DYJetsToLL_M-50_m2" + self.fs + ".root"
          self.filename = paths['filename'] # passed in from getLambda1_doPara.py
          #self.filename = "DYJetsToLL_M-50_kalman_v4_m2" + self.fs + "_v2.root"
          if isData:
             self.filename = "DoubleLepton_m2" + self.fs + ".root"
#          self.treeFile = TFile("../inputRootFiles/"+self.filename)
#          self.treeFile = TFile("/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"+self.filename)
          self.treeFile = TFile(paths['input']+self.filename)
          self.tree = self.treeFile.Get("passedEvents")
          print 'tree opened'

          # Save
          self.outpath = paths['output']
          self.name = (self.filename.split('.'))[0]
          if self.doLambda1:
             self.name += "_Pt_" + str(self.pTLow_1st)  + "_to_" + str(self.pTHigh_1st) + "_Eta_" + str(self.etaLow_1st) + "_to_" + str(self.etaHigh_1st)
          else:
             self.name += "_Pt_" + str(self.pTLow)  + "_to_" + str(self.pTHigh) + "_Eta_" + str(self.etaLow) + "_to_" + str(self.etaHigh)

          # tag     = "doLambda1_getPara_" + fs
          self.name += "_" + tag
          self.tag = tag

          # Initial shape parameters
          # shapePara = {"mean":0, "alpha":0, "n":0, "tau":0, "fsig":0}
          self.shapePara = shapePara
          self.w = RooWorkspace("w","workspace")

          # Make a couple dataset objects and a histogram object to store data
          self.Data_Zlls = RooDataSet()
          self.Data_Zlls_w = RooDataSet()
          self.Data_Zlls_binned = RooDataHist()
#          self.DataHist = TH2F()
 
          # Holds the input and output of a PDF fit to a dataset
          self.rFit = RooFitResult() 


#____________________________________________________________________________________________________
      def PrepareDataset(self):

#          massZ = RooRealVar("massZ","massZ", self.massZ_lo, self.massZ_hi)
#          massZErr = RooRealVar("massZErr","massZErr", self.massZErr_lo, self.massZErr_hi)

          # At this point, full cuts are applied: mZ, pT1, pT2, eta1, eta2
          cut = self.cut
          self.tree.Draw(">>myList", cut, "entrylist")
          entryList = gDirectory.Get("myList")
          # Not sure what the entryList is for yet...
          # I think it has something to do with PROOF and parallel processing
          self.tree.SetEntryList(entryList) 

          # Make and prepare selector object.
          selector = TSelector.GetSelector("/home/rosedj1/HiggsMeasurement/CMSSW_8_0_32/src/leptonPtErrorCorrector/doCorrection/MySelector.C")
          # These variables are defined in MySelector.C 
          selector.SetRange_massZ(self.massZ_lo, self.massZ_hi) # hard-coded above as [60-120] GeV
          selector.SetRange_massZErr(self.massZErr_lo, self.massZErr_hi) # hard-coded above as [0.2-7.0] GeV
          selector.SetLambda( int(self.doLambda1), self.Lambdas["lambda1"], self.Lambdas["lambda2"] )

# These variables are from MySelector.h. Putting them here for easy reference. 
#   rv_weight   = new RooRealVar("weight","weight", 0.00001, 100);
#   rv_massZ    = new RooRealVar("massZ","massZ", massZ_lo, massZ_hi);
#   rv_massZErr = new RooRealVar("massZErr","massZErr", massZErr_lo, massZErr_hi);
#   rastmp      = new RooArgSet(*rv_massZ, *rv_massZErr, *rv_weight);
#   Data_Zlls   = new RooDataSet("Zlls","Zlls", *rastmp);

          # This is the big boy: run the Process method.
          # Go event by event in the tree and grab the massZ (from the massZ branch) 
          # and the weight from the weight branch.
          # if doLambda1==True: use the massZErr from the massZErr branch. 
          # Else: calculate a new one by varying pT of leps
          self.tree.Process(selector)

          self.Data_Zlls = selector.Data_Zlls # Store the values in a RooDataSet called Data_Zlls
          # Use Data_Zlls dataset to make a new dataset of WEIGHTS? 
          self.Data_Zlls_w = RooDataSet(self.Data_Zlls.GetName(), self.Data_Zlls.GetTitle(), self.Data_Zlls, self.Data_Zlls.get(), "1", "weight")
          print "original RooDataSet has " + str(self.Data_Zlls.numEntries()) + " events"
          print "copied RooDataSet has " + str(self.Data_Zlls_w.numEntries()) + " events"
          print "The cuts used are:\n", self.cut
          self.Data_Zlls_binned = self.Data_Zlls_w.binnedClone()

#____________________________________________________________________________________________________
      def MakeModel_getPara(self):
          """
          Creates the different PDFs (BW, CB) and then creates the model (convolution of CBxBW, exp bkg, and fsig).
          """
          # Variables
          massZ             = RooRealVar("massZ","massZ", self.massZ_lo, self.massZ_hi)
          massZErr          = RooRealVar("massZErr","massZErr", self.massZErr_lo, self.massZErr_hi)

          # BreitWigner
          breitWignerMean   = RooRealVar("breitWignerMean", "m_{Z^{0}}", self.GENZ_mean)
          breitWignerGamma  = RooRealVar("breitWignerGamma", "#Gamma", self.GENZ_width)
          breitWignerGamma.setConstant(kTRUE)
          breitWignerMean.setConstant(kTRUE)
          BW = RooBreitWigner("BW","Breit Wigner theory", massZ, breitWignerMean,breitWignerGamma)

          # Crystal Ball
          mean  = RooRealVar("mean","mean", 0, -1, 1)
          sigma = RooRealVar("sigma", "sigma", 1, 0, 15)
          alpha = RooRealVar("alpha","alpha", 1, 0, 10)
          n     = RooRealVar("n","n", 5, 0, 30)
          #alpha2 = RooRealVar("alpha2","alpha2", 1.2, 0, 50)
          #n2 = RooRealVar("n2","n2", 15, 0.1, 50)
          CB = RooCBShape("CB","CB", massZ, mean, sigma, alpha, n)
          #CB = RooDoubleCB("CB","CB", massZ, mean, sigma, alpha, n, alpha2, n2)
          
          # bkg
          tau = RooRealVar("tau","tau",  -1, 1)
          #pa1 = RooRealVar("pa1","pa1", -0.08, -10,10)
          #pa2 = RooRealVar("pa2","pa2", 0.0098, -10,10)
          #p2 = RooFormulaVar("p2", "@1*@0+@2*@0*@0",RooArgList(massZ,pa1,pa2)) # may not be used

#          bkg = RooExponential("bkg","bkg", p2, tau)
          bkg = RooExponential("bkg","bkg", massZ, tau)

          # fsig
          fsig = RooRealVar("fsig","signal fraction", 0.7, 0.5, 1) # hard-coded fsig?

          #GENZ shape convoluted with crystal ball
#          CBxBW = RooFFTConvPdf("CBxBW","CBxBW", massZ, rhp_genzm, CB)
          CBxBW = RooFFTConvPdf("CBxBW","CBxBW", massZ, BW, CB)

          model = RooAddPdf("model","model", CBxBW, bkg, fsig)
          getattr(self.w,'import')(model) # same as doing: object.attribute

#____________________________________________________________________________________________________
      def MakeModel_getLambda(self):
          """
          Creates the different PDFs (BW, CB). 
          The mean, alpha, and n, from the previous CB are fixed here. Same for tau of exp bkg.
          Sigma is set to massZErr*lambda.
          Creates the model (convolution of CBxBW, exp bkg, and fsig).
          """
          # Variables
          massZ = RooRealVar("massZ","massZ", self.massZ_lo, self.massZ_hi)
          massZErr = RooRealVar("massZErr","massZErr", self.massZErr_lo, self.massZErr_hi)
#          massZ.setBins(1000,"cache")
#          massZ.setMin("cache",50.5) 
#          massZ.setMax("cache",130.5) ;

          # BreitWigner
          breitWignerMean = RooRealVar("breitWignerMean", "m_{Z^{0}}", self.GENZ_mean)
          breitWignerGamma = RooRealVar("breitWignerGamma", "#Gamma", self.GENZ_width)
          breitWignerGamma.setConstant(kTRUE)
          breitWignerMean.setConstant(kTRUE)
          BW = RooBreitWigner("BW","Breit Wigner theory", massZ, breitWignerMean,breitWignerGamma)
#           so far identical to MakeModel_getPara

          # Crystal Ball
          print "\nCalling MakeModel_getLambda."
          print "Fixed parameters going into CB:"
          for key,val in self.shapePara.items():
              print key,":",val
          lambda_   = RooRealVar("lambda","lambda", 1, 0.1, 5.0)     # Start at lambda = 1
          mean      = RooRealVar("mean","mean", self.shapePara["mean"]) # THIS IS WHERE THINGS ARE DIFFERENT
          alpha     = RooRealVar("alpha","alpha", self.shapePara["alpha"])
          n         = RooRealVar("n","n", self.shapePara["n"])
          sigma     = RooFormulaVar("sigma","@1*@0", RooArgList(lambda_,  massZErr))
          CB        = RooCBShape("CB","CB", massZ, mean, sigma, alpha, n)
#         alpha2 = RooRealVar("alpha2","alpha2", self.shapePara["alpha2"])
#         n2 = RooRealVar("n2","n2", self.shapePara["n2"])
#          sigma = RooFormulaVar("sigma","@1*(1+@2/@1*@0)", RooArgList(lambda_, massZ, massZErr))
#          CB = RooDoubleCB("CB","CB", massZ, mean, sigma, alpha, n, alpha2, n2)
#          GENZ shape convoluted with crystal ball
#          rdh_genzm = RooDataHist("rdh_genzm","rdh_genzm", RooArgList(massZ), self.hgenzm)
#          rhp_genzm = RooHistPdf("rhp_genzm","rhp_genzm", RooArgSet(massZ), rdh_genzm)
#          CBxBW = RooFFTConvPdf("CBxBW","CBxBW", massZ, rhp_genzm, CB)

          CBxBW     = RooFFTConvPdf("CBxBW","CBxBW", massZ, BW, CB)

          # Exponential Background
          tau = RooRealVar("tau","tau", self.shapePara["tau"])
          bkg = RooExponential("bkg","bkg", massZ, tau)
#          pa1 = RooRealVar("pa1","pa1", self.shapePara["pa1"])
#          pa2 = RooRealVar("pa2","pa2", self.shapePara["pa2"])
#          p2 = RooFormulaVar("p2", "@1*@0+@2*@0*@0",RooArgList(massZ,pa1,pa2))
#          bkg = RooExponential("bkg","bkg", p2, tau)

          # Signal Fraction (fsig)
          fsig = RooRealVar("fsig","signal fraction", self.shapePara["fsig"])

          model = RooAddPdf("model","model", CBxBW, bkg, fsig)
          
          # I think this is making "model" a global variable...
          getattr(self.w,'import')(model)

#____________________________________________________________________________________________________
      def DoFit_getPara(self):

          print "Number of entries in Dat_Zlls_w:", self.Data_Zlls_w.numEntries()
          if self.Data_Zlls_w.numEntries() < 5000:
             # rFit holds the input and output of the DataSet
             # RooAbsPdf::fitTo(datatofitPDFto, )
             #???? Is this a binned or unbinned dataset?
             print "Using an UNbinned pdf model."
             self.rFit = self.w.pdf("model").fitTo( self.Data_Zlls_w, 
                                                    RooFit.Save(kTRUE), 
                                                    RooFit.SumW2Error(kTRUE), 
                                                    RooFit.PrintLevel(-1), 
                                                    RooFit.Timer(kTRUE) 
                                                    )
          else: 
             print "Using a binned pdf model."
             self.rFit = self.w.pdf("model").fitTo( self.Data_Zlls_binned, 
                                                    RooFit.Save(kTRUE), 
                                                    RooFit.SumW2Error(kTRUE), 
                                                    RooFit.PrintLevel(-1), 
                                                    RooFit.Timer(kTRUE) 
                                                    )
#____________________________________________________________________________________________________
      def DoFit_getLambda(self):

          print "Number of entries in Dat_Zlls_w:", self.Data_Zlls_w.numEntries()
          # If we are dealing with few entries, go unbinned.
          # Unbinned is in general slower, but is more accurate(?) because you are dealing with a 
          # continuous random variable after all. When you bin, you are making the fit more discrete.
          if self.Data_Zlls_w.numEntries() < 5000:
             print "Using an UNbinned fit."
             self.rFit = self.w.pdf("model").fitTo( self.Data_Zlls_w, 
                                                    RooFit.ConditionalObservables( RooArgSet(self.w.var("massZErr")) ),
                                                    RooFit.Save(kTRUE), 
                                                    RooFit.SumW2Error(kTRUE), 
                                                    RooFit.PrintLevel(-9999), 
                                                    RooFit.Timer(kTRUE) 
                                                    )
          else:
             print "Using a binned fit."
             self.rFit = self.w.pdf("model").fitTo( self.Data_Zlls_binned, 
                                                    RooFit.ConditionalObservables( RooArgSet(self.w.var("massZErr")) ),
                                                    RooFit.Save(kTRUE), 
                                                    RooFit.SumW2Error(kTRUE), 
                                                    RooFit.PrintLevel(-9999), 
                                                    RooFit.Timer(kTRUE) 
                                                    )

#____________________________________________________________________________________________________
      def AfterFit_getPara(self):
          """
          Update values in shapePara dict with newly found parameters from fit.
          """
          self.shapePara["mean"]  = self.w.var("mean").getVal()
          self.shapePara["alpha"] = self.w.var("alpha").getVal()
          self.shapePara["n"]     = self.w.var("n").getVal()
          self.shapePara["tau"] = self.w.var("tau").getVal()
          self.shapePara["fsig"] = self.w.var("fsig").getVal()
#          self.shapePara["alpha2"] = self.w.var("alpha2").getVal()
#          self.shapePara["n2"] = self.w.var("n2").getVal()
#          self.shapePara["pa1"] = self.w.var("pa1").getVal()
#          self.shapePara["pa2"] = self.w.var("pa2").getVal()

#____________________________________________________________________________________________________
      def AfterFit_getLambda(self):

          self.Lambdas["lambda"] = self.w.var("lambda").getVal()
          print "w.var('lambda').getVal() is:", self.w.var("lambda").getVal()
          #need to save lambda, pass it to lambda2, save fs, doLambda1, tag(iteration)
          saveLambda = "lambda: " + str(self.Lambdas["lambda"])
          saveLambda += ", lambda1: " + str(self.Lambdas["lambda1"])
          saveLambda += ", lambda2: " + str(self.Lambdas["lambda2"])
          saveLambda += ", lambda*lambda2: " + str(self.Lambdas["lambda"]*self.Lambdas["lambda2"])
          print "saveLambda is (iteration stuff):",saveLambda
#          call('cat "' + saveLambda + '" >> ' + self.outpath+self.name+'.txt', shell=True)

#____________________________________________________________________________________________________
      def PlotFit(self):

          # Make a plotting frame (essentially a canvas).
          PmassZ = self.w.var("massZ").frame(RooFit.Bins(100))
          PmassZ.GetXaxis().SetTitle("this is a test [GeV]")
#          PmassZ.GetXaxis().SetTitle("m_{\\ell\\ell}\\ [GeV]")
          PmassZ.GetYaxis().SetTitleOffset(1.3)

          # This adds the data to the plot.
          self.Data_Zlls_w.plotOn(PmassZ)

          self.w.pdf("model").plotOn(PmassZ, 
                                     RooFit.ProjWData(self.Data_Zlls_w, kTRUE),
                                     RooFit.LineColor(2), 
                                     RooFit.LineWidth(1) 
                                     )
          # Adds a box with parameters values to the frame.
          self.w.pdf("model").paramOn(PmassZ, 
                                      RooFit.Layout(0.17, 0.47, 0.9), 
                                      RooFit.Format("NE", RooFit.FixedPrecision(4))
                                      )

          PmassZ.getAttText().SetTextSize(0.03)
          # Perform a chi^2 test on the massZ fit
          # Also return a list of floating parameters after fit
          chi2 = PmassZ.chiSquare(self.rFit.floatParsFinal().getSize())
          dof =  self.rFit.floatParsFinal().getSize()

          # Draw the bkg function and 
          self.w.pdf("model").plotOn(PmassZ, 
                                     RooFit.Components("bkg"), 
                                     RooFit.LineStyle(kDashed)
                                     )
          self.Data_Zlls_w.plotOn(PmassZ)
          self.w.pdf("model").plotOn(PmassZ, 
                                     RooFit.ProjWData(self.Data_Zlls_w,kTRUE),
                                     RooFit.LineColor(2), 
                                     RooFit.LineWidth(1) 
                                     )

          ch = TCanvas("ch","ch",1000,800)
          ch.cd()

          PmassZ.Draw("")

          latex = TLatex()
          latex.SetNDC()
          latex.SetTextSize(0.55*ch.GetTopMargin())
          latex.SetTextFont(42)
          latex.SetTextAlign(11)

          # DrawLatex(xcoord, ycoord, "text")
          latex.DrawLatex(0.70, 0.85, "#chi^{2}/DOF = %.3f" %(chi2/dof))

          # "getLambda" is originally found in getLambda1_doLambda.py (which is "step 2")
          # Therefore, the plot only has its parameters printed after the getLambda1_doLambda.py step
          if "getLambda" in self.tag:
             latex.DrawLatex(0.70, 0.8, "#alpha = %.3f" %(self.w.var("alpha").getVal()))
             latex.DrawLatex(0.70, 0.75, "fsig = %.3f" %(self.w.var("fsig").getVal()))
             latex.DrawLatex(0.70, 0.7, "n = %.3f" %(self.w.var("n").getVal()))
#             latex.DrawLatex(0.75, 0.65, "pa1 = %.3f" %(self.w.var("pa1").getVal()))
#             latex.DrawLatex(0.75, 0.6, "pa2 = %.3f" %(self.w.var("pa2").getVal()))
#             latex.DrawLatex(0.75, 0.55, "#sigma_{CB} = %.3f" %(self.w.function("sigma").getVal()))
             latex.DrawLatex(0.70, 0.65, "#tau = %.3f" %(self.w.var("tau").getVal()))

          ch.SaveAs(self.outpath + self.name + '.png')
          ch.SaveAs(self.outpath + self.name + '.pdf')

          return PmassZ, chi2, dof, ch, latex

#___________________________________________________________________________
      def MakeSmallTree(self):

          f = TFile(self.path+self.name+".root","recreate")
          #f = TFile(self.outpath+self.name+".root","recreate")
          t = TTree( 't1', 'tree with massZZ, massZZErr, weight' )

          massZ = array( 'f', [ 0 ] )
          massZErr = array( 'f', [ 0 ] )
          weight = array( 'f', [ 0 ] )

          t.Branch( 'massZ', massZ, 'massZ/D' )
          t.Branch( 'massZErr', massZErr, 'massZErr/D' )
          t.Branch( 'weight', weight, 'weight/D' )


          for i in range(self.tree.GetEntries()): 
              self.tree.GetEntry(i)
              massZ[0] = self.tree.massZ
              weight[0] = self.tree.weight
              massZErr[0] = self.UpdateMassZErr(self.tree.pT1, self.tree.eta1, self.tree.phi1, self.tree.m1,
                                         self.tree.pT2, self.tree.eta2, self.tree.phi2, self.tree.m2,
                                         self.tree.pterr1, self.tree.pterr2, self.Lambdas['lambda1'], self.Lambdas['lambda2'])
              t.Fill()
          t.Write()
              
      

      def UpdateMassZErr(self, pT1, eta1, phi1, m1, 
                         pT2, eta2, phi2, m2,
                         pterr1, pterr2, corr1, corr2):

          lep1 = TLorentzVector(0,0,0,0)
          lep2 = TLorentzVector(0,0,0,0)
          lep1.SetPtEtaPhiM(pT1,eta1,phi1,m1)
          lep2.SetPtEtaPhiM(pT2,eta2,phi2,m2)

          lep1p = TLorentzVector(0,0,0,0)
          lep2p = TLorentzVector(0,0,0,0)
          lep1p.SetPtEtaPhiM(pT1*(1+pterr1*corr1),(eta1),(phi1),m1)
          lep2p.SetPtEtaPhiM(pT2*(1+pterr2*corr2),(eta2),(phi2),m2)

          dm1 = (lep1p+lep2).M()-(lep1+lep2).M()
          dm2 = (lep1+lep2p).M()-(lep1+lep2).M()

          massZErr = TMath.Sqrt(dm1*dm1+dm2*dm2)

          return massZErr

        
#____________________________________________________________________________________________________
      def doLambdaCut(self):
          """
          PURPOSE: Apply pT and eta cuts to lep1 and lep2
          """
          # Bin1
          lep1InBin1 = " (pT1 > " + str(self.pTLow_1st) + " && pT1 < " + str(self.pTHigh_1st) + ")"
          lep1InBin1 += " && (abs(eta1) > " + str(self.etaLow_1st) + " && abs(eta1) < " + str(self.etaHigh_1st) + ")"

          lep2InBin1 = " (pT2 > " + str(self.pTLow_1st) + " && pT2 < " + str(self.pTHigh_1st) + ")"
          lep2InBin1 += " && (abs(eta2) > " + str(self.etaLow_1st) + " && abs(eta2) < " + str(self.etaHigh_1st) + ")"

          # Bin2
          lep1InBin2 = " (pT1 > " + str(self.pTLow) + " && pT1 < " + str(self.pTHigh) + ")"
          lep1InBin2 += " && (abs(eta1) > " + str(self.etaLow) + " && abs(eta1) < " + str(self.etaHigh) + ")"

          lep2InBin2 = " (pT2 > " + str(self.pTLow) + " && pT2 < " + str(self.pTHigh) + ")"
          lep2InBin2 += " && (abs(eta2) > " + str(self.etaLow) + " && abs(eta2) < " + str(self.etaHigh) + ")"

#          if self.fs == "e":
#              self.cut += self.relpTerr_cut

          # User selects electron region and correct parameters are grabbed via e_region_dict. 
          if self.fs == 'e': 
              lep1InBin1 += " (lep1_ecalDriven && pterr1/pT1 " + e_region_dict[e_region]['rel_pTErr'] 
              lep1InBin1 += " && pT1 > " + str(self.pTLow_1st) + " && pT1 < " + str(self.pTHigh_1st) + ")"
              #lep1InBin1 += " (lep1_ecalDriven && pterr1/pT1 < 0.07 && pT1 > " + str(self.pTLow_1st) + " && pT1 < " + str(self.pTHigh_1st) + ")"
              
              lep2InBin1 += " (lep2_ecalDriven && pterr2/pT2 " + e_region_dict[e_region]['rel_pTErr'] 
              lep2InBin1 += " && pT2 > " + str(self.pTLow_1st) + " && pT2 < " + str(self.pTHigh_1st) + ")"
              #lep2InBin1 = " (lep2_ecalDriven && pterr2/pT2 < 0.07 && pT2 > " + str(self.pTLow_1st) + " && pT2 < " + str(self.pTHigh_1st) + ")"
              
              lep1InBin2 += " (lep1_ecalDriven && pterr1/pT1 " + e_region_dict[e_region]['rel_pTErr'] 
              lep1InBin2 += " && pT1 > " + str(self.pTLow_1st) + " && pT1 < " + str(self.pTHigh_1st) + ")"
              #lep1InBin2 += " && (abs(eta1) > " + str(self.etaLow_1st) + " && abs(eta1) < " + str(self.etaHigh_1st) + ")"
              
              lep2InBin2 += " (lep2_ecalDriven && pterr2/pT2 " + e_region_dict[e_region]['rel_pTErr'] 
              lep2InBin2 += " && pT2 > " + str(self.pTLow_1st) + " && pT2 < " + str(self.pTHigh_1st) + ")"
              #lep2InBin2 += " && (abs(eta2) > " + str(self.etaLow_1st) + " && abs(eta2) < " + str(self.etaHigh_1st) + ")"

          if self.doLambda1:
             # apply all cuts so far (mZ,pT1,pT2,eta1,eta2) assuming leps are in same bin
             self.cut += lep1InBin1 + " && " + lep2InBin1 
          else:
             # Take leptons to be in different bins: lep1 in bin1, lep2 in bin2
             self.cut += "((" + lep1InBin1 + " && " + lep2InBin2 + ") || (" + lep2InBin1 + " && " + lep1InBin2 + "))"

    
#____________________________________________________________________________________________________
      def DriverGetPara(self):

#         self.MakeSmallTree()

         # Run over NTuple, apply cuts, grab TTree values
         self.PrepareDataset()
         print 'dataset successfully made for parameters\n'
         # Prepare PDFs
         self.MakeModel_getPara()
         print 'model successfully made for parameters\n'

#         self.w.Print()

         # Fitting the PDFs to the DataSet
         self.DoFit_getPara()
         print 'fit done for parameters\n'

         # Update shapePara with newly found parameters from fit
         self.AfterFit_getPara()
         print 'acquired new parameters from fit\n'

         # Make the plot
         PmassZ, chi2, dof, ch, latex = self.PlotFit()
         print 'plot successfully made for parameters\n'
         return PmassZ, chi2, dof, ch, latex 
         
#____________________________________________________________________________________________________
      def DriverGetLambda(self):

#         self.MakeSmallTree()

         # Run over NTuple, apply cuts, grab TTree values
         self.PrepareDataset()
         print 'dataset successfully made for lambda\n'

         # Use parameters from previous fit (except sigma). 
         # Initialize new CB with sigma = lambda*massZErr. Make model.
         self.MakeModel_getLambda()
         print 'model successfully made for lambda\n'

#         self.w.Print()

         # Fit the massZ values using ConditionalObservables method on massZErr
         self.DoFit_getLambda()
         print 'fit successfully done for lambda\n'

         # Update Lambda dictionary  
         self.AfterFit_getLambda()
         print 'acquired lambda\n'

         # Make the plot
         PmassZ, chi2, dof, ch, latex = self.PlotFit()
         print 'plot successfully made for lambda\n'
         return PmassZ, chi2, dof, ch, latex
          
