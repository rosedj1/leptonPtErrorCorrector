
#ifndef __CINT__
#include "RooGlobalFunc.h"
#endif

#include <iostream>
#include <iomanip>
#include <string>
#include <cstdlib>
#include <stdio.h>
#include <map>
#include <utility>
#include <iterator>

#include "TROOT.h"
#include "TFile.h"
#include "TString.h"
#include "TH1.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TF1.h"
#include "TLegend.h"
#include "TMultiGraph.h"
#include "THStack.h"
#include "TCanvas.h"
#include "TPad.h"
#include "TMath.h"
#include "TTree.h"
#include "TTreeIndex.h"
#include "TH2F.h"
#include "TLatex.h"
#include "TLine.h"
#include "TGraphAsymmErrors.h"
#include "Math/QuantFuncMathCore.h"

#include "TSystem.h"
#include "TStyle.h"
#include "TPaveText.h"

#include "TPaveLabel.h"
#include "TLegend.h"

#include "TLorentzRotation.h"
#include "TVector3.h"
#include "TLorentzVector.h"
//
#include <vector>
#include <fstream>
//
#include "TRandom3.h"
  
#include "RooRealVar.h"
#include "RooArgSet.h"
#include "RooGaussian.h"
#include "RooBreitWigner.h"
#include "RooProdPdf.h"
#include "RooDataSet.h"
#include "RooGlobalFunc.h"
#include "RooDataHist.h"
#include "RooHistPdf.h"
#include "RooCBShape.h"
#include "RooMinuit.h"
#include "RooFormulaVar.h"
#include "RooAddPdf.h"
#include "RooGenericPdf.h"

#include "RooPlot.h"

// customized PDF
//#include "ZmassConstraintLinkDef.h"
//#include "include/HZZ2L2QRooPdfs.cc"
#include "RooClassFactory.h"
#ifndef __CINT__
#include "MyRooDoubleCBShape.h"
#endif

#include "RooSimultaneous.h"

#include <algorithm>

//#include "loader.C"
using namespace std;

/////////////////////

void setAddresses(TTree* tree);
void ReadTree(TTree* tree, TString fs, TTree* & newtree);

bool debug_;

TString filename;

// For HRes Reweighting

using namespace RooFit;
using namespace std;

// tree content

  std::vector<float>* Z_mass; 
  std::vector<float>* Z_noFSR_mass;
  std::vector<float>* Z_massErr;

  std::string *triggersPassed;
  ULong64_t Run, LumiSect, Event;

  std::vector<int> *lep_id;
  std::vector<int> *lep_Sip;
  std::vector<int> *lep_tightId;

  std::vector<float>* lep_mass;
  std::vector<float> *lep_pt; std::vector<float> *lep_eta; std::vector<float> *lep_phi;
  std::vector<int> *lep_genindex;
  std::vector<float> *lep_RelIso;
  std::vector<float> *lep_pterr;
  std::vector<float> *lep_pterrold;

  std::vector<float> *lep_dataMC;
  std::vector<float>   *GENZ_mass;
  std::vector<float>  *GENlep_pt;
  std::vector<float>  *GENlep_eta;
  std::vector<float>  *GENlep_phi;
  std::vector<float>  *GENlep_mass;


  double massZ, massZErr, massZErrOld, pT1, pT2, eta1, eta2;
  double m1,m2, phi1,phi2;
  double pterr1, pterr2;
  double pterr1old, pterr2old;  
  double genzm, GENmass2l;
  double weight;
  double genLep_pt1=-999, genLep_pt2=-999;
  double genLep_eta1=-999, genLep_eta2=-999;
  double genLep_phi1=-999, genLep_phi2=-999;

  int nFSRPhotons;
  double Met;
  float_t met;
  bool passedTrig;
  bool passedFullSelection; 

int main(int argc, char *argv[])
{    
     
  gStyle->SetOptStat(0000);
  //gStyle->SetOptTitle(0);
     
  using namespace std;
     
  if(argc != 4)  {
      cout<<argv[0]<<" filename "<<argv[1]<<" fs "<<argv[2]<<" outdir" <<argv[3]<<endl;
      return -1;
    }

  gStyle->SetOptStat(0000);
  //gStyle->SetOptTitle(0);
  //gSystem->Load("$CMSSW_BASE/lib/slc5_amd64_gcc462/libHiggsAnalysisCombinedLimit.so");
  gSystem->Load("$CMSSW_BASE/lib/slc6_amd64_gcc493/pluginUFHZZAnalysisRun2UFHZZ4LAna.so");

  // control ALL txt format
  debug_ =   true;

  /////////////////////

  TString filename = argv[1];
  TString fs = argv[2];
  TString outdir = argv[3];
  if(fs!="2e" && fs!="2mu")
  cout<<"fs has to be 2e, or 2mu"<<endl;

  /////////////////////

  cout<<"fs is "<<fs<<endl;

  cout<<"read file"<<endl;

  TFile* infile = new TFile("inputRootBeforeSkim/" + filename+".root");
//  TFile* infile = new TFile("/cms/data/store/user/t2/users/dsperka/Run2/HZZ4l/SubmitArea_13TeV/rootfiles_Run1Fid_20160222/DYJetsToLL_M-50_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8_RunIIFall15MiniAODv2-PU25nsData2015v1_76X_mcRun2_asymptotic_v12-v1.root");
  TTree* tree; 

  if(infile) tree = (TTree*) infile->Get("Ana/passedEvents");
  if(!tree) { cout<<"ERROR could not find the tree for "<<filename<<endl; return -1;}

  // read tree     
  TString name = filename+"_m"+fs;
  TFile* tmpFile =  new TFile(outdir + name+".root","RECREATE");

  TTree* newtree = new TTree("passedEvents","passedEvents");

  cout<<"start setting tree "<<endl;

  newtree->Branch("massZ",&massZ,"massZ/D");
  newtree->Branch("massZErr",&massZErr,"massZErr/D");
  newtree->Branch("massZErrOld",&massZErrOld,"massZErrOld/D");

  newtree->Branch("pT1",&pT1,"pT1/D");
  newtree->Branch("pT2",&pT2,"pT2/D");
  newtree->Branch("eta1",&eta1,"eta1/D");
  newtree->Branch("eta2",&eta2,"eta2/D");
  newtree->Branch("phi1",&phi1,"phi1/D");
  newtree->Branch("phi2",&phi2,"phi2/D");
  newtree->Branch("m1",&m1,"m1/D");
  newtree->Branch("m2",&m2,"m2/D");

  newtree->Branch("pterr1",&pterr1,"pterr1/D");
  newtree->Branch("pterr2",&pterr2,"pterr2/D");
  newtree->Branch("pterr1old",&pterr1old,"pterr1old/D");
  newtree->Branch("pterr2old",&pterr2old,"pterr2old/D");
  newtree->Branch("Met", &Met, "Met/D");
  newtree->Branch("weight",&weight,"weight/D");
  newtree->Branch("genzm",&genzm,"genzm/D");
  newtree->Branch("GENmass2l",&GENmass2l,"GENmass2l/D");
  newtree->Branch("genLep_pt1", &genLep_pt1, "genLep_pt1/D");
  newtree->Branch("genLep_pt2", &genLep_pt2, "genLep_pt2/D");
  newtree->Branch("genLep_eta1", &genLep_eta1, "genLep_eta1/D");
  newtree->Branch("genLep_eta2", &genLep_eta2, "genLep_eta2/D");
  newtree->Branch("genLep_phi1", &genLep_phi1, "genLep_phi1/D");
  newtree->Branch("genLep_phi2", &genLep_phi2, "genLep_phi2/D");

  newtree->Branch("nFSRPhotons", &nFSRPhotons, "nFSRPhotons/I");
  cout<<"start reading tree "<<endl;

  ReadTree(tree, fs, newtree);

  cout<<"end reading tree"<<endl;

  tmpFile->cd();

  newtree->Write("passedEvents",TObject::kOverwrite);

  tmpFile->Write();
  tmpFile->Close(); 

  //delete infile; delete tmpFile;


}



void ReadTree(TTree* tree, TString fs, TTree* & newtree){

        setAddresses(tree);

        for(int mcfmEvt_HZZ=0; mcfmEvt_HZZ < tree->GetEntries(); mcfmEvt_HZZ++) { //event loop
            tree->GetEntry(mcfmEvt_HZZ);
//            if(!passedTrig) continue;
            if((*lep_id).size()<2) continue;
            vector<int> passLepIndex;
            for(unsigned int il=0; il<(*lep_pt).size(); il++){
                 if(!(*lep_tightId)[il]) continue; 
                 if(!(*lep_RelIso)[il]>0.35) continue; 
                 passLepIndex.push_back(il);

            }
            if(passLepIndex.size()!=2) continue;

            unsigned int L1 = passLepIndex[0]; unsigned int L2 = passLepIndex[1];
            int idL1 = (*lep_id)[L1]; int idL2 = (*lep_id)[L2];
            if((idL1+idL2)!=0) continue;
            if(fs=="2e" && abs(idL1)!=11) continue;
            if(fs=="2mu" && abs(idL1)!=13) continue;

            weight = (*lep_dataMC)[L1]*(*lep_dataMC)[L2];

            TLorentzVector lep1(0,0,0,0);
            TLorentzVector lep2(0,0,0,0);
            phi1 = double((*lep_phi)[L1]); m1 = double((*lep_phi)[L1]);
            phi2 = double((*lep_phi)[L2]); m2 = double((*lep_phi)[L2]);

            lep1.SetPtEtaPhiM(double((*lep_pt)[L1]),double((*lep_eta)[L1]),double((*lep_phi)[L1]),double((*lep_mass)[L1]));
            lep2.SetPtEtaPhiM(double((*lep_pt)[L2]),double((*lep_eta)[L2]),double((*lep_phi)[L2]),double((*lep_mass)[L2]));

            massZ = (lep1+lep2).M();
            pterr1 = double((*lep_pterr)[L1]); pterr2 = double((*lep_pterr)[L2]);
            pterr1old = double((*lep_pterrold)[L1]); pterr2old = double((*lep_pterrold)[L2]);

//            if(massZ<80 || massZ>100) continue;

            TLorentzVector lep1p, lep2p;
            lep1p.SetPtEtaPhiM(double((*lep_pt)[L1]+pterr1),double((*lep_eta)[L1]),double((*lep_phi)[L1]),double((*lep_mass)[L1]));
            lep2p.SetPtEtaPhiM(double((*lep_pt)[L2]+pterr2),double((*lep_eta)[L2]),double((*lep_phi)[L2]),double((*lep_mass)[L2]));
            double dm1 = (lep1p+lep2).M()-(lep1+lep2).M();
            double dm2 = (lep1+lep2p).M()-(lep1+lep2).M();
 
            massZErr = TMath::Sqrt(dm1*dm1+dm2*dm2);

            lep1p.SetPtEtaPhiM(double((*lep_pt)[L1]+pterr1old),double((*lep_eta)[L1]),double((*lep_phi)[L1]),double((*lep_mass)[L1]));
            lep2p.SetPtEtaPhiM(double((*lep_pt)[L2]+pterr2old),double((*lep_eta)[L2]),double((*lep_phi)[L2]),double((*lep_mass)[L2]));

            dm1 = (lep1p+lep2).M()-(lep1+lep2).M();
            dm2 = (lep1+lep2p).M()-(lep1+lep2).M();

            massZErrOld = TMath::Sqrt(dm1*dm1+dm2*dm2);

            pT1 = (*lep_pt)[L1]; pT2 = (*lep_pt)[L2];
            eta1 = (*lep_eta)[L1]; eta2 = (*lep_eta)[L2];

            Met = met; 

            genzm=0; GENmass2l=0;
            if(GENZ_mass->size()>0) genzm = (*GENZ_mass)[0];

            TLorentzVector GENlep1p, GENlep2p;
            
            if((*lep_genindex)[L1] >= 0 && (*lep_genindex)[L2] >= 0) {

              genLep_pt1=(*GENlep_pt)[(*lep_genindex)[L1]]; genLep_pt2=(*GENlep_pt)[(*lep_genindex)[L2]];
              genLep_eta1=(*GENlep_eta)[(*lep_genindex)[L1]]; genLep_eta2=(*GENlep_eta)[(*lep_genindex)[L2]];
              genLep_phi1=(*GENlep_phi)[(*lep_genindex)[L1]]; genLep_phi2=(*GENlep_phi)[(*lep_genindex)[L2]];

              int genindex1 = (*lep_genindex)[L1];
              int genindex2 = (*lep_genindex)[L2];

              GENlep1p.SetPtEtaPhiM(double((*GENlep_pt)[genindex1]),double((*GENlep_eta)[genindex1]),double((*GENlep_phi)[genindex1]),double((*GENlep_mass)[genindex1]));
              GENlep2p.SetPtEtaPhiM(double((*GENlep_pt)[genindex2]),double((*GENlep_eta)[genindex2]),double((*GENlep_phi)[genindex2]),double((*GENlep_mass)[genindex2]));
              GENmass2l = (GENlep1p+GENlep2p).M();

              }

            newtree->Fill();

        }

}

void setAddresses(TTree* tree){

    tree->SetBranchStatus("*",0);
    tree->SetBranchStatus("passedFullSelection",1);
    tree->SetBranchStatus("passedTrig",1);
    tree->SetBranchStatus("triggersPassed",1);
    tree->SetBranchStatus("lep_id",1);
    tree->SetBranchStatus("lep_tightId",1);
    tree->SetBranchStatus("lep_pt",1);
    tree->SetBranchStatus("lep_eta",1);
    tree->SetBranchStatus("lep_phi",1);
    tree->SetBranchStatus("lep_mass",1);
    tree->SetBranchStatus("lep_RelIso",1);
    tree->SetBranchStatus("lep_pterr",1);
    tree->SetBranchStatus("lep_pterrold",1);
    tree->SetBranchStatus("lep_Sip",1);
    tree->SetBranchStatus("lep_dataMC",1);
    tree->SetBranchStatus("lep_genindex",1);

    tree->SetBranchAddress("passedFullSelection",&passedFullSelection);
    tree->SetBranchAddress("passedTrig",&passedTrig);
    tree->SetBranchAddress("lep_tightId", &lep_tightId);
    tree->SetBranchAddress("lep_id", &lep_id);
    tree->SetBranchAddress("lep_pt",&lep_pt);
    tree->SetBranchAddress("lep_eta",&lep_eta);
    tree->SetBranchAddress("lep_phi",&lep_phi);
    tree->SetBranchAddress("lep_mass",&lep_mass);
    tree->SetBranchAddress("lep_RelIso",&lep_RelIso);
    tree->SetBranchAddress("lep_pterr",&lep_pterr);
    tree->SetBranchAddress("lep_pterrold",&lep_pterrold);
    tree->SetBranchAddress("lep_Sip", &lep_Sip); 
    tree->SetBranchAddress("lep_dataMC", &lep_dataMC); 
    tree->SetBranchAddress("lep_genindex", &lep_genindex);

    tree->SetBranchStatus("Run",1);
    tree->SetBranchStatus("LumiSect",1);
    tree->SetBranchStatus("Event",1);
    tree->SetBranchAddress("Run",&Run);
    tree->SetBranchAddress("LumiSect",&LumiSect);
    tree->SetBranchAddress("Event",&Event);
    tree->SetBranchStatus("met",1);
    tree->SetBranchAddress("met", &met);
    tree->SetBranchStatus("GENZ_mass",1);
    tree->SetBranchAddress("GENZ_mass", &GENZ_mass);

    tree->SetBranchStatus("GENlep_pt",1);
    tree->SetBranchAddress("GENlep_pt", &GENlep_pt);
    tree->SetBranchStatus("GENlep_eta",1);
    tree->SetBranchAddress("GENlep_eta", &GENlep_eta);
    tree->SetBranchStatus("GENlep_phi",1);
    tree->SetBranchAddress("GENlep_phi", &GENlep_phi);
    tree->SetBranchStatus("GENlep_mass",1);
    tree->SetBranchAddress("GENlep_mass", &GENlep_mass);

    tree->SetBranchStatus("nFSRPhotons",1);
    tree->SetBranchAddress("nFSRPhotons", &nFSRPhotons);
}


