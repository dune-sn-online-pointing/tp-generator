import numpy as np
from .TriggerPrimitive import TriggerPrimitive

#-------------------------------------------
#Primitive hit finding
#-------------------------------------------
def TPFinder(waveform, thresh):
    is_hit = False

    hit_charge =[]    
    this_hit = TriggerPrimitive()
   
    hits = []

    for tick, adc  in enumerate(waveform):
        if (adc > thresh and is_hit==False):
            is_hit = True
            this_hit.time_start =tick
           
        if(is_hit == True):
            hit_charge.append(adc)
           
        if (is_hit and adc<thresh):
            time_end  = tick
            is_hit = False
           
            for index, ADC in enumerate(hit_charge):
                if (ADC == np.max(hit_charge)):
                    this_hit.adc_peak = ADC
                    this_hit.time_peak = index
            this_hit.adc_integral = np.sum(hit_charge)
            this_hit.time_over_threshold = time_end - this_hit.time_start
            hits.append(this_hit)

            #clean up for next hit
            hit_charge = []
            this_hit = TriggerPrimitive()
            
    return hits #return set of hits for waveform
