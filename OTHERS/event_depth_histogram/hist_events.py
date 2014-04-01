# simple script to plot the number of events vs depth

import matplotlib.pyplot as plt
from obspy import UTCDateTime
import pickle

max_date = UTCDateTime(2013, 1, 1)

aa = open('event_list')
events = pickle.load(aa)
counter = {}

#for i in range(len(events)):
#    if not str(-int(events[i]['depth']*10)) in counter.keys():
#        counter[str(-int(events[i]['depth']*10))] = 1
#    else:
#        counter[str(-int(events[i]['depth']*10))] += 1
#for i in counter.keys():
#    if counter[i]>100:
#        plt.bar(int(i)/10.-0.05, 100, 0.1)
#    else:
#        plt.bar(int(i)/10.-0.05, counter[i], 0.1)


#for i in range(len(events)):
#    if not str(-int(events[i]['depth'])) in counter.keys():
#        counter[str(-int(events[i]['depth']))] = 1
#    else:
#        counter[str(-int(events[i]['depth']))] += 1
#for i in counter.keys():
#    if counter[i] > 100:
#        plt.bar(int(i)-0.5, 100, 1)
#    else:
#        plt.bar(int(i)-0.5, counter[i], 1)

#for i in range(len(events)):
#    if not str(-int(events[i]['depth'])) in counter.keys():
#        counter[str(-int(events[i]['depth']))] = 1
#    else:
#        counter[str(-int(events[i]['depth']))] += 1
#for i in counter.keys():
#        plt.bar(int(i)-0.5, counter[i], 1)
#
counting = 0
for i in range(len(events)):
    if events[i]['datetime'] > max_date: 
        print '%s > %s' %(events[i]['datetime'], max_date)
        continue
    if not str(-int(events[i]['depth'])) in counter.keys():
        counter[str(-int(events[i]['depth']))] = 1
    else:
        counter[str(-int(events[i]['depth']))] += 1
    counting += 1

print 'Number of all used events: %s' % counting
for i in counter.keys():
    #if 100 <= counter[i]:
        #plt.bar(int(i)-0.5, counter[i], 1, log=True)
        plt.bar(int(i)-0.5, counter[i], 1)

plt.ion()
plt.xlim(xmin=-2, xmax=100)
plt.ylim(ymax=1100)
plt.xlabel('Depth (km)', size=36, weight='bold')
plt.ylabel('Number of events', size=36, weight='bold')
plt.xticks(size=32, weight='bold')
plt.yticks(size=32, weight='bold')
plt.title('Depth=10km (1002 events)    Depth=33km (254 events)\n', size=36, weight='bold')
plt.show()

