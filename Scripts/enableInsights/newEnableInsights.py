import os
import shutil
import sys
from logging import error, warning

from Scripts.toolBoox.excelJsonToolBox import readCsv, readJson, updateJson
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getPath, getSolution, modelVersion

searchedCoreFolders = ["product-subscriptions-biz-unit", "product-budgets-biz-unit", "product-debt-biz-unit",
                       os.path.join("product-engage-biz-unit", "Projects"), "product-pa-biz-unit"]
searchedModelFolders = ['product-subscriptions-biz-unit', 'product-portfolio-biz-unit']


def getChannels(solution):
    path = os.path.dirname(solution)
    channels = []
    for x in os.listdir(path):
        if os.path.isdir(os.path.join(path, x)):
            channels.append(x)
    return channels


def chooseChanel(channels, sg=None):
    event, values = sg.Window('Choose an option', [
        [sg.Text('Select one->'), sg.Listbox(channels, size=(20, 3), key='LB')],
        [sg.Button('Ok')]]).read(close=True)
    channel = values["LB"][0]
    channel = channel[channel.index('$'):]
    return channel


def validInsight(insightName):
    try:
        int(insightName)
        return False
    except:
        pass
    for char in insightName:
        if char in (' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            return False
    return True


def searchInsightInCore(core, modelPath, insightName, useModel):
    for coreFolder in searchedCoreFolders:
        if useModel and 'SUB_' in insightName:
            try:
                currFolder = os.path.join(modelPath, coreFolder, "Core", "Insights")
            except Exception as e:
                error('Path Error:' + e.__str__()[e.index(']') + 1:])
                return
        else:
            try:
                currFolder = os.path.join(core, coreFolder, 'Core', 'Insights')
            except Exception as e:
                error('Path Error:' + e.__str__()[e.index(']') + 1:])
        if os.path.exists(currFolder) and insightName in os.listdir(currFolder):
            return os.path.join(currFolder, insightName)
    return


def getUcsList(insightName, ucs):
    try:
        return [insightName + "_UC" + str(int(ucs))]
    except:
        return [insightName + "_UC" + uc for uc in ucs.split(',')]


def cleanSInsight(ucsList, SInsightPath):
    SInsightData = readJson(SInsightPath)
    SInsightData.pop('dependencies')
    for key in SInsightData['insightMetadata'].keys():
        if key not in ['activated', 'name', 'description']:
            SInsightData['insightMetadata'].pop(key)
        if key == 'activated':
            SInsightData['insightMetadata'][key] = 'TRUE'
    for uc in SInsightData['useCases']:
        if SInsightData['useCases'][uc]['id'] in ucsList:
            SInsightData['useCases'][uc]['activated'] = 'TRUE'
    updateJson(SInsightPath, SInsightData)


def overwriteInsight(solutionPath, cocorePathre, modelPath, insightName, ucs, useModel):
    notFound = 0
    insightCorePath = searchInsightInCore(cocorePathre, modelPath, insightName, useModel)
    try:
        os.mkdir(os.path.join(solutionPath, insightName))
    except Exception as e:
        error('Path Error:' + e.__str__()[e.index(']') + 1:])
        return
    ucsList = getUcsList(insightName, ucs)
    try:
        shutil.copytree(os.path.join(insightCorePath, 'SInsight.json'),
                        os.path.join(solutionPath, insightName, 'SInsight.json'))
    except Exception as e:
        if len(e.args) > 1 and 'Cannot create a file when that file already exists' == e.args[1]:
            warning('uc already exists in solution: SInsight.json')
        else:
            error('file not found: SInsight.json wasn\'t found.')
    for uc in ucsList:
        try:
            shutil.copytree(os.path.join(insightCorePath, uc), os.path.join(solutionPath, insightName, uc))
        except Exception as e:
            if len(e.args) > 1 and 'Cannot create a file when that file already exists' == e.args[1]:
                warning('uc already exists in solution: %s', uc)
            else:
                ucsList.remove(uc)
                notFound += 1
                error('UC not found: {} wasn\'t found.'.format(uc))
    cleanSInsight(ucsList, os.path.join(solutionPath, insightName, 'SInsight.json'))
    return notFound


def sortInsights(solutionPath, corePath, modelPath, enableCsv, useModel):
    notFound = 0
    total = 0
    for i in enableCsv.index:
        insightName = enableCsv['insight'][i]
        if not validInsight(insightName):
            warning("insight name is illegal: " + insightName)
        ucs = enableCsv['UC'][i]
        total += len(ucs)
        notFound = overwriteInsight(solutionPath, corePath, modelPath, insightName, ucs, useModel)
    return notFound


def main(argv):
    startLog()
    corePath = os.path.join(getPath('corePath'), 'product-bizpack')
    modelPath = os.path.join(getPath('modelPath'), 'product-models-bizpack')
    try:
        solutionPath = os.path.join(getSolution(getPath('solution')), 'Insights')
    except:
        error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    channels = getChannels(solutionPath)
    if len(channels) > 3:
        theChannel = chooseChanel(channels)
        solutionPath = solutionPath + theChannel
    
    if not os.path.exists(solutionPath):
        error(solutionPath + ' dosn\'t exists')
        return
    useModel = modelVersion(getPath('solution'))
    inputFile = argv[0]
    enableCsv = readCsv(inputFile)
    notFound = sortInsights(solutionPath, corePath, modelPath, enableCsv, useModel)
    endLog()
    
    return notFound


if __name__ == "__main__":
    main(sys.argv[1:])

#   0 - file with the list of insights to enable by use cases
