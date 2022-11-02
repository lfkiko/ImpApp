import os.path
import sys
from logging import info, error

from Scripts.toolBoox.excelJsonToolBox import readJson, updateJson
from Scripts.toolBoox.toolBoox import getPath, getSolution, createPath


def getSource(corePath, batchName):
    filePath = os.path.join(corePath, batchName + '.json')
    fileData = readJson(filePath)
    return fileData


def updateProperties(solution, autoRegisterApi):
    propertiesPath = createPath(solution, 'srv-engage\\src\\main\\resources\\config\\pserver.service.properties')
    enabled = True
    method = True
    with open(propertiesPath, 'r+') as f:
        lines = f.readlines()
        f.seek(0)
        for line in lines:
            if line != '\n' and '=' in line:
                tmpLine = line
                p, v = line.split('=')
                if p == 'AUTO_REGISTER_ENABLED':
                    v = 'true'
                    tmpLine = p + '=' + v + '\n'
                    enabled = False
                if p == 'AUTO_REGISTER_METHOD':
                    v = autoRegisterApi
                    tmpLine = p + '=' + v + '\n'
                    method = False
                f.write(tmpLine)
        if enabled:
            f.write('AUTO_REGISTER_ENABLED = true\n')
        if method:
            f.write('AUTO_REGISTER_METHOD = ' + autoRegisterApi + '\n')


def updateContexts(solution, context, groupName):
    insightsContextsPath = createPath(solution, 'Insights\\SEntities\\SInsightsContexts.json')
    contextJson = readJson(insightsContextsPath)
    for x in contextJson['insightsContexts']:
        if x['id'] == context:
            x['config']['batchGroup'] = groupName


def checkBatch(sourceFile, userFile):
    batch = dict()
    for x in userFile.key:
        if x not in ['id', 'active']:
            if x in sourceFile and userFile[x] != sourceFile[x]:
                batch[x] = userFile[x]
    return batch


def overrideBatch(solution, batchName, overrideFile, qaCopy, adhocCopy):
    filePath = os.path.join(solution, batchName + '.json')
    updateJson(filePath, overrideFile)
    tmpOverrideFile = overrideFile
    if adhocCopy:
        tmpOverrideFile['id'] = overrideFile['id'] + '-adhoc'
        tmpOverrideFile['active'] = False
        tmpOverrideFile['taskType'] = 'adhoc'
        filePath = os.path.join(solution, batchName + '-adhoc.json')
        updateJson(filePath, tmpOverrideFile)
    if qaCopy:
        tmpOverrideFile['id'] = overrideFile['id'] + '-qa'
        tmpOverrideFile['active'] = False
        tmpOverrideFile['channel'] = overrideFile['channel'].replace('_LIVE', '_QA')
        filePath = os.path.join(solution, batchName + '-qa.json')
        updateJson(filePath, tmpOverrideFile)


def main(argv):
    info("Starting batches override")
    try:
        solution = createPath(getSolution(getPath('solution')), 'Batch\\SBatch')
    
    except Exception as e:
        print(e)
        error('Path Error:' + getPath('solution') + ' is not a correct path Data library didn\'t run')
        return
    try:
        corePath = createPath(getPath('corePath'),
                              'product-bizpack\\product-system-biz-unit\\Projects\\Core\\Batch\\SBatch')
    except:
        error('Path Error:' + getPath('corePath') + ' is not a correct path Data library didn\'t run')
        return
    
    sourceFile = getSource(corePath, argv[0])
    overrideFile = checkBatch(sourceFile, argv[1])
    overrideBatch(solution, argv[0], overrideFile, argv[2], argv[3])
    if overrideFile['importMethods'] == 'autoRegister':
        updateContexts(getSolution(getPath('solution')), argv[4], overrideFile['groupName'])
        updateProperties(getPath('solution'), argv[5])
    info("Batches override is over")


if __name__ == "__main__":
    main(sys.argv[1:])

#     0 - batch name
#     1 - batch file - dic()
#     2 - qa - boolean
#     3 - adhoc - boolean
#     4 - apiContext
#     5 - AutoRegisterApi
