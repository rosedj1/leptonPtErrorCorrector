############################################################################
## PURPOSE: Count the number of events in each relative pT error vs. eta region for muons,
##          tracker electrons, and ECAL electrons in a skimmed NTuple. 
## SYNTAX:  python <script.py> <inputfile.root> <finalstate>
## NOTES:   The NTuple should have branches like: massZ, massZErr, pT1, etc.
##          - <finalstate> must either be "2e" or "2mu"
## AUTHOR:  Jake Rosenzweig
## DATE:    2019-06-21
## UPDATED: 2019-08-08
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
# Limited stats check: n_kinematic_bin/n_total*100% < lim_stats_percentage
lim_stats_percentage = 0.05

if fs not in ["2e","2mu"]:
    print 'ERROR: You must pass in either "2e" or "2mu"'
    sys.exit()
#___________________________________________________________________________
# Definitions of kinematic bins:
ECAL_reg_1a_lep1_cuts = "0<abs(eta1) && abs(eta1)<0.8 && pterr1/pT1<0.03 && lep1_ecalDriven==1"
ECAL_reg_1a_lep2_cuts = "0<abs(eta2) && abs(eta2)<0.8 && pterr2/pT2<0.03 && lep2_ecalDriven==1"
ECAL_reg_1a_cuts = ECAL_reg_1a_lep1_cuts +" && "+ ECAL_reg_1a_lep2_cuts

ECAL_reg_1b_lep1_cuts = "0.8<abs(eta1) && abs(eta1)<1.0 && pterr1/pT1<0.03 && lep1_ecalDriven==1"
ECAL_reg_1b_lep2_cuts = "0.8<abs(eta2) && abs(eta2)<1.0 && pterr2/pT2<0.03 && lep2_ecalDriven==1"
ECAL_reg_1b_cuts = ECAL_reg_1b_lep1_cuts +" && "+ ECAL_reg_1b_lep2_cuts

ECAL_reg_2_lep1_cuts = "0<abs(eta1) && abs(eta1)<1.0 && pterr1/pT1>0.03 && lep1_ecalDriven==1"
ECAL_reg_2_lep2_cuts = "0<abs(eta2) && abs(eta2)<1.0 && pterr2/pT2>0.03 && lep2_ecalDriven==1"
ECAL_reg_2_cuts  = ECAL_reg_2_lep1_cuts +" && "+ ECAL_reg_2_lep2_cuts

ECAL_reg_3a_lep1_cuts = "1.0<abs(eta1) && abs(eta1)<1.2 && pterr1/pT1<0.07 && lep1_ecalDriven==1"
ECAL_reg_3a_lep2_cuts = "1.0<abs(eta2) && abs(eta2)<1.2 && pterr2/pT2<0.07 && lep2_ecalDriven==1"
ECAL_reg_3a_cuts = ECAL_reg_3a_lep1_cuts +" && "+ ECAL_reg_3a_lep2_cuts

ECAL_reg_3b_lep1_cuts = "1.2<abs(eta1) && abs(eta1)<1.44 && pterr1/pT1<0.07 && lep1_ecalDriven==1"
ECAL_reg_3b_lep2_cuts = "1.2<abs(eta2) && abs(eta2)<1.44 && pterr2/pT2<0.07 && lep2_ecalDriven==1"
ECAL_reg_3b_cuts = ECAL_reg_3b_lep1_cuts +" && "+ ECAL_reg_3b_lep2_cuts

ECAL_reg_3c_lep1_cuts = "1.44<abs(eta1) && abs(eta1)<1.57 && pterr1/pT1<0.07 && lep1_ecalDriven==1"
ECAL_reg_3c_lep2_cuts = "1.44<abs(eta2) && abs(eta2)<1.57 && pterr2/pT2<0.07 && lep2_ecalDriven==1"
ECAL_reg_3c_cuts = ECAL_reg_3c_lep1_cuts +" && "+ ECAL_reg_3c_lep2_cuts

ECAL_reg_3d_lep1_cuts = "1.57<abs(eta1) && abs(eta1)<2.0 && pterr1/pT1<0.07 && lep1_ecalDriven==1"
ECAL_reg_3d_lep2_cuts = "1.57<abs(eta2) && abs(eta2)<2.0 && pterr2/pT2<0.07 && lep2_ecalDriven==1"
ECAL_reg_3d_cuts = ECAL_reg_3d_lep1_cuts +" && "+ ECAL_reg_3d_lep2_cuts

ECAL_reg_3e_lep1_cuts = "2.0<abs(eta1) && abs(eta1)<2.5 && pterr1/pT1<0.07 && lep1_ecalDriven==1"
ECAL_reg_3e_lep2_cuts = "2.0<abs(eta2) && abs(eta2)<2.5 && pterr2/pT2<0.07 && lep2_ecalDriven==1"
ECAL_reg_3e_cuts = ECAL_reg_3e_lep1_cuts +" && "+ ECAL_reg_3e_lep2_cuts

ECAL_reg_4_lep1_cuts = "1.0<abs(eta1) && abs(eta1)<1.2 && pterr1/pT1>0.07 && lep1_ecalDriven==1"
ECAL_reg_4_lep2_cuts = "1.0<abs(eta2) && abs(eta2)<1.2 && pterr2/pT2>0.07 && lep2_ecalDriven==1"
ECAL_reg_4_cuts = ECAL_reg_4_lep1_cuts +" && "+ ECAL_reg_4_lep2_cuts

Tracker_reg_1_lep1_cuts = "0<abs(eta1) && abs(eta1)<1.44 && lep1_ecalDriven==0"
Tracker_reg_1_lep2_cuts = "0<abs(eta2) && abs(eta2)<1.44 && lep2_ecalDriven==0"
Tracker_reg_1_cuts = Tracker_reg_1_lep1_cuts +" && "+ Tracker_reg_1_lep2_cuts

Tracker_reg_2_lep1_cuts = "1.44<abs(eta1) && abs(eta1)<1.6 && lep1_ecalDriven==0"
Tracker_reg_2_lep2_cuts = "1.44<abs(eta2) && abs(eta2)<1.6 && lep2_ecalDriven==0"
Tracker_reg_2_cuts = Tracker_reg_2_lep1_cuts +" && "+ Tracker_reg_2_lep2_cuts

Tracker_reg_3_lep1_cuts = "1.6<abs(eta1) && abs(eta1)<2.0 && lep1_ecalDriven==0"
Tracker_reg_3_lep2_cuts = "1.6<abs(eta2) && abs(eta2)<2.0 && lep2_ecalDriven==0"
Tracker_reg_3_cuts = Tracker_reg_3_lep1_cuts +" && "+ Tracker_reg_3_lep2_cuts

Tracker_reg_4_lep1_cuts = "2.0<abs(eta1) && abs(eta1)<2.5 && lep1_ecalDriven==0"
Tracker_reg_4_lep2_cuts = "2.0<abs(eta2) && abs(eta2)<2.5 && lep2_ecalDriven==0"
Tracker_reg_4_cuts = Tracker_reg_4_lep1_cuts +" && "+ Tracker_reg_4_lep2_cuts

Muon_reg_1_cuts = "(0<abs(eta1) && abs(eta1)<0.9) && (0<abs(eta2) && abs(eta2)<0.9)"
Muon_reg_2_cuts = "(0.9<abs(eta1) && abs(eta1)<1.8) && (0.9<abs(eta2) && abs(eta2)<1.8)"
Muon_reg_3_cuts = "(1.8<abs(eta1) && abs(eta1)<2.4) && (1.8<abs(eta2) && abs(eta2)<2.4)"

# Only allowed to apply limited statistic procedure to ECAL reg 2,4 and all Tracker regions.
lim_stat_ECAL_reg_1a_AND_ECAL_reg_2_cuts    = "("+ ECAL_reg_1a_lep1_cuts +" && "+ ECAL_reg_2_lep2_cuts +") || ("+ ECAL_reg_2_lep1_cuts +" && "+ ECAL_reg_1a_lep2_cuts +")"
lim_stat_ECAL_reg_1a_AND_ECAL_reg_4_cuts    = "("+ ECAL_reg_1a_lep1_cuts +" && "+ ECAL_reg_4_lep2_cuts +") || ("+ ECAL_reg_4_lep1_cuts +" && "+ ECAL_reg_1a_lep2_cuts +")"
lim_stat_ECAL_reg_1a_AND_Tracker_reg_1_cuts = "("+ ECAL_reg_1a_lep1_cuts +" && "+ Tracker_reg_1_lep2_cuts +") || ("+ Tracker_reg_1_lep1_cuts +" && "+ ECAL_reg_1a_lep2_cuts +")"
lim_stat_ECAL_reg_1a_AND_Tracker_reg_2_cuts = "("+ ECAL_reg_1a_lep1_cuts +" && "+ Tracker_reg_2_lep2_cuts +") || ("+ Tracker_reg_2_lep1_cuts +" && "+ ECAL_reg_1a_lep2_cuts +")"
lim_stat_ECAL_reg_1a_AND_Tracker_reg_3_cuts = "("+ ECAL_reg_1a_lep1_cuts +" && "+ Tracker_reg_3_lep2_cuts +") || ("+ Tracker_reg_3_lep1_cuts +" && "+ ECAL_reg_1a_lep2_cuts +")"
lim_stat_ECAL_reg_1a_AND_Tracker_reg_4_cuts = "("+ ECAL_reg_1a_lep1_cuts +" && "+ Tracker_reg_4_lep2_cuts +") || ("+ Tracker_reg_4_lep1_cuts +" && "+ ECAL_reg_1a_lep2_cuts +")"
#___________________________________________________________________________
# Functions
def countEventsWithCuts(tree, region, cuts, text):
    n_events = tree.GetEntries(cuts)
    perc_of_total = n_events*100./ntot  # Percentage of total events
    print "%s\t%s\t%d\tevents, which is\t%.6f%%\tof total events" % (region,text,n_events,perc_of_total)
    return n_events, perc_of_total
    #sys.exit()
#___________________________________________________________________________
# MAIN
print "\nTotal events in NTuple:", ntot

#############
# ELECTRONS #
#############
if fs == "2e":
    print "Counting pairs of electrons:"
    #___________________________________________________________________________
    # ECAL electrons
    n_ecal_reg1a, perc_ecal_reg1a = countEventsWithCuts( t, "ECAL_region_1a:", ECAL_reg_1a_cuts, "[0, 0.8]\trel_pTErr < 3%:")
    n_ecal_reg1b, perc_ecal_reg1b = countEventsWithCuts( t, "ECAL_region_1b:", ECAL_reg_1b_cuts, "[0.8, 1.0]\trel_pTErr < 3%:")
    print

    n_ecal_reg2, perc_ecal_reg2 = countEventsWithCuts( t, "ECAL_region_2:", ECAL_reg_2_cuts, "[0, 1.0]\trel_pTErr > 3%:")
    print

    n_ecal_reg3a, perc_ecal_reg3a = countEventsWithCuts( t, "ECAL_region_3a:", ECAL_reg_3a_cuts, "[1.0, 1.2]\trel_pTErr < 7%:")
    n_ecal_reg3b, perc_ecal_reg3b = countEventsWithCuts( t, "ECAL_region_3b:", ECAL_reg_3b_cuts, "[1.2, 1.44]\trel_pTErr < 7%:")
    n_ecal_reg3c, perc_ecal_reg3c = countEventsWithCuts( t, "ECAL_region_3c:", ECAL_reg_3c_cuts, "[1.44, 1.57]\trel_pTErr < 7%:")
    n_ecal_reg3d, perc_ecal_reg3d = countEventsWithCuts( t, "ECAL_region_3d:", ECAL_reg_3d_cuts, "[1.57, 2.0]\trel_pTErr < 7%:")
    n_ecal_reg3e, perc_ecal_reg3e = countEventsWithCuts( t, "ECAL_region_3e:", ECAL_reg_3e_cuts, "[2.0, 2.5]\trel_pTErr < 7%:")
    print

    n_ecal_reg4, perc_ecal_reg4 = countEventsWithCuts( t, "ECAL_region_4:", ECAL_reg_4_cuts, "[1.0, 1.2]\trel_pTErr > 7%:")
    print

    ##___________________________________________________________________________
    ## TRACKER electrons
    n_tracker_reg1, perc_tracker_reg1 = countEventsWithCuts( t, "Tracker_region_1:", Tracker_reg_1_cuts, "[0, 1.44]:\t")
    n_tracker_reg2, perc_tracker_reg2 = countEventsWithCuts( t, "Tracker_region_2:", Tracker_reg_2_cuts, "[1.44, 1.6]:\t")
    n_tracker_reg3, perc_tracker_reg3 = countEventsWithCuts( t, "Tracker_region_3:", Tracker_reg_3_cuts, "[1.6, 2.0]:\t")
    n_tracker_reg4, perc_tracker_reg4 = countEventsWithCuts( t, "Tracker_region_4:", Tracker_reg_4_cuts, "[2.0, 2.5]:\t")
    print

    #___________________________________________________________________________
    ######################
    # LIMITED STATISTICS #
    ######################
    def countEventsInLimitedStatsRegion(t,new_region,old_region,cuts,text,old_nevents,old_perc):
        """
        This function should print out all necessary information about limited stats regions.
        """
        if old_perc <= lim_stats_percentage: 
            print "WARNING! Limited statistics found in region: %s" % new_region
            print "(percentage of events in this region is < %.3f)" % lim_stats_percentage
            print "Using limited statistics procedure to increase statistics..."
            
            n_events, new_perc = countEventsWithCuts(t,new_region,cuts,text)
            print "Old region percentage of total events compared to new region percentage: %.6f\tvs.\t%.6f" % (old_perc,new_perc)
            print "%s has %.3f more events than %s\n" % (new_region, float(n_events)/old_nevents, old_region)

            return n_events, new_perc

        else: return
        

    countEventsInLimitedStatsRegion(
                      t,
                      "Limited_stats_ECAL_region_1a_AND_ECAL_region_2:",
                      "ECAL_region_2:",
                      lim_stat_ECAL_reg_1a_AND_ECAL_reg_2_cuts,
                      "EMPTYTEXT\t", 
                      n_ecal_reg2,
                      perc_ecal_reg2
                  )

    countEventsInLimitedStatsRegion(
                      t,
                      "Limited_stats_ECAL_region_1a_AND_ECAL_region_4:",
                      "ECAL_region_4:",
                      lim_stat_ECAL_reg_1a_AND_ECAL_reg_4_cuts,
                      "EMPTYTEXT\t",
                      n_ecal_reg4,
                      perc_ecal_reg4
                  )

    countEventsInLimitedStatsRegion(
                      t,
                      "Limited_stats_ECAL_region_1a_AND_Tracker_region_1:",
                      "Tracker_region_1:",
                      lim_stat_ECAL_reg_1a_AND_Tracker_reg_1_cuts,
                      "EMPTYTEXT\t",
                      n_tracker_reg1,
                      perc_tracker_reg1
                  )

    countEventsInLimitedStatsRegion(
                      t,
                      "Limited_stats_ECAL_region_1a_AND_Tracker_region_2:",
                      "Tracker_region_2:",
                      lim_stat_ECAL_reg_1a_AND_Tracker_reg_2_cuts,
                      "EMPTYTEXT\t",
                      n_tracker_reg2,
                      perc_tracker_reg2
                  )

    countEventsInLimitedStatsRegion(
                      t,
                      "Limited_stats_ECAL_region_1a_AND_Tracker_region_3:",
                      "Tracker_region_3:",
                      lim_stat_ECAL_reg_1a_AND_Tracker_reg_3_cuts,
                      "EMPTYTEXT\t",
                      n_tracker_reg3,
                      perc_tracker_reg3
                  )

    countEventsInLimitedStatsRegion(
                      t,
                      "Limited_stats_ECAL_region_1a_AND_Tracker_region_4:",
                      "Tracker_region_4:",
                      lim_stat_ECAL_reg_1a_AND_Tracker_reg_4_cuts,
                      "EMPTYTEXT\t",
                      n_tracker_reg4,
                      perc_tracker_reg4
                  )

#___________________________________________________________________________
#########
# MUONS #
#########
else:
    print "Counting pairs of muons:"
    n_muons_reg1, perc_muons_reg1 = countEventsWithCuts( t, "Muon_region_1:", Muon_reg_1_cuts, "[0, 0.9]:\t")
    n_muons_reg2, perc_muons_reg2 = countEventsWithCuts( t, "Muon_region_2:", Muon_reg_2_cuts, "[0.9, 1.8]:\t")
    n_muons_reg3, perc_muons_reg3 = countEventsWithCuts( t, "Muon_region_3:", Muon_reg_3_cuts, "[1.8, 2.4]:\t")
    print
