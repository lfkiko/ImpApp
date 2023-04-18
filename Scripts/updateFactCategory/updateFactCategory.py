from Scripts.toolBoox import *
import sys
import os
from logging import error, warning


def updateFacts(insightPath, insightUc, categoriesDict):
    insightFactsPath = os.path.join(insightPath, insightUc, "JInsightFacts.json")
    factUpdated = False
    if os.path.exists(insightPath):
        try:
            insightFacts = readJson(insightFactsPath)
        except:
            insightFacts = readJsonUtf8Sig(insightFactsPath)
        for fact in insightFacts.keys():
            if fact != 'storyId' and 'category' in insightFacts[fact]['cols']:
                factLen = len(insightFacts[fact]['cols'])
                cgIndex = insightFacts[fact]['cols'].index('category')
                if 'categoryDescription' in insightFacts[fact]['cols']:
                    descriptionIndex = insightFacts[fact]['cols'].index('categoryDescription')
                else:
                    descriptionIndex = factLen
                if 'categoryGroup' in insightFacts[fact]['cols']:
                    categoryGroupIndex = insightFacts[fact]['cols'].index('categoryGroup')
                else:
                    categoryGroupIndex = factLen
                if descriptionIndex != factLen or categoryGroupIndex != factLen:
                    factUpdated = True
                    for row in range(len(insightFacts[fact]['rows']) - 1):
                        cgDescription = categoriesDict[insightFacts[fact]['rows'][row][cgIndex]]
                        if descriptionIndex != factLen:
                            insightFacts[fact]['rows'][row][descriptionIndex] = cgDescription
                        if categoryGroupIndex != factLen:
                            insightFacts[fact]['rows'][row][categoryGroupIndex] = cgDescription
        
        if factUpdated:
            try:
                updateJsonMultiLang(insightFactsPath, insightFacts)
            except:
                updateJsonMultiLangUtf8Sig(insightFactsPath, insightFacts)
    
    else:
        warning('There is no such file = ' + insightPath)


def checkFacts(solution, insights, categoriesDict):
    for insight in insights:
        insightUcs = []
        insightPath = os.path.join(solution, insight)
        for root, dirNames, filenames in os.walk(insightPath):
            insightUcs = dirNames
            if 'doc' in insightUcs:
                insightUcs.remove('doc')
            break
        for useCase in insightUcs:
            try:
                updateFacts(insightPath, useCase, categoriesDict)
            except Exception as e:
                error(e.__str__() + ' ' + insight + ' ' + useCase)


def creatDict(categoriesJson):
    categoriesDict = dict()
    for cg in categoriesJson['categoryGroups']:
        categoriesDict[cg['id']] = cg['description']['langMap']
    return categoriesDict


def main(argv):
    startLog()
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'Insights')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    try:
        categoriesPath = os.path.join(getSolution(getPath('solution')), 'SEntities')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    try:
        categoriesJson = readJson(os.path.join(categoriesPath, 'SCategoryGroups.json'))
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    
    # insights = os.listdir(solution)
    # insights.remove('SEntities')
    # categoriesDict = creatDict(categoriesJson)
    # checkFacts(solution, insights, categoriesDict)
    print('Not ready yet')
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])
