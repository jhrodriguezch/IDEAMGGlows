import pandas as pd
import geoglows as ggs
import pandas as pd


dir_cni_estaciones = r'D:\IDEAM\0_ejecucion\3.informacionSecundaria\NASA_SERVIR_AMAZONIA\Otros insumos\estaciones_fews\CNE_FEWS_may_2020.xls'
df_estaciones = pd.read_excel(dir_cni_estaciones)
df_estaciones = df_estaciones[[ 'CODIGO', 'nombre', 'latitud', 'longitud', 'CORRIENTE']].copy()

# df_estaciones = df_estaciones.head(2)

comid_list = []
dist_list  = []
lat_creach = []
lon_creach = []

for ii, df_estacion in df_estaciones.iterrows():
    
    try:
        inf_station = ggs.streamflow.latlon_to_reach(lat=df_estacion['latitud'], lon=df_estacion['longitud'])
        comid_list.append(inf_station['reach_id'])
        dist_list.append(inf_station['distance'])
        lat_tmp, lon_tmp = ggs.streamflow.reach_to_latlon(inf_station['reach_id'])
        lat_creach.append(lat_tmp)
        lon_creach.append(lon_tmp)
    except:
        print('Error')
        print(df_estacion)

df_estaciones['reach_id'] = comid_list
df_estaciones['dist_reach'] = dist_list
df_estaciones['lat_cent_reach'] = lat_creach
df_estaciones['lon_cent_reach'] = lon_creach

df_estaciones.set_index('CODIGO', inplace=True, drop=False)

df_estaciones.to_csv(r'D:\IDEAM\0_ejecucion\7.Datos\csv\comit_from_reach.csv')
df_estaciones.to_json(r'D:\IDEAM\0_ejecucion\7.Datos\csv\comit_from_reach.json', orient='index')
