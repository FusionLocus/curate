# -*- coding: utf-8 -*-
import numpy as np
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
Last Updated: 29/06/2020
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