import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, shiftgrid, cm
import numpy as np
from operator import itemgetter
import os

# ---------- INPUT -----------
fileadd = '../topo04.dat'
proj = 'moll'
minlat = -90
maxlat = +90
minlon = -180
maxlon = 180
step = 1
nx = 360*2
ny = 180*2
# ---------- END INPUT -----------

fi_read = np.loadtxt(os.path.join(fileadd))

# sort based on the first colomn (longitude in this case)
lon_lat_dat = sorted(fi_read, key=itemgetter(0))

arr_dat = np.zeros([len(np.arange(minlat, maxlat+1, step)),
                    len(np.arange(minlon, maxlon+1, step))])

for i in range(len(lon_lat_dat)):
    arr_dat[int(lon_lat_dat[i][1]+90), int(lon_lat_dat[i][0]+180)] = \
        lon_lat_dat[i][2]

if proj.lower() in ['robin', 'moll']:
    m = Basemap(projection=proj.lower(), lat_0=0, lon_0=0)
elif proj.lower() == 'mill':
    m = Basemap(projection='mill', resolution='c')
else:
    sys.exit('%s has not implemented!' % proj)

m.drawcoastlines()
m.drawcountries()
m.drawstates()
parallels = np.arange(-90., 91, 30.)
m.drawparallels(parallels)
meridians = np.arange(-180., 181., 30.)
m.drawmeridians(meridians)

lons = np.arange(minlon, maxlon+1, step)
lats = np.arange(minlat, maxlat+1, step)
trans_dat = m.transform_scalar(arr_dat, lons, lats, nx, ny)

tran_lons = np.linspace(minlon, maxlon, nx)
tran_lats = np.linspace(minlat, maxlat, ny)
lon, lat = np.meshgrid(tran_lons, tran_lats)

m.pcolormesh(lon, lat, trans_dat,
             shading='flat', cmap=plt.cm.jet, latlon=True)

plt.show()

##fig = plt.figure()
##ax = fig.add_axes([0.1,0.1,0.8,0.8])
##im = m.imshow(topodat,cm.GMT_haxby)
