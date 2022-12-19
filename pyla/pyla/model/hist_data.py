import io
import urllib
import requests
import pandas as pd
from datetime import datetime


class Historical_data:
    def __init__(self, dict_var):
        self.dict_var = dict_var


    def __call__(self, station_code: str):
        self.station_code = station_code
        self.ulr_dir = self.station_code
        return self.get_historical_data()


    # Properties
    @property
    def station_code(self):
        return self._station_code

    @station_code.setter
    def station_code(self, station_code):
        self._station_code = str(station_code)
    

    @property
    def ulr_dir(self):
        return self._ulr_dir

    @ulr_dir.setter
    def ulr_dir(self, station_code):
        url = self.dict_var['HYDROSHARE URL'] + station_code + '.csv'
        req_data = requests.get(url, verify=True)
        if int(req_data.status_code) >= 400:
            raise Exception('Station code does not exist.')
        self.req_data = req_data
        self._url = url


    # Methods
    def get_historical_data(self):
        try:
            return self._get_historical_data
        except:
            dateColName = self.dict_var['HYDROSHARE DATE COLUMN NAME']
            formatDate  = self.dict_var['HYDROSHARE FORMAT DATE']

            response = self.req_data.content
            rv = pd.read_csv(io.StringIO(response.decode('utf-8')),
                         parse_dates=[dateColName],
                         date_parser=lambda x: datetime.strptime(x, formatDate),
                         index_col=0)\
                        .rename_axis('date')
            rv.rename(columns={rv.columns[0]: 'data'}, inplace=True)

            self._get_historical_data = rv
            return rv


class Fews_data:
    def __init__(self, dict_var):
        self.dict_var = dict_var
        self.informacion_de_estaciones = self.dict_var['FEWS URL ESTACIONES']
        self.column_name_id = self.dict_var['FEWS COLUMN NAME ESTACIONES']

    # Properties
    @property
    def column_name_id(self):
        return self._column_name_id
    @column_name_id.setter
    def column_name_id(self, id_code):
        if not id_code in self.informacion_de_estaciones.columns:
            raise Exception(f'\n"FEWS COLUMN NAME ESTACIONES" no existe.\nBuscado : {id_code}\nDisponibles : {self.informacion_de_estaciones.columns}\n')
        self._column_name_id = id_code
        self.informacion_de_estaciones[id_code] = self.informacion_de_estaciones[id_code].astype(str)

    @property
    def informacion_de_estaciones(self):
        return self._informacion_de_estaciones
    @informacion_de_estaciones.setter
    def informacion_de_estaciones(self, url):
        req = urllib.request.urlopen(url)
        if req.status >= 400:
            raise Exception('El servidor de FEWS presento error.')
        df_fews = req.read()
        df_fews = pd.read_csv(io.StringIO(df_fews.decode('latin-1')))
        self._informacion_de_estaciones = df_fews
    

    # Get methods
    def get_station_information(self, station_code):
        try:
            return self._get_station_information
        except:
            tmp_df = self.informacion_de_estaciones[self.informacion_de_estaciones[self.column_name_id] == station_code].copy()
            tmp_df.reset_index(drop=True, inplace=True)
            rv = tmp_df.to_dict(orient='list')
            self._get_station_information = rv
            return self._get_station_information