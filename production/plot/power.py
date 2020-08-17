
import os
#
import global_var
import global_tools
from . import subplot
#
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters; register_matplotlib_converters()
from matplotlib.font_manager import FontProperties
global_tools.set_mpl(mpl, plt, FontProperties())
#

def power(df,
          map_code          = None,
          production_source = None,
          production_nature = None,
          unit_name         = None,
          date_min          = None,
          date_max          = None,
          source            = None,
          folder_out        = None,
          close             = True,
          figsize           = global_var.figsize_horizontal,
          ):

    ### Interactive mode
    if close:
        plt.ioff()
    else:
        plt.ion()
    
    ### Figure
    fig, ax = plt.subplots(figsize = figsize,
                           nrows = 1, 
                           ncols = 1, 
                           )
        
    ### subplot
    subplot.power(ax,
                  df,
                  map_code          = map_code,
                  unit_name         = unit_name,
                  production_source = production_source,
                  production_nature = production_nature,
                  label             = global_tools.format_latex(' - '.join([e
                                                                            for e in [map_code,unit_name,production_nature]
                                                                            if bool(e)
                                                                            ])),
                   )

    ### Ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %d/%m/%Y %H:%M"))
    fig.autofmt_xdate()
    if date_min and date_max:
        ax.set_xlim(date_min, date_max)
    
    ### labels                
    ax.set_xlabel(global_tools.format_latex(df.index.name))
    
    ### Add legend
    lns01, labs01 = ax.get_legend_handles_labels()
    by_label0 = dict(zip(labs01, lns01))
    ax.legend(by_label0.values(),
              by_label0.keys(),
              loc = 0,
              )
                    
    ### Finalize
    title = ' - '.join(filter(None, ['source = {source}' if source else '',
                                     'map_code = {map_code}'if map_code else '',
                                     'unit_name = {unit_name}' if unit_name else '',
                                     'production_source = {production_source}' if production_source else '',
                                     ])).format(source            = source,
                                                map_code          = map_code,
                                                unit_name         = unit_name,
                                                production_source = production_source,
                                                )
    fig.suptitle(global_tools.format_latex(title))
    plt.tight_layout(rect = [0, 0.01, 1, 0.95])
    
    # Save
    full_path = os.path.join(folder_out,
                             "production_power",
                             "period_{begin}_{end}".format(begin = date_min.strftime('%Y%m%d_%H%M'), 
                                                           end   = date_max.strftime('%Y%m%d_%H%M'), 
                                                           ) if date_min and date_max else '',
                             title,
                             )
    os.makedirs(os.path.dirname(full_path), 
                exist_ok = True,
                )
    plt.savefig(full_path + ".png", 
                format      = "png", 
                bbox_inches = "tight",
                )
    if close:
        plt.close()
        
    