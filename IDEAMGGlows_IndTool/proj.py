from cProfile import label
from turtle import color
import model
import matplotlib.pyplot as plt
import pandas as pd
import geoglows as ggs
import os, sys
from datetime import date, datetime
import datetime as dt


def emptyPorcentage(df):
    return 100 * len(df[df['data'].isna()]) / len(df)

def main():
    
    fooModel = model.ModelRoutine()
    fooModel()

    stationID = '15017030'
    comitRiver = 9000151

    # Read historical obs

    # print('hist Sim')
    # hisQSim  = fooModel.getStreamFlowsSimulatedHist(comitRiver)
    # 
    histQObs_fw, _, _ = fooModel.getFewsData(stationID, 'Q')

    hisQObs_sdb = pd.read_csv(os.path.join(r'D:\IDEAM\0_ejecucion\4.scripts\IDEAMGGlows\model\static\timeSeries\CAUDALMEDIODIARIO', '{0}.csv'.format(stationID)),
                              parse_dates=['Fecha'],
                              date_parser=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M'),
                              index_col='Fecha')
    
    hisQObs_sdb.rename({'Valor':'data'}, axis = 1, inplace=True)
    hisQObs_sdb.rename_axis('date', axis=0, inplace=True)
    hisQObs_sdb = hisQObs_sdb['data'].to_frame()

    # hisQObs_sdb = hisQObs_sdb.loc[hisQObs_sdb.index > '2010-01-01'].copy()

    recQObs = fooModel.getStreamFlowsSimulatedRecords(comitRiver)

    #hisQObs_sdb = fooModel.getDailyAverageDataHist_hs(stationID, 'Q')

    hisQSim  = fooModel.getStreamFlowsSimulatedHist(comitRiver)
    # hisQSim = hisQSim.loc[hisQSim.index > '2010-01-01'].copy()

    hisQSim_F = fooModel.getBiasCorrectData(hisQSim, hisQSim, hisQObs_sdb)

    recQObs_F = fooModel.getBiasCorrectData(recQObs, hisQSim, hisQObs_sdb)

    for dateInit in pd.date_range("2022-08-23",periods=10):
         
        month = str(dateInit.month) if  dateInit.month >= 10 else '0' + str(dateInit.month)
        day = str(dateInit.day) if  dateInit.day >= 10 else '0' + str(dateInit.day)

        dateInit = (str(dateInit.year) + month + day)

        ensbSim = fooModel.getStreamFlowsSimulatedEnsemble(comitRiver, dateInit = dateInit) #'20220801')
        
        for col in ensbSim.columns:
            ensbSim[col+'_fix'] = fooModel.getBiasCorrectData(ensbSim[col], hisQSim, hisQObs_sdb)


        # hisQObs_hs  = fooModel.getDailyAverageDataHist_hs(stationID, 'Q')

        # hisHObs  = fooModel.getDailyAverageDataHist_hs(stationID, 'H')

        left = dt.date(2022, 8, 18)
        right = dt.date(2022, 9, 20)
        
        col_fix = []
        for col in ensbSim.columns:
            if 'fix' in col:
                plt.plot(ensbSim.index, ensbSim[col], color='gray', alpha=0.2)
                col_fix.append(col)

        plt.plot(ensbSim.index, ensbSim[col_fix].max(axis=1), 'r--', alpha=0.5)
        plt.plot(ensbSim.index, ensbSim[col_fix].min(axis=1), 'r--', alpha=0.5)

        plt.plot(ensbSim.index, ensbSim[col_fix].quantile(0.75, axis=1), 'b.', alpha=0.7, label='q75')
        plt.plot(ensbSim.index, ensbSim[col_fix].quantile(0.25, axis=1), 'b.', alpha=0.7, label='q25')

        plt.plot(hisQObs_sdb.index, hisQObs_sdb.data, label='Observado historico')
        plt.plot(hisQSim_F.index, hisQSim_F.data, label='Simulado Historico')
        plt.plot(recQObs_F.index, recQObs_F.data, label='Record ensamble')
        plt.plot(histQObs_fw.index, histQObs_fw.data, label='Datos fews')

        plt.grid()
        plt.xlim(left, right)
        plt.ylim(-5, 50)
        plt.legend()
        plt.show()

    # print('')
    # print('hist ob static')
    # hisQObs_sdb = fooModel.getDailyAverageDataHist_static(stationID, 'Q')
    # print(hisQObs_sdb)

    # print('')
    # print('hist sim f')
    # hisQSimF = fooModel.getBiasCorrectData(hisQSim, hisQSim, hisQObs_hs)
    # print(hisQSimF.head(3))

    # print('')
    # print('hist sim f 2 ')
    # ensbSim = fooModel.getStreamFlowsSimulatedEnsemble(comitRiver)
    # hisQSimF = fooModel.getBiasCorrectData(ensbSim[ensbSim.columns[1]], hisQSim, hisQObs_hs)
    # print(hisQSimF.head(3))

    # print(ensbSim[ensbSim.columns[0]])
    # print(hisQSimF)

    # hisHObs  = fooModel.getDailyAverageDataHist(stationID, 'H')
    # cGasto   = fooModel.getCurvaDeGasto(stationID)



if __name__ == "__main__":
    main()