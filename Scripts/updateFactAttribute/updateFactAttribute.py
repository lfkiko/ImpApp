from Scripts.toolBoox import *
import sys
import os
from logging import error, warning


def updateFacts(insightPath, insightUc, fact, fieldName, fieldVal, fieldOldVal):
    insightFactsPath = os.path.join(insightPath, insightUc, "JInsightFacts.json")
    if os.path.exists(insightPath):
        try:
            insightFacts = readJson(insightFactsPath)
        except:
            insightFacts = readJsonUtf8Sig(insightFactsPath)
        if fact in insightFacts.keys():
            col = insightFacts[fact]['cols'].index(fieldName)
            for row in insightFacts[fact]['rows']:
                if row[col] == fieldOldVal or row[col] is None:
                    row[col] = fieldVal
            try:
                updateJsonMultiLang(insightFactsPath, insightFacts)
            except:
                updateJsonMultiLangUtf8Sig(insightFactsPath, insightFacts)
        else:
            warning(fact + 'is not part of ' + insightPath)
    else:
        warning('There is no such file = ' + insightPath)


def checkFacts(solution, insights, fact, fieldName, fieldVal, fieldOldVal):
    for insight in insights:
        insightUcs = []
        insightPath = os.path.join(solution, insight)
        for root, dirNames, filenames in os.walk(insightPath):
            insightUcs = dirNames
            break
        for useCase in insightUcs:
            try:
                updateFacts(insightPath, useCase, fact, fieldName, fieldVal, fieldOldVal)
            except Exception as e:
                error(e.__str__() + ' ' + insight + ' ' + useCase)


def main(argv):
    startLog()
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'Insights')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    fact = argv[0]
    fieldName = argv[1]
    fieldVal = argv[2]
    fieldOldVal = argv[3]
    insights = os.listdir(solution)
    insights.remove('SEntities')
    checkFacts(solution, insights, fact, fieldName, fieldVal, fieldOldVal)
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 - fact
# 1 - field's name
# 2 - value
# 3 - type
