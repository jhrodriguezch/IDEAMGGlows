
import os
import numpy as np
import pandas as pd

class Exteact_river_profile:
    def __init__(self, dict_var):
        # Assig values
        self.dict_var = dict_var
        self.db_profile_file = self.dict_var['PROFILE DATABASE']

        # Load Database
        try:
            self.db = pd.read_json(self.db_profile_file, orient='table')
        except Exception as e:
            print(e)
            raise ImportError(f'Importing: {self.db_profile_file}')

        # Lod database columns
        self.disp_columns = self.db.columns.values
        self.columns_to_extract = self.disp_columns

    def __call__(self, **kwards):
        # Define data to search
        self.name_col_srch = list(kwards.keys())[0]
        self.value_to_srch = kwards[self.name_col_srch]

        tmp_columns = np.unique([*[self.name_col_srch], *self.columns_to_extract]).tolist()
        rv = self.db.loc[self.db[self.name_col_srch] == self.value_to_srch, tmp_columns].copy()
        rv.reset_index(inplace = True, drop=True)
        self.result = rv
        return rv

    # Properties methods
    @property
    def db_profile_file(self):
        return self._db_profile_file
    @db_profile_file.setter
    def db_profile_file(self, input_val):
        if not os.path.exists(input_val):
            raise NameError(f'\n{input_val}\nFile does not exsist.')
        self._db_profile_file = input_val


    @property
    def name_col_srch(self):
        return self._name_col_srch
    @name_col_srch.setter
    def name_col_srch(self, input_value):
        if not input_value in self.disp_columns:
            error_tmp=f'Colums identified. \n {self.disp_columns} \nNot found column "{input_value}" in columns.'
            raise Exception(error_tmp)
        self._name_col_srch = input_value


    @property
    def value_to_srch(self):
        return self._value_to_srch
    @value_to_srch.setter
    def value_to_srch(self, input_value):
        self._value_to_srch = input_value


    @property
    def columns_to_extract(self):
        return self._columns_to_extract
    @columns_to_extract.setter
    def columns_to_extract(self, input_value):
        if not set(input_value).issubset(self.disp_columns):
            raise Exception('Not found in columns to extract.')
        self._columns_to_extract = input_value