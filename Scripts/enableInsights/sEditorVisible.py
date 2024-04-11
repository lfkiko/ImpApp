import json
import os
import sys
from logging import error

from Scripts.enableInsights import transfer
from Scripts.enableInsights.newEnableInsights import ucsDict
from Scripts.toolBoox.excelJsonToolBox import readCsv, writeJson, readJsonZip, getCol, updateJson
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getFile, getPath, getSolution


def modifyJson(fileName, jsonData):
    data = readCsv(fileName)
    insightsList = getCol(fileName, 'insight')
    remove = []
    
    for insight in jsonData['visible'].keys():
        if insight not in insightsList:
            remove.append(insight)
    
    for insight in insightsList:
        if insight not in remove and insight not in jsonData['visible'].keys():
            jsonData['visible'][insight] = []
    
    for insight in remove:
        jsonData['visible'].pop(insight)
    
    for insight in jsonData['visible'].keys():
        uc = data['UC'][insightsList.index(insight)].split(",")
        for i in uc:
            new = insight + "_UC" + i
            jsonData["visible"][insight].append(new)
    return jsonData


def main(argv):
    startLog()
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'SEditorDefinition')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    insights = getCol(argv[0], 'Insight')
    ucs = getCol(argv[0], 'UC')
    exposed = getCol(argv[0], 'Exposed in EB')
    tmpInsights = list()
    tmpUcs = list()
    for i in range(len(insights)):
        if exposed[i] == 'V':
            tmpInsights.append(insights[i])
            tmpUcs.append(ucs[i])
    insights = list(set(tmpInsights))
    insights.sort()
    # print(insights)
    # insights.sort()
    # print(insights)
    ucsDictionary = ucsDict(insights, ucs)
    jsonData = {"visible": ucsDictionary}
    # transfer.main([argv[0], 'visible'])
    # fileName = getFile(argv[0])
    # jsonData = modifyJson(fileName, jsonData)
    jsonPath = os.path.join(solution, 'SEditorVisible.json')
    if os.path.exists(jsonPath):
        updateJson(jsonPath, jsonData)
    else:
        writeJson(jsonPath, jsonData)
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 - excel file
