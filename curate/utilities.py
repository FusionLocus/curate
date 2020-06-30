# -*- coding: utf-8 -*-

import numpy as np

"""
Name: f_lifetimeget
Description: Extracts lifetime of sets of events from Picasso picked localisation data.
Arguments: 
    a_framedata - (Int Array) 1D numpy array containing all frames where an event was registered.
Returns:
    a_lifetimes - (Int Array) 1D numpy array containing all lifetimes in frames.
Dependencies: numpy
Last Updated: 29/06/2020
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
            if v_diff > 1 :
                a_lifetimes[idx1] = idx2 
                idx1 += idx2
                # Break out of second while loop.
                v_truth = False
            else :
               idx2 +=  1
   
    # Remove all the extra zeros.
    a_lifetimes = np.array([x for x in a_lifetimes if x != 0])        
    
    return a_lifetimes

# -*- coding: utf-8 -*-
"""
Name: f_fft
Description: Performs discrete fft on an array of datapoints.
Arguments: 
    a_dspace - (Int Array) 1D numpy array containing real (direct) space data.
Returns:
    a_rspace - (Int Array) 1D numpy array containing frequency (reciprocal) space data.
Dependencies: numpy
Last Updated: 29/06/2020
"""

def f_fft(a_dspace) :
    np.fft.fft(a_dspace)
    
    
    
    return a_rspace