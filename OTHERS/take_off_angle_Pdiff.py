# This is a simple script for plotting the take-off angle of
# different seismic phases

import matplotlib.pyplot as plt
import numpy as np
from obspy import taup

seismic_phase = ['P', 'Pdiff']
min_degree = 90.
max_degree = 180.
step_degree = 1.
evdepth = 0.

dist_pdiff = []
dist_all = []
take_off = []

for dist in np.arange(min_degree, max_degree, step_degree):
    flag = False
    tt = taup.getTravelTimes(delta=dist, depth=evdepth)
    for i in range(len(tt)):
        if tt[i]['phase_name'] in seismic_phase:
            flag = True
            take_off_tmp = tt[i]['take-off angle']
            time_tmp = tt[i]['time']
            if tt[i]['phase_name'] == 'Pdiff':
                dist_pdiff.append(dist)
            break
    if flag: 
        take_off.append(take_off_tmp)
        dist_all.append(dist)

plt.plot(dist_all, take_off, lw=3)
plt.xlabel('Distance (deg)', size='large', weight='bold')
plt.ylabel('Take-off angle', size='large', weight='bold')
plt.xticks(size='large', weight='bold')
plt.yticks(size='large', weight='bold')
if dist_pdiff:
    plt.vlines(dist_pdiff[0], min(take_off)-0.05*min(take_off), 
                                max(take_off)+0.05*max(take_off))
    print 'WARNING: vertical line is just the FIRST occurance of Pdiff'
titex = 'Depth: %s' %(evdepth)
plt.title(titex, size='large', weight='bold')
plt.show()
