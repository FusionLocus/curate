# -*- coding: utf-8 -*-
"""
Classes and instance variables available for use.
"""
class c_PickField:
    def __init__(self,name,idx,unit):
        self.name = name
        self.idx = idx
        self.unit = unit
        
# Instances for localisation data.
i_frame = c_PickField('frame',0,'')

i_x = c_PickField('x',1,'px')

i_y = c_PickField('y',2,'px')

i_photons = c_PickField('photons',3,'')

i_sx = c_PickField('sx',4,'px')

i_sy = c_PickField('sy',5,'px')

i_bg = c_PickField('bg',6,'')

i_lpx = c_PickField('lpx',7,'px') 

i_lpy = c_PickField('lpy',8,'px')   

i_ellipticity = c_PickField('ellipticity',9,'')        

i_netgradient = c_PickField('net_gradient',10,'')

#l added here to differentiate it from pick properties group
i_lgroup = c_PickField('group',11,'') 

# Instances for pickproperties data.
i_pgroup = c_PickField('group',0,'')

i_nevents = c_PickField('n_events',1,'')

i_framemean = c_PickField('frame_mean',2,'')

i_framestd = c_PickField('frame_std',3,'')

i_xmean = c_PickField('x_mean',4,'px')

i_xstd = c_PickField('x_std',5,'px')

i_ymean = c_PickField('y_mean',6,'px')

i_ystd = c_PickField('y_std',7,'px')

i_photonsmean = c_PickField('photons_mean',8,'')

i_photonsstd = c_PickField('photons_std',9,'')

i_sxmean = c_PickField('sx_mean',10,'px')

i_sxstd = c_PickField('sx_std',11,'px')

i_symean = c_PickField('sy_mean',12,'px')

i_systd = c_PickField('sy_std',13,'px')

"""
Need to finish this.
i_pgroup = c_PickField('',0,'')

i_pgroup = c_PickField('',0,'')

i_pgroup = c_PickField('',0,'')

i_pgroup = c_PickField('',0,'')

i_pgroup = c_PickField('',0,'')

i_pgroup = c_PickField('',0,'')
"""