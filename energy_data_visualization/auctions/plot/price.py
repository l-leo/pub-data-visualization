
import numpy as np
import os
#
from ... import global_tools, global_var
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


def price(dg,
          source     = None,
          map_code   = None,
          date_min   = None, 
          date_max   = None,
          folder_out = None,
          close      = None,
          figsize = global_var.figsize_horizontal,
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
    
    ### Subplot
    subplot.price(ax,
                  dg,
                  )

    ### Ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %d/%m/%Y %H:%M"))
    fig.autofmt_xdate()
    if date_min and date_max:
        ax.set_xlim(date_min, date_max)
    
    ### labels                
    ax.set_xlabel(global_tools.format_latex(global_var.contract_delivery_begin_dt_UTC))
    ax.set_ylabel(global_var.auction_price_euro_mwh)
    
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
                                     ])).format(source            = source,
                                                map_code          = map_code,
                                                )
    fig.suptitle(global_tools.format_latex(title))
    plt.tight_layout(rect = [0, 0.01, 1, 0.95])
    
    # Save
    full_path = os.path.join(folder_out,
                             "auctions_price",
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
        
    