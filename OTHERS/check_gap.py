from obspy.iris import Client
from obspy.core import UTCDateTime
from obspy.core import read
import os
from lxml import objectify
###################### XML_list_avail ##################################

def XML_list_avail(xmlfile):

    """
    This module changes the XML file got from availability to a list
    """

    sta_obj = objectify.XML(xmlfile)
    sta_req = []

    for i in range(0, len(sta_obj.Station)):

        station = sta_obj.Station[i]
        net = station.get('net_code')
        sta = station.get('sta_code')

        lat = str(station.Lat)
        lon = str(station.Lon)
        ele = str(station.Elevation)

        for j in range(0, len(station.Channel)):
            cha = station.Channel[j].get('chan_code')
            loc = station.Channel[j].get('loc_code')

            sta_req.append([net, sta, loc, cha, lat, lon, ele])

    return sta_req

#################

client = Client()

#t1 = UTCDateTime(raw_input("Please enter the start time: (format: 1998-01-01)\n"))
#t2 = UTCDateTime(raw_input("Please enter the end time: (format: 1998-01-02)\n"))
t1 = UTCDateTime(2012,5,19)
t2=UTCDateTime(2012,5,21)
file_name = raw_input('Enter the name of the stream file!\n')


print t1
print t2

######## 
#st = client.saveWaveform("./G.SSB.00.BHE", "G", "SSB", "*", "BHE", t1, t2)
#st = client.getWaveform("G", "SSB", "10", "*", t1, t2)
#### Permete d avoir toutes les donnes meeme s il y a des trous
#st = client.timeseries("GB", "CWF", "", "BHZ", t1, t2, output = 'miniseed')
#### timesseries used by obspy give the same result when output is mseed or sacbl
### BUT tiemseries ftrhough webservice from iris directly give a diffetent result when the output is sac or mseed
#### only output mseed is correct
avail = client.availability("GB", "CWF", "", "BHZ", t1, t2,output='xml')
metadata=XML_list_avail(avail)
# 1eme indice = station
print lat,lon
print avail
st = client.timeseries("GB", "CWF", "", "BHZ", t1, t2, output = 'sacbl')
############ NE PAS UTILISER getWavform CAR 
##### give only one file the longest one in case of gaps
## st = client.getWaveform("GB", "CWF", "", "BHZ", t1, t2)

print st
st.write(file_name, format = 'SAC')
st=read(file_name+'*')
for i in range(0,len(st)):
    lat=metadata[i][4]
    lon=metadata[i][5]
    tr.stats.sac.stla=lat
    tr.stats.sac.stlo=lon
st.write(file_name, format = 'SAC')


os.system('obspy-scan ' + file_name + '*')
