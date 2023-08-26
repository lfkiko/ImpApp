from Scripts.toolBoox import *
import sys
import os
from logging import error, warning


def updateCategories(insightPath, insightUc, categoriesDict):
    insightFactsPath = os.path.join(insightPath, insightUc, "JInsightFacts.json")
    if os.path.exists(insightPath):
        try:
            insightFacts = readJsonMultilingual(insightFactsPath)
        except Exception as e:
            error(e.__str__())
        factUpdated = False
        for fact in insightFacts.keys():
            if fact == 'categories':
                cgRemove = []
                for category in range(len(insightFacts[fact]['rows'])):
                    cg = insightFacts[fact]['rows'][category][0]
                    if cg in categoriesDict.keys():
                        insightFacts[fact]['rows'][category][1] = categoriesDict[cg]
                    else:
                        cgRemove.append(category)
                if len(cgRemove) > 0:
                    for cg in reversed(cgRemove):
                        fact['categories']['rows'].remove(cg)
                factUpdated = True
            
            elif fact == 'budgets':
                cgIndex = insightFacts[fact]['cols'].index('budgetCategoryKey')
                index = insightFacts[fact]['cols'].index('budgetCategoryName')
                for row in range(len(insightFacts[fact]['rows'])):
                    insightFacts[fact]['rows'][row][index] = categoriesDict[insightFacts[fact]['rows'][row][cgIndex]]
            
            elif fact != 'storyId' and any(
                col in insightFacts[fact]['cols'] for col in ('categoryGroup', 'categoryDescription')):
                cgIndex = insightFacts[fact]['cols'].index('category')
                indexes = {'categoryGroup': 0, 'categoryDescription': 0}
                for col in ['categoryGroup', 'categoryDescription']:
                    if col in insightFacts[fact]['cols']:
                        indexes[col] = insightFacts[fact]['cols'].index(col)
                    else:
                        indexes[col] = -1
                for row in range(len(insightFacts[fact]['rows'])):
                    cgDescription = categoriesDict[insightFacts[fact]['rows'][row][cgIndex]]
                    if indexes['categoryGroup'] > 0:
                        insightFacts[fact]['rows'][row][indexes['categoryGroup']] = cgDescription
                    if indexes['categoryDescription'] > 0:
                        insightFacts[fact]['rows'][row][indexes['categoryDescription']] = cgDescription
                factUpdated = True
        
        if factUpdated:
            try:
                updateJsonMultiLang(insightFactsPath, insightFacts)
            except Exception as e:
                print('check')
                error(e.__str__())
        else:
            warning('There are no categories in = ' + insightPath)
    
    else:
        warning('There is no such file = ' + insightPath)


def checkFactsCatefories(solution, insights, categoriesDict):
    for insight in insights:
        insightUcs = []
        insightPath = os.path.join(solution, insight)
        for root, dirNames, filenames in os.walk(insightPath):
            insightUcs = dirNames
            break
        for useCase in insightUcs:
            try:
                updateCategories(insightPath, useCase, categoriesDict)
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
        categoriesPath = os.path.join(getSolution(getPath('solution')), 'SEntities', 'SCategoryGroups.json')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    
    categoriesJson = readJsonMultilingual(categoriesPath)
    
    insights = os.listdir(solution)
    insights.remove('SEntities')
    categoriesDict = creatDict(categoriesJson)
    prettyPrintJson(categoriesDict)
    checkFactsCatefories(solution, insights, categoriesDict)
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])
