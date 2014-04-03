"""
Simple script to change the format from seismic data (seed, sac and...) to ASCII
Format:
Time,Data
"""
import glob
import numpy as np
from obspy import read
import os

# --------- INPUT ---------------
identity = './*.*.B*'
# Freq for low-pass filtering
freq = 1/10.
# -------------------------------

add = glob.glob(identity)

for i in range(len(add)):
    base_name = os.path.basename(add[i])
    st = read(add[i])

    # Processing
    st.taper()
    st.filter('lowpass', freq=freq)
    # end of processing!

    st_time = np.linspace(0, (st[0].stats.npts-1)/st[0].stats.sampling_rate, st[0].stats.npts)

    st_fio = open(os.path.join('.', base_name + '.dat'), 'w')
    for j in range(len(st_time)):
        st_fio.writelines('%s,%s\n' % (st_time[j], st[0].data[j]))
    st_fio.close
