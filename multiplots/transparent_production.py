
import os
#
import global_var
import global_tools
import production.plot.subplot as production_subplot
import outages.plot.subplot    as outages_subplot
#
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters; register_matplotlib_converters()
from matplotlib.font_manager import FontProperties
global_tools.set_mpl(mpl, plt, FontProperties())
#

def transparent_production(program,
                           df_prod,
                           source_outages    = None,
                           source_production = None,
                           map_code          = None,
                           unit_name         = None,
                           date_min          = None,
                           date_max          = None, 
                           production_nature = None,
                           production_source = None,
                           figsize           = global_var.figsize_horizontal,
                           folder_out        = None, 
                           close             = True,
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
    ### Subplots
    production_subplot.power(ax,
                             df_prod,
                             map_code  = map_code,
                             unit_name = unit_name,
                             production_nature = production_nature,
                             production_source = production_source,
                             label     = global_tools.format_latex('{0} - {1}'.format(map_code,
                                                                                      unit_name,
                                                                                      )
                             ))
    outages_subplot.expected_program(ax,
                                     program.squeeze(),
                                     label = 'last publications',
                                     )

    ### Ticks
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%a %d/%m/%Y %H:%M"))
    fig.autofmt_xdate()
    if date_min and date_max:
        ax.set_xlim(date_min, date_max)
    
    ### labels                
    ax.set_ylabel(production_nature)
    
    ### Add legend
    lns01, labs01 = ax.get_legend_handles_labels()
    by_label0 = dict(zip(labs01,
                         lns01,
                         ))
    ax.legend(by_label0.values(),
              by_label0.keys(),
              loc = 0,
               )
                    
    ### Finalize
    title = ' - '.join(filter(None, [
                                     'source_outages = {source_outages}' if source_outages else '',
                                     'map_code = {map_code}'if map_code else '',
                                     'unit_name = {unit_name}' if unit_name else '',
                                     'production_source = {production_source}' if production_source else '',
                                     ])).format(source_outages = source_outages,
                                                map_code       = map_code,
                                                unit_name      = unit_name,
                                                production_source = production_source,
                                                )
    fig.suptitle(global_tools.format_latex(title))
    plt.tight_layout(rect = [0, 0.01, 1, 0.95])
    
    # Save
    full_path = os.path.join(folder_out,
                             "multiplots_transparent_production",
                             "period_{begin}_{end}".format(begin = date_min.strftime('%Y%m%d_%H%M'), 
                                                           end   = date_max.strftime('%Y%m%d_%H%M'), 
                                                           ) if date_min and date_max else '',
                             title,
                             )
    os.makedirs(os.path.dirname(full_path),
                exist_ok = True, 
                )
    plt.savefig(full_path + ".png",
                format = "png",
                bbox_inches = "tight",
                )

    if close:
        plt.close()

