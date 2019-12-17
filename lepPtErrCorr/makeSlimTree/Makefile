CXX=g++
CC=gcc
CFLAGS=-O2 -Wall
LDFLAGS=-Llib
PRFFLAGS=-lProof
THRDFLAGS=-lThread
INS=-I$(ROOTSYS)/include
INS2=-I$(ROOFITSYS)/include
INS3=-I$(ROOSTATSYS)/include
INSS=-I./include
INSSS=-I.

LD1=-L$(ROOFITSYS)/lib

CFLAGS += `root-config --cflags`
LIBS += `root-config --ldflags --glibs`
LIBS += -L$(ROOFITSYS)/lib -lRooFit -lRooFitCore -lRooStats
LDFLAGS=`root-config -ldflags glibs` -lRooFit -lRooFitCore -lMinuit

LDa=-lRooFitCore
LDb=-lRooFit

OBJ=DY_TreeSlim.o
OBJ1=DY_MerrCorrection.o
OBJ2=DY_MerrCorrection_SimFit.o

libHiggsAnalysisCombinedLimit=${CMSSW_BASE}/lib/slc6_amd64_gcc493/libHiggsAnalysisCombinedLimit.so

.PHONY: clean all main test

all: DY_TreeSlim 

DY_TreeSlim: DY_TreeSlim.o
	$(CXX) -o DY_TreeSlim.exe $(OBJ) $(LIBS)

#DY_MerrCorrection: DY_MerrCorrection.o
#	$(CXX) -o DY_MerrCorrection.exe $(OBJ1) $(LIBS) $(libHiggsAnalysisCombinedLimit)

#DY_MerrCorrection_SimFit: DY_MerrCorrection_SimFit.o
#	$(CXX) -o DY_MerrCorrection_SimFit.exe $(OBJ2) $(LIBS)


clean:
	@rm *.o *.exe

##############RULES##############
.cc.o:
	$(CXX) $(CFLAGS) $(INS) $(INS2) $(INS3) $(INSS) ${INSSS} -c $<
.cpp.o:
	$(CXX) $(CFLAGS) $(INS) -c $<

