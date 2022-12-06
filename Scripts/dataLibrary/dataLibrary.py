import os
import sys
from logging import error, warning
from Scripts.toolBoox.excelJsonToolBox import getheader, getRow, getCol, readJsonUtf8Sig, updateJsonUtf8Sig
from Scripts.toolBoox.logs import startLog, endLog
from Scripts.toolBoox.toolBoox import createPath, getSolution, getPath

requireFieldsForTriggerLogic = ['type', 'dataAttributeId', 'droolClass', 'relatedEntity']
javaEntitiesStrings = dict({})


def getVal(colName, colVal):
    if colVal == "" or colName in ["LastUpdate", "created"]:
        return ""
    
    if colName in ["tags", "dataItemLocation", "factName"]:
        colVal = colVal.replace(" ", "").split(",")
        return colVal
    if colVal == 'availableValues' and len(colVal) != 0:
        colVal = {'sourceOfData': 'list', 'values': colVal.replace(" ", "").split(",")}
    
    colVal = str(colVal).encode('ascii', 'ignore').decode("utf-8")
    return colVal


def buildTriggerLogic(jsonEntity, rowNumber, corePath):
    if "visibleLogic" not in jsonEntity or jsonEntity['visibleLogic'] == "FALSE":
        return jsonEntity
    for colName in requireFieldsForTriggerLogic:
        if colName not in jsonEntity:
            error(
                "ERROR 2: trigger logic not created for raw number: {0}, id: {1} missing on of the require fields: {2}\n"
                    .format(rowNumber, jsonEntity['id'], requireFieldsForTriggerLogic))
            return jsonEntity
    fieldId = jsonEntity['dataAttributeId']
    javaClass = jsonEntity['droolClass']
    
    # handle dynamic
    if 'dynamicTechType' in jsonEntity:
        dynamicTriggerLogic = {"type": "attribute", "attribute": {'id': fieldId,
                                                                  'type': jsonEntity['type'],
                                                                  "techType": jsonEntity['dynamicTechType'],
                                                                  "dynamic": True, "evalOnly": True}}
        jsonEntity['triggerLogic'] = dynamicTriggerLogic
        del jsonEntity['dynamicTechType']
        return jsonEntity
    if isProfile(javaClass):
        if jsonEntity['type'] == 'Number':
            jsonEntity['triggerLogic'] = {'type': 'profile', 'level': jsonEntity['relatedEntity'],
                                          'class': javaClass,
                                          'value': {'id': fieldId,
                                                    'type': jsonEntity['type']}}
        if jsonEntity['type'] == 'Date':
            jsonEntity['triggerLogic'] = {'type': 'profile', 'level': jsonEntity['relatedEntity'],
                                          'class': javaClass,
                                          'value': {'id': fieldId,
                                                    'type': jsonEntity['type'],
                                                    'techType': 'PDate',
                                                    'evalOnly': 'true'}}
        if jsonEntity['type'] == 'String':
            jsonEntity['triggerLogic'] = {'type': 'profile', 'level': jsonEntity['relatedEntity'],
                                          'class': javaClass,
                                          'value': {'id': fieldId,
                                                    'type': jsonEntity['type'],
                                                    'evalOnly': 'true'}}
        return jsonEntity
    
    # handle string
    if jsonEntity['type'] == 'String' and existInJava(javaClass, 'String', fieldId, corePath):
        if 'availableValues' in jsonEntity:
            jsonEntity['triggerLogic'] = {"type": "attribute", "attribute": {'id': fieldId,
                                                                             'techType': "String",
                                                                             'type': "List",
                                                                             "evalOnly": True}}
        else:
            jsonEntity['triggerLogic'] = {"type": "attribute", "attribute": {'id': fieldId,
                                                                             'type': "String",
                                                                             "evalOnly": True}}
    # handle date
    if jsonEntity['type'] == 'Date' and existInJava(javaClass, 'PDate', fieldId, corePath):
        jsonEntity['triggerLogic'] = {"type": "attribute", "attribute": {'id': fieldId,
                                                                         'type': "Date",
                                                                         "evalOnly": True}}
    # handle boolean
    if jsonEntity['type'] == 'Binary' or jsonEntity['type'] == 'Boolean':
        if existInJava(javaClass, 'PExtendedBoolean', fieldId, corePath):
            jsonEntity['triggerLogic'] = {"type": "attribute",
                                          "attribute": {'id': fieldId,
                                                        'techType': "PExtendedBoolean",
                                                        'type': "Binary"},
                                          "evalOnly": True}
            return jsonEntity
        if existInJava(javaClass, 'Boolean', fieldId, corePath):
            jsonEntity['triggerLogic'] = {"type": "attribute",
                                          "attribute": {'id': fieldId,
                                                        'type': "Binary"}}
    # handle number
    if jsonEntity['type'] == 'Number':
        if existInJava(javaClass, 'PAmount', fieldId, corePath):
            getter = fieldId + '.getDoubleAmount()'
            jsonEntity['triggerLogic'] = {"type": "attribute", "attribute": {'id': fieldId,
                                                                             'type': "Number",
                                                                             "getter": getter,
                                                                             "evalOnly": True}}
        else:
            jsonEntity['triggerLogic'] = {"type": "attribute", "attribute": {'id': fieldId,
                                                                             'type': "Number"}}
    if 'triggerLogic' in jsonEntity:
        return jsonEntity
    if javaClass not in ["PInsightCombinedHistory"]:
        error("ERROR 3: trigger logic not created for raw number: {0}, id:{1}, the field {2} may not defined in the "
              "java class: {3}\n".format(rowNumber, jsonEntity['id'], fieldId, javaClass))
    return jsonEntity


def existInJava(javaClass, fieldType, fieldId, corePath):
    if fieldId == 'id':
        return True
    if javaClass not in javaEntitiesStrings:
        if not loadJavaFile(javaClass, corePath):
            return False
    javaFileText = javaEntitiesStrings.get(javaClass)
    return str(javaFileText).__contains__(fieldType + " " + fieldId)


def loadJavaFile(javaClass, corePath):
    if javaClass in ['PInsightCombinedHistory']:
        return False
    for model in ["core-model", "mod-logic"]:
        fullPath = createPath(corePath, model + '\\src\\main\\java\\com\\personetics\\entities\\' + javaClass + '.java')
        if os.path.exists(fullPath):
            javaFile = open(fullPath, "r", encoding='utf-8-sig')
            javaEntitiesStrings[javaClass] = javaFile.read().replace('\t', ' ')
            javaFile.close()
            return True
    
    return False


def isProfile(javaClass):
    return javaClass.startswith('DA') and javaClass != 'DAccount' and javaClass != 'DATM'


def saveJson(jsonEntity, rowNumber, solutionPath):
    if validateBeforeSave(jsonEntity, rowNumber):
        jsonName = jsonEntity['id'] + '.json'
        jsonPath = os.path.join(solutionPath, jsonName)
        if jsonName in os.listdir(solutionPath):
            os.remove(jsonPath)
        updateJsonUtf8Sig(jsonPath, jsonEntity)


def validateBeforeSave(jsonEntity, rowNumber):
    if jsonEntity == {}:
        return False
    elif 'id' in jsonEntity:
        return True
    elif 'dataAttributeId' in jsonEntity and 'droolClass' in jsonEntity:
        jsonEntity['id'] = jsonEntity['droolClass'] + '-' + jsonEntity['dataAttributeId']
        return True
    error("ERROR 4: raw number: {0} missing 'id' column, and also missing 'dataAttributeId' or 'droolClass' "
          "thus can not create id (and file name) \n".format(rowNumber))
    return False


def removeDeactivated(solution):
    startLog('removeDeactivated')
    countFalse = 0
    countAll = 0
    for attribute in [j for j in os.listdir(solution) if os.path.isfile(os.path.join(solution, j))]:
        countAll += 1
        jsonPath = os.path.join(solution, attribute)
        dataAttribute = readJsonUtf8Sig(jsonPath)
        
        if dataAttribute['activate'] == 'FALSE':
            countFalse += 1
            os.remove(jsonPath)
    print(str(countFalse) + " out of " + str(countAll))
    endLog(True, removeDeactivated)


def main(argv):
    startLog()
    
    try:
        solution = createPath(getSolution(getPath('solution')), 'SEditorDefinition\\DataAttribute')
    except Exception as e:
        error('Path Error:' + e.__str__()[e.index(']') + 1:])
        return
    
    try:
        corePath = getPath('corePath')
    except:
        error('Path Error:' + getPath('corePath') + ' is not a correct path Data library didn\'t run')
        return
    if argv[1]:
        attributes = getCol(argv[0], 'id')
        allHeaders = getheader(argv[0])
        colsRange = range(len(allHeaders))
        rowNumber = 1
        for rows in attributes:
            row = getRow(argv[0], attributes.index(rows) + 1)
            jsonEntity = {}
            for index in colsRange:
                colName = allHeaders[index]
                colVal = row[index]
                colVal = getVal(colName, colVal)
                if colVal == "":
                    continue
                
                jsonEntity[colName] = colVal
            jsonEntity = buildTriggerLogic(jsonEntity, rowNumber, corePath)
            saveJson(jsonEntity, rowNumber, solution)
            rowNumber += 1
    
    if argv[2]:
        removeDeactivated(solution)
    endLog()


if __name__ == "__main__":
    main(sys.argv[1:])
    
    # 0 - excel file
    # 1 - update data library - boolean
    # 2 - remove deactivated - boolean
