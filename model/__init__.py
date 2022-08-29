
import os
import sys
import warnings

from model.auxFun import *

sys.path.insert(1, r'D:\IDEAM\0_ejecucion\4.scripts\py')
from TestFile import test1
from initialDict import initialDict

'''
/////////////////////////////////////////////////////////////////////////

                                __init__.py

/////////////////////////////////////////////////////////////////////////

Date :      Agust 23, 2022

Modified:   Agust 26, 2022

Purpose:    IDEAMGGLows main source

Needs:      See requirements.txt

Usage:      python __init__.py
            model.ModelRoutine()

Contends:   ModelRoutine
                
                getStreamFlowsSimulatedEnsemble
                getStreamFlowsSimulatedRecords
                getStreamFlowsSimulatedHist
                getStreamFlowsSimulatedDayAvg
                getStreamFlowsSimulatedMonthAvg

                getFewsData

                getCaudalMedioDiarioData
                getCurvaDeGasto
                getNivelMedioDiario

                getCatchmentGDF
                getPerfilTransversal
                getSeccionesTransversales
'''


class ModelRoutine:
    def __init__(self):
        self.staticDataBase = initialDict()
        
        self.__reviewPaths__()
    

    def __call__(self):
        # Read catchment data
        with open(self.catchmentPath) as f:
            self.catchmentdb = readCatchmentFile(self.catchmentPath)

        # Read Transversal section data
        self.crossSectionDb = readTransversalSectionDb(self.crossSectionPath)

        # Read curvasDeGasto files
        self.curvasGastoFiles = {}
        [self.curvasGastoFiles.update({ii.split('_')[0]: ii}) for ii in os.listdir(self.curvasGastoPath)]

        
    def __reviewPaths__(self):
        # Path build
        self.catchmentPath = os.path.join(__path__[0],
                                          self.staticDataBase["CATCHMENT"]['FOLDER'],
                                          self.staticDataBase["CATCHMENT"]['FILE'])
        
        self.crossSectionPath = os.path.join(__path__[0],
                                             self.staticDataBase["SECTIONS"]['FOLDER'],
                                             self.staticDataBase["SECTIONS"]['FILE'])
        
        self.curvasGastoPath = os.path.join(__path__[0],
                                            self.staticDataBase["CURVASGASTO"]["FOLDER"])

        # Assert existence of the folder
        assert os.path.exists(self.catchmentPath)       , "{} does not exist.".format(self.catchmentPath)
        assert os.path.exists(self.catchmentPath)       , "{} does not exist.".format(self.catchmentPath)
        assert len(os.listdir(self.curvasGastoPath)) > 0, "Does not files in {} directory.".format(self.curvasGastoPath)

    # Get Function static data
    def getCatchmentGDF(self):
        return self.catchmentdb
    

    def getCrossSectionDataBase(self):
        return self.crossSectionDb

    # Get function dynamic data
    def getStreamFlowsSimulatedEnsemble(self, comid: int):
        '''
        var  :
             - comid : int -> reach chanel id
        return :
           ensembles : pandas.DataFrame -> discharge result of all ensembles.
                       delta time: depends of some ensemble
                       forecast (depend of ensemble)
        Test results:
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedEnsemble
            Elapsed time in 50 run test = 2.5405158376693726 seconds
            //////////////////////////////////////////////////////////////////////////
            26/AGO
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedEnsemble
            Elapsed time in 50 run test = 2.114068832397461 seconds
            //////////////////////////////////////////////////////////////////////////
        
        '''
        assert type(comid) == int, "comid should be integer"
        return extractForecastEnsembles(comid)

    
    def getStreamFlowsSimulatedRecords(self, comid: int):
        '''
        var  :
             - comid : int -> reach chanel id
        return :
           records : pandas.DataFrame -> discharge
           delta time depends of the ensembled used
           From 01/01/present year to today
        Test results:
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedRecords
            Elapsed time in 50 run test = 2.6571688747406004 seconds
            //////////////////////////////////////////////////////////////////////////            
            26 AGO
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedRecords
            Elapsed time in 50 run test = 2.6040759468078614 seconds
            //////////////////////////////////////////////////////////////////////////
        '''
        assert type(comid) == int, "comid should be integer"
        return extractForecastRecords(comid)

    
    def getStreamFlowsSimulatedHist(self, comid: int):
        '''
        var  :
             - comid : int -> reach chanel id
        return :
           historic data : pandas.DataFrame -> discharge of the data 
                                               delta time daily
                                               from 1979 to 2022-04-30(randon date to finish)
        Test results:
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedHist
            Elapsed time in 50 run test = 3.879017152786255 seconds
            //////////////////////////////////////////////////////////////////////////
            26 AGO
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedHist
            Elapsed time in 50 run test = 7.871127128601074 seconds
            //////////////////////////////////////////////////////////////////////////
        '''
        assert type(comid) == int, "comid should be integer"
        return extractHistoricSimulation(comid)

    
    def getStreamFlowsSimulatedDayAvg(self, comid: int):
        '''
        var  :
            - comid : int -> reach chanel id
        return :
           daily average : pandas.DataFrame -> discharge for all 
           days of a year.
        Test results:
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedDayAvg
            Elapsed time in 50 run test = 1.5180004358291626 seconds
            //////////////////////////////////////////////////////////////////////////
            26 AGO
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedDayAvg
            Elapsed time in 50 run test = 4.840162954330444 seconds
            //////////////////////////////////////////////////////////////////////////
        '''
        assert type(comid) == int, "comid should be integer"
        return extractDailyAverages(comid)

    
    def getStreamFlowsSimulatedMonthAvg(self, comid: int):
        '''
        var  :
            - comid : int -> reach chanel id
        return :
           monthly average : pandas.DataFrame -> discharge for all 
           month of a year.
        Test results:
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedMonthAvg
            Elapsed time in 50 run test = 5.176962566375733 seconds
            //////////////////////////////////////////////////////////////////////////
            26 AGO
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getStreamFlowsSimulatedMonthAvg
            Elapsed time in 50 run test = 4.80470419883728 seconds
            //////////////////////////////////////////////////////////////////////////
        '''
        assert type(comid) == int, "comid should be integer"
        # TODO: Add conditional for error in comid
        return extractMonthlyAverages(comid)

    
    def getFewsData(self, stationID: str, typeData: str):
        """
        obj  : Obtain data for fews web server
        var:
            - stationID : str -> station code.
            - typeData  : str -> Type of data to extract. Shoud be H or Q; H for water depth
                                 and Q for charge.
        return:
            data    : DataFrame -> Data observed. obs.data in json
            dataSen : DataFrame -> Data sensor. obs.sen in json
            dataP   : DataFrame -> Data precipitation. obs.prec in json
        Test results: 
            - 24/08/2022
            - Time reading data + dataframe construct: 
                //////////////////////////////////////////////////////////////////////////
                Test 1
                Test for function : getFewsData
                Elapsed time in 50 run test = 0.03583229064941406 seconds
                //////////////////////////////////////////////////////////////////////////
            - Time reading data + dataframe construct + dataFrame fix:
                //////////////////////////////////////////////////////////////////////////
                Test 1
                Test for function : getFewsData
                Elapsed time in 50 run test = 0.04199528694152832 seconds
                //////////////////////////////////////////////////////////////////////////
            26 AGO
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getFewsData
            Elapsed time in 50 run test = 0.040893268585205075 seconds
            //////////////////////////////////////////////////////////////////////////
        """
        assert type(stationID) == str, 'StationID should be a string format (str).'
        assert type(typeData) == str, 'typeData should be a string format (str).'
        assert typeData.upper() in ["H", "Q"], 'typeData only should be H or Q, not {}'.format(typeData)
        
        # Build url
        url_dir = self.staticDataBase['FEWS']['URL'] + '/json' + typeData + '/'
        stationFile = '00' + stationID + typeData + 'obs.json'
        
        # Extrac data
        # try:
        #     response = urlopen(url_dir + stationFile)
        #     response = json.loads(response.read())
        # except:
        #     print('URLError: {} does not exist.'.format(url_dir + stationFile))
        #     sys.exit()
        # TODO: Add conditional id station id does not exist
        return jfews2df(url_dir + stationFile)

    
    def getDailyAverageDataHist(self, stationID, typeData: str):
        '''
        obj  : Obtain data for hydroshare web server
        var:
            - stationID : str -> station code.
            - typeData  : str -> Type of data to extract. Shoud be H or Q; H for water depth
                                 and Q for charge.
        return:
            data    : DataFrame -> Data observed. Hydroviwer web page
        Test results: 
            //////////////////////////////////////////////////////////////////////////
            Test 1 - Discharge
            Test for function : getDailyAverageDataHist
            Elapsed time in 50 run test = 4.755099439620972 seconds
            //////////////////////////////////////////////////////////////////////////
            //////////////////////////////////////////////////////////////////////////
            Test 1 - Water level
            Test for function : getDailyAverageDataHist
            Elapsed time in 50 run test = 8.713570265769958 seconds
            //////////////////////////////////////////////////////////////////////////
        26 AGO
        //////////////////////////////////////////////////////////////////////////
        Test 1 - Discharge
        Test for function : getDailyAverageDataHist
        Elapsed time in 50 run test = 4.752217206954956 seconds
        //////////////////////////////////////////////////////////////////////////
        //////////////////////////////////////////////////////////////////////////
        Test 1
        Test for function : getDailyAverageDataHist
        Elapsed time in 50 run test = 8.738563523292541 seconds
        //////////////////////////////////////////////////////////////////////////
        '''
        assert type(stationID) == str, 'StationID should be a string format (str).'
        assert type(typeData) == str, 'typeData should be a string format (str).'
        assert typeData.upper() in ["H", "Q"], 'typeData only should be H or Q, not {}'.format(typeData)
        
        # Select folder of the data
        if typeData.upper() == 'Q':
            typeDataURL = 'Discharge_Data/'

            # Build url direction
            urlDir = self.staticDataBase['HYDROSHARE']['URL_D'] + typeDataURL + stationID + '.csv'
        elif typeData.upper() == 'H':
            typeDataURL = 'Water_Level_Data/'

            # Build url direction
            urlDir = self.staticDataBase['HYDROSHARE']['URL_WL'] + stationID + '.csv'

        # Extract data
        # try:
        #     response = requests.get(urlDir, verify=True).content
        # except:
        #     print('URLError: {} does not exist.'.format(urlDir))
        #     sys.exit()
        # TODO: Add conditional id station id does not exist
        # TODO: Add actual data (2020 - actual)
        return hydroShare2df(urlDir)

    
    def getCurvaDeGasto(self, stationID):
        """
        var     : stationID : str -> Identificador de la estacion de trabajo
        return  : pandas.DataFrame with curvas de gasto of station
                  99 id curva gasto does not exist
        Test    :
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getCurvaDeGasto
            Elapsed time in 50 run test = 0.037938528060913086 seconds
            //////////////////////////////////////////////////////////////////////////
        26 AGO
        //////////////////////////////////////////////////////////////////////////
        Test 1
        Test for function : getCurvaDeGasto
        Elapsed time in 50 run test = 0.033310894966125486 seconds
        //////////////////////////////////////////////////////////////////////////
        """
        assert type(stationID) == str, 'StationID should be a string format (str).'

        if stationID in list(self.curvasGastoFiles.keys()):        
            filePath = os.path.join(__path__[0],
                                    self.staticDataBase["CURVASGASTO"]["FOLDER"],
                                    self.curvasGastoFiles[stationID])
            return readXMLCurvasGasto(filePath)
        else:
            warnings.warn("Curva de gasto does not found.")
            return 99

    
    def getSeccionesTransversales(self, stationID):
        ''' 
        var    : stationID : str -> Identificador de la estacion de trabajo
        retunr : Cross sections: (pamdas.DataFrame) for the station or 
                 99: (int) if cross sections does not exist.
        Test   : 
            //////////////////////////////////////////////////////////////////////////
            Test 1
            Test for function : getSeccionesTransversales
            Elapsed time in 50 run test = 0.00045877456665039063 seconds
            //////////////////////////////////////////////////////////////////////////
        26 AGO
        //////////////////////////////////////////////////////////////////////////
        Test 1
        Test for function : getSeccionesTransversales
        Elapsed time in 50 run test = 0.0004388427734375 seconds
        //////////////////////////////////////////////////////////////////////////
        '''
        assert type(stationID) == str, 'StationID should be a string format (str).'
        assert len(self.crossSectionDb['CODIGO'].unique()) > 0, "Review data base of the cross sections."

        if int(stationID) in self.crossSectionDb['CODIGO'].unique():
            return substrackCrossSectionDb(self.crossSectionDb, int(stationID))
        else:
            warnings.warn("Warning: Cross Section does not exist for the station {}.".format(stationID))
            return 99

