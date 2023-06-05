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
            if '-docs' in zipDir:
                zipDir = zipDir[0:zipDir.rindex('-')] + zipDir[zipDir.rindex('.'):]
            return zipDir
    return FileNotFoundError


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
    try:
        SInsightData = readJson(SInsightPath)
    except Exception as e:
        print(SInsightPath)
        error(e.__str__())
        return
    if 'dependencies' in SInsightData.keys():
        SInsightData.pop('dependencies')
    
    keysToRemove = list(SInsightData['insightMetadata'].keys())
    for key in ['activated', 'name', 'description']:
        keysToRemove.remove(key)
    
    for key in keysToRemove:
        SInsightData['insightMetadata'].pop(key)
        
    SInsightData['insightMetadata']['activated'] = 'TRUE'
    ucs = len(SInsightData['useCases'])
    toRemove = []
    for uc in range(ucs):
        if SInsightData['useCases'][uc]['id'] in ucsList:
            SInsightData['useCases'][uc]['activated'] = 'TRUE'
        else:
            toRemove.append(uc)
            # try:
            #     pass
            # except Exception as e:
            #     print(SInsightPath)
            #     error(e.__str__())
    if len(toRemove) == 0:
        for i in reversed(toRemove):
            SInsightData['useCases'].remove(i)
    updateJson(SInsightPath, SInsightData)


def reOverwriteInsight(solutionPath, corePath, insightName, ucs):
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
        reOverwriteInsight(solutionPath, corePath, insightName, ucs)


def createInsightDirectory(solutionPath, insights):
    for i in insights:
        try:
            os.mkdir(os.path.join(solutionPath, i))
        except Exception as e:
            if 'already exists' in e.__str__():
                warning('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])


def createUcDirectory(solutionPath, ucs):
    for u in ucs:
        insight = u[0: u.rindex('_')]
        try:
            os.mkdir(os.path.join(solutionPath, insight, u))
        except Exception as e:
            if 'already exists' in e.__str__():
                warning('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])


def ucsDict(insights, ucs):
    tmpDict = dict()
    for i in insights:
        tmpDict[i] = list()
        for u in ucs:
            if i == u[0: u.rindex('_')]:
                tmpDict[i].append(u)
    return tmpDict


def overwriteInsight(solution, corePath, insight, allUcs):
    try:
        insightZipDir = searchInsightInCore(corePath, insight)
        insightCorePath = os.path.join(corePath, insightZipDir)
        if insightZipDir == FileNotFoundError:
            return
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    
    finally:
        insightPath = os.path.join(solution, insight)
        with zipfile.ZipFile(insightCorePath) as z:
            srcFiles = filesInZip(corePath, insightZipDir, 'Core/Insights/' + insight + '/')
            for file in srcFiles:
                if file.split('/')[-1] == 'SInsight.json':
                    try:
                        with z.open(file) as j:
                            sInsight = jsonifyZip(j.read())
                            if os.path.exists(os.path.join(insightPath, 'SInsight.json')):
                                updateJson(os.path.join(insightPath, 'SInsight.json'), sInsight)
                            else:
                                writeJson(os.path.join(insightPath, 'SInsight.json'), sInsight)
                    except Exception as e:
                        error(e.__str__())
                    cleanSInsight(allUcs[insight], os.path.join(insightPath, 'SInsight.json'))
                # print(file.split('/')[-1])
                # if file.split('/')[-2] in allUcs[insight] and file.split('/')[-1] != '':
                #     print(allUcs[insight])
                #     print(file)
                if file.split('/')[-2] in allUcs[insight] and file.split('/')[-1] != '':
                    # print('here')
                    # ucFiles = filesInZip(corePath, insightZipDir, 'Core/DemoData/' + insight + '/' + file + '/')
                    # for uc in ucFiles:
                    tempInsightPath = os.path.join(insightPath, file.split('/')[-2], file.split('/')[-1])
                    try:
                        with z.open(file) as ucj:
                            jsonFile = jsonifyZip(ucj.read())
                            if os.path.exists(tempInsightPath):
                                updateJsonMultiLang(tempInsightPath, jsonFile)
                            else:
                                writeJsonMultiLang(tempInsightPath, jsonFile)
                    except Exception as e:
                        print('here - ' + file.split('/')[-2] + '/' + file.split('/')[-1])
                        error(e.__str__())
                    # print(file)
                    # ucFiles = filesInZip(corePath, insightZipDir, 'Core/DemoData/' + insight + '/' + file + '/')
                    # for ucFile in ucFiles:
                    #     try:
                    #         with z.open(ucFile) as ucJ:
                    #             jsonFile = jsonifyZip(j.read())
                    #             writeJson(os.path.join(insightPath, ucFile), jsonFile)
                    #             # newJason = open(os.path.join(insightPath, file.split('/')[-1]), 'a')
                    #             # newJason.write(
                    #             #     json.dumps(json.loads(ucJ.read().decode(encoding='utf-8-sig')), indent=4))
                    #     except Exception as e:
                    #         error(e.__str__())


def main(argv):
    startLog()
    try:
        solution = getSolution(getPath('solution'))
    except:
        error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    try:
        corePath = createPath(getPath('solution'), 'package\\target\\DataLoad')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    channels = getChannels(solution)
    if len(channels) > 3:
        theChannel = chooseChanel(channels)
        try:
            solution = os.path.join(solution + theChannel, 'Insights')
        except Exception as e:
            error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
            return
    else:
        try:
            solution = os.path.join(getSolution(getPath('solution')), 'Insights')
        except Exception as e:
            error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
            return
    
    insights = getCol(argv[0], 'Insight')
    ucs = getCol(argv[0], 'UC')
    activated = getCol(argv[0], 'Activated')
    tmpInsights = list()
    tmpUcs = list()
    for i in range(len(insights)):
        if activated[i] == 'V':
            tmpInsights.append(insights[i])
            tmpUcs.append(ucs[i])
    insights = tmpInsights
    ucs = tmpUcs
    insights = set(insights)
    createInsightDirectory(solution, insights)
    createUcDirectory(solution, ucs)
    ucsDictionary = ucsDict(list(insights), ucs)
    
    # prettyPrintJson(ucsDictionary)
    # print(insights)
    # print(ucs)
    
    for insight in insights:
        overwriteInsight(solution, corePath, insight, ucsDictionary)
    # if not os.path.exists(solutionPath):
    #     error(solutionPath + ' dosn\'t exists')
    #     return
    # inputFile = argv[0]
    # print(argv[0])
    # enableCsv = readCsv(inputFile)
    # print(enableCsv)
    # sortInsights(solutionPath, corePath, enableCsv)
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])

#   0 - file with the list of insights to enable by use cases
