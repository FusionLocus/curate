# m_curate
Curate contains a few basic tools for working with data from Picasso. More tools will be added as I go (hopefully not just trivial ones).

Author: Joe Pollacco, Undergraduate, Department of Physics, University of Oxford

Some notes about how Picasso stores its data: 

Picasso stores much of its data as hdf5 files, which contain a structure of named groups and datasets.
The format of picasso data seems to be as one big dataset. Individual rows correspond to (groups of) events. 

Some important columns and the data they contain are given below: 
   n_events 2
   sx_mean  11
   sx_std 12
   sy_mean 13
   sy_std 14
   lpx_mean 17
   lpx_std 18
   lpy_mean 19
   lpy_std 20    
