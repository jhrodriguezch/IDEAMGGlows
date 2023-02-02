import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import hydroeval as he
from scipy.stats import mstats

import pyAGIS

def main_fun(name_estacion, codigo_estacion, rv_return):

    # Define folder to plot images
    folder_to_plot  = r'D:\IDEAM\0_ejecucion\10.presentacion\navegacion_imgs\magnitud'

    file_serie      = codigo_estacion + '_obs_sim.pdf'

    rv = {}

    ################################ START ###############################

    comid, _        = pyAGIS.data_download.get_comit_from_station(ID = codigo_estacion)

    # Build time series
    serie_hist_observada, _      = pyAGIS.data_download.get_historical_data(codigo_estacion)
    serie_hist_simulada, _       = pyAGIS.data_download.get_historical_sim_data(comid, serie_hist_observada)

    # Fix time series
    serie_hist_simulada.rename(columns={'data' : 'Sim'}, inplace=True)
    serie_hist_simulada['Obs'] = serie_hist_observada['data']

    serie_hist_simulada['__year__'] = serie_hist_simulada.index.year
    serie_hist_simulada['__date__'] = serie_hist_simulada.index

    hist_minMonth = serie_hist_simulada.groupby(['__year__']).min()[['Sim', 'Obs']]
    
    # Main
    hist_minMonth_notnan = hist_minMonth.dropna(axis=0)
    kge, r, alpha, beta = he.evaluator(he.kge, hist_minMonth_notnan['Sim'], hist_minMonth_notnan['Obs'])
    r_pearson, pvalue_pearson = mstats.pearsonr(hist_minMonth_notnan['Sim'], hist_minMonth_notnan['Obs'])

    # Save results
    rv.update({'max_obs'  : hist_minMonth['Obs'].max(skipna=True)})
    rv.update({'mean_obs' : hist_minMonth['Obs'].mean(skipna=True)})
    rv.update({'min_obs'  : hist_minMonth['Obs'].min(skipna=True)})

    rv.update({'max_sim'  : hist_minMonth['Sim'].max(skipna=True)})
    rv.update({'mean_sim' : hist_minMonth['Sim'].mean(skipna=True)})
    rv.update({'min_sim'  : hist_minMonth['Sim'].min(skipna=True)})

    rv.update({'kge' : {'kge' : kge[0], 'r':r[0], 'alpha':alpha[0], 'beta':beta[0]}})
    rv.update({'r2 Pearson' : {'r': r_pearson, 'p_value' : pvalue_pearson}})
    # Plot time series
    hist_minMonth.rename(columns={'Obs' : 'Observada', 'Sim' : 'Simulada'}, inplace=True)

    fig, axs = plt.subplots(1, 2, figsize=(11, 4.5))
    fig.tight_layout(pad=4.5)

    # Left image
    axs[0].plot(hist_minMonth.index, hist_minMonth['Observada'], label='Observada', color='blue')
    axs[0].plot(hist_minMonth.index, hist_minMonth['Simulada'], label='Simulada', color='red')

    axs[0].hlines(y = [rv['max_obs'], rv['min_obs']], color='b', linestyles='dotted',
                  xmax=hist_minMonth.index.max(), xmin=hist_minMonth.index.min(),
                  label='Extremos observados')
    axs[0].hlines(y = [rv['mean_obs']], color='b', linestyles='dashdot', 
                  xmax=hist_minMonth.index.max(), xmin=hist_minMonth.index.min(),
                  label='Promedio observado')
    axs[0].hlines(y = [rv['max_sim'], rv['min_sim']], color='r', linestyles='dotted', 
                  xmax=hist_minMonth.index.max(), xmin=hist_minMonth.index.min(),
                  label='Extremos simulados')
    axs[0].hlines(y = [rv['mean_sim']], color='r', linestyles='dashdot', 
                  xmax=hist_minMonth.index.max(), xmin=hist_minMonth.index.min(),
                  label='Promedio simulado')

    axs[0].legend(fontsize=7)
    axs[0].set_title('KGE : {:.4}'.format(rv["kge"]["kge"]), fontsize = 10)
    axs[0].set_ylabel('Nivel [cm]')
    axs[0].set_xlabel('Año')
    axs[0].grid()

    # Right image
    axs[1].scatter(x = hist_minMonth['Observada'], y = hist_minMonth['Simulada'])
    axs[1].plot([min(rv['min_obs'], rv['min_sim']), max(rv['max_obs'], rv['max_sim'])], [min(rv['min_obs'], rv['min_sim']), max(rv['max_obs'], rv['max_sim'])], '--k')
    axs[1].set_title('$r^2$ : {:.4}'.format(rv["r2 Pearson"]["r"]), fontsize = 10)
    axs[1].set_aspect('equal', 'box')
    axs[1].set_ylabel('Nivel simulado [cm]')
    axs[1].set_xlabel('Nivel observado [cm]')
    axs[1].grid()

    # General image
    fig.suptitle(f'Caudales mínimos anuales\n Estación: {name_estacion} - Código: {codigo_estacion}')

    plt.show()
    # plt.savefig(os.path.join(folder_to_plot, file_serie))
    plt.close()

    rv_return.update({codigo_estacion : rv})

    return rv_return

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

# data_input = {'32097010': 'Mapiripan',
#               '31097010': 'Cuayare'}


for row in data_input:
    name_estacion   = data_input[row]
    codigo_estacion = row
    
    print(name_estacion, codigo_estacion)

    rv = main_fun(name_estacion, codigo_estacion, rv)

# Plot results 
df_rv = pd.DataFrame(rv)
# df_rv.T.to_csv(r'D:\IDEAM\0_ejecucion\10.presentacion\navegacion_imgs\magnitud\METADATA.csv')
