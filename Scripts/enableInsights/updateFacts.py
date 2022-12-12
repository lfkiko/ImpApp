import os
import sys
from logging import error

from Scripts.toolBoox.excelJsonToolBox import readJson, updateJson
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getSolution, getPath


def getCurrency(path):
    localCurrencyCd = 'USD'
    currencyCd = '$'
    try:
        projectProperties = os.path.join(path, 'project.projectProperties')
        with open(projectProperties, "r+") as f:
            properties = f.readlines()
            f.seek(0)
    except Exception as e:
        print(e.__str__())
    for line in properties:
        if line != '\n' and '=' in line:
            prop, value = line.split('=')
            if prop == 'DEFAULT_CURRENCY':
                currencyCd = value
            if prop == 'LocalCurrencyCd':
                localCurrencyCd = value
    
    return currencyCd, localCurrencyCd


def updateFacts(insightPath, useCase, currencyCd, currencyCdOriginal):
    storyFacts = readJson(os.path.join(insightPath, useCase))
    for table in storyFacts.keys():
        if type(storyFacts[table]) == dict:
            try:
                indexCd = storyFacts[table]['cols'].index('currencyCd')
            except:
                indexCd = -1
            try:
                indexOriginal = storyFacts[table]['cols'].index('currencyCdOriginal')
            except:
                indexOriginal = -1
            if indexCd != indexOriginal:
                for row in storyFacts[table]['rows']:
                    if indexCd > -1: row[indexCd] = currencyCd
                    if indexOriginal > -1: row[indexOriginal] = currencyCdOriginal
    try:
        updateJson(os.path.join(insightPath, useCase), storyFacts)
    except Exception as e:
        print(e.__str__())


def updateFacts(solutionPath, currencyCd, currencyCdOriginal):
    for insight in os.listdir(solutionPath):
        insightPath = os.path.join(solutionPath, insight)
        if insight != 'SEntities' and os.path.isdir(insightPath):
            for root, dirNames, filenames in os.walk(insightPath):
                insightUcs = dirNames
            for useCase in insightUcs:
                try:
                    updateFacts(insightPath, useCase, currencyCd, currencyCdOriginal)
                except Exception as e:
                    error(e.__str__() + ' ' + insight + ' ' + useCase)


def main(argv):
    startLog()
    try:
        solutionPath = os.path.join(getSolution(getPath('solution')), 'Insights')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    
    currencyCd, currencyCdOriginal = getCurrency(getSolution(getPath('solution')))
    if currencyCd != '$' or currencyCdOriginal != 'USD':
        updateFacts(solutionPath, currencyCd, currencyCdOriginal)
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])
