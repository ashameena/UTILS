# Simple script to plot the number of event-station pairs for each 
# Dominant period

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

'''
The term microseism refers to ocean-wave generated
seismic signals in two frequency bands, that of ocean gravity
waves (0.04, 0.17 Hz), known as primary microseisms (PM),
and a higher frequency band at twice the ocean wave fre-
quency (0.08, 0.34 Hz), known as double-frequency (DF)
microseisms.
'''

microseism_freq_low = 1/10.
microseism_freq_high = 1/5.

micro_time_high = 1./microseism_freq_low
micro_time_low = 1./microseism_freq_high

x_label = 'Dominant Period (sec)'
y_label = 'nr of source-recever pairs'

x = [2.7, 3.7, 5.3, 7.5, 10.6, 15.0, 21.2, 30.0]
y = np.array([70647, 62283, 50295, 44891, 54719, 72781, 87370, 93204])

fig = plt.figure()
ax = fig.add_subplot(1,1,1)

plt.plot(x,y,'o-', lw = 3, markersize = 8, c = '0.0')
rect = patches.Rectangle((micro_time_low,40000), width=micro_time_high - micro_time_low,
                            height=60000, color='yellow', alpha=0.5)
ax.add_patch(rect)

plt.vlines(micro_time_low, 40000, 100000, linestyle='--')
plt.vlines(micro_time_high, 40000, 100000, linestyle='--')


x_ticks = [2.7, 5.3, 7.5, 10.6, 15.0, 21.2, 30.0]
plt.xlabel(x_label, size = 'xx-large', weight = 'bold')
plt.ylabel(y_label, size = 'xx-large', weight = 'bold')
plt.xticks(x_ticks, fontsize = 'xx-large', weight = 'bold')
plt.yticks(fontsize = 'xx-large', weight = 'bold')
plt.xlim(1.7, 31)
plt.ylim(40000, 100000)

plt.show()

