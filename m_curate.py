# -*- coding: utf-8 -*-
"""
m_curate: Some handling utilities for work with Picasso data. Contains several small functions designed to make life a little easier.
Author: Joe Pollacco
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
    v_type - (string) takes either 'locs' or 'props'. Returns false if this is specified incorrectly.
Returns:
    a_props - (array) contains the requested data. Each row is a property, each column corresponds to a given event.
Version: v0.9
Dependencies: numpy, h5py, os.
Last Updated: 23/06/2020
"""

def f_hdf5analyse(a_wantedprops,v_relpath='',v_type='props'):
    # Get present working directory and combine this with relative path to the hdf5 file.
    v_pwd = os.getcwd() # Current working directory
    v_fullpath = os.path.join(v_pwd,v_relpath) # Create a full path
    
    # Create a hdf5 dataset object and get its length (ie. number of rows).
    a_hd5propsfileobj = h5.File(v_fullpath,'r')
    
    # If we're dealing with pick properties.
    if v_type == 'props' :
        a_hd5props = a_hd5propsfileobj['groups']
        v_hd5propslen = (a_hd5props.shape)[0]
    # If we're dealing with localisation data.
    elif v_type == 'locs' :
        a_hd5props = a_hd5propsfileobj['locs']
        v_hd5propslen = (a_hd5props.shape)[0]
    else :
        print('Data type incorrectly specified. Aborting...')
        return False
    
    # Preallocation of array for the attributes we want.
    a_props = np.zeros((len(a_wantedprops),v_hd5propslen))
    
    # Iterate through the rows one at a time and get the required properties of each event.
    idx2 = 0  # Define an index to loop over.
    while idx2 < v_hd5propslen :
        idx3 = 0 # Index used to index into a_props in the correct row.
        for idx1 in a_wantedprops :
            a_props[idx3,idx2] = a_hd5props[idx2][idx1]
            idx3 += 1 # Look at the next row of a_props.
        idx2 += 1

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
Returns:
    fig, ax - pyplot objects.
Dependencies: numpy, matplotlib.
Last Updated: 24/06/2020
"""


def f_1dhistplotter(a_histdata,v_bins=20,v_qname='x',v_qunit=''):
    # Prepare figure
    fig, ax = plt.subplots()
    # Generate Histogram
    n, bins, patches = plt.hist(a_histdata, v_bins,histtype='step')
    
    # Label the histogram
    plt.xlabel(v_qname + ' (' + v_qunit + ')')
    plt.ylabel('Counts')
    plt.title('Histogram showing distribution of ' + v_qname + '.')
    
    
    return fig, ax

"""
Name: f_lifetimeget
Description: Extracts lifetime of sets of events from Picasso picked localisation data.
Arguments: 
    a_framedata - (Int Array) 1D numpy array containing all frames where an event was registered.
Returns:
    a_lifetimes - (Int Array) 1D numpy array containing all lifetimes in frames.
Dependencies: numpy
Last Updated: 28/06/2020
"""



def f_lifetimeget(a_framedata):
    # The strategy here will be to locate groups of events at the same position that differ only by one or two frames and define these as being part of the same event.
    # Luckily, picasso sorts such events by position and then by frame so this is a relatively simple problem.
    idx1 = 0 # Current position in the data.
    a_lifetimes = np.zeros_like(a_framedata) #Preallocate an array of zeros (maximum size possible).
    v_framedatalen = a_framedata.shape[0] - 1  # Get the size of the array of frame data.
    
    # Only want to loop through data while we are less than or equal to the total length of the frame data.
    while idx1 <= v_framedatalen :
        v_truth = True # Truth counter. Use this to control when events are grouped.
        idx2 =  1 # Index to use for determining whether nearby events (in the array) should be grouped together
        # If we're going to index out of our array, need to escape to avoid an index error.
        if (idx1 + idx2 > v_framedatalen ) :
            # Break out of the first while loop.
            break
       
        while v_truth == True :
            # Get the difference in frames between the base event and a subsequent event.
            v_diff = a_framedata[idx1+idx2] - a_framedata[idx1+idx2-1]
            # If the frame difference is greater than two frames, events are considered separate.
            if v_diff > 2 :
                a_lifetimes[idx1] = idx2 
                idx1 += idx2
                # Break out of second while loop.
                v_truth = False
            else :
               idx2 +=  1
   
    # Remove all the extra zeros.
    a_lifetimes = np.array([x for x in a_lifetimes if x != 0])        
    
    return a_lifetimes
