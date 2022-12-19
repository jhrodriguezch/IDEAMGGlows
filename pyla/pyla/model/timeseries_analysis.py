import numpy as np
from scipy import stats
from sklearn.metrics import mean_squared_error

import matplotlib.pyplot as plt

class Return_periode_and_serie_analysis:
    def __init__(self):
        self.rp_dict = {'obs'       : {},
                        'normal'    : {'fun' : stats.norm,
                                       'para' : {'loc'  : None,
                                                 'scale': None}},
                        'lognormal' : {'fun' : stats.pearson3,
                                       'para' : {'loc'  : None,
                                                 'scale': None,
                                                 'skew' : 1}},
                        'weibull'   : {'fun' : stats.dweibull,
                                       'para' : {'loc'  : None,
                                                 'scale': None,
                                                 'c'    : 1}},
                        'chi2'      : {'fun' : stats.chi2,
                                       'para' : {'loc'  : None,
                                                 'scale': None,
                                                 'df'   : 2}},
                        'gumbel'    : {'fun' : stats.gumbel_r,
                                       'para' : {'loc'  : None,
                                                 'scale': None}}}


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
        p = 1 - (np.array(self.input_data).astype(float) ** -1)
        mean = np.nanmean(self.time_serie)
        std = np.nanstd(self.time_serie)

        # obs calc
        data_hist, bind_edges = np.histogram(a=self.time_serie, bins='sturges', density=True)
        self.rp_dict['obs'].update({'data' : data_hist})
        bind_edges_mean = (bind_edges[:-1] + bind_edges[1:]) / 2.0
        self.rp_dict['obs'].update({'bind' : bind_edges_mean})

        for distri in self.rp_dict.keys():
            if 'obs' == distri:
                continue

            # Extract pdf
            self.rp_dict[distri].update({'pdf' : self.__extracpdf__(distri=distri, bind=bind_edges_mean, mean=mean, std=std)})
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
        mean = np.nanmean(self.time_serie)
        std = np.nanstd(self.time_serie)

        # obs calc
        data_hist, bind_edges = np.histogram(a=self.time_serie, bins='sturges', density=True)
        self.rp_dict['obs'].update({'data' : data_hist})
        bind_edges_mean = (bind_edges[:-1] + bind_edges[1:]) / 2.0
        self.rp_dict['obs'].update({'bind' : bind_edges_mean})

        for distri in self.rp_dict.keys():
            if 'obs' == distri:
                continue

            # Extract pdf
            self.rp_dict[distri].update({'pdf' : self.__extracpdf__(distri=distri, bind=bind_edges_mean, mean=mean, std=std)})
            self.rp_dict[distri].update({'metrics': self.__calcmetricts__(distri=distri)})

        self.__best_pdf__()

        p = self.__bestdistri_return_p__(self.input_data )
        rv = (1 - p) ** -1
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
        sim = self.rp_dict[distri]['pdf']
        obs = self.rp_dict['obs']['data']
        
        '''
        plt.scatter(x = self.rp_dict['obs']['bind'],
                    y = self.rp_dict[distri]['pdf'])
        plt.plot(self.rp_dict['obs']['bind'],
                 self.rp_dict['obs']['data'],
                 '--')
        plt.title(distri)
        plt.show()
        '''

        return mean_squared_error(y_true=obs,y_pred=sim)

    def __extracpdf__(self, distri, bind, mean, std):
        self.rp_dict[distri]['para']['loc'] = mean
        self.rp_dict[distri]['para']['scale'] = std
        return self.rp_dict[distri]['fun'].pdf(x=bind, **self.rp_dict[distri]['para'])    

    def __best_pdf__(self):
        best_distri = [[distri, self.rp_dict[distri]['metrics']] for distri in self.rp_dict.keys() if distri != 'obs']
        best_distri = np.reshape(best_distri, (len(best_distri), 2)).T
        best_distri = best_distri[:, best_distri[1].astype(float) == min(best_distri[1].astype(float))][0][0]
        self.rp_dict['obs'].update({'best_distri' : best_distri})

    def __bestdistri_return_data__(self, p):
        best_distri_name =  self.rp_dict['obs']['best_distri']
        rv = self.rp_dict[best_distri_name]['fun'].ppf(q=p, **self.rp_dict[best_distri_name]['para'])
        return rv

    def __bestdistri_return_p__(self, x):
        best_distri_name =  self.rp_dict['obs']['best_distri']
        rv = self.rp_dict[best_distri_name]['fun'].cdf(x=x, **self.rp_dict[best_distri_name]['para'])
        return rv

    def __changeforwaterlevel__(self):
        tmp_rp  = self.input_data.copy()
        tmp_max = tmp_rp.data.max()
        tmp_rp['data'] = -1 * (tmp_rp['data'] - tmp_max)
        return tmp_rp, tmp_max
