#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -------------------------------------------------------------------
#   Filename:  kh_utils.py
#   Purpose:   Collection of utility codes
#   Author:    Kasra Hosseini
#   Email:     hosseini@geophysik.uni-muenchen.de
#   License:   GPLv3
# -------------------------------------------------------------------

# -----------------------------------------------------------------------
# ----------------Import required Modules (Python and Obspy)-------------
# -----------------------------------------------------------------------

# Required Python modules will be imported in this part.

from matplotlib.colors import LinearSegmentedColormap
import multiprocessing
import numpy as np
from obspy.core.util import locations2degrees
from obspy.taup import getTravelTimes
import scipy.io as sio
from scipy.spatial import cKDTree
import sys
import time

# ---------------------- geocen_array ---------------------------


def _get_colormap(colors, colormap_name):
    """
    A simple helper function facilitating linear colormap creation.
    """
    # Sort and normalize from 0 to 1.
    indices = np.array(sorted(colors.iterkeys()))
    normalized_indices = (indices - indices.min()) / indices.ptp()

    # Create the colormap dictionary and return the colormap.
    cmap_dict = {"red": [], "green": [], "blue": []}
    for _i, index in enumerate(indices):
        color = colors[index]
        cmap_dict["red"].append((normalized_indices[_i], color[0], color[0]))
        cmap_dict["green"].append((normalized_indices[_i], color[1], color[1]))
        cmap_dict["blue"].append((normalized_indices[_i], color[2], color[2]))
    return LinearSegmentedColormap(colormap_name, cmap_dict)

# ---------------------- geocen_array ---------------------------


def geocen_array(arr):
    """
    Calculate geocentric latitudes on an array of latitudes
    :param arr:
    :return:
    """
    fac = 0.993305621334896

    # ----------------- First for station:
    colat = 90.0 - arr
    colat[abs(colat) < 1.0e-5] = np.sign(colat[abs(colat) < 1.0e-5])*1.0e-5
    # arg = colat*rpd
    colat *= np.pi/180.
    colat_sin = np.sin(colat)
    colat_sin[colat_sin < 1.0e-30] = 1.0e-30
    # geocen=pi2-atan(fac*cos(arg)/(max(1.0e-30,sin(arg))))
    geocen_colat = np.pi/2. - np.arctan(fac*np.cos(colat)/colat_sin)
    geocen_colat = geocen_colat*180./np.pi
    geocen_lat = 90.0 - geocen_colat

    return geocen_lat

# ---------------------- taup_parallel ---------------------------


def taup_parallel(stlats, stlons, evlats, evlons, evdps,
                  n_proc=1, req_phase='Pdiff', geocen='False'):
    """
    calculate arrival times using taup (parallel version)
    :param stlats:
    :param stlons:
    :param evlats:
    :param evlons:
    :param evdps:
    :param n_proc:
    :param req_phase:
    :param geocen:
    :return:
    """
    if geocen:
        stlats = geocen_array(stlats)
        evlats = geocen_array(evlats)

    st_counter = np.arange(1, len(stlats)+1)
    stev_info = np.empty([len(stlats), 6], dtype=object)
    stev_info[:, 0] = stlats
    stev_info[:, 1] = stlons
    stev_info[:, 2] = evlats
    stev_info[:, 3] = evlons
    stev_info[:, 4] = evdps
    stev_info[:, 5] = st_counter

    if not np.mod(len(stev_info), n_proc) == 0:
        sub_stev_info = \
            np.split(stev_info[0:-np.mod(len(stev_info), n_proc)], n_proc)
        sub_stev_info.append(stev_info[-np.mod(len(stev_info), n_proc):])
    else:
        sub_stev_info = np.split(stev_info, n_proc)

    par_job = []
    for nj in range(len(sub_stev_info)):
        par_job.append(
            multiprocessing.Process(target=travel_time_calc_array,
                                    args=(sub_stev_info[nj], nj, req_phase)))
    for nj in range(len(par_job)):
        par_job[nj].start()
    for nj in range(len(par_job)):
        check_par_jobs(par_job, 0.2)

# ---------------------- travel_time_calc_array ---------------------------


def travel_time_calc_array(stev_info, proc_name=0, req_phase='Pdiff',
                           bg_model='iasp91'):
    """
    calculate arrival time of different seismic phases
    :param evla:
    :param evlo:
    :param stla:
    :param stlo:
    :param evdp:
    :param bg_model:
    :return:
    """
    import subprocess
    tt_all = np.empty(len(stev_info), dtype=object)
    for se in range(len(stev_info)):
        taup_process = subprocess.Popen(['taup_time',
                                         '-mod', bg_model,
                                         '-time',
                                         '-h', str(stev_info[se, 4]),
                                         '-ph', req_phase,
                                         '-sta', str(stev_info[se, 0]),
                                         str(stev_info[se, 1]),
                                         '-evt', str(stev_info[se, 2]),
                                         str(stev_info[se, 3])],
                                        stdout=subprocess.PIPE)
        tt_raw = taup_process.communicate()[0]
        try:
            tt = tt_raw.split('\n')[0].split()[-1]
            tt = float(tt)
        except Exception, e:
            tt = False
        tt_all[se] = tt
    np.save('tt_all_%s' % proc_name, tt_all)

# ---------------------- travel_time_calc ---------------------------


def travel_time_calc(evla, evlo, stla, stlo, evdp, bg_model):
    """
    calculate arrival time of different seismic phases
    :param evla:
    :param evlo:
    :param stla:
    :param stlo:
    :param evdp:
    :param bg_model:
    :return:
    """
    # --------------- TAUP
    dist = locations2degrees(evla, evlo, stla, stlo)
    try:
        tt = [_i for _i in getTravelTimes(dist, evdp, bg_model)
              if 'Pdiff' == _i['phase_name']][0]['time']
    except Exception, e:
        tt = False
    return tt

# ------------------ SphericalNearestNeighbour ---------------------------


class SphericalNearestNeighbour():
    """
    Spherical nearest neighbour queries using scipy's fast kd-tree
    implementation.
    """
    def __init__(self, lat, lon, el_dp, eradius=6371009):
        cart_data = self.spherical2cartesian(lat, lon, el_dp, eradius)
        self.kd_tree = cKDTree(data=cart_data, leafsize=10)
        self.eradius = eradius

    def query(self, lat, lon, el_dp, k=1):
        points = self.spherical2cartesian(lat, lon, el_dp, self.eradius)
        d, i = self.kd_tree.query(points, k=k)
        return d, i

    def query_pairs(self, maximum_distance):
        return self.kd_tree.query_pairs(maximum_distance)

    def spherical2cartesian(self, lat, lon, el_dp, eradius):
        """
        Converts a list of :class:`~obspy.fdsn.download_status.Station`
        objects to an array of shape(len(list), 3) containing x/y/z in meters.
        """
        shape = len(lat)
        r = eradius + el_dp
        # Convert data from lat/lng to x/y/z.
        colat = 90.0 - lat
        cart_data = np.empty((shape, 3), dtype=np.float64)
        cart_data[:, 0] = r * np.sin(np.deg2rad(colat)) * \
        np.cos(np.deg2rad(lon))
        cart_data[:, 1] = r * np.sin(np.deg2rad(colat)) * \
        np.sin(np.deg2rad(lon))
        cart_data[:, 2] = r * np.cos(np.deg2rad(colat))
        return cart_data

# ---------------------- check_par_jobs ---------------------------


def check_par_jobs(jobs, sleep_time=1):
    """
    check whether all the parallel jobs are finished or not
    :param jobs:
    :param sleep_time:
    :return:
    """
    pp_flag = True
    while pp_flag:
        for proc in jobs:
            if proc.is_alive():
                print '.',
                sys.stdout.flush()
                time.sleep(sleep_time)
                pp_flag = True
                break
            else:
                pp_flag = False
    if not pp_flag:
        print '\n\nAll %s processes are finished...\n' % len(jobs)


# ---------------------- py2mat ---------------------------


def py2mat(pyobject, name='pyobj', filename='out'):
    """
    pyobject: the Python object that you want to convert to MATLAB
    name: given name (this will be used in MATLAB)
    :param pyobject:
    :param name:
    :param filename:
    :return:
    """

    sio.savemat(filename, {name: pyobject})
    print "\n\n===================="
    print "converted to %s (MATLAB) and saved in %s.mat" \
                    %(name, filename)
    print "\nFrom matlab consule type:"
    print "load %s.mat" %(filename)
    print "%s" %(name)
    print "===================="

# ---------------------- unique_row ---------------------------


def unique_rows(data):
    """
    Make a unique array based on the array's row
    :param data:
    :return:
    """
    data_mid =np.ascontiguousarray(data).view(
        np.dtype((np.void, data.dtype.itemsize * data.shape[1])))
    _, idx = np.unique(data_mid, return_index=True)
    unique_data = data[idx]
    return unique_data

# ---------------------- progress_bar ---------------------------


def progress_bar(curr_indx, total_number):
    """
    Showing the progress in a loop
    :param curr_indx:
    :param total_number:
    :return:
    """
    sys.stdout.write('\r')
    sys.stdout.write("[%-100s] %d%%"
                     % ('='*int(100.*(curr_indx+1)/total_number),
                        100.*(curr_indx+1)/total_number))
    sys.stdout.flush()
