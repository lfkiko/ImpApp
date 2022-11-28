import sys
import os
from logging import info, error

from Scripts.toolBoox.excelJsonToolBox import readJsonUtf8Sig, prettyPrintJson, updateJson, updateJsonUtf8Sig
from Scripts.toolBoox.toolBoox import getInsightsDir, getFile, readJson, getPath, getSolution, modelVersion

searchedFolders = ["product-subscriptions-biz-unit", "product-budgets-biz-unit", "product-debt-biz-unit",
                   os.path.join("product-engage-biz-unit", "Projects"), "product-pa-biz-unit"]


def searchForInsight(solution, core, modelPath, insight, useModel, factor):
    overridden = False
    for coreDir in searchedFolders:
        currentDir = os.path.join(core, coreDir, "Core", "Insights")
        if useModel and coreDir in searchedModelFolders:
            currentDir = os.path.join(modelPath, coreDir, "Core", "Insights")
        
        if insight in os.listdir(currentDir):
            currentDir = os.path.join(currentDir, insight)
            if 'SThresholds.json' in os.listdir(currentDir):
                fileType = 'SThresholds.json'
            elif 'SParameters.json' in os.listdir(currentDir):
                fileType = 'SParameters.json'
            else:
                Warning('Missing json' + insight + " has no SThresholds.json or SParameters.json to modify")
                return
            
            currentDir = os.path.join(currentDir, fileType)
            
            try:
                jsonData = readJson(currentDir)
            except:
                jsonData = readJsonUtf8Sig(currentDir)
            
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
                try:
                    updateJson(os.path.join(solution, insight, fileType), jsonData)
                except:
                    updateJsonUtf8Sig(os.path.join(solution, insight, fileType), jsonData)
            else:
                Warning('Missing parameters' + insight + " has no Amount/Balance to modify")


def main(argv):
    info("Starting SThresholds factor updated")
    core = os.path.join(getPath('corePath'), 'product-bizpack')
    modelPath = os.path.join(getPath('modelPath'), 'product-models-bizpack')
    try:
        solution = os.path.join(getSolution(getPath('solution')), 'Insights')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.index(']') + 1:])
        return
    useModel = modelVersion(getPath('solution'))
    for insight in os.listdir(solution):
        if insight != 'SEntities':
            searchForInsight(solution, core, modelPath, insight, useModel, argv[0])
    
    info("All relevant SThresholds are updated")


searchedModelFolders = ['product-subscriptions-biz-unit', 'product-portfolio-biz-unit']

if __name__ == "__main__":
    main(sys.argv[1:])

# 0 factor
