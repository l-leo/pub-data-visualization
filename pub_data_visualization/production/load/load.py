
import pandas as pd
#
from ... import global_var
from . import eco2mix, entsoe, rte


def load(source            = None,
         map_code          = None,
         date_min          = pd.Timestamp('2012').tz_localize('CET'),
         date_max          = pd.Timestamp('2019').tz_localize('CET'),
         ):
    """
        Calls the appropriate loader of the production data
        from the given data source,
        in a given delivery_zone,
        and between two dates.
 
        :param source: The data source
        :param map_code: The bidding zone
        :param date_min: The left bound
        :param date_max: The right bound
        :type source: string
        :type map_code: string
        :type date_min: pd.Timestamp
        :type date_max: pd.Timestamp
        :return: The selected production data
        :rtype: pd.DataFrame
    """
    
    if source == global_var.data_source_eco2mix:
        df_mw = eco2mix.load(date_min = date_min,
                             date_max = date_max,
                             map_code = map_code,
                             )
    
    elif source == global_var.data_source_rte:
        df_mw = rte.load()
        
    elif source == global_var.data_source_entsoe:
        df_mw = entsoe.load(map_code = map_code)
    
    else: 
        raise ValueError
    
    dg_mw = df_mw.pivot_table(values  = global_var.quantity_value, 
                              index   = global_var.production_dt_UTC, 
                              columns = [global_var.production_nature,
                                         global_var.geography_map_code,
                                         global_var.production_source,
                                         global_var.unit_name,
                                         ],
                              )
    dg_gw         = dg_mw/1e3
    dg_gw.columns = dg_gw.columns.set_levels([global_var.production_nature_observation_gw],
                                             level = global_var.production_nature,
                                             )
    dg            = pd.concat([dg_mw,dg_gw], axis = 1)
    dg_mw = dg_mw.reindex(sorted(dg_mw.columns), axis = 1)
    dg_mw = dg_mw.sort_index()
    
    dh = dg.loc[  pd.Series(True, index = dg.index)
                & ((dg.index >= date_min) if bool(date_min) else True)
                & ((dg.index <  date_max) if bool(date_max) else True)
                ]
    
    assert dh.shape[0] > 0
    assert dh.index.is_unique

    return dh


