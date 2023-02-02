import numpy as np
import pandas as pd
from scipy import stats
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import matplotlib.pyplot as plt

class Return_periode_and_serie_analysis:
    def __init__(self, probability = '__exceedance__'):
        '''
        Calc data from the FDC (Flow duration curve)
        probability : str (__exceedance__ || __occurrence__) -> Type of calc of probability.
        '''
        self.rp_dict = {'obs'       : {},
                        'norm'    : {'fun' : stats.norm,
                                     'para' : {'loc'  : lambda x : np.nanmean(x),
                                               'scale': lambda x : np.nanstd(x)}},
                        'lognorm' : {'fun' : stats.pearson3,
                                     'para' : {'loc'  : lambda x : np.nanmean(x),
                                               'scale': lambda x : np.nanstd(x),
                                               'skew' : lambda x : 1}},
                        'dweibull'   : {'fun' : stats.dweibull,
                                        'para' : {'loc'  : lambda x : np.nanmean(x),
                                                  'scale': lambda x : np.nanstd(x),
                                                  'c'    : lambda x : 1}},
                        'chi2'      : {'fun' : stats.chi2,
                                       'para' : {'loc'  : lambda x : np.nanmean(x),
                                                 'scale': lambda x : np.nanstd(x),
                                                 'df'   : lambda x : 2}},
                        'gumbel_r'    : {'fun' : stats.gumbel_r,
                                         'para' : {'loc'  : lambda x : np.nanmean(x) - 0.45005 * np.nanstd(x),
                                                   'scale': lambda x : 0.7797 * np.nanstd(x)}}}

        if probability == '__exceedance__':
            self.calc_rp = lambda p   : (1 - p) ** -1
            self.calc_p  = lambda rp  : 1 - rp ** -1
        elif probability == '__occurrence__':
            self.calc_rp = lambda p  : p ** -1
            self.calc_p  = lambda rp : rp ** -1
        else:
            assert ValueError('"probability" input variable should be __exceedance__ or __occurrence__')


    # Set methods
    def set_time_serie(self, time_serie: list):
        self.time_serie = time_serie


    # Get methods
    def get_data_from_return_period(self, rp: float):
        ''' 
        rp : float -> Return peride
        time_serie : list -> Time serie
        [] + rp -> data 
        '''
        self.input_data = rp

        # Main values
        # p = 1 - (np.array(self.input_data).astype(float) ** -1)
        p    = self.calc_p(np.array(self.input_data).astype(float))
        # mean = np.nanmean(self.time_serie)
        # std  = np.nanstd(self.time_serie)

        # obs calc
        data_hist, bind_edges = np.histogram(a=self.time_serie, bins='auto', density=True)
        bind_edges_mean = (bind_edges[:-1] + bind_edges[1:]) / 2.0

        self.rp_dict['obs'].update({'data' : data_hist})
        self.rp_dict['obs'].update({'bind' : bind_edges_mean})

        for distri in self.rp_dict.keys():
            if 'obs' == distri:
                continue

            # Extract pdf
            self.rp_dict[distri].update({'pdf' : self.__extracpdf__(distri=distri, bind=bind_edges_mean)})
            self.rp_dict[distri].update({'metrics': self.__calcmetricts__(distri=distri)})

        self.__best_pdf__()

        rv = self.__bestdistri_return_data__(p)
        return rv


    def get_return_period_from_data(self, data : float):
        ''' 
        data : float -> data to search
        time_serie : list -> Time serie
        [] + data -> rp 
        '''
        self.input_data = data

        # Main values
        # mean = np.nanmean(self.time_serie)
        # std = np.nanstd(self.time_serie)

        # obs calc
        data_hist, bind_edges = np.histogram(a=self.time_serie, bins='auto', density=True)
        bind_edges_mean = (bind_edges[:-1] + bind_edges[1:]) / 2.0

        self.rp_dict['obs'].update({'data' : data_hist})
        self.rp_dict['obs'].update({'bind' : bind_edges_mean})

        for distri in self.rp_dict.keys():
            if 'obs' == distri:
                continue

            # Extract pdf
            self.rp_dict[distri].update({'pdf' : self.__extracpdf__(distri=distri, bind=bind_edges_mean)})
            self.rp_dict[distri].update({'metrics': self.__calcmetricts__(distri=distri)})

        self.__best_pdf__()

        p = self.__bestdistri_return_p__(self.input_data)
        # rv = (1 - p) ** -1
        rv = self.calc_rp(p)
        return rv


    # Properties
    @property
    def input_data(self):
        return self._input_data
    @input_data.setter
    def input_data(self, value):
        if value < 0:
            raise Exception(f'El dato de entrada debe ser positivo.')
        try:
            value = float(value)
        except:
            raise Exception(f'El dato de entrada debe ser float.')
        self._input_data = value

    @property
    def time_serie (self):
        return self._time_serie
    @time_serie.setter
    def time_serie (self, input):
        self._time_serie = np.array(input).astype(float)
        self._time_serie = self._time_serie[~np.isnan(self._time_serie)]


    # Hidden methods
    def __calcmetricts__(self, distri):
        '''
        TODO : Implement p value with xi square test
        '''
        # Calc CFD
        sim = self.rp_dict[distri]['pdf'].cumsum() / self.rp_dict[distri]['pdf'].sum()
        obs = self.rp_dict['obs']['data'].cumsum() / self.rp_dict['obs']['data'].sum()
        
        df = pd.DataFrame()
        df['sim'] = sim
        df['obs'] = obs

        df.dropna(inplace=True, how='all')

        if df.shape[0] != 0:
            sim = df['sim'].values
            obs = df['obs'].values
        else:
            print('Error in clasification!')
            rv = {'MSE' : 999999,
                  'k-s dist': 999999}

            return rv

        # print(sim)
        # print(obs)
        # print(df)
        # print('')

        '''
        plt.scatter(x = self.rp_dict['obs']['bind'],
                    y = self.rp_dict[distri]['pdf'].cumsum()/self.rp_dict[distri]['pdf'].sum())
        plt.plot(self.rp_dict['obs']['bind'],
                 self.rp_dict['obs']['data'].cumsum()/self.rp_dict['obs']['data'].sum(),
                 '--')
        plt.title(distri)
        plt.show()
        '''

        mse    = mean_squared_error(y_true=obs,y_pred=sim)
        ksdist = np.nanmax(abs(np.array(obs) - np.array(sim)))

        rv = {'MSE' : mse,
              'k-s dist': ksdist}

        return rv


    def __extracpdf__(self, distri, bind):

        # self.rp_dict[distri]['para']['loc'] = mean
        # self.rp_dict[distri]['para']['scale'] = std

        para_dict  = {}
        for para_name in self.rp_dict[distri]['para'].keys():
            para_dict.update({ para_name : self.rp_dict[distri]['para'][para_name](self.time_serie)})

        return self.rp_dict[distri]['fun'].pdf(x=bind, **para_dict)    


    def __best_pdf__(self):
        # Select metric name to search
        __paracomp__ = 'k-s dist'

        best_distri = [[distri, self.rp_dict[distri]['metrics'][__paracomp__]] for distri in self.rp_dict.keys() if distri != 'obs']
        best_distri = np.reshape(best_distri, (len(best_distri), 2)).T
        
        # print(best_distri)
        
        best_distri = best_distri[:, best_distri[1].astype(float) == np.nanmin(best_distri[1].astype(float))][0][0]
        
        self.rp_dict['obs'].update({'best_distri' : best_distri})


    def __bestdistri_return_data__(self, p):
        '''Calc data from probability'''
        best_distri_name =  self.rp_dict['obs']['best_distri']
        
        para_dict  = {}
        for para_name in self.rp_dict[best_distri_name]['para'].keys():
            para_dict.update({ para_name : self.rp_dict[best_distri_name]['para'][para_name](self.time_serie)})
        
        rv = self.rp_dict[best_distri_name]['fun'].ppf(q=p, **para_dict)
        return rv


    def __bestdistri_return_p__(self, x):
        '''Calc probability from data'''
        best_distri_name =  self.rp_dict['obs']['best_distri']

        para_dict  = {}
        for para_name in self.rp_dict[best_distri_name]['para'].keys():
            para_dict.update({ para_name : self.rp_dict[best_distri_name]['para'][para_name](self.time_serie)})

        rv = self.rp_dict[best_distri_name]['fun'].cdf(x=x, **para_dict)
        return rv


    def __changeforwaterlevel__(self):
        tmp_rp  = self.input_data.copy()
        tmp_max = tmp_rp.data.max()
        tmp_rp['data'] = -1 * (tmp_rp['data'] - tmp_max)
        return tmp_rp, tmp_max


class Main_values_from_serie:
    def __init__(self, data):
        self.time_serie = data.copy()
        self.time_serie['__year__'] = self.time_serie.index.year
        self.time_serie['__month__'] = self.time_serie.index.month


    # Main functions
    def low_flows(self):
        '''
        Mean values for monthly low flows.
        https://doi.org/10.1111/j.1752-1688.2007.00099.x
        '''
        rv = self.time_serie.groupby(['__year__', '__month__']).min().groupby(['__month__']).mean()
        rv.index.name = 'month'
        self.time_serie.drop(['__year__', '__month__'], axis=1, inplace=True)
        return rv


    def extreme_low_flows(self):
        '''
        10th percentile of monthly low flows.
        https://doi.org/10.1111/j.1752-1688.2007.00099.x
        '''
        rv = self.time_serie.groupby(['__year__', '__month__']).min().dropna()['data'].quantile(0.1)
        self.time_serie.drop(['__year__', '__month__'], axis=1, inplace=True)
        return rv
    

    # Properties
    @property
    def time_serie(self):
        return self._time_serie
    @time_serie.setter
    def time_serie(self, input):
        if type(input) != type(pd.DataFrame()):
            raise AttributeError(f'Time series should be pandas.DataFrame().')
        if len(input.columns) > 1:
            raise AttributeError(f'Time series columns should be one.')
        if input.columns[0] != 'data':
            raise Exception('Column name should be "data"')
        if input.index.name != 'date':
            raise Exception('Index name should be "date"')
        # TODO: input.index review format
        self._time_serie = input


# Auxiliar functions
def R2(time_serie_1, time_serie_2):
    return r2_score(time_serie_1, time_serie_2)


def min_monthly_yearly(time_serie):
    time_serie['year']  = time_serie.index.year
    time_serie['month'] = time_serie.index.month
    time_serie['day']   = 1

    rv = time_serie.groupby([time_serie.index.year, time_serie.index.month]).min()
    rv.reset_index(inplace=True, drop=True)

    rv.index = pd.to_datetime({'year'  : rv['year'],
                                'month' : rv['month'],
                                'day'   : rv['day']})
    rv.index.name = 'date'

    rv.drop(['year', 'month', 'day'], axis=1, inplace=True)

    return rv

def min_monthly(time_serie):
    time_serie['year']  = 2022
    time_serie['month'] = time_serie.index.month
    time_serie['day']   = 1

    rv = time_serie.groupby([time_serie.index.month]).min()
    rv.reset_index(inplace=True, drop=True)

    rv.index = pd.to_datetime({'year'  : rv['year'],
                               'month' : rv['month'],
                               'day'   : rv['day']})
    rv.index.name = 'date'

    rv.drop(['year', 'month', 'day'], axis=1, inplace=True)

    return rv

def min_yearly(time_serie):
    time_serie['year']  = time_serie.index.year
    time_serie['month'] = 1
    time_serie['day']   = 1

    rv = time_serie.groupby([time_serie.index.year]).min()
    rv.reset_index(inplace=True, drop=True)

    rv.index = pd.to_datetime({'year'  : rv['year'],
                               'month' : rv['month'],
                               'day'   : rv['day']})
    rv.index.name = 'date'

    rv.drop(['year', 'month', 'day'], axis=1, inplace=True)

    return rv
