from turtle import st
import pandas as pd
import geoglows as ggs
import pandas as pd
import numpy as np
from math import cos, sin, asin, sqrt, radians
from datetime import datetime

"""
Fecha: 12 - 09- 2022
"""


def calc_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km

dist_list  = []
lat_creach = []
lon_creach = []

error_txt = ['\nError al identificar los COMID de las estaciones.\n']

dir_station_data = r'D:\IDEAM\0_ejecucion\7.Datos\csv\comit_from_catchment_V1.csv'
df_station = pd.read_csv(dir_station_data)

# df_station = df_station.head(5)

for _, station in df_station.iterrows():
    if not np.isnan(station.COMID):
        lat_tmp, lon_tmp = ggs.streamflow.reach_to_latlon(station['COMID'])
        lat_creach.append(lat_tmp)
        lon_creach.append(lon_tmp)
        dist_list.append(calc_distance(station['lat'], station['lng'], lat_tmp, lon_tmp))
    else:
        error_txt.append('Error en la estacion {0}.'.format(station['nombre']))
        lat_creach.append(np.nan)
        lon_creach.append(np.nan)
        dist_list.append(np.nan)

error_txt.append('\nNumero de errores : {0}.'.format(len(error_txt)))


df_station['lat_cent_reach'] = lat_creach
df_station['lon_cent_reach'] = lon_creach
df_station['dist_reach']     = dist_list

df_station.to_csv(r'D:\IDEAM\0_ejecucion\7.Datos\csv\comit_from_catchment_V1_dis.csv')
df_station.to_json(r'D:\IDEAM\0_ejecucion\7.Datos\csv\comit_from_catchment_V1_dis.json', orient='index')

error_txt.append('Archivo final: D:/IDEAM/0_ejecucion/7.Datos/csv/comit_from_catchment_V1_dis.csv')
error_txt.append('Archivo final: D:/IDEAM/0_ejecucion/7.Datos/csv/comit_from_catchment_V1_dis.json')
error_txt.append('Notas:')
error_txt.append(' - Distancia en km')
error_txt.append(' - COMID obtenidos de los catchments.')
error_txt.append('Fecha : {0}'.format(datetime.now()))
error_txt.append('')

with open(r'D:\IDEAM\0_ejecucion\7.Datos\csv\error_v1.txt', 'w') as fp:
    for item in error_txt:
        fp.write("%s\n" % item)
    print('Done!')



# dir_cni_estaciones = r'D:\IDEAM\0_ejecucion\3.informacionSecundaria\NASA_SERVIR_AMAZONIA\Otros insumos\estaciones_fews\CNE_FEWS_may_2020.xls'
# df_estaciones = pd.read_excel(dir_cni_estaciones)
# df_estaciones = df_estaciones[[ 'CODIGO', 'nombre', 'latitud', 'longitud', 'CORRIENTE']].copy()

# df_estaciones = df_estaciones.head(2)

# comid_list = []
# dist_list  = []
# lat_creach = []
# lon_creach = []

# for ii, df_estacion in df_estaciones.iterrows():
    
#     try:
#         inf_station = ggs.streamflow.latlon_to_reach(lat=df_estacion['latitud'], lon=df_estacion['longitud'])
#         comid_list.append(inf_station['reach_id'])
#         dist_list.append(inf_station['distance'])
#         lat_tmp, lon_tmp = ggs.streamflow.reach_to_latlon(inf_station['reach_id'])
#         lat_creach.append(lat_tmp)
#         lon_creach.append(lon_tmp)
#     except:
#         print('Error')
#         print(df_estacion)
#         comid_list.append(float('nan'))
#         dist_list.append(float('nan'))
#         lat_creach.append(float('nan'))
#         lon_creach.append(float('nan'))

# df_estaciones['reach_id'] = comid_list
# df_estaciones['dist_reach'] = dist_list
# df_estaciones['lat_cent_reach'] = lat_creach
# df_estaciones['lon_cent_reach'] = lon_creach

# df_estaciones.set_index('CODIGO', inplace=True, drop=False)

# df_estaciones.to_csv(r'D:\IDEAM\0_ejecucion\7.Datos\csv\comit_from_reach.csv')
# df_estaciones.to_json(r'D:\IDEAM\0_ejecucion\7.Datos\csv\comit_from_reach.json', orient='index')

