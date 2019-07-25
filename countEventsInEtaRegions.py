############################################################################
## PURPOSE: Count the number of events in each relative pT error vs. eta region for muons,
##          tracker electrons, and ECAL electrons in a skimmed NTuple. 
## SYNTAX:  python <script.py> <inputfile.root> <finalstate>
## NOTES:   The NTuple should have branches like: massZ, massZErr, pT1, etc.
##          - <finalstate> must either be "2e" or "2mu"
## AUTHOR:  Jake Rosenzweig
## DATE:    2019-06-21
## UPDATED: 2019-07-07
############################################################################
import ROOT
import sys
#___________________________________________________________________________
# Automatic Stuff
inputfile = str(sys.argv[1])
fs        = str(sys.argv[2])
f = ROOT.TFile.Open(inputfile)
t = f.Get("passedEvents")
ntot = t.GetEntries()

if fs not in ["2e","2mu"]:
    print 'ERROR: You must pass in either "2e" or "2mu"'
#___________________________________________________________________________
# Functions
def countEventsWithCuts(tree, title, cuts, text):
    n_events = tree.GetEntries(cuts)
    print "%s\t%s: %d events...\t%.4E%% of total events" % (title,text,n_events,n_events*100./ntot)
    return n_events
    sys.exit()
#___________________________________________________________________________
# MAIN
print "\nTotal events in NTuple:", ntot
print "...finding how many pairs of each lepton belong to same eta region...\n"

#############
# ELECTRONS #
#############

# ECAL electrons
# Region 1
if fs == "2e":

    n_ecal_reg1a = countEventsWithCuts(
        t, 
        "ECAL eta region 1a:",
        "(0<abs(eta1) && abs(eta1)<0.8) && (0<abs(eta2) && abs(eta2)<0.8) && pterr1/pT1<0.03 && pterr2/pT2<0.03 && lep1_ecalDriven==1 && lep2_ecalDriven==1",
        "[0, 0.8]\trel_pTErr < 3%:"
        )

    n_ecal_reg1b = countEventsWithCuts(
        t, 
        "ECAL eta region 1b:",
        "(0.8<abs(eta1) && abs(eta1)<1.0) && (0.8<abs(eta2) && abs(eta2)<1.0) && pterr1/pT1<0.03 && pterr2/pT2<0.03 && lep1_ecalDriven==1 && lep2_ecalDriven==1",
        "[0.8, 1.0]\trel_pTErr < 3%:"
        )
    print

    # Region 2
    n_ecal_reg2 = countEventsWithCuts(
        t, 
        "ECAL eta region 2:",
        "(0<abs(eta1) && abs(eta1)<1.0) && (0<abs(eta2) && abs(eta2)<1.0) && pterr1/pT1>0.03 && pterr2/pT2>0.03 && lep1_ecalDriven==1 && lep2_ecalDriven==1",
        "[0, 1.0]\trel_pTErr > 3%:"
        )
    print

    # Region 3
    n_ecal_reg3a = countEventsWithCuts(
        t, 
        "ECAL eta region 3a:",
        "(1.0<abs(eta1) && abs(eta1)<1.2) && (1.0<abs(eta2) && abs(eta2)<1.2) && pterr1/pT1<0.07 && pterr2/pT2<0.07 && lep1_ecalDriven==1 && lep2_ecalDriven==1",
        "[1.0, 1.2]\trel_pTErr < 7%:"
        )

    n_ecal_reg3b = countEventsWithCuts(
        t, 
        "ECAL eta region 3b:",
        "(1.2<abs(eta1) && abs(eta1)<1.44) && (1.2<abs(eta2) && abs(eta2)<1.44) && pterr1/pT1<0.07 && pterr2/pT2<0.07 && lep1_ecalDriven==1 && lep2_ecalDriven==1",
        "[1.2, 1.44]\trel_pTErr < 7%:"
        )

    n_ecal_reg3c = countEventsWithCuts(
        t, 
        "ECAL eta region 3c:",
        "(1.44<abs(eta1) && abs(eta1)<1.57) && (1.44<abs(eta2) && abs(eta2)<1.57) && pterr1/pT1<0.07 && pterr2/pT2<0.07 && lep1_ecalDriven==1 && lep2_ecalDriven==1",
        "[1.44, 1.57]\trel_pTErr < 7%:"
        )

    n_ecal_reg3d = countEventsWithCuts(
        t, 
        "ECAL eta region 3d:",
        "(1.57<abs(eta1) && abs(eta1)<2.0) && (1.57<abs(eta2) && abs(eta2)<2.0) && pterr1/pT1<0.07 && pterr2/pT2<0.07 && lep1_ecalDriven==1 && lep2_ecalDriven==1",
        "[1.57, 2.0]\trel_pTErr < 7%:"
        )

    n_ecal_reg3e = countEventsWithCuts(
        t, 
        "ECAL eta region 3e:",
        "(2.0<abs(eta1) && abs(eta1)<2.5) && (2.0<abs(eta2) && abs(eta2)<2.5) && pterr1/pT1<0.07 && pterr2/pT2<0.07 && lep1_ecalDriven==1 && lep2_ecalDriven==1",
        "[2.0, 2.5]\trel_pTErr < 7%:"
        )
    print

    # Region 4
    n_ecal_reg4 = countEventsWithCuts(
        t, 
        "ECAL eta region 4:",
        "(1.0<abs(eta1) && abs(eta1)<1.2) && (1.0<abs(eta2) && abs(eta2)<1.2) && pterr1/pT1>0.07 && pterr2/pT2>0.07 && lep1_ecalDriven==1 && lep2_ecalDriven==1",
        "[1.0, 1.2]\trel_pTErr > 7%:"
        )
    print

    #___________________________________________________________________________
    # TRACKER electrons
    # Region 1
    n_tracker_reg1 = countEventsWithCuts(
        t, 
        "Tracker eta region 1:",
        "(0<abs(eta1) && abs(eta1)<1.44) && (0<abs(eta2) && abs(eta2)<1.44) && lep1_ecalDriven==0 && lep2_ecalDriven==0",
        "[0, 1.44]:\t"
        )

    # Region 2
    n_tracker_reg2 = countEventsWithCuts(
        t, 
        "Tracker eta region 2:",
        "(1.44<abs(eta1) && abs(eta1)<1.6) && (1.44<abs(eta2) && abs(eta2)<1.6) && lep1_ecalDriven==0 && lep2_ecalDriven==0",
        "[1.44, 1.6]:\t"
        )

    # Region 3
    n_tracker_reg3 = countEventsWithCuts(
        t, 
        "Tracker eta region 3:",
        "(1.6<abs(eta1) && abs(eta1)<2.0) && (1.6<abs(eta2) && abs(eta2)<2.0) && lep1_ecalDriven==0 && lep2_ecalDriven==0",
        "[1.6, 2.0]:\t"
        )

    # Region 4
    n_tracker_reg4 = countEventsWithCuts(
        t, 
        "Tracker eta region 4:",
        "(2.0<abs(eta1) && abs(eta1)<2.5) && (2.0<abs(eta2) && abs(eta2)<2.5) && lep1_ecalDriven==0 && lep2_ecalDriven==0",
        "[2.0, 2.5]:\t"
        )
    print
#___________________________________________________________________________
#########
# MUONS #
#########
else:
    # Region 1
    n_muons_reg1 = countEventsWithCuts(
        t, 
        "Muon eta region 1:",
        "(0<abs(eta1) && abs(eta1)<0.9) && (0<abs(eta2) && abs(eta2)<0.9)",
        "[0, 0.9]:\t"
        )

    # Region 2
    n_muons_reg2 = countEventsWithCuts(
        t, 
        "Muon eta region 2:",
        "(0.9<abs(eta1) && abs(eta1)<1.8) && (0.9<abs(eta2) && abs(eta2)<1.8)",
        "[0.9, 1.8]:\t"
        )

    # Region 3
    n_muons_reg3 = countEventsWithCuts(
        t, 
        "Muon eta region 3:",
        "(1.8<abs(eta1) && abs(eta1)<2.4) && (1.8<abs(eta2) && abs(eta2)<2.4)",
        "[1.8, 2.4]:\t"
        )
    print
