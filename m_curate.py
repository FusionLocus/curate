# -*- coding: utf-8 -*-
"""
m_curate: Some handling utilities for work with Picasso data. Contains several small functions designed to make life a little easier.
Author: Joe Pollacco
Notes: 
Format of picasso data seems to be as one big dataset (moderately weird) so have to have more advance knowledge of what exists where.
Structure is as one big dataset. Individual rows correspond to (groups of) Important columns: 
   n_events 2
   sx_mean  11
   sx_std 12
   sy_mean 13
   sy_std 14
   lpx_mean 17
   lpx_std 18
   lpy_mean 19
   lpy_std 20    
"""


import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import h5py as h5
import os

"""
Name: f_hdf5analyse
Description: Gets desired data from localised events obtained from picasso pick properties data, which are stored as a .hdf5.
Arguments:
    a_wantedprops - (int array) which headings from the picasso data are wanted. Numbered from 1 upwards (not 0 - beware!) - see beginning of m_curate for list of some useful ones.
    v_relpath - (string) relative path from the main project directory.
Version: v0.9
Dependencies: numpy, scipy, matplotlib, h5py, os.
Last Updated: 23/06/2020
"""

def f_hdf5analyse(a_wantedprops,v_relpath=''):
    # Get present working directory and combine this with relative path to the hdf5 file.
    v_pwd = os.getcwd() # Current working directory
    v_fullpath = os.path.join(v_pwd,v_relpath) # Create a full path
    
    # Create a hdf5 dataset object and get its length (ie. number of (groups of) events).
    a_hd5propsfileobj = h5.File(v_fullpath,'r')
    a_hd5props = a_hd5propsfileobj['groups']
    v_hd5propslen = (a_hd5props.shape)[0]
    
    # Pick a property to find (or pick array of them). Just here to have for redundancy purposes.
    a_props = np.zeros((len(a_wantedprops),v_hd5propslen)) # Preallocation of array for the attributes we want.
    
    # Iterate through the properties one at a time.
    idx3 = 0 # Index used to index into a_props in the correct row.
    for idx1 in a_wantedprops :
        # Get a copy of each of these properties for each group in the data.
        # Define an index to loop over.
        idx2 = 0
        while idx2 < v_hd5propslen :
            a_props[idx3,idx2] = a_hd5props[idx2][idx1]
            idx2 += 1
        idx3 += 1 # Look at the next row of a_props.

    a_hd5propsfileobj.close() # Close file object to avoid problems.
    return a_props

"""
Name: f_1dhistplotter
Description: *Very* simple function to plot a 1D histogram of the desired quantity.
Arguments:
    a_histdata - (Float/Int Array) 1D numpy array.
    v_bins - (Int) Number of bins to use. Default: 20.
    v_qname - (String) Name of quantity being plotted. Default: 'x'.
    v_qunit - (String) Unit of quantity being plotted.
Dependencies: numpy, scipy, matplotlib.
Author: Joe Pollacco
Last Updated: 24/06/2020
"""


def f_1dhistplotter(a_histdata,v_bins=20,v_qname='x',v_qunit=''):
    # Prepaare figure
    fig, ax = plt.subplots()
    # Generate Histogram
    n, bins, patches = plt.hist(a_histdata, v_bins,histtype='step')
    
    # Label the histogram
    plt.xlabel(v_qname + ' (' + v_qunit + ')')
    plt.ylabel('Counts')
    plt.title('Histogram showing distribution of ' + v_qname + '.')
    
    
    return fig, ax

