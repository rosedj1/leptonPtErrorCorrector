import ROOT, sys, os, string, re
from ROOT import *
from array import array
from math import *
from tdrStyle import *
from subprocess import call

setTDRStyle()

class GetCorrection():

      def __init__(self, binEdge, isData, fs, doLambda1, lambdas, shapePara, path, tag):

          if not doLambda1:
             self.pTLow_1st = {'e': 7, 'mu': 40}
             self.pTHigh_1st = {'e': 100, 'mu': 50}
             self.etaLow_1st = {'e': 0, 'mu': 0}
             self.etaHigh_1st = {'e': 1, 'mu': 0.9}
          else:
             self.pTLow_1st = {'e': binEdge['pTLow'], 'mu': binEdge['pTLow']}
             self.pTHigh_1st = {'e': binEdge['pTHigh'], 'mu': binEdge['pTHigh']}
             self.etaLow_1st = {'e': binEdge['etaLow'], 'mu': binEdge['etaLow']}
             self.etaHigh_1st = {'e': binEdge['etaHigh'], 'mu': binEdge['etaHigh']}

          #can also set first bin as dict

          self.pTLow = binEdge['pTLow']
          self.pTHigh = binEdge['pTHigh']
          self.etaLow = binEdge['etaLow']
          self.etaHigh = binEdge['etaHigh']

          self.Lambdas = {'lambda1': lambdas['lambda1'],
                          'lambda2': lambdas['lambda2'],
                          'lambda': 1}

          self.massZ_lo = 60
          self.massZ_hi = 120

          self.fs = fs
          self.doLambda1 = doLambda1
          #cut to make dataset
          self.cut = " (massZ > "+str(self.massZ_lo)+" && massZ < "+str(self.massZ_hi)+") && "
#          self.cut += " (genzm > 80 && genzm < 100) && " 
          self.cut += " (massZErr > 0.2 && massZErr < 7.2) && "
#          self.cut += " (Met < 30 && GENmass2l > 0) && "
          self.doLambdaCut() # doLambda1Cut or doLambda2Cut

          #tree to get information
#          self.fileName = "DYJetsToLL_M-50_m2" + self.fs + ".root"
          self.fileName = "DYJetsToLL_M-50_kalman_v4_m2" + self.fs + ".root"
          if isData:
             self.fileName = "DoubleLepton_m2" + self.fs + ".root"
#          self.treeFile = TFile("../inputRootFiles/"+self.fileName)

          self.treeFile = TFile("/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"+self.fileName)
          self.tree = self.treeFile.Get("passedEvents")
          self.chain = TChain("passedEvents")
          self.chain.Add("/raid/raid9/mhl/HZZ4L_Run2_post2016ICHEP/outputRoot/DY_2015MC_kalman_v4_NOmassZCut_addpTScaleCorrection/"+self.fileName)
          print 'tree opened'

          #save
          self.path = path
          self.name = (self.fileName.split('.'))[0]
          self.name += "_Pt_" + str(self.pTLow)  + "_to_" + str(self.pTHigh) + "_Eta_" + str(self.etaLow) + "_to_" + str(self.etaHigh)
          self.name += "_" + tag

          self.tag = tag

          '''
          self.hgenzm = TH1F("hgenzm","hgenzm",200,80,100)
#used for data
          if isData:
             tmpName = self.name.replace("DoubleLepton","DYJetsToLL_M-50").replace(self.tag, "doLambda2_getPara_" + fs)
             genzmFile = TFile("genZShape/" + tmpName + "_genZShape.root")
             tmp_hgenzm = genzmFile.Get("hgenzm")
             for i in range(tmp_hgenzm.GetSize()-1):
                 if i >= 1:
                    self.hgenzm.SetBinContent(i, tmp_hgenzm.GetBinContent(i))
#used for mc
          else:
             self.tree.Project(self.hgenzm.GetName(), "GENmass2l", "weight*(" + self.cut + ")")
             genzmFile = TFile("genZShape/" + self.name + "_genZShape.root", "RECREATE")
             genzmFile.cd()
             self.hgenzm.Write()
             genzmFile.Close()
          '''

          #initial shape parameters
          self.shapePara = shapePara
          self.w = RooWorkspace("w","workspace")

          #dataset
          self.Data_Zlls = RooDataSet()
          self.Data_Zlls_w = RooDataSet()
          self.Data_Zlls_binned = RooDataHist()
 
          self.rFit = RooFitResult() 


      def PrepareDataset(self):

          cut = self.cut
#          self.chain.Draw(">>myList", cut, "entrylist")
#          entryList = gDirectory.Get("myList")
#          self.chain.SetEntryList(entryList)
          print cut
          self.tree.Draw(">>myList", cut, "entrylist")
          entryList = gDirectory.Get("myList")
          self.tree.SetEntryList(entryList)

#          p0 = TParameter(int)( "doLambda1", int(self.doLambda1) )
#          p1 = TParameter(float)( "lambda1", self.Lambdas['lambda1'] )
#          p2 = TParameter(float)( "lambda2", self.Lambdas['lambda2'] )

#          proof = TProof.Open("")
#          proof.AddInput(p0)
#          proof.AddInput(p1)
#          proof.AddInput(p2)

          selector = TSelector.GetSelector("MySelector.C+")
#          self.chain.SetProof()
          self.tree.Process(selector)
#          self.chain.Process(selector)

          self.Data_Zlls = selector.Data_Zlls

          self.Data_Zlls_w = RooDataSet(self.Data_Zlls.GetName(), self.Data_Zlls.GetTitle(), self.Data_Zlls, self.Data_Zlls.get(), "1", "weight")
          print "dataset has " + str(self.Data_Zlls_w.numEntries()) + " events"

#          massZ.setBins(40,"fft")
#          massZErr.setBins(40,"fft")
          self.Data_Zlls_binned = self.Data_Zlls_w.binnedClone()
          del selector

      def MakeModel_getPara(self):

          #variables
          massZ = RooRealVar("massZ","massZ", self.massZ_lo, self.massZ_hi)
#          massZ = RooRealVar("massZ","massZ", 60, 120)
          massZErr = RooRealVar("massZErr","massZErr", 0.2, 7.2)
          #BreitWigner
          breitWignerMean = RooRealVar("breitWignerMean", "m_{Z^{0}}", 91.2)#91.14)#187)
          breitWignerGamma = RooRealVar("breitWignerGamma", "#Gamma", 2.446)#2.546)#4952)
          breitWignerGamma.setConstant(kTRUE)
          breitWignerMean.setConstant(kTRUE)
          BW = RooBreitWigner("BW","Breit Wigner theory", massZ, breitWignerMean,breitWignerGamma)
          #Crystalball
          mean = RooRealVar("mean","mean", 0, -1, 1)
          alpha = RooRealVar("alpha","alpha", 1, 0, 10)
          n = RooRealVar("n","n", 5, 0, 30)
          #alpha2 = RooRealVar("alpha2","alpha2", 1.2, 0, 50)
          #n2 = RooRealVar("n2","n2", 15, 0.1, 50)
          sigma = RooRealVar("sigma", "sigma", 1, 0, 10)
          CB = RooCBShape("CB","CB", massZ, mean, sigma, alpha, n)
          #CB = RooDoubleCB("CB","CB", massZ, mean, sigma, alpha, n, alpha2, n2)
          #GENZ shape convoluted with crystal ball
#          rdh_genzm = RooDataHist("rdh_genzm","rdh_genzm", RooArgList(massZ), self.hgenzm)
#          rhp_genzm = RooHistPdf("rhp_genzm","rhp_genzm", RooArgSet(massZ), rdh_genzm)
#          CBxBW = RooFFTConvPdf("CBxBW","CBxBW", massZ, rhp_genzm, CB)
          CBxBW = RooFFTConvPdf("CBxBW","CBxBW", massZ, BW, CB)
          #bkg
          tau = RooRealVar("tau","tau",  -1, 1)
          pa1 = RooRealVar("pa1","pa1", -0.08, -10,10)
          pa2 = RooRealVar("pa2","pa2", 0.0098, -10,10)
          p2 = RooFormulaVar("p2", "@1*@0+@2*@0*@0",RooArgList(massZ,pa1,pa2))
#          bkg = RooExponential("bkg","bkg", p2, tau)
          bkg = RooExponential("bkg","bkg", massZ, tau)
          #fsig
          fsig = RooRealVar("fsig","signal fraction", 0.7, 0.5, 1)
          model = RooAddPdf("model","model", CBxBW, bkg, fsig)
          getattr(self.w,'import')(model)

      def MakeModel_getLambda(self):

          #variables
          massZ = RooRealVar("massZ","massZ", self.massZ_lo, self.massZ_hi)
#          massZ = RooRealVar("massZ","massZ", 60, 120)
          massZErr = RooRealVar("massZErr","massZErr", 0.2, 7.2)
          #BreitWigner
          breitWignerMean = RooRealVar("breitWignerMean", "m_{Z^{0}}", 91.2)#87)
          breitWignerGamma = RooRealVar("breitWignerGamma", "#Gamma", 2.446)#4952)
          breitWignerGamma.setConstant(kTRUE)
          breitWignerMean.setConstant(kTRUE)
          BW = RooBreitWigner("BW","Breit Wigner theory", massZ, breitWignerMean,breitWignerGamma)
          #Crystalball
          mean = RooRealVar("mean","mean", self.shapePara["mean"])
          alpha = RooRealVar("alpha","alpha", self.shapePara["alpha"])
          n = RooRealVar("n","n", self.shapePara["n"])
          #alpha2 = RooRealVar("alpha2","alpha2", self.shapePara["alpha2"])
          #n2 = RooRealVar("n2","n2", self.shapePara["n2"])
          lambda_ = RooRealVar("lambda","lambda", 1, 0.7, 1.3)
#          sigma = RooFormulaVar("sigma","@1*(1+@2/@1*@0)", RooArgList(lambda_, massZ, massZErr))
          sigma = RooFormulaVar("sigma","@1*@0", RooArgList(lambda_,  massZErr))
          CB = RooCBShape("CB","CB", massZ, mean, sigma, alpha, n)
          #CB = RooDoubleCB("CB","CB", massZ, mean, sigma, alpha, n, alpha2, n2)
          #GENZ shape convoluted with crystal ball
#          rdh_genzm = RooDataHist("rdh_genzm","rdh_genzm", RooArgList(massZ), self.hgenzm)
#          rhp_genzm = RooHistPdf("rhp_genzm","rhp_genzm", RooArgSet(massZ), rdh_genzm)
          #CBxBW = RooFFTConvPdf("CBxBW","CBxBW", massZ, rhp_genzm, CB)

          CBxBW = RooFFTConvPdf("CBxBW","CBxBW", massZ, BW, CB)

          tau = RooRealVar("tau","tau", self.shapePara["tau"])
          pa1 = RooRealVar("pa1","pa1", self.shapePara["pa1"])
          pa2 = RooRealVar("pa2","pa2", self.shapePara["pa2"])
          p2 = RooFormulaVar("p2", "@1*@0+@2*@0*@0",RooArgList(massZ,pa1,pa2))
#          bkg = RooExponential("bkg","bkg", p2, tau)
          bkg = RooExponential("bkg","bkg", massZ, tau)

          #fsig
          fsig = RooRealVar("fsig","signal fraction", self.shapePara["fsig"])
          model = RooAddPdf("model","model", CBxBW, bkg, fsig)
          
          getattr(self.w,'import')(model)

      def DoFit_getPara(self):

          if self.Data_Zlls_w.numEntries() < 5000:
             self.rFit = self.w.pdf("model").fitTo( self.Data_Zlls_w, \
                                                    RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1), RooFit.Timer(kTRUE) )
          else: 
             self.rFit = self.w.pdf("model").fitTo( self.Data_Zlls_binned, \
                                                    RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1), RooFit.Timer(kTRUE) )
      def DoFit_getLambda(self):

          if self.Data_Zlls_w.numEntries() < 5000:
             self.rFit = self.w.pdf("model").fitTo( self.Data_Zlls_w, RooFit.ConditionalObservables( RooArgSet(self.w.var("massZErr")) ),\
                                                    RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1), RooFit.Timer(kTRUE) )
          else:
             self.rFit = self.w.pdf("model").fitTo( self.Data_Zlls_binned, RooFit.ConditionalObservables( RooArgSet(self.w.var("massZErr")) ),\
                                                    RooFit.Save(kTRUE), RooFit.SumW2Error(kTRUE), RooFit.PrintLevel(-1), RooFit.Timer(kTRUE) )

      def AfterFit_getPara(self):

          self.shapePara["mean"] = self.w.var("mean").getVal()
          self.shapePara["alpha"] = self.w.var("alpha").getVal()
          self.shapePara["n"] = self.w.var("n").getVal()
#          self.shapePara["alpha2"] = self.w.var("alpha2").getVal()
#          self.shapePara["n2"] = self.w.var("n2").getVal()
          self.shapePara["tau"] = self.w.var("tau").getVal()
#          self.shapePara["pa1"] = self.w.var("pa1").getVal()
#          self.shapePara["pa2"] = self.w.var("pa2").getVal()
          self.shapePara["fsig"] = self.w.var("fsig").getVal()

      def AfterFit_getLambda(self):

          self.Lambdas["lambda"] = self.w.var("lambda").getVal()
          #need to save lambda, pass it to lambda2, save fs, doLambda1, tag(iteration)
          saveLambda = "lambda: " + str(self.Lambdas["lambda"])
          saveLambda += ", lambda1: " + str(self.Lambdas["lambda1"])
          saveLambda += ", lambda2: " + str(self.Lambdas["lambda2"])
          saveLambda += ", lambda*lambda2: " + str(self.Lambdas["lambda"]*self.Lambdas["lambda2"])
#          call('cat "' + saveLambda + '" >> ' + self.path+self.name+'.txt', shell=True)

      def PlotFit(self):

          PmassZ = self.w.var("massZ").frame(RooFit.Bins(50))
          PmassZ.GetXaxis().SetTitle("massZ(GeV)")
          PmassZ.GetYaxis().SetTitleOffset(1.3)

          self.Data_Zlls_w.plotOn(PmassZ)
          self.w.pdf("model").plotOn(PmassZ, RooFit.ProjWData(self.Data_Zlls_w,kTRUE),\
                                      RooFit.LineColor(2), RooFit.LineWidth(1) )
          self.w.pdf("model").paramOn(PmassZ, RooFit.Layout(0.17, 0.47, 0.9), RooFit.Format("NE", RooFit.FixedPrecision(4)))
          PmassZ.getAttText().SetTextSize(0.03)
          chi2 = PmassZ.chiSquare(self.rFit.floatParsFinal().getSize())
          dof =  self.rFit.floatParsFinal().getSize()
          self.w.pdf("model").plotOn(PmassZ, RooFit.Components("bkg"), RooFit.LineStyle(kDashed))
          self.Data_Zlls_w.plotOn(PmassZ)
          self.w.pdf("model").plotOn(PmassZ, RooFit.ProjWData(self.Data_Zlls_w,kTRUE),\
                                      RooFit.LineColor(2), RooFit.LineWidth(1) )

          ch = TCanvas("ch","ch",1000,800)
          ch.cd()

          PmassZ.Draw("")

          latex = TLatex()
          latex.SetNDC()
          latex.SetTextSize(0.55*ch.GetTopMargin())
          latex.SetTextFont(42)
          latex.SetTextAlign(11)
          latex.DrawLatex(0.75, 0.85, "#chi^{2}/DOF = %.3f" %(chi2/dof))

          if "getLambda" in self.tag:
             latex.DrawLatex(0.75, 0.8, "alpha = %.3f" %(self.w.var("alpha").getVal()))
             latex.DrawLatex(0.75, 0.75, "fsig = %.3f" %(self.w.var("fsig").getVal()))
             latex.DrawLatex(0.75, 0.7, "n = %.3f" %(self.w.var("n").getVal()))
#             latex.DrawLatex(0.75, 0.65, "pa1 = %.3f" %(self.w.var("pa1").getVal()))
#             latex.DrawLatex(0.75, 0.6, "pa2 = %.3f" %(self.w.var("pa2").getVal()))
             latex.DrawLatex(0.75, 0.55, "sigma = %.3f" %(self.w.function("sigma").getVal()))
             latex.DrawLatex(0.75, 0.5, "tau = %.3f" %(self.w.var("tau").getVal()))

          ch.SaveAs(self.path + self.name + '.png')

      def MakeSmallTree(self):

          f = TFile(self.path+self.name+".root","recreate")
          t = TTree( 't1', 'tree with massZZ, massZZErr, weight' )

          massZ = array( 'f', [ 0 ] )
          massZErr = array( 'f', [ 0 ] )
          weight = array( 'f', [ 0 ] )

          t.Branch( 'massZ', massZ, 'massZ/D' )
          t.Branch( 'massZErr', massZErr, 'massZErr/D' )
          t.Branch( 'weight', weight, 'weight/D' )


          for i in range(self.tree.GetEntries()): 
              print "hh"
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
          lep1p.SetPtEtaPhiM(pT1+pterr1*corr1,(eta1),(phi1),m1)
          lep2p.SetPtEtaPhiM(pT2+pterr2*corr2,(eta2),(phi2),m2)

          dm1 = (lep1p+lep2).M()-(lep1+lep2).M()
          dm2 = (lep1+lep2p).M()-(lep1+lep2).M()

          massZErr = TMath.Sqrt(dm1*dm1+dm2*dm2)

          return massZErr

        
      def doLambdaCut(self):

          lep1InBin1 = " (pT1 > " + str(self.pTLow_1st[self.fs]) + " && pT1 < " + str(self.pTHigh_1st[self.fs]) + ")"
          lep1InBin1 += " && (abs(eta1) > " + str(self.etaLow_1st[self.fs]) + " && abs(eta1) < " + str(self.etaHigh_1st[self.fs]) + ")"

          lep2InBin1 = " (pT2 > " + str(self.pTLow_1st[self.fs]) + " && pT2 < " + str(self.pTHigh_1st[self.fs]) + ")"
          lep2InBin1 += " && (abs(eta2) > " + str(self.etaLow_1st[self.fs]) + " && abs(eta2) < " + str(self.etaHigh_1st[self.fs]) + ")"

          lep1InBin2 = " (pT1 > " + str(self.pTLow) + " && pT1 < " + str(self.pTHigh) + ")"
          lep1InBin2 += " && (abs(eta1) > " + str(self.etaLow) + " && abs(eta1) < " + str(self.etaHigh) + ")"

          lep2InBin2 = " (pT2 > " + str(self.pTLow) + " && pT2 < " + str(self.pTHigh) + ")"
          lep2InBin2 += " && (abs(eta2) > " + str(self.etaLow) + " && abs(eta2) < " + str(self.etaHigh) + ")"

          if self.doLambda1:
             self.cut += lep1InBin1 + " && " + lep2InBin1
          else:
             self.cut += "((" + lep1InBin1 + " && " + lep2InBin2 + ") || (" + lep2InBin1 + " && " + lep1InBin2 + "))"

    
      def DriverGetPara(self):

#         self.MakeSmallTree()
         self.PrepareDataset()
         print 'dataset made'
         self.MakeModel_getPara()
         print 'model made'

         self.w.Print()

         self.DoFit_getPara()
         print 'fit done'
         self.AfterFit_getPara()
         print 'parameter got'
         self.PlotFit()
         print 'plot made'
 
         
      def DriverGetLambda(self):

#         self.MakeSmallTree()
         self.PrepareDataset()
         self.MakeModel_getLambda()

         self.w.Print()

         self.DoFit_getLambda()
         self.AfterFit_getLambda()
         self.PlotFit()

          
