import json
import os
import sys

from Scripts.enableInsights import transfer
from Scripts.toolBoox.toolBoox import getFile, readCsv, findDir, rewriteText, fixPath


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
    path = findDir(argv[0], 'SEditorDefinition')
    transfer.main([argv[1], 'visible'])
    file_name = getFile(argv[1])
    json_data = json.dumps(createJson(file_name), indent=4)
    json_name = fixPath(os.path.join(path, 'SEditorVisible.json'))
    rewriteText(json_name, json_data)
    return "Overwriting finished"


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # [Path, excel file]
