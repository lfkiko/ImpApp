import os
import shutil
import sys
from logging import error, warning
import Scripts.toolBoox as Tool

searchedCoreFolders = ["product-subscriptions-biz-unit", "product-budgets-biz-unit", "product-debt-biz-unit",
                       os.path.join("product-engage-biz-unit", "Projects"), "product-pa-biz-unit"]
searchedModelFolders = ['product-subscriptions-biz-unit', 'product-portfolio-biz-unit']


def validInsight(insightName):
    try:
        int(insightName)
        return False
    except:
        pass
    for char in insightName:
        if char in (' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'):
            return False
    return True


def getUcsList(insightName, ucs):
    try:
        return [insightName + "_UC" + str(int(ucs))]
    except:
        return [insightName + "_UC" + uc for uc in ucs.split(',')]


def buildSinsights(insightName, ucs, insightProductPath):
    filePath = os.path.join(insightProductPath, "SInsight.json")
    if os.path.exists(filePath):
        insightData = Tool.readJson(filePath)
        useCases = list()
        wasUpdate = False
        for case in insightData["useCases"]:
            useCases.append(case["id"])
        for uc in ucs:
            if uc not in useCases:
                wasUpdate = True
                insightData["useCases"].append({"id": uc, "activated": "TRUE"})
        if wasUpdate:
            Tool.updateJson(filePath, insightData)
        # else:

    else:
        Sinsight = {"id": insightName,
                    "insightMetadata": {
                        "activated": "TRUE"
                    },
                    "useCases": []
                    }
        for uc in ucs:
            Sinsight["useCases"].append({"id": uc, "activated": "TRUE"})

        Tool.updateJson(filePath, Sinsight)


def searchInsightInCore(core, modelPath, insightName, useModel):
    for coreFolder in searchedCoreFolders:
        if useModel and 'SUB_' in insightName:
            try:
                currFolder = os.path.join(modelPath, coreFolder, "Core", "Insights")
            except Exception as e:
                error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
                return
        else:
            try:
                currFolder = os.path.join(core, coreFolder, 'Core', 'Insights')
            except Exception as e:
                error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        if os.path.exists(currFolder) and insightName in os.listdir(currFolder):
            return os.path.join(currFolder, insightName)
    return


def overwriteInsight(solution, core, modelPath, insightName, ucs, useModel, notFound):
    insightCorePath = searchInsightInCore(core, modelPath, insightName, useModel)
    try:
        os.mkdir(os.path.join(solution, insightName))
    except Exception as e:
        error('Path Error:' + e.__str__()[e.__str__().index(']') + 1:])
        return

    ucsList = getUcsList(insightName, ucs)
    for uc in ucsList:
        try:
            shutil.copytree(os.path.join(insightCorePath, uc), os.path.join(solution, insightName, uc))
        except Exception as e:
            if len(e.args) > 1 and 'Cannot create a file when that file already exists' == e.args[1]:
                warning('uc already exists in solution: %s', uc)
            else:
                notFound.append(uc)
                error('{} can\'t be found in: unknown path'.format(uc))

    buildSinsights(insightName, ucsList, os.path.join(solution, insightName))


def runOverInsights(core, solution, modelPath, enableCsv, useModel):
    notFound = list()
    for i in enableCsv.index:
        insightName = enableCsv['insight'][i]
        if not validInsight(insightName):
            print("insight name is illegal: {}".format(insightName), "row: {}".format(i + 2))
        ucs = enableCsv['UC'][i]
        overwriteInsight(solution, core, modelPath, insightName, ucs, useModel, notFound)
    return notFound





def main(argv):
    Tool.startLog()
    corePath = os.path.join(Tool.getPath('corePath'), 'product-bizpack')
    modelPath = os.path.join(Tool.getPath('modelPath'), 'product-models-bizpack')
    try:
        solutionPath = Tool.getSolution(Tool.getPath('solution'))
    except:
        error(Tool.getPath('solution') + ' is not a correct path Demo data didn\'t run')
        return
    channels = Tool.getChannels(solutionPath)
    if len(channels) > 3:
        theChannel = Tool.chooseChanel(channels)
        solutionPath = solutionPath + theChannel

    if not os.path.exists(solutionPath):
        error(solutionPath + ' dosn\'t exists')
        return
    useModel = Tool.modelVersion(Tool.getPath('solution'))
    inputFile = argv[0]
    enableCsv = Tool.readCsv(inputFile)
    notFound = runOverInsights(corePath, solutionPath, modelPath, enableCsv, useModel)
    for i in notFound:
        warning("Not Found: " + i + " wasn't found")
    Tool.endLog()
    return 'notFound'


if __name__ == "__main__":
    main(sys.argv[1:])

    # 0 file with the list of insights to enable
