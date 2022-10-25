import json
import os
import sys
from logging import error, info

from Scripts.enableInsights import transfer
from Scripts.toolBoox.excelJsonToolBox import readCsv, writeJson
from Scripts.toolBoox.toolBoox import getFile, rewriteText, fixPath, getPath, getSolution


def createJson(file_name):
    data = readCsv(file_name)
    json_data = {"visible": {}}
    for i in data.index:
        json_data["visible"][data['insight'][i]] = []
        uc = data['UC'][i].split(",")
        for j in uc:
            if len(uc) == 1:
                new = data['insight'][i] + "_UC1"
            else:
                new = data['insight'][i] + "_UC" + j
            json_data["visible"][data['insight'][i]].append(new)
    return json_data


def main(argv):
    info("Starting SEditorVisible.json override")
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'SEditorDefinition')
    except:
        error(getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    transfer.main([argv[0], 'visible'])
    file_name = getFile(argv[0])
    json_data = json.dumps(createJson(file_name), indent=4)
    json_name = fixPath(os.path.join(solution, 'SEditorVisible.json'))
    if os.path.exists(solution + "\\" + json_name):
        rewriteText(json_name, json_data, solution)
    else:
        writeJson(json_name, json_data)
    info("SEditorVisible.json overwriting is finished")


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 - excel file
