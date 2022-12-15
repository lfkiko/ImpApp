import sys
from Scripts.toolBoox import *

from Scripts.enableInsights.newEnableInsights import searchInsightInCore


def searchForInsight(solution, core, insight, factor):
    overridden = False
    try:
        insightZipDir = searchInsightInCore(core, insight)
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    with zipfile.ZipFile(os.path.join(core, insightZipDir)) as z:
        for file in z.namelist():
            if insight in file:
                if 'SThresholds.json' in file:
                    filePath = file
                    fileType = 'SThresholds.json'
                elif 'SParameters.json' in file:
                    filePath = file
                    fileType = 'SParameters.json'
                else:
                    Warning('Missing json' + insight + " has no SThresholds.json or SParameters.json to modify")
                    return
    
    jsonData = readJsonZip(core, insightZipDir, filePath)
    parType = fileType[1:fileType.index('.')].lower()
    parList = []
    
    for parameter in jsonData[parType]:
        if 'Amount' in parameter['name'] or 'Balance' in parameter['name']:
            oldVal = int(parameter['value'])
            newVal = oldVal * int(factor)
            parameter['value'] = str(newVal)
            parList.append(parameter)
            if not overridden:
                overridden = True
    
    if overridden:
        jsonData.update({parType: parList})
        if os.path.exists(os.path.join(solution, insight, fileType)):
            updateJson(os.path.join(solution, insight, fileType), jsonData)
        else:
            writeJson(os.path.join(solution, insight, fileType), jsonData)
    else:
        Warning('Missing parameters' + insight + " has no Amount/Balance to modify")


def main(argv):
    startLog()
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'Insights')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    
    core = getPath('DataLoad')
    
    for insight in os.listdir(solution):
        if insight != 'SEntities':
            searchForInsight(solution, core, insight, argv[0])
    
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])

# 0 factor
