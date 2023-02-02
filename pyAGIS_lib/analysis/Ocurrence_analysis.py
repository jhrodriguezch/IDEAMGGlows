import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import pyAGIS

class Main_fun:
    def __call__(self, name_estacion, codigo_estacion, rv_end):
        rv = {}

        # ----- Define folder to plot images -----
        folder_to_plot  = r'D:\IDEAM\0_ejecucion\10.presentacion\navegacion_imgs\ocurrencia'

        path_file_serie_obs = os.path.join(folder_to_plot, codigo_estacion + '.serieObs.Ocurrence.pdf')
        path_file_serie_sim = os.path.join(folder_to_plot, codigo_estacion + '.serieSim.Ocurrence.pdf')

        ################################ START ###############################

        comid, _        = pyAGIS.data_download.get_comit_from_station(ID = codigo_estacion)

        # ----- Build time series -----
        serie_hist_observada, _      = pyAGIS.data_download.get_historical_data(codigo_estacion)
        serie_hist_simulada, _       = pyAGIS.data_download.get_historical_sim_data(comid, serie_hist_observada)
        
        # ----- Fix time series -----
        minY_obs = serie_hist_observada.rolling(window=7).mean().groupby(serie_hist_observada.index.year).min()
        minY_sim = serie_hist_simulada.rolling(window=7).mean().groupby(serie_hist_simulada.index.year).min()
        
        # ----- Calc early warnings -----
        # Obs
        rv.update({'Obs' : {}})

        nivel_de_alerta_bajos_obs, _ = pyAGIS.data_download.get_alerta_minima_fews(codigo_estacion)
        nivel_de_alerta_bajos_obs = nivel_de_alerta_bajos_obs * 100
        if not np.isnan(nivel_de_alerta_bajos_obs):
            rv['Obs'].update({'ew_fews_obs' : {'value' : nivel_de_alerta_bajos_obs,
                                               'color' : 'darkblue',
                                               'name'  : 'FEWS'}})

        ew_7n10_obs = self.__ew7n10__(minY_obs)
        rv['Obs'].update({'ew_7n10_obs' : {'value' : ew_7n10_obs,
                                           'color' : 'darkgreen',
                                           'name' : '7n10'}})

        p10_minY = serie_hist_observada.groupby(serie_hist_observada.index.year).min().quantile(0.1).values[0]
        rv['Obs'].update({'ew_p10_minY' : {'value' : p10_minY,
                                           'color' : 'darkred',
                                           'name'  : 'p10_minY'}})
        
        # Sim
        rv.update({'Sim' : {}})

        if not np.isnan(nivel_de_alerta_bajos_obs):
            ew_from_fews_sim = self.__calc_ex_from_fews__(value     = nivel_de_alerta_bajos_obs,
                                                          obs_serie = serie_hist_observada,
                                                          sim_serie = serie_hist_simulada)
            rv['Sim'].update({'ew_from_fews_sim' : {'value' : ew_from_fews_sim,
                                                    'color' : 'darkblue',
                                                    'name'  : 'FEWS'}})

        ew_7n10_sim = self.__ew7n10__(minY_sim)
        rv['Sim'].update({'ew_7n10_sim' : {'value' : ew_7n10_sim,
                                           'color' : 'darkgreen',
                                           'name'  : '7n10'}})

        p10_minY_sim = serie_hist_simulada.groupby(serie_hist_simulada.index.year).min().quantile(0.1).values[0]
        rv['Sim'].update({'p10_minY_sim' : {'value' : p10_minY_sim,
                                           'color' : 'darkred',
                                           'name'  : 'p10_minY'}})

        # ----- Main -----
        # Obs
        for hlines_name in rv['Obs'].keys():
            df_tmp = serie_hist_observada.copy()
            hline_comp = rv['Obs'][hlines_name]['value']
            
            df_tmp['ew'] = 0.0
            df_tmp.loc[df_tmp['data'] <= hline_comp, 'ew'] = 1.0
            
            rv['Obs'][hlines_name].update({'Existence' : df_tmp['ew'].to_frame()})

        # Sim
        for hlines_name in rv['Sim'].keys():
            df_tmp = serie_hist_simulada.copy()
            hline_comp = rv['Sim'][hlines_name]['value']
            
            df_tmp['ew'] = 0.0
            df_tmp.loc[df_tmp['data'] <= hline_comp, 'ew'] = 1.0
            
            rv['Sim'][hlines_name].update({'Existence' : df_tmp['ew'].to_frame()})

        # Cualitative comparation
        # Obs and Sim
        for key_obs, key_sim in list(zip(rv['Obs'].keys(), rv['Sim'].keys())):
            df_ew_obs = rv['Obs'][key_obs]['Existence'].copy()
            df_ew_sim = rv['Sim'][key_sim]['Existence'].copy()

            # Fix dataframes
            df_ew_sim.rename(columns={'ew' : 'Sim'}, inplace=True)
            df_ew_sim['Obs'] = df_ew_obs['ew']
            df_ew_sim.dropna(inplace=True, axis=0)

            # Confussion matrix
            tp = df_ew_sim[(df_ew_sim['Obs'] == 1) & (df_ew_sim['Sim'] == 1)].shape[0]
            tn = df_ew_sim[(df_ew_sim['Obs'] == 0) & (df_ew_sim['Sim'] == 0)].shape[0]
            fn = df_ew_sim[(df_ew_sim['Obs'] == 1) & (df_ew_sim['Sim'] == 0)].shape[0]
            fp = df_ew_sim[(df_ew_sim['Obs'] == 0) & (df_ew_sim['Sim'] == 1)].shape[0]

            # Metrics
            tpr = tp / (tp + fn) if (tp + fn) != 0 else np.nan
            fpr = fp / (fp + tn) if (fp + tn) != 0 else np.nan
            acc = (tn + tp) / (tn + fp + fn + tp) if (tn + fp + fn + tp) != 0 else np.nan
            sen = tp / (tp + fn) if (tp + fn) != 0 else np.nan
            spe = tn / (tn + fp) if (tn + fp) != 0 else np.nan
            pre = tp / (fp + tp) if (fp + tp) != 0 else np.nan
            f1s = (2 * pre * sen) / (pre + sen) if (pre + sen) != 0 else np.nan

            # Save metricts
            rv['Sim'][key_sim].update({'Matrix de confusion : '       : np.array([[tp, fp], [fn, tn]]),
                                       'True positives rate : '       : tpr,
                                       'False positives rate : '      : fpr,
                                       'Exactitud (Accurracy) : '     : acc,
                                       'Sensibilidad (Recall) : '     : sen,
                                       'Especificidad (Specifity) : ' : spe,
                                       'Precision (precision) : '     : pre,
                                       'f1-score : '                  : f1s })

            del df_ew_obs, df_ew_sim
        
        # ----- Plot -----
        # OBS
        # plot variables
        n_cols = len(rv['Obs']) + 1 
        height_ratios = [4] + [0.5]*(len(rv['Obs']))
        figsize = (12 , 3 + 1 * (len(rv['Obs'])) )

        # Draw
        fig, axs = plt.subplots(n_cols, 1,
                                figsize=figsize,
                                gridspec_kw={'height_ratios': height_ratios},
                                sharex=True)
        fig.tight_layout(pad=3.0)
        axs[0].plot(serie_hist_observada.index, serie_hist_observada['data'], label='Observado')

        if not np.isnan(nivel_de_alerta_bajos_obs):
            axs[0].hlines(y=nivel_de_alerta_bajos_obs, colors='darkblue', linestyles='dotted',
                          xmin=serie_hist_observada.index.min(), xmax=serie_hist_observada.index.max(),
                          label='Nivel bajo - FEWS - {} cm'.format(np.round(nivel_de_alerta_bajos_obs, 1)))
        
        axs[0].hlines(y=ew_7n10_obs, colors='darkgreen', linestyles='dotted',
                      xmin=serie_hist_observada.index.min(), xmax=serie_hist_observada.index.max(),
                      label='Nivel bajo - 7Q10(N) - {} cm'.format(np.round(ew_7n10_obs, 1)))

        axs[0].hlines(y = p10_minY, colors='darkred', linestyles='dotted',
                      xmin = serie_hist_observada.index.min(), xmax=serie_hist_observada.index.max(),
                      label ='Nivel bajo - P10(NMinY) - {} cm'.format(np.round(p10_minY, 1)))

        axs[0].legend(fontsize=7)
        axs[0].grid()

        for num, hline_name in enumerate(rv['Obs'].keys()):
            rv['Obs'][hline_name]['Existence'].plot.area(ax = axs[num + 1], legend=False, color=rv['Obs'][hline_name]['color'])
            axs[num + 1].set_title('Nivel menor : {:.1f} cm\nAlerta: {}'.format(rv['Obs'][hline_name]['value'], hline_name), fontsize=7)
            axs[num + 1].set_ylim((0,1))
            axs[num + 1].set_xlabel('')
            
        axs[num+1].set_xlabel('Fecha')
        
        fig.suptitle(f'Ocurrencia de niveles bajos (Observado).\n Estación: {name_estacion} ID: {codigo_estacion}')
        plt.show()
        # plt.savefig(path_file_serie_obs)
        plt.close()

        # SIM
        ## plot variables
        n_cols = len(rv['Sim']) + 1 
        height_ratios = [4] + [0.5]*(len(rv['Sim']))
        figsize = (12 , 3 + 1 * (len(rv['Sim'])) )

        # Draw series
        fig, axs = plt.subplots(n_cols, 1,
                                figsize=figsize,
                                gridspec_kw={'height_ratios': height_ratios},
                                sharex=True)
        fig.tight_layout(pad=3.0)
        axs[0].plot(serie_hist_simulada.index, serie_hist_simulada['data'], label='Simulada', color='red')

        
        if not np.isnan(nivel_de_alerta_bajos_obs):
            axs[0].hlines(y=ew_from_fews_sim, colors='darkblue', linestyles='dotted',
                          xmin=serie_hist_simulada.index.min(), xmax=serie_hist_simulada.index.max(),
                          label='Nivel bajo - FEWS - {} cm'.format(np.round(nivel_de_alerta_bajos_obs, 1)))
        

        axs[0].hlines(y=ew_7n10_sim, colors='darkgreen', linestyles='dotted',
                      xmin=serie_hist_simulada.index.min(), xmax=serie_hist_simulada.index.max(),
                      label='Nivel bajo - 7Q10(N) - {} cm'.format(np.round(ew_7n10_sim, 1)))

        axs[0].hlines(y = p10_minY_sim, colors='darkred', linestyles='dotted',
                      xmin = serie_hist_simulada.index.min(), xmax=serie_hist_simulada.index.max(),
                      label ='Nivel bajo - P10(NMinY) - {} cm'.format(np.round(p10_minY_sim, 1)))

        axs[0].legend(fontsize=7)
        axs[0].grid()

        for num, hline_name in enumerate(rv['Sim'].keys()):
            rv['Sim'][hline_name]['Existence'].plot.area(ax = axs[num + 1], legend=False, color=rv['Sim'][hline_name]['color'])
            axs[num + 1].set_title('Nivel menor : {:.1f} cm\nAlerta: {}'.format(rv['Sim'][hline_name]['value'], hline_name), fontsize=7)
            axs[num + 1].set_ylim((0,1))
            axs[num + 1].set_xlabel('')

        axs[num+1].set_xlabel('Fecha')
        
        fig.suptitle(f'Ocurrencia de niveles bajos (Simulado).\n Estación: {name_estacion} ID: {codigo_estacion}')
        plt.show()
        # plt.savefig(path_file_serie_sim)
        plt.close()

        ## Draw matrix
        for key_sim, key_obs in zip(rv['Sim'].keys(), rv['Obs'].keys()):

            fig, axs = plt.subplots(1,1, figsize=(3.5, 4.0))
            fig.tight_layout(pad=5.0)
            axs.matshow(rv['Sim'][key_sim]['Matrix de confusion : '], cmap='seismic')

            for (i, j), z in np.ndenumerate(rv['Sim'][key_sim]['Matrix de confusion : ']):
                axs.text(j, i, '{}'.format(z), ha='center', va='center',
                         bbox=dict(pad=5.0, facecolor='white', edgecolor='0.3', alpha=0.7))

            axs.set_xticklabels(['', 'Si', 'No'])
            axs.set_yticklabels(['', 'Si', 'No'])
            
            axs.set_ylabel('Alerta simulada\n[{:.1f} cm]'.format(rv['Sim'][key_sim]['value']))
            axs.set_xlabel('Alerta observada\n[{:.1f} cm]'.format(rv['Obs'][key_obs]['value']))

            axs.set_title('Matrix de confusión. - {}\nEstación: {}\nID: {}\nTPR: {:.2f}, FPR: {:.2f}, f1-score:{:.2f}'.format(rv['Sim'][key_sim]['name'],
                                                                                                                             name_estacion,
                                                                                                                             codigo_estacion,
                                                                                                                             rv['Sim'][key_sim]['True positives rate : '],
                                                                                                                             rv['Sim'][key_sim]['False positives rate : '],
                                                                                                                             rv['Sim'][key_sim]['f1-score : ']))
            # plt.show()
            path_file_conf_mat = os.path.join(folder_to_plot, '.'.join([codigo_estacion, rv['Sim'][key_sim]['name'], 'ConfusionMatrix','Ocurrence','pdf']))
            plt.show()
            # plt.savefig(path_file_conf_mat)
            plt.close()

        for key_obs, key_sim in zip(rv['Obs'].keys(), rv['Sim'].keys()):

            rv['Sim'][key_sim]['Matrix de confusion : '] = {'tp' : rv['Sim'][key_sim]['Matrix de confusion : '][0,0],
                                                            'fp' : rv['Sim'][key_sim]['Matrix de confusion : '][0,1],
                                                            'fn' : rv['Sim'][key_sim]['Matrix de confusion : '][1,0],
                                                            'tn' : rv['Sim'][key_sim]['Matrix de confusion : '][1,1]}

            del rv['Obs'][key_obs]['Existence']
            del rv['Sim'][key_sim]['Existence']

        rv_end.update({codigo_estacion : rv})
        print('\n{}\n'.format("\N{box drawings light horizontal}" * 40))

        return rv_end


    def __ew7n10__(self, minY):
        rv, _ = pyla.data_analysis.get_data_from_return_period(rp = 10, time_serie = minY)
        return rv

    def __calc_ex_from_fews__(self, value, obs_serie, sim_serie):
        
        
        def lin_trans(input_data, max_data):
            return -1* (input_data - max_data)

        def lin_trans_inv(input_data, max_data):
            return (-1 * input_data) + max_data
        
        obs_minY_serie = obs_serie.groupby(obs_serie.index.year).min()
        sim_minY_serie = sim_serie.groupby(sim_serie.index.year).min()
        
        
        obs_max_minY = obs_minY_serie.data.max()
        sim_max_minY = sim_minY_serie.data.max()
        
        obs_minY_serie_fix = lin_trans(obs_minY_serie, obs_max_minY)
        sim_minY_serie_fix = lin_trans(sim_minY_serie, sim_max_minY)
        value_fix          = lin_trans(value, obs_max_minY)
        
        rp_value, _ = pyla.data_analysis.get_return_period_from_data(data = value_fix, time_serie = obs_minY_serie_fix.data.values.tolist(), probability = '__exceedance__')
        rv   , _    = pyla.data_analysis.get_data_from_return_period(rp   = rp_value,  time_serie = sim_minY_serie_fix.data.values.tolist(), probability = '__exceedance__')

        rv_fix = lin_trans_inv(rv, sim_max_minY)
        
        return rv_fix
    


def main_fun(*args, **kwards):
    foo = Main_fun()
    return foo(*args, **kwards)

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
# df_rv.T.to_csv(r'D:\IDEAM\0_ejecucion\10.presentacion\navegacion_imgs\ocurrencia\METADATA.csv')
