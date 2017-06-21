#!/usr/bin/env python3
"""
Created on Fri May 26 12:50:08 2017

@author: Jackson
"""

import matplotlib.pyplot as plt
import numpy as np
from context import LandauFilm as lf
from context import HysteresisData as hd

plt.close('all')

leakageComp = False
device = 1

### FeFETD1 - FE ###
if device == 0:
    freqdir = r".\testData\FeFETD1\MFS+\die84\FeFETD1_die84_MFS+_100_10x10_freqs"
    tempdir = r".\testData\FeFETD1\MFS+\die84\FeFETD1_die84_MFS+_100_10x10_temps"
    templkgdir = r".\testData\FeFETD1\MFS+\die84\FeFETD1_die84_MFS+_100_10x10_lkg"
    forcFile = r".\testData\FeFETD1\MFS+\die84\FeFETD1_die84_MFS+_100_10x10_forc\FeFETD1_die84_MFS+_100_10x10 0Hz 5V 1Average Table1.tsv"
    t = 10E-7 
    a = 1E-4 # mask defined area that was used in measurement 
    aReal = 8.1E3 # includes effect of undercut during M1 etch
###############

#### FeFETD5 - AFE ###
if device == 1:
    freqdir = r".\testData\FeFETD5\MFS+\die84\FeFETD5_die84_MFS+_60_20x20_freqs"
    tempdir = r".\testData\FeFETD5\MFS+\die84\FeFETD5_die84_MFS+_60_20x20_temps"
    templkgdir = r".\testData\FeFETD5\MFS+\die84\FeFETD5_die84_MFS+_60_20x20_lkg"
    forcFile = r".\testData\FeFETD5\MFS+\die84\FeFETD5_die84_MFS+_60_20x20_FORC\FeFETD5_die68_MFS+_60_20x20_FORC_5V 0Hz 5V 1Average Table2.tsv"
    t = 10E-7
    a = 2.4E-4
    aReal = 2.166E4 # includes effect of undercut during M1 etch
################



tempfiles = hd.dirRead(tempdir)
templkgfiles = hd.dirRead(templkgdir)
if leakageComp:
    tempData = hd.listRead(tempfiles, templkgfiles, plot = False,
                           thickness = t, area = a)
else:
    tempData = hd.listRead(tempfiles, plot = False,
                            thickness = t, area = a)     

freqfiles = hd.dirRead(freqdir)
freqData = hd.listRead(freqfiles)
hfo2 = lf.LandauFull(thickness = t, area = aReal)
cCompData = freqData[1]

hfo2.c = hfo2.cCalc(freqData, plot=1)
compensatedData, hfo2.pr = hfo2.cCompensation(cCompData)
hd.hystPlot([cCompData,compensatedData],
            ['Before C Compensation', 'After Compensation'],
            plotE=False)
freqCompData = list(map(lambda x:hfo2.cCompensation(x)[0],freqData))
hfo2.rhoCalc(freqData)

hfo2.a0 = hfo2.a0Calc(tempData)

freqDataLkgComp = hd.listRead(freqfiles, templkgfiles)
cCompDataLkgComp = freqDataLkgComp[1]
hd.hystPlot([cCompData,cCompDataLkgComp],
            ["With Leakage","Without Leakage"],plotE=False)

### FORC Calculation


hfo2_forc = hd.HysteresisData(thickness = t, area = a)
hfo2_forc.tsvRead(forcFile)
hfo2_forc.hystPlot(plotE=1)
e, er, probs = hfo2_forc.forcCalc(plot = False)
    
domains = hfo2.domainGen(e, er, probs, n=100, plot = False)

esweep = np.linspace(-4.5E6,4.5E6,num=1000)
esweep = np.append(esweep,esweep[::-1])
hfo2.calcEfePreisach(esweep, domains, plot=1)

# Following code plots a series of diff freq hystdata files on same plot

hystData = []
legend = []
for f in freqfiles:
    data = hd.HysteresisData()
    data.tsvRead(f)
#    data.dvdtPlot() # plots dvdt for analysis - unrelated to freq hystPlot
    hystData.append(data)
    legend.append(int(data.freq))

legend = sorted(legend)
hystData = sorted(hystData, key=lambda data: int(data.freq))

legend = [str(x)+' Hz' for x in legend]  
hd.hystPlot(hystData, legend)

# Following code plots a series of diff temp hystdata files on same plot

hystData = []
legend = []
for f in tempfiles:
    data = hd.HysteresisData()
    data.tsvRead(f)
    hystData.append(data)
    legend.append(int(data.temp))

legend = sorted(legend)
hystData = sorted(hystData, key=lambda data: int(data.temp))

legend = [str(x)+' K' for x in legend]  
hd.hystPlot(hystData, legend)

# Following code plots a series of diff temp hystdata files on same plot
# with leakage current subtraction

if leakageComp:
    hystData = []
    legend = []
    for f in tempfiles:
        data = hd.HysteresisData()
        data.tsvRead(f)
        hystData.append(data)
        legend.append(int(data.temp))
    
    legend = sorted(legend)
    hystData = sorted(hystData, key=lambda data: int(data.temp))
    tempData = sorted(tempData, key=lambda data: int(data.temp))
    
    legend = [str(x)+' K' for x in legend]  
    hd.hystPlot(tempData, legend)

# Following code plots a series of diff temp leakagedata files on same plot

leakageData = []
legend = []
for f in templkgfiles:
    data = hd.LeakageData()
    data.lcmRead(f)
    leakageData.append(data)
    legend.append(int(data.temp))

legend = sorted(legend)
leakageData = sorted(leakageData, key=lambda data: int(data.temp))
legend = [str(x)+' K' for x in legend]  
hd.lcmPlot(leakageData, legend)