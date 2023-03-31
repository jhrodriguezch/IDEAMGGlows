import os, sys
import warnings
import pandas as pd

class Extract_flow_rating_curve:
    def __init__(self, dict_var) -> None:
        # Assig values
        self.dict_var = dict_var
        self.curvasGastoFiles = {}
        [self.curvasGastoFiles.update({ii.split('_')[0]: os.path.join(self.dict_var['FOLDER FLOW RATING CURVE'], ii)}) for ii in os.listdir(self.dict_var['FOLDER FLOW RATING CURVE'])]


    def __call__(self, stationID):

        if str(stationID) in list(self.curvasGastoFiles.keys()):        
            filePath = self.curvasGastoFiles[stationID]
            print(self.curvasGastoFiles[stationID])
            return self.readXMLCurvasGasto(filePath)
        else:
            warnings.warn("Flow rating curve does not found.")
            return 99
        

    def readXMLCurvasGasto(self,
                           dirFile, 
                           strToSplitDf="CÓDIGO",
                           headerLenght=10, 
                           dateColumns=['F. INICIAL','F. FINAL'],
                           formatDate="%d/%m/%Y"):

        # read dataframe
        df = pd.read_excel(dirFile,
                           skiprows=range(headerLenght), 
                           header=None)

        # Fix dataframe
        df.dropna(axis=1, how='all', inplace=True)
        df.dropna(axis=0, how='all', inplace=True)
        df.reset_index(drop=True, inplace=True)
        
        # row where the data will be splited
        splitRows = list(df[df[1] == strToSplitDf].index)

        # build result dataframe
        df_res = pd.DataFrame()
        for row, ii in enumerate(splitRows[:-1]):
            
            # extract principal identification parameters
            names_gnrl = list(df.loc[ii].dropna())
            data_gnrl  = list(df.loc[ii + 1].dropna())
            names_esp  = list(df.loc[ii + 2].dropna())
            
            # extract data of the dataframe
            data_col   = df.loc[ii + 3: splitRows[row + 1] - 1].copy()
            data_col.reset_index(inplace=True, drop=True)
            data_col.dropna(axis=1,  how='all', inplace=True)
            
            # merge in the temporal dataframe
            df_tmp = pd.DataFrame()
            for namesCol, dataCol in list(zip(names_gnrl, data_gnrl)):
                df_tmp[namesCol] = [dataCol] * len(data_col)

            for num, nameCol in enumerate(names_esp):
                df_tmp[nameCol] = data_col.iloc[:, num]

            # add to result dataframe
            df_res = pd.concat([df_res, df_tmp], ignore_index=True)

            del df_tmp

        # build date columns
        for dateCol in dateColumns:
            df_res[dateCol] = pd.to_datetime(df_res[dateCol], format=formatDate)

        return df_res