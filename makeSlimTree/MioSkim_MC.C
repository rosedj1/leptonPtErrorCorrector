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

using namespace std;

void MioSkim_MC(TString fs, TString year, TString reconstruction, bool max_entry, int set_low, int set_max, TString subname){

//   std::vector<float>* Z_mass; 
//   std::vector<float>* Z_noFSR_mass;
//   std::vector<float>* Z_massErr;
// 
//   std::string *triggersPassed;
  ULong64_t Run, LumiSect, Event;
// 
  std::vector<int> *lep_id = 0;
  std::vector<int> *lep_Sip = 0;
  std::vector<int> *lep_tightId = 0;
  std::vector<float>* lep_mass = 0;
  std::vector<float> *lep_pt = 0;
  std::vector<float> *lepFSR_pt = 0; 
  std::vector<float> *lep_eta = 0;
  std::vector<float> *lep_phi = 0;
  std::vector<int> *lep_genindex = 0;
  std::vector<float> *lep_RelIso = 0;
  std::vector<float> *lep_pterr = 0;
  std::vector<float> *lep_pterrold = 0;
  std::vector<int> *lep_ecalDriven = 0;

  std::vector<float>  *lep_dataMC = 0;
  std::vector<float>  *GENZ_mass = 0;
  std::vector<float>  *GENlep_pt = 0;
  std::vector<float>  *GENlep_eta = 0;
  std::vector<float>  *GENlep_phi = 0;
  std::vector<float>  *GENlep_mass = 0;


  double massZ, massZErr, massZErrOld, pT1, pT2, eta1, eta2;
  double Iso1, Iso2;
  int Id1, Id2;
  int Tight1, Tight2;
  double m1,m2, phi1,phi2;
  double pterr1, pterr2;
  double pterr1old, pterr2old;  
  double genzm, GENmass2l;
  double weight;
  double genLep_pt1=-999, genLep_pt2=-999;
  double genLep_eta1=-999, genLep_eta2=-999;
  double genLep_phi1=-999, genLep_phi2=-999;
  int lep1_ecalDriven = -1, lep2_ecalDriven = -1;
  int nFSRPhotons;
  double Met;
  float_t met;
  bool passedTrig;
  bool passedFullSelection; 
  float massZ1, massZ2;
  int i_max;
  
  if(fs!="2e" && fs!="2mu"){
  	cout<<"fs has to be 2e, or 2mu"<<endl;
  	return;
  }


  cout<<"---- fs is "<<fs<<endl;

  cout<<"---- read file"<<endl;

  
  TString infilename;
  infilename = "root://cmsio5.rc.ufl.edu//store/user/t2/users/ferrico/Full_RunII/" + reconstruction + "/" + year + ".root";
  
  std::cout<<infilename<<std::endl;
  
  TFile* infile = infile = TFile::Open(infilename);

  TTree* tree; 
  if(infile){ 
  	std::cout<<"File trovato.OK"<<std::endl;
    infile->cd("Ana");
    tree = (TTree*)gDirectory->Get("passedEvents");
  }
  else{ std::cout<<"ERROR could not find the file"<<std::endl; return -1;}

  if(!tree) { cout<<"ERROR could not find the tree"<<endl; return -1;}

  TString name = "Data_m" + fs + "_" + run;
  TFile* tmpFile =  new TFile("/raid/raid8/ferrico/Useful_Code_HZZ/CMSSW_10_2_15/src/Full_RunII/" + reconstruction + "/DYJetsToLL_M-50_Full_RunII_" + reconstruction + "_m" + fs + "_" + year + subanem + ".root","RECREATE");

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

  newtree->Branch("Iso1",&Iso1,"Iso1/D");
  newtree->Branch("Iso2",&Iso2,"Iso2/D");
  newtree->Branch("Id1",&Id1,"Id1/I");
  newtree->Branch("Id2",&Id2,"Id2/I");
  newtree->Branch("Tight1",&Tight1,"Tight1/I");
  newtree->Branch("Tight2",&Tight2,"Tight2/I");

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
  newtree->Branch("lep1_ecalDriven", &lep1_ecalDriven, "lep1_ecalDriven/I");
  newtree->Branch("lep2_ecalDriven", &lep2_ecalDriven, "lep2_ecalDriven/I");

  cout<<"start reading tree "<<endl;
        Long64_t nentries = tree->GetEntries();
// 
        tree->SetBranchStatus("*",0);//1);                       
        tree->SetBranchStatus("passedFullSelection",1);     
        tree->SetBranchStatus("passedTrig",1);              
        tree->SetBranchStatus("triggersPassed",1);          
        tree->SetBranchStatus("lep_id",1);                  
        tree->SetBranchStatus("lep_tightId",1);             
        tree->SetBranchStatus("lep_pt",1);                  
        tree->SetBranchStatus("lepFSR_pt",1);               
        tree->SetBranchStatus("lep_eta",1);                 
        tree->SetBranchStatus("lep_phi",1);                 
        tree->SetBranchStatus("lep_mass",1);                
        tree->SetBranchStatus("lep_RelIso",1);              
        tree->SetBranchStatus("lep_pterr",1);               
        tree->SetBranchStatus("lep_pterrold",1);            
        tree->SetBranchStatus("lep_Sip",1);                 
        tree->SetBranchStatus("lep_dataMC",1);              
        tree->SetBranchStatus("lep_genindex",1);            
        tree->SetBranchStatus("lep_ecalDriven", 1);
        tree->SetBranchStatus("Run",1);                           
        tree->SetBranchStatus("LumiSect",1);                      
        tree->SetBranchStatus("Event",1);                         
        tree->SetBranchStatus("met",1);                           
        tree->SetBranchStatus("GENZ_mass",1);                     
        tree->SetBranchStatus("GENlep_pt",1);                     
        tree->SetBranchStatus("GENlep_eta",1);                    
        tree->SetBranchStatus("GENlep_phi",1);                    
        tree->SetBranchStatus("GENlep_mass",1);                   
        tree->SetBranchStatus("nFSRPhotons",1);                   


        tree->SetBranchAddress("passedFullSelection",&passedFullSelection);
        tree->SetBranchAddress("passedTrig",&passedTrig);   
        tree->SetBranchAddress("lep_tightId", &lep_tightId);      
        tree->SetBranchAddress("lep_id", &lep_id);                
        tree->SetBranchAddress("lep_pt", &lep_pt);                 
        tree->SetBranchAddress("lepFSR_pt",&lepFSR_pt);           
        tree->SetBranchAddress("lep_eta",&lep_eta);               
        tree->SetBranchAddress("lep_phi",&lep_phi);               
        tree->SetBranchAddress("lep_mass",&lep_mass);             
        tree->SetBranchAddress("lep_RelIso",&lep_RelIso);         
        tree->SetBranchAddress("lep_pterr",&lep_pterr);           
        tree->SetBranchAddress("lep_pterrold",&lep_pterrold);     
        tree->SetBranchAddress("lep_Sip", &lep_Sip);              
        tree->SetBranchAddress("lep_dataMC", &lep_dataMC);        
        tree->SetBranchAddress("lep_genindex", &lep_genindex);    
        tree->SetBranchAddress("lep_ecalDriven", &lep_ecalDriven);  
        tree->SetBranchAddress("Run",&Run);                       
        tree->SetBranchAddress("LumiSect",&LumiSect);             
        tree->SetBranchAddress("Event",&Event);                   
        tree->SetBranchAddress("met", &met);                      
        tree->SetBranchAddress("GENZ_mass", &GENZ_mass);                                                                                 
        tree->SetBranchAddress("GENlep_pt", &GENlep_pt);          
        tree->SetBranchAddress("GENlep_eta", &GENlep_eta);        
        tree->SetBranchAddress("GENlep_phi", &GENlep_phi);        
        tree->SetBranchAddress("GENlep_mass", &GENlep_mass);          
        tree->SetBranchAddress("nFSRPhotons", &nFSRPhotons);      

//         tree->Draw("lep_ecalDriven");
//         return;

        std::cout<<"after tree set\t"<<tree->GetEntries()<<std::endl;
        
        if(max_entry)  i_max = nentries;
        else i_max = set_max;
    
        
        for(int mcfmEvt_HZZ = set_low; mcfmEvt_HZZ < i_max; mcfmEvt_HZZ++) { //event loop

            tree->GetEntry(mcfmEvt_HZZ);
            if(mcfmEvt_HZZ % 1000000 == 0)
            std::cout<<mcfmEvt_HZZ<<" --- Dentro il tree --- "<<std::endl;
//          
//          if(!passedTrig) continue;
            if((*lep_id).size()<2) continue;
            vector<int> passLepIndex;
            for(unsigned int il=0; il<(*lep_pt).size(); il++){
                 if(!(*lep_tightId)[il]) continue; 
//                  if(!((*lep_RelIso)[il]>0.35)) continue;
//                  if(!(*lep_RelIso)[il]>0.35) continue; 
                 if((*lep_RelIso)[il] > 0.35) continue; 
                 passLepIndex.push_back(il);
//                  if((*lep_RelIso)[il]> 0.3 && (*lep_RelIso)[il] < 0.4) std::cout<<(*lep_RelIso)[il]<<std::endl;

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

            eta1 = (*lep_eta)[L1]; eta2 = (*lep_eta)[L2];
			/*
            if (abs(idL1) == 13 && abs(idL2) == 13) {

               if (abs(eta1) < 0.9) (*lep_pt)[L1] = (*lep_pt)[L1]/(1-0.00070374);
               if (abs(eta1) > 0.9 && abs(eta1) < 1.8) (*lep_pt)[L1] = (*lep_pt)[L1]/(1-0.0015881);
               if (abs(eta1) > 1.8 && abs(eta1) < 2.4) (*lep_pt)[L1] = (*lep_pt)[L1]/(1-0.0029359);
 
               if (abs(eta2) < 0.9) (*lep_pt)[L2] = (*lep_pt)[L2]/(1-0.00070374);
               if (abs(eta2) > 0.9 && abs(eta2) < 1.8) (*lep_pt)[L2] = (*lep_pt)[L2]/(1-0.0015881);
               if (abs(eta2) > 1.8 && abs(eta2) < 2.4) (*lep_pt)[L2] = (*lep_pt)[L2]/(1-0.0029359);

               }
			*/

            phi1 = double((*lep_phi)[L1]); m1 = double((*lep_phi)[L1]);
            phi2 = double((*lep_phi)[L2]); m2 = double((*lep_phi)[L2]);
            pT1 = (*lepFSR_pt)[L1]; pT2 = (*lepFSR_pt)[L2];
//            pT1 = (*lep_pt)[L1]; pT2 = (*lep_pt)[L2];
            Iso1 = (*lep_RelIso)[L1]; Iso2 = (*lep_RelIso)[L2];
            Id1 = (*lep_id)[L1]; Id2 = (*lep_id)[L2];
            Tight1 = (*lep_tightId)[L1]; Tight2 = (*lep_tightId)[L2];

            lep1.SetPtEtaPhiM(double((*lepFSR_pt)[L1]),double((*lep_eta)[L1]),double((*lep_phi)[L1]),double((*lep_mass)[L1]));
            lep2.SetPtEtaPhiM(double((*lepFSR_pt)[L2]),double((*lep_eta)[L2]),double((*lep_phi)[L2]),double((*lep_mass)[L2]));
//            lep1.SetPtEtaPhiM(double((*lep_pt)[L1]),double((*lep_eta)[L1]),double((*lep_phi)[L1]),double((*lep_mass)[L1]));
//            lep2.SetPtEtaPhiM(double((*lep_pt)[L2]),double((*lep_eta)[L2]),double((*lep_phi)[L2]),double((*lep_mass)[L2]));

            massZ = (lep1+lep2).M();
            pterr1 = double((*lep_pterr)[L1]); pterr2 = double((*lep_pterr)[L2]);
            pterr1old = double((*lep_pterrold)[L1]); pterr2old = double((*lep_pterrold)[L2]);

//            if(massZ<80 || massZ>100) continue;

            TLorentzVector lep1p, lep2p;
//            lep1p.SetPtEtaPhiM(double((*lep_pt)[L1]+pterr1),double((*lep_eta)[L1]),double((*lep_phi)[L1]),double((*lep_mass)[L1]));
//            lep2p.SetPtEtaPhiM(double((*lep_pt)[L2]+pterr2),double((*lep_eta)[L2]),double((*lep_phi)[L2]),double((*lep_mass)[L2]));
            lep1p.SetPtEtaPhiM(double((*lepFSR_pt)[L1]+pterr1),double((*lep_eta)[L1]),double((*lep_phi)[L1]),double((*lep_mass)[L1]));
            lep2p.SetPtEtaPhiM(double((*lepFSR_pt)[L2]+pterr2),double((*lep_eta)[L2]),double((*lep_phi)[L2]),double((*lep_mass)[L2]));

            double dm1 = (lep1p+lep2).M()-(lep1+lep2).M();
            double dm2 = (lep1+lep2p).M()-(lep1+lep2).M();
 
            massZErr = TMath::Sqrt(dm1*dm1+dm2*dm2);

            lep1p.SetPtEtaPhiM(double((*lepFSR_pt)[L1]+pterr1old),double((*lep_eta)[L1]),double((*lep_phi)[L1]),double((*lep_mass)[L1]));
            lep2p.SetPtEtaPhiM(double((*lepFSR_pt)[L2]+pterr2old),double((*lep_eta)[L2]),double((*lep_phi)[L2]),double((*lep_mass)[L2]));
//            lep1p.SetPtEtaPhiM(double((*lep_pt)[L1]+pterr1old),double((*lep_eta)[L1]),double((*lep_phi)[L1]),double((*lep_mass)[L1]));
//            lep2p.SetPtEtaPhiM(double((*lep_pt)[L2]+pterr2old),double((*lep_eta)[L2]),double((*lep_phi)[L2]),double((*lep_mass)[L2]));

            dm1 = (lep1p+lep2).M()-(lep1+lep2).M();
            dm2 = (lep1+lep2p).M()-(lep1+lep2).M();

            massZErrOld = TMath::Sqrt(dm1*dm1+dm2*dm2);
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

            if (lep_ecalDriven->size() > 0) {

               lep1_ecalDriven = (*lep_ecalDriven)[L1];
               lep2_ecalDriven = (*lep_ecalDriven)[L2];
 
               }

            newtree->Fill();

        }

                                                            
     cout<<"end reading tree"<<endl;                       
                                                               
     tmpFile->cd();                                        
                                                                  
     newtree->Write("passedEvents",TObject::kOverwrite);   
                                                                     
     tmpFile->Write();                                     
     tmpFile->Close();   
}
