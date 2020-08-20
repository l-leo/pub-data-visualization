#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
The script allows the user to draw the comparison
between the initially announced length of the outages
and the finnaly observed length of the outages
of a given set of production units.
"""

#
from energy_data_visualization import global_var, outages

###############################################################################
data_source_outages = global_var.data_source_rte
map_code            = global_var.geography_map_code_france
company_outages     = None
production_source   = global_var.production_source_nuclear
unit_name           = None
date_min            = None
date_max            = None
###############################################################################
figsize    = global_var.figsize_horizontal_ppt
folder_out = global_var.path_plots
close      = False
###############################################################################

### Load
df = outages.load(source    = data_source_outages,
                  map_code  = map_code,
                  company   = company_outages,
                  unit_name = unit_name,
                  production_source  = production_source,
                  publication_dt_min = date_min,
                  publication_dt_max = date_max,
                  )                        


### Plot
outages.plot.regression_delays(df,
                               source            = data_source_outages,
                               company           = company_outages,
                               production_source = production_source,
                               unit_name         = unit_name,
                               figsize           = figsize,
                               close             = close,
                               folder_out        = folder_out,
                               )





    
    
    
