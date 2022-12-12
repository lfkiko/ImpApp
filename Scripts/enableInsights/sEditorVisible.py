import json
import os
import sys
from logging import error

from Scripts.enableInsights import transfer
from Scripts.toolBoox.excelJsonToolBox import readCsv, writeJson, readJsonZip, prettyPrintJson, getCol, updateJson
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import getFile, rewriteText, fixPath, getPath, getSolution


def modifyJson(fileName, jsonData):
    data = readCsv(fileName)
    insightsList = getCol(fileName, 'insight')
    remove = []
    # print(data)
    # print(data['insight'])
    # print(data['UC'])
    # print(insightsList)
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
    
    # for insight in
    prettyPrintJson(jsonData)
    # for i in data.index:
    #     json_data["visible"][data['insight'][i]] = []
    #     uc = data['UC'][i].split(",")
    #     for j in uc:
    #         if len(uc) == 1:
    #             new = data['insight'][i] + "_UC1"
    #         else:
    #             new = data['insight'][i] + "_UC" + j
    #         json_data["visible"][data['insight'][i]].append(new)
    return jsonData


def main(argv):
    startLog()
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'SEditorDefinition')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    jsonData = json.loads(readJsonZip(getPath('DataLoad'), 'product-editor-engage-biz-unit.zip', 'SEditorVisible.json'))
    prettyPrintJson(jsonData)
    # print(type(jsonData))
    transfer.main([argv[0], 'visible'])
    fileName = getFile(argv[0])
    jsonData = modifyJson(fileName, jsonData)
    jsonPath = os.path.join(solution, 'SEditorVisible.json')
    if os.path.exists(jsonPath):
        updateJson(jsonPath, jsonData)
    else:
        writeJson(jsonPath, jsonData)
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 - excel file
