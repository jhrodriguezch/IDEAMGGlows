import pyla
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def extrac_number_of_warnings(codigo_estacion):
    comid, _ = pyla.data_download.get_comit_from_station(ID = codigo_estacion)

    serie_hist_observada_full, _ = pyla.data_download.get_historical_data(codigo_estacion)

    print(serie_hist_observada_full)
    # print(codigo_estacion)
    # print(serie_hist_observada_full.head(4))

    # Fix to dates
    # Initial date : 2014/01/01 - End date : 2019/12/31
    # serie_hist_observada=serie_hist_observada_full.loc['2014':'2019'].copy()

    '''
    # Extrac warning early
    ###################################
    fews_alerta_bajos_obs, _ = pyla.data_download.get_alerta_minima_fews(codigo_estacion) 
    fews_alerta_bajos_obs = 100 * fews_alerta_bajos_obs
    ###################################
    quantile10_minmen = serie_hist_observada_full.groupby([serie_hist_observada_full.index.year]).min().quantile(0.1)
    quantile10_minmen = quantile10_minmen.values[0]
    ###################################
    W7N10_obs_serie = serie_hist_observada_full.rolling(window=7).mean().groupby(serie_hist_observada_full.index.year).min().dropna()['data'].tolist()
    WP_7N10_obs, _ = pyla.data_analysis.get_data_from_return_period(rp   = 10, time_serie = W7N10_obs_serie)
    ###################################
    w_hist_min = serie_hist_observada_full.min(skipna=True).values[0]


    # Calc
    fews_alerta_bajos_count = serie_hist_observada.values <= fews_alerta_bajos_obs
    fews_alerta_bajos_count = np.sum(fews_alerta_bajos_count.flatten())

    quantile10_minmen_count = serie_hist_observada.values <= quantile10_minmen
    quantile10_minmen_count = np.sum(quantile10_minmen_count.flatten())

    WP_7N10_count = serie_hist_observada.values <= WP_7N10_obs
    WP_7N10_count = np.sum(WP_7N10_count.flatten())

    w_hist_min_count = serie_hist_observada.values <= w_hist_min
    w_hist_min_count = np.sum(w_hist_min_count.flatten())

    return ({'comid' : comid,
             'fews_alerta_bajos_obs' : {'valor' : fews_alerta_bajos_obs, 'count' : fews_alerta_bajos_count},
             'quantile10_minmen'     : {'valor' : quantile10_minmen,     'count' : quantile10_minmen_count},
             'WP_7N10_obs'           : {'valor' : WP_7N10_obs,           'count' : WP_7N10_count},
             'w_hist_min'            : {'valor' : w_hist_min,            'count' : w_hist_min_count}})
    '''
    return serie_hist_observada_full

'''
# Rio Meta
codigo_estacion_list = [ '35257020',
                         '35257040',
                         '35267080',
                         '35267030',
                         '35117010',
                         '35107030',
                         '35017020']

# Rio Putumayo
codigo_estacion_list = ['47017070',
                        '47017160',
                        '47017200',
                        '47017190',
                        '47047040',
                        '47067020',
                        '47107010']

# Rio Magdalena
codigo_estacion_list = ['29037020',
                        '29017010',
                        '25027020',
                        '25027330',
                        '25027410',
                        '23217030',
                        '23187280',
                        '23207040',
                        '23167010',
                        '23097030',
                        '23097040',
                        '23037010',
                        '21237020',
                        '21237010',
                        '21137010',
                        '21137050',
                        '21097070',
                        '21097120',
                        '21077020',
                        '21047010',
                        '21027010',
                        '21017040',
                        '21017060',
                        '21017030']

# Rio Arauca
codigo_estacion_list = ['37057020',
                        '37057060']

# Rio Guaviare
codigo_estacion_list = ['32207010',
                        '31097010',
                        '32157060',
                        '32157040',
                        '32097010',
                        '32157010',
                        '32107010']

'''
codigo_estacion_list = ['29067120']
rv = extrac_number_of_warnings(codigo_estacion=codigo_estacion_list[0])
obs_search = rv.loc['2017-10-29']
print('')
print(obs_search)

print('')
print(rv.loc['2017-10'])
print(rv.min())
print(rv.max())

rv.loc['2017-10'].plot()
plt.hlines(obs_search, xmin=rv.loc['2017-10'].index.min(), xmax=rv.loc['2017-10'].index.max())
plt.show()


# '35017020', '35107030']
'''
rv = {}

for codigo_estacion in codigo_estacion_list:
    rv.update({codigo_estacion : extrac_number_of_warnings(codigo_estacion=codigo_estacion)})

df = pd.DataFrame(rv).T
'''
# df.to_csv(r'D:\IDEAM\0_ejecucion\1.navegacion\estaciones_rio_guaviare.csv')