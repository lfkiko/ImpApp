import sys
import os
from logging import error, warning

from Scripts.toolBoox.excelJsonToolBox import readJson, updateJson, checkEndCode, readJsonUtf8Sig, updateJsonUtf8Sig
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getPath, getSolution, createPath


def updateFacts(insightPath, insightUc, fact, fieldName, fieldType, fieldVal):
    insightFactsPath = os.path.join(insightPath, insightUc, "JInsightFacts.json")
    if os.path.exists(insightPath):
        try:
            insightFacts = readJson(insightFactsPath)
        except:
            insightFacts = readJsonUtf8Sig(insightFactsPath)
        if fact in insightFacts.keys():
            insightFacts[fact]['cols'].append(fieldName)
            for row in insightFacts[fact]['rows']:
                row.append(fieldVal)
            insightFacts[fact]['attributesTypes'].append(fieldType)
            try:
                updateJson(insightFactsPath, insightFacts)
            except:
                updateJsonUtf8Sig(insightFactsPath, insightFacts)
        else:
            warning(fact + 'is not part of ' + insightPath)
    else:
        warning('There is no such file = ' + insightPath)


def checkFacts(solution, insights, fact, fieldName, fieldType, fieldVal):
    for insight in insights:
        insightUcs = []
        insightPath = os.path.join(solution, insight)
        for root, dirNames, filenames in os.walk(insightPath):
            insightUcs = dirNames
            break
        for useCase in insightUcs:
            
            try:
                updateFacts(insightPath, useCase, fact, fieldName, fieldType, fieldVal)
            except Exception as e:
                error(e.__str__() + ' ' + insight + ' ' + useCase)


def main(argv):
    startLog()
    try:
        solution = createPath(getSolution(getPath('solution')), 'Insights')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.index(']') + 1:])
        return
    fact = argv[0]
    fieldName = argv[1]
    fieldVal = argv[2]
    fieldType = argv[3]
    insights = os.listdir(solution)
    insights.remove('SEntities')
    checkFacts(solution, insights, fact, fieldName, fieldType, fieldVal)
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 - fact
# 1 - field's name
# 2 - value
# 3 - type
