import numpy as np
import matplotlib.pyplot as plt
from include.TriggerPrimitive import TriggerPrimitive as TriggerPrimitive
from include.TPFinder import TPFinder as TPFinder
import sys

#load waveform data (100 low energy electron events, 5 - 100 MeV)
col = np.loadtxt("data/PedSubWaveform_Collection_Dump.txt")
ind = np.loadtxt("data/PedSubWaveform_Induction_Dump.txt")

event = 2
threshold = 30

#plot collection waveforms from event
plt.figure(figsize = (10,6))
offset = 0
for data in col:
    if (data[0]==event):
        ADCS = data[2:]
        plt.title("Collection waveforms (event %.0f)" %event)
        plt.plot(ADCS + offset)#offset by channel number
       
        hits = TPFinder(ADCS, threshold)
        for hit in hits:
            plt.plot(hit.time_start,hit.adc_peak + offset,'o')
           
        plt.text(len(ADCS) + 100, offset, 'channel : %.0f' %data[1])
        offset+=100
        plt.ylabel("Offset Amplitude [ADC]")
        plt.xlabel("Time [ticks]")
plt.show()

#plot induction waveforms for event
plt.figure(figsize = (10,6))
for data in ind:
    if (data[0]==event):
        ADCS = data[2:]
        plt.title("Induction waveforms (event %.0f)" %event)
        plt.plot(ADCS + offset)#offset by channel number
        plt.text(len(ADCS) + 100, offset, 'channel : %.0f' %data[1])
        offset+=100
        plt.ylabel("Offset Amplitude [ADC]")
        plt.xlabel("Time [ticks]")
plt.show()