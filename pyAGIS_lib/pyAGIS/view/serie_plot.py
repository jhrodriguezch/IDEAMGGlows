import numpy as np
import pandas as pd
from   ..model.timeseries_analysis import min_monthly_yearly, min_monthly, min_yearly, R2

class Monthly_minimum_plot:
    def __init__(self, obs_serie, sim_serie, ax):
        self.obs = obs_serie
        self.sim = sim_serie
        self.ax  = ax

    def __call__(self):

        # Calc principal time series
        self.monthly_yearly_observate_timeserie = min_monthly_yearly(self.obs)
        self.monthly_yearly_simulate_timeserie  = min_monthly_yearly(self.sim)
        self.monthly_yearly_dataframe           = self.__join_time_serie__(obs = self.monthly_yearly_observate_timeserie, 
                                                                           sim = self.monthly_yearly_simulate_timeserie)

        self.monthly_observate_min_timeserie = min_monthly(self.obs)
        self.monthly_simulate_min_timeserie  = min_monthly(self.sim)
        self.monthly_dataframe               = self.__join_time_serie__(obs = self.monthly_observate_min_timeserie, 
                                                                        sim = self.monthly_simulate_min_timeserie)

        self.yearly_observate_min_timeserie = min_yearly(self.obs)
        self.yearly_simulate_min_timeserie  = min_yearly(self.sim)
        self.yearly_dataframe               = self.__join_time_serie__(obs = self.yearly_observate_min_timeserie, 
                                                                       sim = self.yearly_simulate_min_timeserie)


    # Get methods
    def get_monthly_minimum_scatter(self, type_serie):

        if type_serie == 'min_monthly_yearly':
            r2_rv = R2(self.monthly_yearly_dataframe.dropna().obs, self.monthly_yearly_dataframe.dropna().sim)
            obs_data = self.monthly_yearly_dataframe.obs
            sim_data = self.monthly_yearly_dataframe.sim
        elif type_serie == 'min_monthly':
            r2_rv = R2(self.monthly_dataframe.dropna().obs, self.monthly_dataframe.dropna().sim)
            obs_data = self.monthly_dataframe.obs
            sim_data = self.monthly_dataframe.sim
        elif type_serie == 'min_yearly':
            r2_rv = R2(self.yearly_dataframe.dropna().obs, self.yearly_dataframe.dropna().sim)
            obs_data = self.yearly_dataframe.obs
            sim_data = self.yearly_dataframe.sim

        max_value = max(np.nanmax(obs_data), np.nanmax(sim_data))
        min_value = min(np.nanmin(obs_data), np.nanmin(sim_data))

        self.ax.scatter(x = obs_data,
                        y = sim_data)
        self.ax.plot([min_value, max_value], [min_value, max_value], '-k')

        self.ax.set_title(f'Niveles minimos mensuales - comparación - r2={r2_rv}')
        self.ax.set_xlabel('Datos observados')
        self.ax.set_ylabel('Datos simulados')
        self.ax.set_xlim(min_value, max_value)
        self.ax.set_ylim(min_value, max_value)
        self.ax.set_aspect('equal', 'box')


    def get_monthly_minimum_serie(self, type_serie):

        if type_serie == 'min_monthly_yearly':
            obs_data = self.monthly_yearly_dataframe.obs
            sim_data = self.monthly_yearly_dataframe.sim
        elif type_serie == 'min_monthly':
            obs_data = self.monthly_dataframe.obs
            sim_data = self.monthly_dataframe.sim
        elif type_serie == 'min_yearly':
            obs_data = self.yearly_dataframe.obs
            sim_data = self.yearly_dataframe.sim

        self.ax.plot(obs_data, '-', label='Datos observados')
        self.ax.plot(sim_data, '-', label='Datos simulados')
        self.ax.legend()
        self.ax.set_xlabel('Fecha')
        self.ax.set_ylabel('Niveles del río - cm')
        self.ax.set_title('Niveles minimos mensuales')

    # Hidden methods
    @staticmethod
    def __join_time_serie__(obs, sim):
        tmp = obs.copy()
        tmp['obs'] = obs.data
        tmp['sim'] = sim.data
        tmp.drop('data', axis=1, inplace=True)
        return tmp

    # Attributes get and set
    @property
    def obs(self):
        return self._obs
    @obs.setter
    def obs(self, input_value):
        input_value = self.__time_serie_review__(input_value)
        self._obs = input_value.copy()

    @property
    def sim(self):
        return self._sim
    @sim.setter
    def sim(self, input_value):
        input_value = self.__time_serie_review__(input_value)
        self._sim = input_value.copy()

    @staticmethod
    def __time_serie_review__(input_value):
        if len(input_value.columns) > 1:
            raise AttributeError(f'Time series columns should be one.')
        if input_value.columns[0] != 'data':
            raise Exception('Column name should be "data"')
        if input_value.index.name != 'date':
            raise Exception('Index name should be "date"')

        return input_value