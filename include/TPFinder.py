import numpy as np
from .TriggerPrimitive import TriggerPrimitive

#-------------------------------------------
#Primitive hit finding
#-------------------------------------------
#This is same function as in TPFinder, put here for testing
def TPFinder(waveform, thresh):

    is_hit = False

    hit_charge =[]    
    this_hit = TriggerPrimitive()
    start_adc = []
    end_adc=[]
    hits = []
    true_adc_areas = []
    for tick, adc  in enumerate(waveform):
        if (adc > thresh and is_hit==False):
            is_hit = True
            this_hit.time_start =tick
            temp_tick = tick
            start_adc.append(adc)
            while (waveform[temp_tick]>0):
                temp_tick = temp_tick - 1
            first_zero = temp_tick
            mean_noise = np.mean(waveform[first_zero-10:first_zero])
            temp_tick = tick
            while (waveform[temp_tick]>mean_noise):
                temp_tick = temp_tick - 1
            true_start = temp_tick
                
                
            '''print(f"True Start: {true_start}")
            print(f"True Start ADC: {waveform[true_start]}")
            print(f"Time Start: {tick}")
            print(f"Time Start ADC: {waveform[tick]}")'''
           
        if(is_hit == True):
            hit_charge.append(adc)
           
        if (is_hit and adc<=thresh):
            time_end  = tick
            is_hit = False
            temp_tick_f = tick
            end_adc.append(waveform[tick-1])
           
            for index, ADC in enumerate(hit_charge):
                if (ADC == np.max(hit_charge)):
                    this_hit.adc_peak = ADC
                    this_hit.time_peak = index
            this_hit.adc_integral = np.sum(hit_charge)
            this_hit.time_over_threshold = time_end - this_hit.time_start
            hits.append(this_hit)
            while(waveform[temp_tick]>mean_noise):
                temp_tick_f+=1
            true_end = temp_tick_f
            '''print(f"True End: {true_end}")
            print(f"True End ADC: {waveform[true_end]}")
            print(f"Time End: {tick}")
            print(f"Time End ADC: {waveform[tick]}")
            '''
            true_adc = 0
            for i in range(true_start,true_end):
                true_adc = true_adc + waveform[i]
            true_adc_areas.append(true_adc)

            #clean up for next hit
            hit_charge = []
            this_hit = TriggerPrimitive()
            
    return hits,true_adc_areas,start_adc,end_adc #return set of hits for waveform
    
