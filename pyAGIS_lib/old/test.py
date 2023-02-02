import pyla
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

codigo_estacion = '47017160'

codigo_estacion = '47017150'

codigo_estacion = '11117050'
codigo_estacion = '37057020'
codigo_estacion = '44037040'

codigo_estacion = '51027060'

codigo_estacion = '21237020'
codigo_estacion = '23037010'
'''
codigo_estacion = '36027050'
codigo_estacion = '12017010'

codigo_estacion = '47017170'

'''

# Extract data
# ------------
comid, _                     = pyla.data_download.get_comit_from_station(ID = codigo_estacion)
serie_hist_observada, _      = pyla.data_download.get_historical_data(codigo_estacion)
serie_hist_simulada, _       = pyla.data_download.get_historical_sim_data(comid, serie_hist_observada)
perfil_del_rio, _            = pyla.data_download.get_perfil_del_rio(estacion = codigo_estacion)
# pronostico_cache, _ = pyla.data_download.get_forecast_data_cache(station = codigo_estacion)

# Main values for series
nivel_de_alerta_bajos_obs, _ = pyla.data_download.get_alerta_minima_fews(codigo_estacion)

caudales_bajos_mens_obs    , _ = pyla.data_analysis.get_low_flows(data=serie_hist_observada)
caudales_extremos_bajos_obs, _ = pyla.data_analysis.get_extreme_low_flows(data=serie_hist_observada)

caudales_bajos_mens_sim    , _ = pyla.data_analysis.get_low_flows(data=serie_hist_simulada)
caudales_extremos_bajos_sim, _ = pyla.data_analysis.get_extreme_low_flows(data=serie_hist_simulada)

# Fix units
# ---------
nivel_de_alerta_bajos_obs    = nivel_de_alerta_bajos_obs * 100

# Data Analysis
# -------------
min_anual_data_obs = serie_hist_observada.copy()
min_anual_data_obs = min_anual_data_obs.groupby(min_anual_data_obs.index.year).min()
max_min_anual_data_obs = min_anual_data_obs.data.max()

min_anual_data_sim = serie_hist_simulada.copy()
min_anual_data_sim = min_anual_data_sim.groupby(min_anual_data_sim.index.year).min()
max_min_anual_data_sim = min_anual_data_sim.data.max()

# Manejo del periodo de retorno
# -----------------------------

def lineal_tranformation(input_data, max_data):
    return -1* (input_data - max_data)
def inv_lineal_transformation(input_data, max_data):
    return (-1 * input_data) + max_data



min_anual_data_obs              = lineal_tranformation(min_anual_data_obs, max_min_anual_data_obs)
nivel_de_alerta_bajos_obs       = lineal_tranformation(nivel_de_alerta_bajos_obs, max_min_anual_data_obs)

min_anual_data_sim              = lineal_tranformation(min_anual_data_sim, max_min_anual_data_sim)

rp_nivel_de_alerta_bajos_obs, _ = pyla.data_analysis.get_return_period_from_data(data = nivel_de_alerta_bajos_obs,    time_serie = min_anual_data_obs.data.values.tolist())
nivel_de_alerta_bajos_sim, _    = pyla.data_analysis.get_data_from_return_period(rp   = rp_nivel_de_alerta_bajos_obs, time_serie = min_anual_data_sim.data.values.tolist())

# rp_100_sim, _ = pyla.get_data_from_return_period(rp = 100, time_serie = min_anual_data_sim.data.values.tolist())
# rp_50_sim, _  = pyla.get_data_from_return_period(rp = 25,  time_serie = min_anual_data_sim.data.values.tolist())
# rp_25_sim, _  = pyla.get_data_from_return_period(rp = 2,  time_serie = min_anual_data_sim.data.values.tolist())

# rp_100_obs, _ = pyla.get_data_from_return_period(rp = 100, time_serie = min_anual_data_obs.data.values.tolist())
# rp_50_obs, _  = pyla.get_data_from_return_period(rp = 25,  time_serie = min_anual_data_obs.data.values.tolist())
# rp_25_obs, _  = pyla.get_data_from_return_period(rp = 2,  time_serie = min_anual_data_obs.data.values.tolist())

min_anual_data_obs              = inv_lineal_transformation(min_anual_data_obs, max_min_anual_data_obs)
nivel_de_alerta_bajos_obs       = inv_lineal_transformation(nivel_de_alerta_bajos_obs, max_min_anual_data_obs)

min_anual_data_sim              = inv_lineal_transformation(min_anual_data_sim, max_min_anual_data_sim)
nivel_de_alerta_bajos_sim       = inv_lineal_transformation(nivel_de_alerta_bajos_sim, max_min_anual_data_sim)

# rp_100_sim = inv_lineal_transformation(rp_100_sim, max_min_anual_data_sim)
# rp_50_sim  = inv_lineal_transformation(rp_50_sim,  max_min_anual_data_sim)
# rp_25_sim  = inv_lineal_transformation(rp_25_sim,  max_min_anual_data_sim)

# rp_100_sim = rp_100_sim if rp_100_sim > 0 else 0
# rp_50_sim  = rp_50_sim if rp_50_sim > 0 else 0
# rp_25_sim  = rp_25_sim if rp_25_sim > 0 else 0

# rp_100_obs = inv_lineal_transformation(rp_100_obs, max_min_anual_data_obs)
# rp_50_obs  = inv_lineal_transformation(rp_50_obs,  max_min_anual_data_obs)
# rp_25_obs  = inv_lineal_transformation(rp_25_obs,  max_min_anual_data_obs)

# rp_100_obs = rp_100_obs if rp_100_obs > 0 else 0
# rp_50_obs  = rp_50_obs if rp_50_obs > 0 else 0
# rp_25_obs  = rp_25_obs if rp_25_obs > 0 else 0

print('')
print(f'Nivel de alerta bajo FEWS : {nivel_de_alerta_bajos_obs}')
print(f'Periodo de retorno de nivel de alerta bajo FEWS : {rp_nivel_de_alerta_bajos_obs}')
print(f'Nivel de alerta bajo Sim: {nivel_de_alerta_bajos_sim} para periodo de retorno : {rp_nivel_de_alerta_bajos_obs} ')
print('')

'''
# Comparacion de resultados
# -------------------------
comp_time_series        = serie_hist_observada.copy()
comp_time_series['obs'] = serie_hist_observada['data']
comp_time_series.drop('data', inplace=True, axis=1)
comp_time_series['sim'] = serie_hist_simulada['data']
comp_time_series.dropna(inplace=True, how='any')

comp_time_series['obs_flag'] = 0
comp_time_series.loc[comp_time_series['obs'] <= nivel_de_alerta_bajos_obs, 'obs_flag'] = 1
comp_time_series['sim_flag'] = 0
comp_time_series.loc[comp_time_series['sim'] <= nivel_de_alerta_bajos_sim, 'sim_flag'] = 1

confusion_matrix = pd.crosstab(comp_time_series['obs_flag'], 
                               comp_time_series['sim_flag'], 
                               rownames=['Alertas observadas'], 
                               colnames=['Alertas simuladas'])
confusion_matrix_array = confusion_matrix.values

print('')
print('Matriz de confusión:')
print(confusion_matrix)
print('')

cpd       = confusion_matrix_array[1,1] / sum(confusion_matrix_array[1,:]) # Porcentaje de casos positivos detectados
cnd       = confusion_matrix_array[0,0] / sum(confusion_matrix_array[0,:]) # Porcentaje de casos negativos detectados
ppc       = confusion_matrix_array[1,1] / sum(confusion_matrix_array[:, 1]) # Porcentaje de predicciones positivas correctas
accurracy = (confusion_matrix_array[0,0] + confusion_matrix_array[1,1]) / np.sum(confusion_matrix_array) # Porcentaje de predicciones correctas

print( 'Porcentaje de casos positivos detectados {0:.2f}%'.format(cpd*100))
print( 'Porcentaje de casos negativos detectados {0:.2f}%'.format(cnd*100))
print( 'Porcentaje de predicciones positivas correctas {0:.2f}%'.format(ppc*100))
print( 'Porcentaje de predicciones correctas {0:.2f}%'.format(accurracy*100))
print('')

'''

def consecutive_days_pos_neg(serie_hist_observada):
    diff_1_hist_obs = serie_hist_observada.data.diff(1).to_frame()

    diff_1_hist_obs_sng = diff_1_hist_obs.data / abs(diff_1_hist_obs.data)

    hist_obs_consecutive_days_pos = diff_1_hist_obs_sng.copy()
    hist_obs_consecutive_days_neg = -1 * (diff_1_hist_obs_sng.copy())

    hist_obs_consecutive_days_pos.loc[hist_obs_consecutive_days_pos < 0 ] = 0
    hist_obs_consecutive_days_neg.loc[hist_obs_consecutive_days_neg < 0 ] = 0

    hist_obs_consecutive_days_pos = hist_obs_consecutive_days_pos.to_frame()
    hist_obs_consecutive_days_neg = hist_obs_consecutive_days_neg.to_frame()

    hist_obs_consecutive_days_pos.loc[hist_obs_consecutive_days_pos.data == 0] = float('nan')
    hist_obs_consecutive_days_neg.loc[hist_obs_consecutive_days_neg.data == 0] = float('nan')

    cumsum = hist_obs_consecutive_days_pos.data.cumsum().fillna(method='pad')
    reset  = -cumsum[hist_obs_consecutive_days_pos.data.isnull()].diff().fillna(cumsum)
    hist_obs_consecutive_days_pos.data = hist_obs_consecutive_days_pos.data.where(hist_obs_consecutive_days_pos.data.notnull(), reset).cumsum()
    hist_obs_consecutive_days_pos.loc[hist_obs_consecutive_days_pos.data == 0] = float('nan')

    cumsum = hist_obs_consecutive_days_neg.data.cumsum().fillna(method='pad')
    reset  = -cumsum[hist_obs_consecutive_days_neg.data.isnull()].diff().fillna(cumsum)
    hist_obs_consecutive_days_neg.data = hist_obs_consecutive_days_neg.data.where(hist_obs_consecutive_days_neg.data.notnull(), reset).cumsum()
    hist_obs_consecutive_days_neg.loc[hist_obs_consecutive_days_neg.data == 0] = float('nan')

    return hist_obs_consecutive_days_pos, hist_obs_consecutive_days_neg, diff_1_hist_obs_sng, diff_1_hist_obs

hist_obs_consecutive_days_pos, hist_obs_consecutive_days_neg, diff_1_hist_obs_sng, diff_1_hist_obs = consecutive_days_pos_neg(serie_hist_observada)
hist_sim_consecutive_days_pos, hist_sim_consecutive_days_neg, diff_1_hist_sim_sng, diff_1_hist_sim = consecutive_days_pos_neg(serie_hist_simulada)

# Analysis cosecutive days

print('Analisis de dias consecutivos: ')
consecutive_days = diff_1_hist_obs_sng.to_frame()
consecutive_days['obs'] = consecutive_days.data
consecutive_days.drop('data', axis=1, inplace=True)
consecutive_days['sim'] = diff_1_hist_sim_sng.to_frame().data

confusion_matrix = pd.crosstab(consecutive_days['obs'], 
                               consecutive_days['sim'], 
                               rownames=['Dias consecutivos observados'], 
                               colnames=['Días consecutivos simulados'])
confusion_matrix_array = confusion_matrix.values
confusion_matrix_array = confusion_matrix.values

print('')
print('Matriz de confusión:')
print(confusion_matrix)
print('')

cpd       = confusion_matrix_array[1,1] / sum(confusion_matrix_array[1,:]) # Porcentaje de casos positivos detectados
cnd       = confusion_matrix_array[0,0] / sum(confusion_matrix_array[0,:]) # Porcentaje de casos negativos detectados
ppc       = confusion_matrix_array[1,1] / sum(confusion_matrix_array[:, 1]) # Porcentaje de predicciones positivas correctas
accurracy = (confusion_matrix_array[0,0] + confusion_matrix_array[1,1]) / np.sum(confusion_matrix_array) # Porcentaje de predicciones correctas

print( 'Porcentaje de casos positivos detectados {0:.2f}%'.format(cpd*100))
print( 'Porcentaje de casos negativos detectados {0:.2f}%'.format(cnd*100))
print( 'Porcentaje de predicciones positivas correctas {0:.2f}%'.format(ppc*100))
print( 'Porcentaje de predicciones correctas {0:.2f}%'.format(accurracy*100))
print('')

print('')

print('Analisis de dias consecutivos de ascenso: ')

consecutive_days_pos = hist_obs_consecutive_days_pos.copy()
consecutive_days_pos['obs'] = consecutive_days_pos.data
consecutive_days_pos.drop('data', axis=1, inplace=True)
consecutive_days_pos['sim'] = hist_sim_consecutive_days_pos.data
consecutive_days_pos.dropna(inplace=True, how='any')


confusion_matrix = pd.crosstab(consecutive_days_pos['obs'], 
                               consecutive_days_pos['sim'], 
                               rownames=['Dias consecutivos observados'], 
                               colnames=['Días consecutivos simulados'])
confusion_matrix_array = confusion_matrix.values
print(confusion_matrix)
print('')

print('Analisis de dias consecutivos de descenso: ')
consecutive_days_neg = hist_obs_consecutive_days_neg.copy()
consecutive_days_neg['obs'] = consecutive_days_neg.data
consecutive_days_neg.drop('data', axis=1, inplace=True)
consecutive_days_neg['sim'] = hist_sim_consecutive_days_neg.data
consecutive_days_neg.dropna(inplace=True, how='any')

confusion_matrix = pd.crosstab(consecutive_days_neg['obs'], 
                               consecutive_days_neg['sim'], 
                               rownames=['Dias consecutivos observados'], 
                               colnames=['Días consecutivos simulados'])
confusion_matrix_array = confusion_matrix.values
print(confusion_matrix)
print('')

###########################################################################
#                                  PLOT
###########################################################################

date_to_plot = '2019-12-31'
date_to_plot_f = '2020-12-31'

fig, ax = plt.subplots(nrows=4, 
                       ncols=2, 
                       figsize=(20, 20), 
                       sharex=False,
                       gridspec_kw={
                           'width_ratios':  [5, 1],
                           'height_ratios': [3, 3, 3, 3],
                       'wspace': 0.2,
                       'hspace': 0.2})

ax[0, 0].set_title('Historical serie')
ax[0, 0].plot(serie_hist_observada.data.loc[date_to_plot: date_to_plot_f], label='obs')
ax[0, 0].plot(serie_hist_simulada.data.loc[date_to_plot: date_to_plot_f], label='sim')

ax[0, 0].hlines(y = nivel_de_alerta_bajos_obs,
                xmin = serie_hist_observada.loc[date_to_plot: date_to_plot_f].index[0],
                xmax = serie_hist_observada.loc[date_to_plot: date_to_plot_f].index[-1],
                colors='cyan',
                label='nivel_de_alerta_bajos_obs : {:.2f}'.format(nivel_de_alerta_bajos_obs))


ax[0, 0].hlines(y = nivel_de_alerta_bajos_sim,
                xmin = serie_hist_simulada.loc[date_to_plot: date_to_plot_f].index[0],
                xmax = serie_hist_simulada.loc[date_to_plot: date_to_plot_f].index[-1],
                colors='darkblue',
                label='nivel_de_alerta_bajos_sim : {:.2f} (T:{:.1f} años)'.format(nivel_de_alerta_bajos_sim, rp_nivel_de_alerta_bajos_obs))

ax[0, 1].boxplot([serie_hist_observada.data.loc[date_to_plot: date_to_plot_f].dropna().array,
                  serie_hist_simulada.data.loc[date_to_plot: date_to_plot_f].dropna().array])
ax[0, 1].set_xticklabels(['obs', 'sim'])
ax[0, 1].grid()

ax[1, 0].set_title('Diference to 1 day ')
ax[1, 0].plot(diff_1_hist_obs.loc[date_to_plot: date_to_plot_f], label = 'dif obs')
ax[1, 0].plot(diff_1_hist_sim.loc[date_to_plot: date_to_plot_f], label = 'dif sim')

ax[1, 1].boxplot([diff_1_hist_obs.data.loc[date_to_plot: date_to_plot_f].dropna().array,
                  diff_1_hist_sim.data.loc[date_to_plot: date_to_plot_f].dropna().array])
ax[1, 1].set_xticklabels(['obs', 'sim'])
ax[1, 1].grid()

ax[2, 0].scatter(x = hist_obs_consecutive_days_pos.data.loc[date_to_plot: date_to_plot_f].index,
                 y = hist_obs_consecutive_days_pos.data.loc[date_to_plot: date_to_plot_f],
                 label = 'Up',
                 marker='.')
ax[2, 0].scatter(x = hist_obs_consecutive_days_neg.data.loc[date_to_plot: date_to_plot_f].index,
              y = -1 * hist_obs_consecutive_days_neg.data.loc[date_to_plot: date_to_plot_f],
              label = 'Down',
              marker='.')

ax[2, 1].boxplot([hist_obs_consecutive_days_pos.data.loc[date_to_plot: date_to_plot_f].dropna().array,
                  hist_sim_consecutive_days_pos.data.loc[date_to_plot: date_to_plot_f].dropna().array,])
ax[2, 1].set_xticklabels(['obs', 'sim'])
ax[2, 1].grid()

ax[3, 0].scatter(x = hist_sim_consecutive_days_pos.data.loc[date_to_plot: date_to_plot_f].index,
              y = hist_sim_consecutive_days_pos.data.loc[date_to_plot: date_to_plot_f],
              label = 'Up',
              marker='.')
ax[3, 0].scatter(x = hist_sim_consecutive_days_neg.data.loc[date_to_plot: date_to_plot_f].index,
              y = -1 * hist_sim_consecutive_days_neg.data.loc[date_to_plot: date_to_plot_f],
              label = 'Down',
              marker='.')

ax[3, 1].boxplot([-1 * hist_obs_consecutive_days_neg.data.loc[date_to_plot: date_to_plot_f].dropna().array,
                  -1 * hist_sim_consecutive_days_neg.data.loc[date_to_plot: date_to_plot_f].dropna().array])
ax[3, 1].set_xticklabels(['obs', 'sim'])
ax[3, 1].grid()

ax[0, 0].legend()
ax[1, 0].legend()

ax[2, 0].set_title('Obs - consecutive days behavior')
ax[2, 0].legend()

ax[3, 0].set_title('sim - consecutive days behavior')
ax[3, 0].legend()

ax[0, 0].grid()
ax[1, 0].grid()
ax[2, 0].grid()
ax[3, 0].grid()

plt.show()

# Review plot
#------------
fig, axs = plt.subplots(3, 2, figsize=(15, 15))
fig.tight_layout(pad=5.0)
_ = pyla.data_plot.scatter_monthly_yearly_comparation(obs_serie = serie_hist_observada,
                                                      sim_serie = serie_hist_simulada,
                                                      ax        = axs[0, 0])
_ = pyla.data_plot.serie_monthly_yearly_comparation(obs_serie = serie_hist_observada,
                                                    sim_serie = serie_hist_simulada,
                                                    ax        = axs[0, 1])

_ = pyla.data_plot.scatter_monthly_comparation(obs_serie = serie_hist_observada,
                                               sim_serie = serie_hist_simulada,
                                               ax        = axs[1, 0])
_ = pyla.data_plot.serie_monthly_comparation(obs_serie = serie_hist_observada,
                                             sim_serie = serie_hist_simulada,
                                             ax        = axs[1, 1])

_ = pyla.data_plot.scatter_yearly_comparation(obs_serie = serie_hist_observada,
                                              sim_serie = serie_hist_simulada,
                                              ax        = axs[2, 0])
_ = pyla.data_plot.serie_yearly_comparation(obs_serie = serie_hist_observada,
                                            sim_serie = serie_hist_simulada,
                                            ax        = axs[2, 1])

axs[0, 0].grid()
axs[0, 1].grid()
axs[1, 0].grid()
axs[1, 1].grid()
axs[2, 0].grid()
axs[2, 1].grid()
plt.show()


#############################################################################
#                   Comparison return periods last one
#############################################################################

serie_hist_observada_tmp = serie_hist_observada.copy()
serie_hist_simulada_tmp  = serie_hist_simulada.copy()


serie_hist_observada_tmp['__year__'] = serie_hist_observada_tmp.index.year
serie_hist_observada_tmp['__month__'] = serie_hist_observada_tmp.index.month
mean_year_min_month_data_obs = serie_hist_observada_tmp.groupby(['__year__', '__month__']).min().groupby(['__year__']).mean()

serie_hist_simulada_tmp['__year__'] = serie_hist_simulada_tmp.index.year
serie_hist_simulada_tmp['__month__'] = serie_hist_simulada_tmp.index.month
mean_year_min_month_data_sim = serie_hist_simulada_tmp.groupby(['__year__', '__month__']).min().groupby(['__year__']).mean()

min_yearly_data_obs = serie_hist_observada.groupby([serie_hist_observada.index.year]).min()['data'].values.tolist()
min_yearly_data_sim = serie_hist_simulada.groupby([serie_hist_simulada.index.year]).min()['data'].values.tolist()

# min_yearly_data_obs = mean_year_min_month_data_obs.values.tolist()
# min_yearly_data_sim = mean_year_min_month_data_sim.values.tolist()

def f_get_return_period_from_data(input, serie):
    input       = lineal_tranformation(input, np.nanmax(serie))
    if input > 0:
        rp_nivel_de_alerta_bajos_obs, _ = pyla.data_analysis.get_return_period_from_data(data = input, time_serie = serie)
        return rp_nivel_de_alerta_bajos_obs
    else:
        return np.nan

serie_hist_observada_tmp['obs'] = serie_hist_observada_tmp['data'].map(lambda x : f_get_return_period_from_data(input=x, serie=min_yearly_data_obs))
serie_hist_simulada_tmp['sim']  = serie_hist_simulada_tmp['data'].map(lambda x : f_get_return_period_from_data(input=x, serie=min_yearly_data_sim))

df_rp = serie_hist_observada_tmp.copy()
df_rp['data obs'] = serie_hist_observada_tmp['data']
df_rp['data sim'] = serie_hist_simulada_tmp['data']
df_rp['obs'] = serie_hist_observada_tmp['obs']
df_rp['sim'] = serie_hist_simulada_tmp['sim']
df_rp.drop('data', axis=1, inplace=True)

# df_rp.loc[df_rp['obs'] > 200,'obs'] = np.nan
# df_rp.loc[df_rp['sim'] > 200,'sim'] = np.nan

# df_rp.dropna(inplace=True)

from sklearn.metrics import r2_score as R2

fig, axs = plt.subplots(1, 1)
axs.scatter(x = df_rp['obs'], y = df_rp['sim'])
axs.grid()
axs.set_xscale('log')
axs.set_yscale('log')
axs.set_xlabel('obs')
axs.set_ylabel('sim')
axs.set_title(R2(df_rp.dropna()['obs'], df_rp.dropna()['sim']))
# axs.set_aspect('equal', 'box')
plt.show()


fig, axs = plt.subplots(1, 1, figsize=(18, 5))
df_rp['obs'].plot(ax = axs, label='observada')
df_rp['sim'].plot(ax = axs, label='simulada')
axs.legend()
axs.grid()
axs.set_xlabel('fecha')
axs.set_ylabel('Periodo de retorno')
axs.set_title(R2(df_rp.dropna()['obs'], df_rp.dropna()['sim']))
# axs.set_aspect('equal', 'box')
plt.show()

fig, axs = plt.subplots(1, 1, figsize=(18, 5))
df_rp['data obs'].groupby(df_rp.index.year).min().plot(ax = axs, label='observada')
df_rp['data sim'].groupby(df_rp.index.year).min().plot(ax = axs, label='simulada')
axs.legend()
axs.grid()
axs.set_xlabel('fecha')
axs.set_ylabel('N')
axs.set_title(R2(df_rp.dropna()['data obs'], df_rp.dropna()['data sim']))
# axs.set_aspect('equal', 'box')
plt.show()

print(df_rp)

print(R2(df_rp.groupby(df_rp.index.year).min().dropna(how='any')['sim'], df_rp.groupby(df_rp.index.year).min().dropna(how='any')['obs']))

# 
