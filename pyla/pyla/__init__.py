__version__ = '0.0.1'

from . import const

from .model.hist_data import Historical_data, Fews_data
from .model.sim_data import Historical_simulated_fixed_data
from .model.geojson_data import Extract_data_from_json
from .model.timeseries_analysis import Return_periode_and_serie_analysis
from .model.profile_data import Exteact_river_profile

from .view.serie_plot import Monthly_minimum_plot

import time
import numpy as np


# Decorators functions
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

def decorator_print_demora(fun):
    def f(*args, **kwards):
        before = time.time()
        rv = fun(*args, **kwards)
        print(f'Function: {fun.__name__}(), Delay: {time.time()-before} seg.')
        return rv
    return f

# Functions to download data
# --------------------------
@decorator_print_demora
def get_historical_data(*args, **kwards):
    __time_test__ = '''
    Tiempo promedio de demora:
    9.567645192146301 s.
    Número de intentos: 10
    '''
    foo = Historical_data(const.CONST)
    rv = foo(*args, **kwards)
    return rv, foo


@decorator_print_demora
def get_historical_sim_data(*args, **kwards):
    __time_test__ = '''
    Tiempo promedio de demora:
    8.141277694702149 s.
    Número de intentos: 10
    Fecha: 13/12/2022
    '''
    foo = Historical_simulated_fixed_data(const.CONST)
    rv = foo(*args, **kwards)
    return rv, foo


@decorator_print_demora
def get_comit_from_station(*args, **kwards):
    __time_test__ = '''
    Tiempo promedio de demora:
    0.5479104804992676 s.
    Número de intentos: 100
    '''
    foo = Extract_data_from_json(path_dir=const.CONST['GEOJSON FILE'])
    foo.set_column_to_extract(columns=const.CONST['GEOJSON COLUMNS TO EXTRACT'])
    rv = foo(*args, **kwards)
    rv = str(rv[const.CONST['GEOJSON COLUMNS TO EXTRACT']].values[0][0])
    return rv, foo


@decorator_print_demora
def get_alerta_minima_fews(*args, **kwards):
    __time_test__ = '''
    Tiempo promedio de demora:
    0.08685457944869995 s.
    Número de intentos: 100
    '''
    foo = Fews_data(const.CONST)
    rv = foo.get_station_information(*args, **kwards)
    try:
        rv = rv['ubajos'][0]
    except:
        rv = float('nan')
    return rv , foo


@decorator_print_demora
def get_perfil_del_rio(*args, **kwards):
    __time_test__ = '''
    Tiempo promedio de demora:
    Nombre de la función : get_perfil_del_rio
    0.025811243057250976 s.
    Número de intentos: 100
    '''
    foo = Exteact_river_profile(const.CONST)
    rv = foo(*args, **kwards)
    return rv, foo


# Funtions to analysis
# --------------------
@decorator_print_demora
def get_data_from_return_period(*args, **kwards):
    __time_test__ = '''
    Tiempo promedio de demora:
    0.0017555880546569825 s.
    Número de intentos: 100
    '''
    rp = kwards['rp']
    time_serie = kwards['time_serie']

    foo = Return_periode_and_serie_analysis()
    foo.set_time_serie(time_serie=time_serie)
    rv = foo.get_data_from_return_period(rp=rp)
    return rv, foo


@decorator_print_demora
def get_return_period_from_data(*args, **kwards):
    __time_test__ = '''
    Tiempo promedio de demora:
    Nombre de la función : get_return_period_from_data
    0.00174560546875 s.
    Número de intentos: 100
    '''
    data       = kwards['data']
    time_serie = kwards['time_serie']

    foo = Return_periode_and_serie_analysis()
    foo.set_time_serie(time_serie=time_serie)
    rv = foo.get_return_period_from_data(data=data)
    return rv, foo

# Functions to plot
#------------------
def scatter_monthly_yearly_comparation(*args, **kwards):
    foo = Monthly_minimum_plot(*args, **kwards)
    foo()
    foo.get_monthly_minimum_scatter('min_monthly_yearly')
    return foo

def serie_monthly_yearly_comparation(*args, **kwards):
    foo = Monthly_minimum_plot(*args, **kwards)
    foo()
    foo.get_monthly_minimum_serie('min_monthly_yearly')
    return foo

def scatter_monthly_comparation(*args, **kwards):
    foo = Monthly_minimum_plot(*args, **kwards)
    foo()
    foo.get_monthly_minimum_scatter('min_monthly')
    return foo

def serie_monthly_comparation(*args, **kwards):
    foo = Monthly_minimum_plot(*args, **kwards)
    foo()
    foo.get_monthly_minimum_serie('min_monthly')
    return foo

def scatter_yearly_comparation(*args, **kwards):
    foo = Monthly_minimum_plot(*args, **kwards)
    foo()
    foo.get_monthly_minimum_scatter('min_yearly')
    return foo

def serie_yearly_comparation(*args, **kwards):
    foo = Monthly_minimum_plot(*args, **kwards)
    foo()
    foo.get_monthly_minimum_serie('min_yearly')
    return foo