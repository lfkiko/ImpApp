import json
import sys
import os
from logging import info, error

from Scripts.toolBoox.excelJsonToolBox import readJson, updateJson
from Scripts.toolBoox.toolBoox import getPath, getSolution, createPath


def updateFacts(insightPath, insightUc, fact, fieldName, fieldType, fieldVal):
    insightFactsPath = os.path.join(insightPath, insightUc, "JInsightFacts.json")
    insightFacts = readJson(insightFactsPath)
    insightFacts[fact]['cols'].append(fieldName)
    for row in insightFacts[fact]['rows']:
        row.append(fieldType)
    insightFacts[fact]['attributesTypes'].append(fieldVal)
    updateJson(insightFactsPath, insightFacts)


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
                error('could not update jinsight facts for: ', useCase)


def main(argv):
    info("Starting new field adding")
    try:
        solution = createPath(getSolution(getPath('solution')), 'Insights')
    except Exception as e:
        print(e)
        error('Path Error:' + getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    fact = argv[0]
    fieldName = argv[1]
    fieldVal = argv[2]
    fieldType = argv[3]
    insights = os.listdir(solution)
    checkFacts(solution, insights, fact, fieldName, fieldType, fieldVal)


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 - fact
# 1 - field's name
# 2 - value
# 3 - type
