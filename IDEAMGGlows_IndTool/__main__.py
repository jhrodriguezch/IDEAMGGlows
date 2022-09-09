#!/usr/bin/env python
# -*- coding: utf-8 -*-

__version__     = '0.1'
__author__      = 'Jhonatan Rodriguez Chaves'
__authorEmail__ = 'jhrodriguezch@unal.edu.co'
__license__     = 'GPL'

import model
import view
import template

'''
/////////////////////////////////////////////////////////////////////////

                                __main__.py

/////////////////////////////////////////////////////////////////////////

Date :      Agust 16, 2022

Modified:   Agust 24, 2022

Purpose:    IDEAMGGLows main source

Needs:      See requirements.txt

Usage:      python __main__.py
            python IDEAMGGlows

Contends:   ...

Bibliography & useful links:
    http://www.ideam.gov.co/web/agua/fews
    https://www.hydroshare.org
    https://www.geoglows.org
    http://www.ideam.gov.co
'''

if __name__ == "__main__":
    """ 
    ***********************************************
                        MODEL
    *********************************************** 
    Model: data base manage
    """
    fooModel = model.ModelRoutine()
    fooModel()
    # Get simulation data
    comitRiver = 9022115
    stationID = '47017160'
    '''
    ensemblesSim = fooModel.getStreamFlowsSimulatedEnsemble(comitRiver)
    recordsSim   = fooModel.getStreamFlowsSimulatedRecords(comitRiver)
    histSim      = fooModel.getStreamFlowsSimulatedHist(comitRiver)
    dayAvgSim   = fooModel.getStreamFlowsSimulatedDayAvg(comitRiver)
    monAvgSim   = fooModel.getStreamFlowsSimulatedMonthAvg(comitRiver)
    #  '''
    # Get FEWS data
    stationID = '47017160'
    """
    a, b, c = fooModel.getFewsData(stationID, 'Q')
    a, b, c = fooModel.getFewsData(stationID, 'H')
    # """
    # Get observer historical data
    """
    fooModel.getDailyAverageDataHist(stationID, 'Q')
    fooModel.getDailyAverageDataHist(stationID, 'H')
    # """
    # Get static data bases
    """
    fooModel.getSeccionesTransversales(stationID)
    fooModel.getCurvaDeGasto(stationID)
    fooModel.getCatchmentGDF()
    # """

    # view
    # fooTemplate = template.App()
    # fooTemplate()