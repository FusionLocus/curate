# -*- coding: utf-8 -*-
"""
plotting.py - contains a few basic  functions for rendering plots quickly.

"""

import matplotlib.pyplot as plt


def f_1dhistplotter(a_histdata,v_bins=20,v_qname='x',v_qunit=''):
    """
    Description: *Very* simple function to plot a 1D histogram of the desired quantity.
    
    Arguments:
        a_histdata - (Float/Int Array) 1D numpy array.
        v_bins - (Int) Number of bins to use. Default: 20.
        v_qname - (String) Name of quantity being plotted. Default: 'x'.
        v_qunit - (String) Unit of quantity being plotted.
    Returns:
        n - array containing histogram bin values.
        
    Dependencies: numpy, matplotlib.
    Last Updated: 24/06/2020
    """
    # Prepare figure
    fig, ax = plt.subplots()
    # Generate Histogram
    n, bins, patches = plt.hist(a_histdata, v_bins,histtype='step')
    
    # Label the histogram
    plt.xlabel(v_qname + ' (' + v_qunit + ')')
    plt.ylabel('Counts')
    plt.title('Histogram showing distribution of ' + v_qname + '.')
    
    
    return n, bins, patches

"""



Name: f_2dhistplotter
Description: *Very* simple function to plot a 2D histogram of the desired quantity.
Arguments:
    a_histdata1 - (Float Array) 1D numpy array to be turned into histogram.
    a_histdata2 - (Float Array) 1D numpy array to be turned into histogram.
    v_bins - (Int) Number of bins to use. Default: 20.
    v_qname - (String) Name of quantity being plotted. Default: 'x'.
    v_qunit - (String) Unit of quantity being plotted.
Returns:
    fig, ax - pyplot objects.
Dependencies: numpy, scipy, matplotlib.
Author: Joe Pollacco
Last Updated: 24/06/2020


def f_2dhistplotter(a_histdata,v_bins=20,v_qname='x',v_qunit=''):
    # Prepaare figure
    fig, ax = plt.subplots()
    # Generate Histogram
    n, bins, patches = plt.hist(a_histdata, v_bins,histtype='step')
    
    # Label the histogram
    plt.xlabel(v_qname + ' (' + v_qunit + ')')
    plt.ylabel('Counts')
    plt.title('Histogram showing distribution of ' + v_qname + '.')
    
    
    return fig, ax
    
"""