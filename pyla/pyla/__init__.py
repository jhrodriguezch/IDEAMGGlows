__version__ = '0.0.1'

from . import const

from .model.hist_data import Historical_data, Fews_data
from .model.sim_data import Historical_simulated_fixed_data
from .model.geojson_data import Extract_data_from_json
from .model.timeseries_analysis import Return_periode_and_serie_analysis

import time
import numpy as np


# Extra functions
# ---------------
def decorator_demora(fun):
    def f (*kwards, **args):
        delay = []
        n_times = 100
        for _ in range(n_times):
            before = time.time()
            rv = fun(*kwards, **args)
            delay.append(time.time() - before)

        print('Tiempo promedio de demora:')
        print('Nombre de la función : {}'.format(fun.__name__))
        print(f'{np.nanmean(delay)} s.')
        print(f'Número de intentos: {n_times}')
        print('')

        return rv
    return f


# Functions to download data
# --------------------------
def get_historical_data(*kwards, **args):
    __time_test__ = '''
    Tiempo promedio de demora:
    9.567645192146301 s.
    Número de intentos: 10
    '''
    foo = Historical_data(const.CONST)
    rv = foo(*kwards, **args)
    return rv, foo


def get_historical_sim_data(*kwards, **args):
    __time_test__ = '''
    Tiempo promedio de demora:
    8.141277694702149 s.
    Número de intentos: 10
    Fecha: 13/12/2022
    '''
    foo = Historical_simulated_fixed_data(const.CONST)
    rv = foo(*kwards, **args)
    return rv, foo


def get_comit_from_station(*kwards, **args):
    __time_test__ = '''
    Tiempo promedio de demora:
    0.5479104804992676 s.
    Número de intentos: 100
    '''
    foo = Extract_data_from_json(path_dir=const.CONST['GEOJSON FILE'])
    foo.set_column_to_extract(columns=const.CONST['GEOJSON COLUMNS TO EXTRACT'])
    rv = foo(*kwards, **args)
    rv = str(rv[const.CONST['GEOJSON COLUMNS TO EXTRACT']].values[0][0])
    return rv, foo


def get_alerta_minima_fews(*kwards, **args):
    __time_test__ = '''
    Tiempo promedio de demora:
    0.08685457944869995 s.
    Número de intentos: 100
    '''
    foo = Fews_data(const.CONST)
    rv = foo.get_station_information(*kwards, **args)
    try:
        rv = rv['ubajos'][0]
    except:
        rv = float('nan')
    return rv , foo


# Funtions to analysis
# --------------------
def get_data_from_return_period(*kwards, **args):
    __time_test__ = '''
    Tiempo promedio de demora:
    0.0017555880546569825 s.
    Número de intentos: 100
    '''
    rp = args['rp']
    time_serie = args['time_serie']

    foo = Return_periode_and_serie_analysis()
    foo.set_time_serie(time_serie=time_serie)
    rv = foo.get_data_from_return_period(rp=rp)
    return rv, foo


def get_return_period_from_data(*kwards, **args):
    __time_test__ = '''
    Tiempo promedio de demora:
    Nombre de la función : get_return_period_from_data
    0.00174560546875 s.
    Número de intentos: 100
    '''
    data       = args['data']
    time_serie = args['time_serie']

    foo = Return_periode_and_serie_analysis()
    foo.set_time_serie(time_serie=time_serie)
    rv = foo.get_return_period_from_data(data=data)
    return rv, foo

