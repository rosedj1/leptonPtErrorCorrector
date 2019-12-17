#ifndef AnalysisTree_h
#define AnalysisTree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>
#include <TTree.h>
#include <TClonesArray.h>

  float  GENmassZ1, GENmassZ2;

  double Djet_VAJHU;

  int idL1, idL2, idL3, idL4;

  std::vector<int> * GENlep_id;
  int GENlep_Hindex[4];

  int fsState;

  bool isFromH_L1, isFromH_L2, isFromH_L3, isFromH_L4;

  float RECOmass4l, REFITmass4l;
 
/*
    if( RecoFourMuEvent ){ finalState = 1;}
    if( RecoFourEEvent  ){ finalState = 2;}
    if( RecoTwoETwoMuEvent ){ finalState = 3;}
    if( RecoTwoMuTwoEEvent ){ finalState = 4;}
*/

  bool passedFullSelection, passedTrig;

  bool passedFiducialSelection;

  using namespace std;  

namespace AnalysisTree {

 void setAddressesRECO(TTree* tree){

    tree->SetBranchAddress("passedFullSelection",&passedFullSelection);
    tree->SetBranchAddress("passedTrig",&passedTrig);

    tree->SetBranchAddress("GENmassZ1",&GENmassZ1);
    tree->SetBranchAddress("GENmassZ2",&GENmassZ2);

    tree->SetBranchAddress("Djet_VAJHU",&Djet_VAJHU);
    tree->SetBranchAddress("mass4lREFIT",&REFITmass4l);
    tree->SetBranchAddress("mass4l",&RECOmass4l);

    tree->SetBranchAddress("idL1",&idL1);
    tree->SetBranchAddress("idL3",&idL3);
    tree->SetBranchAddress("idL2",&idL2);
    tree->SetBranchAddress("idL4",&idL4);

    tree->SetBranchAddress("GENlep_id",&GENlep_id);
    tree->SetBranchAddress("GENlep_Hindex",&GENlep_Hindex);
  }


 void setCMS(TH1F* Graph1)
 {

    Graph1->GetXaxis()->SetLabelFont(42);
    Graph1->GetXaxis()->SetLabelOffset(0.003);

    Graph1->GetXaxis()->SetLabelSize(0.035);

    Graph1->GetXaxis()->SetTitleSize(0.04);
    Graph1->GetXaxis()->SetTitleOffset(0.8);
    Graph1->GetXaxis()->SetTitleFont(42);

    Graph1->GetYaxis()->SetLabelFont(42);

    Graph1->GetYaxis()->SetLabelOffset(0.004);
    Graph1->GetYaxis()->SetLabelSize(0.035);
    Graph1->GetYaxis()->SetTitleSize(0.04);
    Graph1->GetYaxis()->SetTitleOffset(1.1);
    Graph1->GetYaxis()->SetTitleFont(42);

 }

 void setCMS(TGraph* Graph1)
 {

    Graph1->GetXaxis()->SetLabelFont(42);
    Graph1->GetXaxis()->SetLabelOffset(0.003);

    Graph1->GetXaxis()->SetLabelSize(0.035);

    Graph1->GetXaxis()->SetTitleSize(0.04);
    Graph1->GetXaxis()->SetTitleOffset(0.8);
    Graph1->GetXaxis()->SetTitleFont(42);

    Graph1->GetYaxis()->SetLabelFont(42);

    Graph1->GetYaxis()->SetLabelOffset(0.004);
    Graph1->GetYaxis()->SetLabelSize(0.035);
    Graph1->GetYaxis()->SetTitleSize(0.04);
    Graph1->GetYaxis()->SetTitleOffset(1.0);
    Graph1->GetYaxis()->SetTitleFont(42);

 }

 void setCMS(TH2F* Graph1)
 {

    Graph1->GetXaxis()->SetLabelFont(42);
    Graph1->GetXaxis()->SetLabelOffset(0.003);

    Graph1->GetXaxis()->SetLabelSize(0.035);

    Graph1->GetXaxis()->SetTitleSize(0.04);
    Graph1->GetXaxis()->SetTitleOffset(0.8);
    Graph1->GetXaxis()->SetTitleFont(42);

    Graph1->GetYaxis()->SetLabelFont(42);

    Graph1->GetYaxis()->SetLabelOffset(0.004);
    Graph1->GetYaxis()->SetLabelSize(0.035);
    Graph1->GetYaxis()->SetTitleSize(0.04);
    Graph1->GetYaxis()->SetTitleOffset(1.1);
    Graph1->GetYaxis()->SetTitleFont(42);
 }

}

#endif
