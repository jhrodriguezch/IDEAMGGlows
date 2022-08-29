from cProfile import label
from turtle import title
import model
import matplotlib.pyplot as plt
import pandas as pd
import geoglows as ggs


def emptyPorcentage(df):
    return 100 * len(df[df['data'].isna()]) / len(df)

def main():
    
    fooModel = model.ModelRoutine()
    fooModel()

    stationID = '29067120'
    comitRiver = 9000639

    hisQSim  = fooModel.getStreamFlowsSimulatedHist(comitRiver)
    hisQObs  = fooModel.getDailyAverageDataHist(stationID, 'Q')
    # hisHObs  = fooModel.getDailyAverageDataHist(stationID, 'H')
    # cGasto   = fooModel.getCurvaDeGasto(stationID)

    # MATH
    histQ = pd.concat([hisQSim.add_suffix("_Sim"), 
                       hisQObs.add_suffix("_Obs")])
    hisQFix = ggs.bias.correct_historical(simulated_data = histQ['data_Sim'],
                                          observed_data  = histQ['data_Obs'])
    hisQFix.rename(columns={hisQFix.columns[0]: 'data'}, inplace=True)
    histQ = pd.concat([histQ, 
                       hisQFix.add_suffix("_Fix")])
    histQ.dropna(axis=0, how="all", inplace=True)

    # TEMPLATE
    fig, ax = plt.subplots(1,1)
    histQ.plot(ax=ax)
    ax.legend(["Simulado", "Observado", "Fix"])
    plt.show()

    # TEST
    print("")
    print('********** CAUDAL OBS **********')
    print(hisQObs.describe())
    print('Init date: {0}'.format(hisQObs.index[0]))
    print('End date : {0}'.format(hisQObs.index[-1]))
    print('% empty : {0:.2f}%'.format(emptyPorcentage(hisQObs)))


    print("")
    print('********** CAUDAL SIM **********')
    print(hisQSim.describe())
    print('Init date: {0}'.format(hisQSim.index[0]))
    print('End date : {0}'.format(hisQSim.index[-1]))
    print('% empty : {0:.2f}%'.format(emptyPorcentage(hisQSim)))


    print("")
    print('********** CAUDAL FIX **********')
    print(hisQFix.describe())
    print('Init date: {0}'.format(hisQFix.index[0]))
    print('End date : {0}'.format(hisQFix.index[-1]))
    print('% empty : {0:.2f}%'.format(emptyPorcentage(hisQFix)))

    # print("")
    # print('********** NIVEL OBS **********')
    # print(hisHObs.describe())
    # print('Init date: {0}'.format(hisHObs.index[0]))
    # print('End date : {0}'.format(hisHObs.index[-1]))
    # print('% empty : {0:.2f}%'.format(emptyPorcentage(hisHObs)))



if __name__ == "__main__":
    main()