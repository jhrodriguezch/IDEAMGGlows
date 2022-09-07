import pandas as pd
import geopandas as gpd
import requests
import io
from datetime import datetime
from urllib.request import urlopen
import json
import geoglows as ggs

'''
/////////////////////////////////////////////////////////////////////////

                                auxFun.py

/////////////////////////////////////////////////////////////////////////

Date :      Agust 24, 2022

Modified:   Agust 26, 2022

Needs:      pandas

Usage:      from auxFun import *
'''
def changeGGLOWSColNames(df):
    df.rename_axis('date', axis=0, inplace=True)
    df.index = df.index.tz_localize(None)
    if len(df.columns) == 1:
        df.rename(columns={df.columns[0]: 'data'}, inplace=True)
    return df


def extractForecastEnsembles(comid, dateInit):
    return changeGGLOWSColNames(ggs.streamflow.forecast_ensembles(comid, forecast_date=dateInit))


def extractForecastRecords(comid):
    return changeGGLOWSColNames(ggs.streamflow.forecast_records(comid))


def extractHistoricSimulation(comid):
    return changeGGLOWSColNames(ggs.streamflow.historic_simulation(comid))


def extractDailyAverages(comid):
    return changeGGLOWSColNames(ggs.streamflow.daily_averages(comid))


def extractMonthlyAverages(comid):
    return changeGGLOWSColNames(ggs.streamflow.monthly_averages(comid))


def readCatchmentFile(fileDir):
    return gpd.GeoDataFrame.from_file(fileDir)


def jfews2df(url_dir):
    response = urlopen(url_dir)
    response = json.loads(response.read())

    data    = pd.DataFrame(response['obs']['data'],
                            columns=['date', 'data'])
    data.index = pd.to_datetime(data['date'], format='%Y/%m/%d %H:%M')
    data.drop(['date'], axis=1, inplace=True)

    dataSen = pd.DataFrame(response['sen']['data'],
                            columns=['date', 'data'])
    dataSen.index = pd.to_datetime(dataSen['date'], format='%Y/%m/%d %H:%M')
    dataSen.drop(['date'], axis=1, inplace=True)

    dataP    = pd.DataFrame(response['prec']['data'],
                            columns=['date', 'data'])
    dataP.index = pd.to_datetime(dataP['date'], format='%Y/%m/%d %H:%M')
    dataP.drop(['date'], axis=1, inplace=True)
    return data, dataSen, dataP


def hydroShare2df(urlDir, dateColName='Datetime', formatDate='%Y-%m-%d'):
    response = requests.get(urlDir, verify=True).content
    rv = pd.read_csv(io.StringIO(response.decode('utf-8')),
                     parse_dates=[dateColName],
                     date_parser=lambda x: datetime.strptime(x, formatDate),
                     index_col=0)\
                    .rename_axis('date')
    rv.rename(columns={rv.columns[0]: 'data'}, inplace=True)
    return rv


def readTransversalSectionDb(dirFile, dateColName='FECHA', formatDate="%d/%m/%Y"):
    return pd.read_csv(dirFile,
                       sep=';',
                       parse_dates=[dateColName],
                       date_parser=lambda x: datetime.strptime(x, formatDate))


def substrackCrossSectionDb(fullDb, idSearch):
    return fullDb[fullDb['CODIGO'] == idSearch].copy()\
                                               .reset_index(drop=True)


def readXMLCurvasGasto(dirFile, strToSplitDf="CÓDIGO",
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

def getBiasCorrectValue(values, sim, obs):
    return changeGGLOWSColNames(ggs.bias.correct_forecast(values, sim, obs))