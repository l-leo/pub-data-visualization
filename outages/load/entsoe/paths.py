
import os
#
import global_var

folder_raw = os.path.join(global_var.path_public_data,
                          '11_ENTSOE',
                          'Outages',
                          )
fpath_tmp = os.path.join(global_var.path_transformed,
                         'ENTSOE',
                         'Outages',
                         'Outages_{map_code}_{file}',
                         )