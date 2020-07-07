# -*- coding: utf-8 -*-

import numpy as np


def f_lifetimeget(a_framedata):
    """
    Description: Extracts lifetime of sets of events from Picasso picked localisation data. Works when pick regions are very small.
    
    Arguments: 
        a_framedata - (Int Array) 1D numpy array containing all frames where an event was registered.
    Returns:
        a_lifetimes - (Int Array) 1D numpy array containing all lifetimes in frames.
    Dependencies: numpy
    Known issues: May fail to recognise multiple events one after another.
    Last Updated: 29/06/2020
    """
    # The strategy here will be to locate groups of events at the same position that differ only by one or two frames and define these as being part of the same event.
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
            try:
                # Going to need more criteria than this.
                v_diff = a_framedata[idx1+idx2] - a_framedata[idx1+idx2-1]
            except IndexError:
                print('Index error due to trailing event at end of set! Fix me!')
            # If the frame difference is greater than two frames, events are considered separate.
            if (v_diff > 1) or (idx1 + idx2 > v_framedatalen) :
                a_lifetimes[idx1] = idx2 
                idx1 += idx2
                # Break out of second while loop.
                v_truth = False
            else :
               idx2 +=  1
   
    # Remove all the extra zeros.
    a_lifetimes = np.array([x for x in a_lifetimes if x != 0])        
    
    return a_lifetimes

def f_propertiesget(a_framedata,track):
    """
    Description: Function for grouping together frames for events while retaining their positions.
    A heavier version of f_lifetimeget() that retains position data and any other properties you might want. Works for localisation regions of any size.
    
    Arguments:
        a_framedata : (float array) ND numpy array containing the frame number, x position, y position, sx, sy photon count, any other properties as each row (must  follow this order).
        track : (boolean) Truth variable, enable to get some printed stats about: how many times the program has grouped events together and what
                the mean and standard deviation off distance between events is.
    Returns:
        a_properties: (float array) ND numpy array containing the lifetimes, average x position, average y position, photon count, any other properties (will follow this order).
    """
    # We will locate groups of events to group together.
    idx1 = 0
    a_outputdata = np.zeros_like(a_framedata) # Preallocate an array.
    v_framedatalen = a_framedata.shape[1] - 1 # Get the size of the array of frames data.   
    v_numprops = a_framedata.shape[0] - 1
    
    if track :
        a_crits = []
        v_simcheck = 0
    
     # Only want to loop through data while we are less than or equal to the total length of the frame data.
    while idx1 <= v_framedatalen :
        v_truth = True # Truth counter. Use this to control when events are grouped.
        idx2 =  1 # Index to use for determining whether nearby events (in the array) should be grouped together
        a_datastore = a_framedata[1:,idx1].reshape(v_numprops,1) # List to store the properties we're interested in
        
        # If we're going to index out of our array, need to escape to avoid an index error.
        if (idx1 + idx2 > v_framedatalen ) :
            # Break out of the first while loop.
            break
    
        while v_truth == True  :
            # Get the difference in frames between the base event and a subsequent event.
            try:
                # Difference in frames
                v_fdiff = abs(a_framedata[0,idx1+idx2] - a_framedata[0,idx1+idx2-1])
                
                # Get the distance v_crit for tracking purposes. Should probably use v_crit^2 for efficiency.
                if track :
                    v_xdiff = a_framedata[1,idx1+idx2] - a_framedata[1,idx1+idx2-1]
                    v_ydiff = a_framedata[2,idx1+idx2] - a_framedata[2,idx1+idx2-1]
                    v_crit = np.sqrt(v_xdiff ** 2 + v_ydiff ** 2)
                # v_crit > 1
           
            except IndexError:
                # Still need to fix this.
                print('Index error due to trailing event at end of set! Fix me!\n')
            
            # If the frame difference is greater than two frames or two events are sufficiently separated, events are considered separate.
            if (v_fdiff > 1)  or (idx1 + idx2 > v_framedatalen) :
                a_outputdata[0,idx1] = idx2
                if idx2 == 1 :
                    a_outputdata[1:,idx1] = a_datastore.reshape(a_datastore.shape[0])
                else :
                    # Sum all the extra data along the 'frame axis' and then average.
                    a_outputdata[1:,idx1] = np.sum((a_datastore),1) / (a_datastore.shape)[0]
                idx1 += idx2
                # Break out of second while loop.
                v_truth = False
            else :
               # If two events are sufficiently similar, store the data from the event just passed and go round again.
               a_datastore = np.append(a_datastore,a_framedata[1:,idx1+idx2].reshape(v_numprops,1),axis=1)
               idx2 +=  1
               
               if track :
                   v_simcheck += 1
                   a_crits.append(v_crit)
    
    if track :
        print('Mean of all the distances between events is ' + np.mean(a_crits) + '\n')
        print('Standard deviation of all the distances between events is ' + np.std(a_crits) + '\n')
        print('The number of times events were counted as similar was ' + v_simcheck + '\n')
    
    a_outputdata = np.transpose(np.array([a_outputdata[:,x] for x in range(v_framedatalen)  \
                    if (a_outputdata[0,x]  != 0 and a_outputdata[1,x] != 0 and a_outputdata[2,x] != 0) ]))
    
    return a_outputdata