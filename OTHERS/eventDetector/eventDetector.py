#!/usr/bin/env python
# -*- coding: utf-8 -*-

#-------------------------------------------------------------------
#   Filename:  eventDetector.py
#   Purpose:   eventDetector Main program 
#   Developed: Maria Tsekhmistrenko, Kasra Hosseini
#   License:   GPLv3
#-------------------------------------------------------------------

#-----------------------------------------------------------------------
#----------------Import required Modules (Python and Obspy)-------------
#-----------------------------------------------------------------------

import matplotlib.pyplot as plt
import multiprocessing
import numpy as np
from obspy import read
#from obspy.core.util import locations2degrees
import os
import pickle
from datetime import datetime

# ------------------- INPUT -------------------------
ls_event_file = './event_list'
waveform_dir = '/media/5130-66CF/isolde2012/data-mseed'
# Minimum magnitude to be used
min_mag = 7.6
# Time before the origin time of the event
tb = 300
# Time after the origin time of the event
ta = 4800
# Min Frequency
fmin = 0.002
# Max Frequency
fmax = 0.1
# Number of processes to be used for parallel finding
limit_np = 4
# ---------------------------------------------------

print '\n*** Event detector ***\n'

# Checks whether FIGS directory is already there!
# If not, it will create one.
if not os.path.isdir('./FIGS'):
    os.mkdir('./FIGS')

########################################################################
###################### Functions are defined here ######################
########################################################################

# ------------------- pre_process -------------------
def pre_process(stream, fmin, fmax):
    """
    This function has some pre-processing tools that
    will be applied to the waveforms.
    """
    stream.filter('lowpass', freq=fmax)
    stream.filter('highpass', freq=fmin)
    return stream


# ------------------- find_core --------------------
def find_core(ev_enum, ls_events, sta_num_inp, chan, ta, tb, 
                    fmin, fmax, waveform_dir):
    """
    The main function for finding the events from the continuous data
    ATTENTION: the function is adapted for the folder structure of 
    ISOLDE2012 dataset
    """
    # clear the current figure
    plt.clf()
    # checks whether there is any plot to save! 
    # (refers to plt.save at the end of this function)
    plt_flag = False
    
    # event enumerator
    ev_num = ls_events[ev_enum]
    print '\n***************'
    print 'Event %s/%s' %(ev_enum+1, len(ls_events))
    print '***************'
    
    # station enumerator
    sta_enum = 0
    t_event = ev_num['datetime']
    t_jul = str(t_event.julday)

    # Add some zeros to the first part of julday to create 
    # three digits julday
    if len(t_jul) != 3:
        t_jul = (3-len(t_jul))*'0' + t_jul
    
    # creating the full name for the waveform to read 
    # (refer to ISOLDE2012 format)
    event_date = '*.%s.*.*.%s.%s.*.*.*.seed' %(chan, t_event.year, t_jul)

    for sta_num in sta_num_inp:
        print '%s tdc%s' %(ev_num['datetime'], sta_num),
        sta = 'tdc%s' %sta_num
        sta_enum += 1
        try:
            st = read(os.path.join(waveform_dir, sta, event_date), 
                       starttime = t_event - tb, endtime = t_event + ta, 
                       headonly = True)
            print st[0]
        except Exception, e:
            print '\n--------------------'
            print 'ERROR:'
            print e
            print '--------------------'
            continue

        if st[0].stats.starttime > (t_event - tb):
            t_jul_tmp1 = str(t_event.julday - 1)
            if len(t_jul_tmp1) != 3:
                t_jul_tmp1 = (3-len(t_jul_tmp1))*'0' + t_jul_tmp1
            event_date_tmp1 = '*.%s.*.*.%s.%s.*.*.*.seed' \
                                %(chan, t_event.year, t_jul_tmp1)
            st.append(read(os.path.join(waveform_dir, sta, event_date_tmp1),
                    starttime = t_event - tb, endtime = t_event + ta)[0])

        if st[0].stats.endtime < (t_event + ta):
            t_jul_tmp2 = str(t_event.julday + 1)
            if len(t_jul_tmp2) != 3:
                t_jul_tmp2 = (3-len(t_jul_tmp2))*'0' + t_jul_tmp2
            event_date_tmp2 = '*.%s.*.*.%s.%s.*.*.*.seed' \
                                %(chan, t_event.year, t_jul_tmp2)
            st.append(read(os.path.join(waveform_dir, sta, event_date_tmp2), 
                    starttime = t_event - tb, endtime = t_event + ta)[0])

        st.append(read(os.path.join(waveform_dir, sta, event_date), 
                    starttime = t_event - tb, endtime = t_event + ta)[0])

        st.merge()
        
        st = pre_process(st, fmin = fmin, fmax = fmax)
        plt.plot(np.linspace(0, st[0].stats.npts/st[0].stats.sampling_rate, 
                    st[0].stats.npts), st[0].data/st[0].max() + sta_enum, 
                    'black')
        plt_flag = True
    
    if plt_flag:
        plt.xlabel('Second', fontsize = 'large', weight = 'bold')
        plt.xticks(fontsize = 'large', weight = 'bold')
        plt.yticks(fontsize = 'large', weight = 'bold')
        plt.title('Event ID %s\nMagnitude: %s' %(ev_num['event_id'], \
                    ev_num['magnitude']), fontsize = 'large', weight = 'bold')
        plt.savefig(os.path.join('FIGS', str(ev_num['magnitude']) + '-' + \
                    str(t_event) + '.png'))


########################################################################
############################# Main Program #############################
########################################################################

# Chan could be E N Z H 
sta_num_inp = raw_input('Enter the station number: (01, 02, ....OR * for all)\n')
if sta_num_inp == '*':
    sta_num_inp = ['0' + str(i) for i in range(1, 10)] + \
                    [str(i) for i in range(10, 27)]
else:    
    sta_num_inp = sta_num_inp.split(',')

for i in range(len(sta_num_inp)):
    sta_num_inp[i] = sta_num_inp[i].strip()

chan = raw_input('Enter the channel ID: (X, Y, Z, H)\n') 

eventFile_open = open(ls_event_file)
ls_events_all = pickle.load(eventFile_open)
ls_events = []
for i in range(0, len(ls_events_all)):
    if ls_events_all[i]['magnitude'] >= min_mag:
        ls_events.append(ls_events_all[i])
print '\nThe number of found events: %s' %len(ls_events)

# This part is the parallel version of creating the plots
# Serial version is as easy as:
for ev_enum in range(0, len(ls_events)):
    find_core(ev_enum, ls_events, sta_num_inp, chan, ta, tb, fmin, fmax, waveform_dir)


#parallel_len_req = range(0, len(ls_events))
#lol = [parallel_len_req[n:n+limit_np] \
#            for n in range(0, len(parallel_len_req), limit_np)]
#jobs = []
#for i in parallel_len_req:
#    p = multiprocessing.Process(target=find_core,\
#                args=(i, ls_events, \
#                sta_num_inp, chan, ta, tb, fmin, fmax, waveform_dir)) 
#    jobs.append(p)
#
#for l in range(0, len(lol)):
#    for ll in lol[l]:
#        jobs[ll].start()
#    jobs[ll].join()
