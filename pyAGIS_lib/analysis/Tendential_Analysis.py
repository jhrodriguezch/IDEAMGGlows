import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pyAGIS
import pymannkendall as mk


def main_fun(name_estacion, codigo_estacion, rv):

    # Define folder to plot images
    folder_to_plot  = r'D:\IDEAM\0_ejecucion\10.presentacion\navegacion_imgs\tendencia'

    file_serie      = codigo_estacion + '_obs_sim.pdf'
    file_tendencial = codigo_estacion + '_MinAnual_tendential.pdf'

    ################################ START ###############################

    comid, _        = pyAGIS.data_download.get_comit_from_station(ID = codigo_estacion)

    # Build time series
    serie_hist_observada, _      = pyAGIS.data_download.get_historical_data(codigo_estacion)
    serie_hist_simulada, _       = pyAGIS.data_download.get_historical_sim_data(comid, serie_hist_observada)

    # Fix time series
    serie_hist_simulada['date'] = serie_hist_simulada.index

    serie_hist_simulada.rename(columns={'data':'sim'}, inplace=True)
    serie_hist_simulada['obs'] = serie_hist_observada['data']

    serie_hist_simulada.dropna(axis=0, inplace=True)

    hist_obs = serie_hist_simulada.groupby([serie_hist_simulada['obs'].index.year]).min()['obs']
    hist_sim = serie_hist_simulada.groupby([serie_hist_simulada['sim'].index.year]).min()['sim']

    serie_hist_simulada['__year__'] = serie_hist_simulada.index.year
    hist_obs = hist_obs.to_frame()
    hist_sim = hist_sim.to_frame()
    hist_obs['__year__'] = hist_obs.index
    hist_sim['__year__'] = hist_sim.index

    serie_hist_simulada = serie_hist_simulada.merge(hist_obs, on='__year__', suffixes=['', '_yearly'])
    serie_hist_simulada = serie_hist_simulada.merge(hist_sim, on='__year__', suffixes=['', '_yearly'])

    # Mann Kendall test
    mk_obs = mk.original_test(hist_obs['obs'].values)
    mk_sim = mk.original_test(hist_sim['sim'].values)

    #  Add results for Mann Kendall Test
    rv.update({codigo_estacion : { 'obs' : mk_obs,
                                'sim' : mk_sim}})

    # Plot Images
    fig, ax = plt.subplots(2,1, figsize=(10, 7), sharex=True)

    ax[0].plot(serie_hist_simulada['date'], serie_hist_simulada['obs'], color='blue')
    ax[1].plot(serie_hist_simulada['date'], serie_hist_simulada['sim'], color='red')

    ax[0].plot(serie_hist_simulada['date'], serie_hist_simulada['obs_yearly'], color='lightblue')
    ax[1].plot(serie_hist_simulada['date'], serie_hist_simulada['sim_yearly'], color='pink')

    ax[0].legend(['Nivel observado', 'Minimo anual'])
    ax[1].legend(['Nivel simulado', 'Minimo anual'])
    ax[1].set_xlabel('Fecha')
    ax[0].set_ylabel('Nivel [cm]')
    ax[1].set_ylabel('Nivel [cm]')
    ax[0].set_title(f'Comparación serie observada y simulada\n Estación: {codigo_estacion}\nNombre : {name_estacion}')
    ax[0].grid()
    ax[1].grid()

    # plt.savefig(os.path.join(folder_to_plot, file_serie))
    plt.show()
    plt.close()


    fig, ax = plt.subplots(1,1, figsize=(10, 5.2))
    ax.plot(hist_obs.index, hist_obs['obs'], color='blue')
    ax.plot(hist_sim.index, hist_sim['sim'], color='red')
    ax.plot(hist_obs.index, np.arange(len(hist_obs)) * mk_obs.slope + mk_obs.intercept, '--b')
    ax.plot(hist_sim.index, np.arange(len(hist_sim)) * mk_sim.slope + mk_sim.intercept, '--r')
    plt.legend(['Niveles minimos anuales observados',
                'Niveles minimos anuales simulados',
                f'Tendencia observada : {mk_obs.trend}',
                f'Tendencia simulada  : {mk_sim.trend}'])
    plt.title(f'Análisis tendencial series minimos anuales\n Estación: {codigo_estacion}\nNombre : {name_estacion}')
    plt.xlabel("Fecha")
    plt.ylabel("Nivel [cm]")
    plt.grid()

    plt.show()
    # plt.savefig(os.path.join(folder_to_plot, file_tendencial))
    plt.close()
    return rv

# Build dictionary to print results
rv = {}

# Build listo of stations to work
data_input = {'37057020' : 'El Alcaraban automatica',
              '37057060' : 'Pte. Internacional',
              '47017070' : 'El Eden',
              '47017160' : 'Pte. Texas',
              '47017200' : 'Los Naranjos',
              '47017190' : 'Bellavista',
              '47047040' : 'San Agustin',
              '47067020' : 'Estrecho Marandua',
              '47107010' : 'Tarapaca',
              '35257020' : 'Patevacal',
              '35257040' : 'Aceitico',
              '35267080' : 'Agua verde',
              '35267030' : 'Sta. Maria',
              '35117010' : 'Humapo',
              '35107030' : 'Cabuyaro',
              '35017020' : 'Pto. Lleras automatica',
              
              '29037020': 'Calamar',
              '29017010': 'Tenerife',
              '25027020': 'El Banco',
              '25027330': 'Peñoncito',
              '25027410': 'Regidor',
              '23217030': 'El Contento',
              '23187280': 'Sitio Nuevo R-11',
              '23207040': 'San Pablo automatica',
              '23167010': 'Peñas Blancas',
              '23097030': 'Pto. Berrio Automatica',
              '23097040': 'Pto. Inmarco',
              '23037010': 'Pto. Salgar',
              '21237020': 'Arranca plumas',
              '21237010': 'Nariño',
              '21137010': 'Purificacion',
              '21137050': 'Angostura',
              '21097070': 'Pte. Santander automatica',
              '21097120': 'La Esperanza',
              '21077020': 'Paso del colegio',
              '21047010': 'Pte. Balseadero',
              '21027010': 'Pericongo',
              '21017040': 'Salado blanco',
              '21017060': 'La Magdalena',
              '21017030': 'Cascada Simon Bolivar',
              '32207010': 'Cejal',
              '32157060': 'Barranco Murcielago',
              '32157040': 'Pueblo Nuevo',
              '32157010': 'Mapiripana',
              '32107010': 'Pto Arturo',
              '32097010': 'Mapiripan',
              '31097010': 'Cuayare'}

for row in data_input:
    name_estacion   = data_input[row]
    codigo_estacion = row
    
    print(name_estacion, codigo_estacion)

    rv = main_fun(name_estacion, codigo_estacion, rv)

# Plot results 
df_rv = pd.DataFrame(rv)
# df_rv.T.to_csv(r'D:\IDEAM\0_ejecucion\10.presentacion\navegacion_imgs\tendencia\METADATA.csv')
