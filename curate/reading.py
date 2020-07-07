# -*- coding: utf-8 -*-
import numpy as np
import h5py as h5
import os


def f_hdf5analyse(a_wantedprops,v_relpath='',v_type='props'):
    """
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

def f_xyfsort(a_framedata):
    """
    Name: f_xyfsort
    Description: Sorts data by x and y coordinate so events in the same selections can be identified. Then sorts by frame.
    Arguments:
        a_framedata - (float array) 5+D numpy array with (frames,x,y,sx,sy,anything else).

    Returns
        a_sorted - (float array) 5+D numpy array that is sorted according to x and y coordinates and frames, and retains (frames,x,y,sx,sy,anything else). 
    Version: v0.4
    Dependencies: numpy.
    Last updated: 03/07/2020
    """
    a_xargs = np.argsort(a_framedata[1,:])
    # Preallocate three arrays that we'll sort into.
    a_sortedx = np.zeros_like(a_framedata)
    a_sortedy = np.zeros_like(a_framedata)
    a_sorted = np.zeros_like(a_framedata)
    # a_diffs = [] # Tracking variable
    
    # Sort the array by the x values.
    idx1 = 0
    for v_xarg in a_xargs :
        a_sortedx[:,idx1] = a_framedata[:,v_xarg]
        idx1 += 1
    
    v_alength = len(a_sortedx[1,:])
    # Index to iterate through the sorted x values.
    idx2 = 1
    # Similarity checking variables.
    v_simx = False
    v_simy = False
    # Tunable errors in x and y.
    v_errorx = 0.05
    v_errory = 0.05
    
    v_diffy = 0
    
    while idx2 <= v_alength :
        # If the two adjacent elements are significantly different
        if v_simx == False:
            # Store the current index.
            idxstore1 = idx2
            v_simx = True
        
        # Prevents an index error later on.
        v_endcheck1 = (idx2 == v_alength)
        
        # Calculate the difference between two adjacent x elements and the errors.
        if v_endcheck1 == False :
            v_diffx = np.round(a_sortedx[1,idx2] - a_sortedx[1,idx2-1],4)
            # a_diffs.append(v_diffx)
            # v_errorx = a_sortedx[3,idx2] + a_sortedx[3,idx2-1]
        
        # Two events are at different x coordinates if they are not the same accounting for errors.
        if v_diffx > v_errorx or v_endcheck1 :
            v_simx = False
            # Store the index of the last event that was the same within errors.
            idxstore2 = idx2 
            # Get the sorting indices that would sort the ys of all the xs that are the same.
            a_yargs = np.argsort(a_sortedx[2,idxstore1-1:idxstore2]) + idxstore1 - 1
            idx3 = idxstore1 - 1
            # Sort the columns again within subsets of close x using the y values.
            for v_yarg in a_yargs :
                a_sortedy[:,idx3] = a_sortedx[:,v_yarg]
                idx3 += 1
            
            # Now must sort the frames (a nested while loop, yay!)
            idx4 = idxstore1
            while (idx4 <= idxstore2) :
                # All events in a given y set are already considered 'close enough' by x so this hopefully is the fastest way to do it.
                if v_simy == False:
                    idxstore3 = idx4
                    v_simy = True
                v_endcheck2 = idx4 == idxstore2
            
                
                if v_endcheck2 == False :
                    # Calculate the difference between the y coordinates of two events.
                    v_diffy = np.round(a_sortedy[2,idx4] - a_sortedy[2,idx4-1],4)
                
                # Two events are at different y if they are not the same accounting for errors.
                if v_diffy > v_errory or v_endcheck2 :
                    v_simy = False
                    idxstore4 = idx4
                    # Get the sorting indices that would sort the frames of all the events where x and y are the same.
                    a_fargs = np.argsort(a_sortedy[0,idxstore3-1:idxstore4]) + idxstore3 - 1 
                    idx5 = idxstore3 - 1
                    # Sort the columns again within subsets where coordinates are sufficiently similar using the frame values
                    for v_farg in a_fargs :
                        a_sorted[:,idx5] = a_sortedy[:,v_farg]
                        idx5 += 1
                idx4 += 1
        idx2 += 1   
    
    # print(np.mean(a_diffs))
    # print(np.std(a_diffs))
    
    return a_sorted