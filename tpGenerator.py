import numpy as np
import matplotlib.pyplot as plt
from include.TriggerPrimitive import TriggerPrimitive as TriggerPrimitive
from include.TPFinder import TPFinder as TPFinder
import sys

#load waveform data (100 low energy electron events, 5 - 100 MeV)
col = np.loadtxt("/eos/home-e/evilla/dune/sn-data/standard/aggregated_prodmarley_nue_spectrum_radiological_decay0_dune10kt_refactored_1x2x6_CC-WFdump-1events_thr30/waveforms_tryWfDumper.txt")
ind = np.loadtxt("data/PedSubWaveform_Induction_Dump.txt")
#
col = col - 500

event = 2
threshold = 30

#plot collection waveforms from event
offset = 0
for data in col:
    ADCS = data[2:]
    hits = TPFinder(ADCS, threshold)
    print(hits)
    #add hits to new row od textfile
       
