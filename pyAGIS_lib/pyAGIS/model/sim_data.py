import os, sys, json
import pandas as pd
import geoglows as ggs
from datetime import timedelta, datetime


class Historical_simulated_fixed_data:
    def __init__(self, dict_var):
        self.dict_var = dict_var

    def __call__(self, comid, serie_hist_observada):
        self.comid = comid
        self.serie_hist_observada = serie_hist_observada
        self.serie_historica_simulada = self.comid

        return self.get_historical_simulated_fixed_data()

    # Properties
    @property
    def comid(self):
        return self._comid
    @comid.setter
    def comid(self, value : str):
        self._comid = str(value)
    
    @property
    def serie_hist_observada(self):
        return self._serie_hist_observada
    @serie_hist_observada.setter
    def serie_hist_observada(self, dataframe : pd.DataFrame()):
        if len(dataframe.columns) != 1:
            ErrorEsp = 'El data frame debe tener una columna.'
            self.__error__('la serie historica observada', ErrorEsp)
        
        if dataframe.columns != ['data']:
            ErrorEsp = 'El nombre de la columna debe ser "data".'
            self.__error__('la serie historica observada', ErrorEsp)

        if dataframe.index.name != 'date':
            ErrorEsp = 'El nombre del indice debe ser "date".'
            self.__error__('la serie historica observada', ErrorEsp)
        self._serie_hist_observada = dataframe

    @property
    def serie_historica_simulada(self):
        return self._serie_historica_simulada
    @serie_historica_simulada.setter
    def serie_historica_simulada(self, comid):
        try:
            rv = ggs.streamflow.historic_simulation(comid)
            rv = self.__fix_utc__(rv)
            rv = self.__changeGGLOWSColNames__(rv)
        except Exception as e:
            self.__error__('la descarga de la serie simulada.',
                           ErrorEsp=e)
        self._serie_historica_simulada = rv       


    # Main functions
    def get_historical_simulated_fixed_data(self):
        try:
            return self._get_historical_simulated_fixed_data
        except:
            rv = ggs.bias.correct_historical(simulated_data = self.serie_historica_simulada,
                                             observed_data = self.serie_hist_observada)
            rv = self.__changeGGLOWSColNames__(rv)
            self._get_historical_simulated_fixed_data = rv
            return rv

    # Hidden methods
    @staticmethod
    def __error__(loc, ErrorEsp):
        raise Exception(f'\n \nError en {loc}.\n{ErrorEsp}\n ')
    
    @staticmethod
    def __changeGGLOWSColNames__(df):
        df.rename_axis('date', axis=0, inplace=True)
        df.index = df.index.tz_localize(None)
        if len(df.columns) == 1:
            df.rename(columns={df.columns[0]: 'data'}, inplace=True)
        return df

    def __fix_utc__(self, df):
        utc = self.dict_var['UTC']
        df.index = df.index + timedelta(hours=utc)

        df['year']  = df.index.year
        df['month'] = df.index.month
        df['day']   = df.index.day
        
        df = df.groupby([df.year, df.month, df.day]).mean()
        df.reset_index(inplace=True, drop=False)
        
        df.index = pd.to_datetime(df[['year', 'month', 'day']])
        df.drop(['year', 'month', 'day'], axis=1, inplace=True)
        df.drop(df.index[0], axis=0, inplace=True)

        return df


class Forecast_data:
    def __init__(self, dict_var):

        self.file_list = [ii for ii in os.listdir(dict_var['FOLDER FORECAST DATABASE']) if '.json' in ii]
        
        sumarice_data = pd.DataFrame()
        sumarice_data['date'] = [datetime.strptime(ii.split('.')[0], '%Y%m%d') for ii in self.file_list]
        sumarice_data['file'] = [os.path.join(dict_var['FOLDER FORECAST DATABASE'], ii) for ii in self.file_list]
        sumarice_data['disp stations'] = sumarice_data['file'].map(lambda x : json.load(open(x))['stations'])

        self.sumarice_data = sumarice_data
        del sumarice_data


    def search_in_cache_database(self, station):
        # Filter to existence data
        self.disp_data = self.sumarice_data[['date', 'file']].copy()
        self.disp_data['disp stations'] = self.sumarice_data['disp stations'].map(lambda x : station if station in x else None)
        
        # Load simulated data
        list_data = []
        for _, row in self.disp_data.iterrows():
            if row['disp stations'] is None:
                list_data.append(None)
                continue
            list_data.append(json.load(open(row['file']))['cont'][row['disp stations']])
            
        self.disp_data['data'] = list_data

        # Remove cols
        self.disp_data.drop(['file', 'disp stations'], axis=1, inplace=True)
        return self.disp_data