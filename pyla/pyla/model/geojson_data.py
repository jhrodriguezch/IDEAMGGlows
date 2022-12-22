import json
import numpy as np
import pandas as pd


class Extract_data_from_json:
    def __init__(self, path_dir):
        self.set_json_path(path=path_dir)
        self.set_json_file()
        self.set_disp_columns()
        
    def __call__(self, *args, **kwards):
        """
        Get modeler area
        Input
            column to search and data to search
            example:
                col_name : str = value_to_search : int/str/float
        """
        # Define data to search
        self.set_name_col_srch(val = list(kwards.keys())[0])
        self.set_value_to_srch(val = kwards[self.name_col_srch])
        
        # Return
        # rv = self.json_file.loc[self.json_file[self.name_col_srch] == self.value_to_srch, [self.name_col_srch] +self.columns_to_extract].copy()
        tmp_columns = np.unique([*[self.name_col_srch], *self.columns_to_extract]).tolist()
        rv = self.json_file.loc[self.json_file[self.name_col_srch] == self.value_to_srch, tmp_columns].copy()
        rv.reset_index(inplace = True, drop=True)
        self.result = rv
        return rv

    
    def set_json_path(self, path):
        self.json_path = path
    def set_json_file(self):
        self.json_file = self.__gjson_load__(path_file = self.json_path)
    def set_disp_columns(self):
        self.disp_columns = self.json_file.columns
    def set_column_to_extract(self, columns):
        self.columns_to_extract = columns
        if not set(self.columns_to_extract).issubset(self.disp_columns):
            raise Exception('Not found in columns to extract.')
            
    def set_name_col_srch(self, val):
        self.name_col_srch = val
        if not self.name_col_srch in self.disp_columns:
            error_tmp=f'Colums identified. \n {self.disp_columns} \nNot found column "{self.name_col_srch}" in columns.'
            raise Exception(error_tmp)
    def set_value_to_srch(self, val):
        self.value_to_srch = val
    
    def get_json_file(self):
        try:
            return self.json_file
        except Exception as e:
            print(e)
            return None
    def get_result(self):
        try:
            return self.result
        except Exception as e:
            print(e)
            return None
    
    
    @staticmethod
    def __gjson_load__(path_file):
        data = json.load(open(path_file))['features']
        df = pd.DataFrame()

        for line in data:
            line_data = line['properties']
            col_names = list(line_data.keys())
            col_data =[line_data[ii] for ii in col_names]
            tmp = pd.DataFrame(data = [col_data],
                               columns=col_names)
            df = pd.concat([df, tmp], ignore_index=True)

        for column in df.columns:
            df[column] = df[column].astype(str)
        return df