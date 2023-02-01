import sys
from Scripts.toolBoox import *

searchedCoreFolders = ['product-act-biz-unit.zip', 'product-budgets-biz-unit.zip',
                       'product-data-and-assets-biz-unit.zip', 'product-debt-biz-unit.zip',
                       'product-engage-biz-unit.zip', 'product-goals-biz-unit.zip', 'product-mt-biz-unit.zip']


def searchInsightInCore(corePath, insightName):
    zips = os.listdir(corePath)
    zips.remove('perso-biz.zip')
    for dirZip in searchedCoreFolders:
        if 'bank' in dirZip or 'docs' in dirZip:
            zips.remove(dirZip)
    for zipDir in zips:
        insightsInPath = filesInZip(corePath, zipDir, 'Core/Insights/' + insightName)
        if len(insightsInPath) != 0:
            return zipDir
    return FileNotFoundError


def searchForInsight(solution, core, insight, factor):
    overridden = False
    notFound = True
    try:
        insightZipDir = searchInsightInCore(core, insight)
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return
    if insightZipDir == FileNotFoundError:
        return
    with zipfile.ZipFile(os.path.join(core, insightZipDir)) as z:
        for file in z.namelist():
            if insight in file:
                if 'SThresholds.json' in file:
                    fileType = 'SThresholds.json'
                    filePath = file
                    notFound = False
                elif 'SParameters.json' in file:
                    fileType = 'SParameters.json'
                    filePath = file
                    notFound = False
        if notFound:
            Warning('Missing json' + insight + " has no SThresholds.json or SParameters.json to modify")
            return
    
    jsonData = readJsonZip(core, insightZipDir, filePath)
    parType = fileType[1:fileType.index('.')].lower()
    parList = []
    for parameter in jsonData[parType]:
        if 'name' in parameter.keys():
            if parameter['name'] == 'A_Amount' or parameter['name'] == 'A_amount' \
                or 'Balance' in parameter['name'] \
                or 'balance' in parameter['name'] \
                or (len(parameter['name']) > 1 and
                    (parameter['name'][0] == 'A' and parameter['name'][1].isnumeric())):
                oldVal = int(parameter['value'])
                newVal = oldVal * int(factor)
                parameter['value'] = str(newVal)
                parList.append(parameter)
                if not overridden:
                    overridden = True
        else:
            print(insight)
    
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
