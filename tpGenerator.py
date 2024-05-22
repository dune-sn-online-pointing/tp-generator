import numpy as np
import matplotlib.pyplot as plt
from include.TriggerPrimitive import TriggerPrimitive as TriggerPrimitive
from include.TPFinder import TPFinder as TPFinder
import sys

#load waveform data (100 low energy electron events, 5 - 100 MeV)
col = np.loadtxt("/eos/home-e/evilla/dune/sn-data/standard/aggregated_prodmarley_nue_spectrum_radiological_decay0_dune10kt_refactored_1x2x6_CC-WFdump-1events_thr30/waveforms_tryWfDumper.txt")
ind = np.loadtxt("data/PedSubWaveform_Induction_Dump.txt")

    #add hits to new row od textfile
       
event = 1
threshold = 30
#returns recovered area (not including adc_integral)
def recover_area(hit): 
    x1,y1,x2,y2= hit.time_start,threshold,hit.time_peak+hit.time_start,hit.adc_peak 
    slope = (y2-y1)/(x2-x1)
    start_x =(0-y1)/slope + x1
    end_x = x1
    
    #x_values = np.linspace(start_x, end_x, 100)
    #y_values = slope * (x_values - x1) + y1
    area_left = (np.abs(start_x-end_x)*threshold)/2  #formula for triangle area

    #Find Equation of Negative Slope Line (Right Side)
    x1,y1,x2,y2= hit.time_start+hit.time_over_threshold,threshold,hit.time_peak+hit.time_start,hit.adc_peak 
    slope = (y2-y1)/(x2-x1)
    start_x = x1
    end_x = (0-y1)/slope + x1
    #x_values = np.linspace(start_x, end_x, 100)
    #y_values = slope * (x_values - x1) + y1
    area_right = (np.abs(start_x-end_x)*threshold)/2  #formula for triangle area
    total_area = area_right+area_left
    return total_area




recovered_area_list = []
#plot collection waveforms from event
fig1 = plt.figure()
offset = 0
count = 0
adc_integral = []
adc_plus_recovered = []
for data in col:
    pedestal = np.mean(data[3:15])
    data[2:] = data[2:] - pedestal
    if (data[0]==event):
        ADCS = data[2:]
        hits = TPFinder(ADCS, threshold)
        print(hits)
        for hit in hits:
            recovered_area = recover_area(hit)
            recovered_area_list.append(recovered_area)
            adc_integral.append(hit.adc_integral)
            adc_plus_recovered.append(recovered_area + hit.adc_integral)