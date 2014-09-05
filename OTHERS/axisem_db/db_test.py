from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
from obspy import UTCDateTime, read, Trace
from obspy.core.util import locations2degrees
import scipy.io
import subprocess

t1 = datetime.now()
from axisem_db import AxiSEMDB, Source, Receiver
print 'import time: %s' % (datetime.now() - t1)



db_add = '/import/neptun-dunkles/hosseini/AXISEM_DB_IASP91/2s_iasp_symplec'

ev_time = UTCDateTime(0)

plt.ion()
plt.figure()

t1 = datetime.now()
axisem_db = AxiSEMDB(db_add)
print 'axisem_db time: %s' % (datetime.now() - t1)

stf_matlab = scipy.io.loadmat('./STF.mat')
all_stf = stf_matlab['STF']
all_time = stf_matlab['TAX']
num_stf = len(all_stf[0])

STF = []
for j in range(num_stf):
    tmp_STF = np.array([])
    time_keeper = 0
    for i in range(0, len(all_stf)):
        if all_stf[i][j] == 0:
                time_keeper += 1
                continue
        if len(tmp_STF) == 0:
                tmp_STF = np.array([all_stf[i][j]])
        else:
                tmp_STF = np.append(tmp_STF, all_stf[i][j])
    stats = {'network': 'STF', 
             'station': 'STF' + str(j), 
             'location': '',
             'channel': '00', 
             'npts': len(tmp_STF), 
             'delta': (all_time[-1][j] - all_time[0][j])/(len(all_time)-1),
             'starttime': (ev_time + all_time[0][j] + stf_matlab['dt_group']),
             'mseed' : {'dataquality': 'D'}}
    STF_tr = Trace(data=tmp_STF, header=stats)
    STF_tr.taper()
    STF.append(STF_tr)

receiver = Receiver(latitude=42.6390, longitude=74.4940)

source = Source(
    latitude=89.91, longitude=0.0, depth_in_m=12000,
    m_rr = 4.710000e+24 / 1E7,
    m_tt = 3.810000e+22 / 1E7,
    m_pp =-4.740000e+24 / 1E7,
    m_rt = 3.990000e+23 / 1E7,
    m_rp =-8.050000e+23 / 1E7,
    m_tp =-1.230000e+24 / 1E7, 
    time_shift=STF[0].stats.starttime - ev_time - 3,
    dt=STF[0].stats.delta,
    sliprate = STF[0].data)
source.resample_sliprate(dt=axisem_db.dt, nsamp=axisem_db.ndumps)
st = axisem_db.get_seismograms(source=source, receiver=receiver, 
                                reconvolve_stf=True)
plt.plot(np.linspace(0, (st[0].stats.npts-1)/st[0].stats.sampling_rate, st[0].stats.npts), st[0].data, c='r')
req_phase = ['P', 'Pdiff', 'PP', 'PcP']

dist = locations2degrees(source.latitude, source.longitude, receiver.latitude, receiver.longitude)

for pha in req_phase:
    taup_process = subprocess.Popen(['taup_time', '-mod', axisem_db.background_model, '-time', '-h', str(source.depth_in_m/1000.),
                                     '-ph', pha, '-deg', str(dist)], stdout=subprocess.PIPE)
    tt_raw = taup_process.communicate()[0]
    try:
        tt = tt_raw.split('\n')[0].split()[-1]
        if tt:
            tt = float(tt)
            plt.vlines(tt, min(st[0].data), max(st[0].data))
    except Exception, e:
        print '-',



source = Source(
    latitude=89.91, longitude=0.0, depth_in_m=12000,
    m_rr = 4.710000e+24 / 1E7,
    m_tt = 3.810000e+22 / 1E7,
    m_pp =-4.740000e+24 / 1E7,
    m_rt = 3.990000e+23 / 1E7,
    m_rp =-8.050000e+23 / 1E7,
    m_tp =-1.230000e+24 / 1E7, 
    time_shift=STF[0].stats.starttime - ev_time,
    dt=STF[0].stats.delta,
    sliprate = STF[0].data)
source.resample_sliprate(dt=axisem_db.dt, nsamp=axisem_db.ndumps)
st = axisem_db.get_seismograms(source=source, receiver=receiver, 
                                reconvolve_stf=True, dt=0.1)
plt.plot(np.linspace(0, (st[0].stats.npts-1)/st[0].stats.sampling_rate, st[0].stats.npts), st[0].data, c='b')


print st
