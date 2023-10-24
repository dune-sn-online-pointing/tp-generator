import numpy as np
from dataclasses import dataclass
import datetime

#-------------------------------------------
#Constants
#-------------------------------------------

# these are taken from https://github.com/DUNE-DAQ/trgdataformats/blob/develop/include/trgdataformats/Types.hpp
# TODO change data types to proper ones (uint32_t, etc)

INVALID_TIMESTAMP = datetime.datetime.max   # uint64_t
INVALID_CHANNEL = 0xFFFFFFFF                # uint32_t
INVALID_VERSION = 0XFFF                     # uint16_t
INVALID_DETIT = 0XFFF                       # uint16_t

#-------------------------------------------
#TriggerPrimitive struct
#-------------------------------------------

# format consistent with the header TriggerPrimitive.hpp: 
# https://github.com/DUNE-DAQ/trgdataformats/blob/develop/include/trgdataformats/TriggerPrimitive.hpp, 
# as of 2021-10-24

@dataclass
class TriggerPrimitive :
    time_start:             int = INVALID_TIMESTAMP
    time_peak:              int = INVALID_TIMESTAMP
    time_over_threshold:    int = INVALID_TIMESTAMP
    channel:                int = INVALID_CHANNEL
    adc_integral:           int = 0                     # probably this should be something else, but it's 0 in the header
    adc_peak:               int = 0                     # probably this should be something else, but it's 0 in the header
    detid :                 int = INVALID_DETIT 
    type :                  int = 0
    algorithm :             int = 0                     # proposal is 1 for fixed thr, 2 for RMS based thr. Neg values for offline
    version :               int = 1
    flags :                 int = 0                     # unused for the moment
    