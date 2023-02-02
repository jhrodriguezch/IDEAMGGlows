import pyla
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

codigo_estacion = '47017160'
'''
codigo_estacion = '47017150'

codigo_estacion = '11117050'
codigo_estacion = '37057020'
codigo_estacion = '44037040'

codigo_estacion = '51027060'

codigo_estacion = '21237020'
codigo_estacion = '23037010'

codigo_estacion = '36027050'
codigo_estacion = '12017010'

codigo_estacion = '47017170'

'''
comid, _                = pyla.data_download.get_comit_from_station(ID = codigo_estacion)

# Series historicas
serie_hist_observada, _ = pyla.data_download.get_historical_data(codigo_estacion)
serie_hist_simulada, _  = pyla.data_download.get_historical_sim_data(comid, serie_hist_observada)

serie_hist_observada['data'] = serie_hist_observada['data'] * (1/100)
serie_hist_simulada['data'] = serie_hist_simulada['data'] * (1/100)

# Medicion actual
serie_curr_observada, _ = pyla.data_download.get_currently_fews_data(station_code = codigo_estacion)   

# Pronostico
pronostico_cache, _     = pyla.data_download.get_forecast_data_cache(station = codigo_estacion)


# Niveles de alerta
WP_p10_obs  = serie_hist_observada.groupby([serie_hist_observada.index.year]).min().quantile(0.1)

WP_7N10_obs_serie = serie_hist_observada.rolling(window=7).mean().groupby(serie_hist_observada.index.year).min().dropna()['data'].tolist()
WP_7N10_obs, _    = pyla.data_analysis.get_data_from_return_period(rp   = 10, time_serie = WP_7N10_obs_serie)

WP_MINH_obs = serie_hist_observada.min()



WP_p10_sim  = serie_hist_simulada.groupby([serie_hist_simulada.index.year]).min().quantile(0.1)

WP_7N10_sim_serie = serie_hist_simulada.rolling(window=7).mean().groupby(serie_hist_simulada.index.year).min().dropna()['data'].tolist()
WP_7N10_sim, _    = pyla.data_analysis.get_data_from_return_period(rp   = 10, time_serie = WP_7N10_sim_serie)

WP_MINH_sim = serie_hist_simulada.min()

fig, axs = plt.subplots(2, 1)

serie_hist_observada.plot(ax=axs[0], label='obs')
serie_hist_simulada.plot(ax=axs[0], label='sim')
serie_curr_observada.plot(ax=axs[1])

axs[0].hlines(WP_p10_obs,
             xmin=serie_hist_observada.index.min(),
             xmax=serie_hist_observada.index.max(),
             label='WP_p10_obs: '+str(WP_p10_obs.values[0]),
             colors='blue')
axs[1].hlines(WP_p10_obs,
              xmin=serie_curr_observada.index.min(), 
              xmax=serie_curr_observada.index.max(), 
              label='WP_p10_obs: '+str(WP_p10_obs.values[0]),
              colors='blue')

axs[0].hlines(WP_p10_sim,
              xmin=serie_hist_simulada.index.min(),
              xmax=serie_hist_simulada.index.max(), 
              label='WP_p10_sim: '+str(WP_p10_sim.values[0]),
              colors='red')
axs[1].hlines(WP_p10_sim, 
              xmin=serie_curr_observada.index.min(), 
              xmax=serie_curr_observada.index.max(), 
              label='WP_p10_sim: '+str(WP_p10_sim.values[0]),
              colors='red')

axs[0].hlines(WP_MINH_obs,
              xmin=serie_hist_simulada.index.min(),
              xmax=serie_hist_simulada.index.max(), 
              label='WP_MINH_obs: '+str(WP_MINH_obs.values[0]),
              colors='orange')
axs[1].hlines(WP_MINH_obs, 
              xmin=serie_curr_observada.index.min(), 
              xmax=serie_curr_observada.index.max(), 
              label='WP_MINH_obs: '+str(WP_MINH_obs.values[0]),
              colors='orange')

axs[0].hlines(WP_MINH_sim,
              xmin=serie_hist_simulada.index.min(),
              xmax=serie_hist_simulada.index.max(), 
              label='WP_MINH_sim: '+str(WP_MINH_sim.values[0]),
              colors='cyan')
axs[1].hlines(WP_MINH_sim, 
              xmin=serie_curr_observada.index.min(), 
              xmax=serie_curr_observada.index.max(), 
              label='WP_MINH_sim: '+str(WP_MINH_sim.values[0]),
              colors='cyan')


axs[0].hlines(WP_7N10_obs,
              xmin=serie_hist_simulada.index.min(),
              xmax=serie_hist_simulada.index.max(), 
              label='WP_7N10_obs: '+str(WP_7N10_obs),
              colors='green')
axs[1].hlines(WP_7N10_obs, 
              xmin=serie_curr_observada.index.min(), 
              xmax=serie_curr_observada.index.max(), 
              label='WP_7N10_obs: '+str(WP_7N10_obs),
              colors='green')

axs[0].hlines(WP_7N10_sim,
              xmin=serie_hist_simulada.index.min(),
              xmax=serie_hist_simulada.index.max(), 
              label='WP_7N10_sim: '+str(WP_7N10_sim),
              colors='lightgreen')
axs[1].hlines(WP_7N10_sim, 
              xmin=serie_curr_observada.index.min(), 
              xmax=serie_curr_observada.index.max(), 
              label='WP_7N10_sim: '+str(WP_7N10_sim),
              colors='lightgreen')


axs[0].legend()
axs[1].legend()
plt.show()
