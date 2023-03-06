from logging import warning

from Scripts.toolBoox import *
import json
import os
import sys
import zipfile

searchedCoreFolders = ['product-act-biz-unit.zip', 'product-budgets-biz-unit.zip',
                       'product-data-and-assets-biz-unit.zip', 'product-debt-biz-unit.zip',
                       'product-engage-biz-unit.zip', 'product-goals-biz-unit.zip', 'product-mt-biz-unit.zip']


def searchInsightInCore(corePath, insightName):
    zips = os.listdir(corePath)
    zips.remove('perso-biz.zip')
    for dirZip in searchedCoreFolders:
        if 'bank' in dirZip or 'docs' in dirZip:
            zips.remove(dirZip)
    for zipDir in zips:
        insightsInPath = filesInZip(corePath, zipDir, 'Core/Insights/' + insightName)
        if len(insightsInPath) != 0:
            return zipDir
    return FileNotFoundError


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
        else:
            try:
                SInsightData['useCases'].remove(uc)
            except Exception as e:
                error(e.__str__())
    updateJson(SInsightPath, SInsightData)


def overwriteInsight(solutionPath, corePath, insightName, ucs):
    try:
        insightZipDir = searchInsightInCore(corePath, insightName)
        insightCorePath = os.path.join(corePath, insightZipDir)
        if insightZipDir == FileNotFoundError:
            return
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    
    ucsList = getUcsList(insightName, ucs)
    try:
        os.mkdir(os.path.join(solutionPath, insightName))
    except:
        warning("Insight: " + insightName + " is all ready exists in the solution level")
    finally:
        insightpath = os.path.join(solutionPath, insightName)
        with zipfile.ZipFile(insightCorePath) as z:
            srcFiles = filesInZip(corePath, insightZipDir, 'Core/DemoData/' + insightName + '/')
            for file in srcFiles:
                if file.split('/')[-1] == 'SInsight.json':
                    try:
                        with z.open(file) as j:
                            newJson = open(insightpath, 'a')
                            newJson.write(json.dumps(json.loads(j.read().decode(encoding='utf-8-sig')), indent=4))
                    except Exception as e:
                        error(e.__str__())
                if file.split('/')[-1] in ucsList:
                    ucFiles = filesInZip(corePath, insightZipDir, 'Core/DemoData/' + insightName + '/' + file + '/')
                    for ucFile in ucFiles:
                        try:
                            with z.open(ucFile) as ucJ:
                                newJason = open(os.path.join(insightpath, file.split('/')[-1]), 'a')
                                newJason.write(
                                    json.dumps(json.loads(ucJ.read().decode(encoding='utf-8-sig')), indent=4))
                        except Exception as e:
                            error(e.__str__())
    
    cleanSInsight(ucsList, os.path.join(insightpath, 'SInsight.json'))


def sortInsights(solutionPath, corePath, enableCsv):
    print(enableCsv)
    for i in enableCsv.index:
        print(i)
        insightName = enableCsv['insight'][i]
        if not validInsight(insightName):
            warning("insight name is illegal: " + insightName)
        ucs = enableCsv['UC'][i]
        overwriteInsight(solutionPath, corePath, insightName, ucs)


def main(argv):
    startLog()
    try:
        solutionPath = os.path.join(getSolution(getPath('solution')), 'Insights')
    except:
        error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    try:
        corePath = createPath(getPath('solution'), 'package\\target\\DataLoad')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    channels = getChannels(getSolution(getPath('solution')))
    if len(channels) > 3:
        theChannel = chooseChanel(channels)
        solutionPath = solutionPath + theChannel
    print(solutionPath)
    print(corePath)
    print(channels)
    print(argv[0])
    insights = getCol(argv[0], 'Insight')
    tmpInsights = list()
    for i in insights:
        if i not in tmpInsights:
            tmpInsights.append(i)
    insights = tmpInsights
    ucs = getCol(argv[0], 'UC')
    activated = getCol(argv[0], 'Activated')
    tmpUc = list()
    for uc in range(len(ucs)):
        if activated[uc] != None:
            tmpUc.append(ucs[uc])
    ucs = tmpUc
    print(insights)
    # insights = set(insights)
    # insights = list(insights).sort()
    # print(insights)
    # UCS = getRow(argv[0], 'UC')
    # insights = getRow(argv[0], 'insight')
    # insights = getRow(argv[0], 'insight')
    # printExcel(argv[0])
    # print(getColCsv(argv[0], 'insight'))
    # print(getColCsv(argv[0], 'UC'))
    # print(getColCsv(argv[0], 'EB'))
    # print(getColCsv(argv[0], 'Activated'))
    #
    # if not os.path.exists(solutionPath):
    #     error(solutionPath + ' dosn\'t exists')
    #     return
    # inputFile = argv[0]
    # # print(argv[0])
    # enableCsv = readCsv(inputFile)
    # print(enableCsv)
    # sortInsights(solutionPath, corePath, enableCsv)
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])

#   0 - file with the list of insights to enable by use cases
